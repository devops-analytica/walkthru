"""Shared helpers for WalkThru guardrail hooks. Standard library only; works on macOS, Linux and Windows.

Every hook reads one JSON object from stdin (the Claude Code hook input) and answers through stdout JSON
or an exit code. Decision helpers below produce exactly the shapes documented at
https://code.claude.com/docs/en/hooks. Hooks fail open on their own errors: a broken hook must never
stop an employee from working, but it must never silently approve either, so errors go to stderr.
"""
import fnmatch, json, os, re, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parent
DEFAULT_CONFIG = PLUGIN_ROOT / 'guardrails.json'
MAX_LOG_FIELD = 400


def read_input():
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f'walkthru-guardrails: hook input is not JSON ({exc})', file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def _merge(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError) as exc:
        print(f'walkthru-guardrails: ignoring unreadable config {path} ({exc})', file=sys.stderr)
        return {}


TIGHTEN_ONLY = ('protected_dirs', 'protected_extensions', 'secret_files', 'bash_denied_patterns', 'm365_mutating_verbs', 'mutating_verbs', 'injection_patterns')
LOCKED_ONLY = ('writable_dirs', 'pii_allowed_dirs', 'allowed_upload_hosts', 'watermark_dirs', 'watermark_extensions')


def _tighten(config, override):
    """Apply an untrusted override: lists that restrict are unioned, lists that loosen are ignored, scalars replace."""
    out = dict(config)
    for key, value in override.items():
        if key in LOCKED_ONLY:
            print(f'walkthru-guardrails: "{key}" can only be changed through WALKTHRU_GUARDRAILS (managed settings); override ignored', file=sys.stderr)
        elif key in TIGHTEN_ONLY:
            out[key] = list(dict.fromkeys([*(config.get(key) or []), *(value if isinstance(value, list) else [value])]))
        elif isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config(hook_input=None):
    """Plugin default, then the IT-locked file, then home/project overrides that can only tighten policy.

    WALKTHRU_GUARDRAILS=<file> (set from managed settings `env`) is the only place that can widen
    writable/PII-exempt folders or the upload-host allowlist. Home and project files may add protected
    paths, denied patterns and verbs, or change audit/watermark/context settings, nothing else.
    """
    config = _load_json(DEFAULT_CONFIG)
    locked = os.environ.get('WALKTHRU_GUARDRAILS')
    if locked:
        config = _merge(config, _load_json(locked))
    config = _tighten(config, _load_json(Path.home() / '.claude' / 'walkthru' / 'guardrails.json'))
    project = os.environ.get('CLAUDE_PROJECT_DIR') or (hook_input or {}).get('cwd')
    if project:
        config = _tighten(config, _load_json(Path(project) / '.claude' / 'walkthru-guardrails.json'))
    return config


def norm_path(path):
    return str(path).replace('\\', '/') if path else ''


def path_matches(path, patterns):
    """True when any pattern is a directory segment of, a suffix of, or a glob match for the path."""
    p = norm_path(path).lower()
    for pattern in patterns or []:
        pat = pattern.lower()
        if pat.endswith('/'):
            if f'/{pat}' in f'/{p}' or p.startswith(pat):
                return True
        elif pat.startswith('.') and '*' not in pat:
            if p.endswith(pat):
                return True
        elif fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(Path(p).name, pat):
            return True
    return False


def dubai_now(tz_name='Asia/Dubai'):
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo(tz_name))
    except Exception:  # zoneinfo data missing on a minimal Windows install: Dubai is fixed UTC+4
        return datetime.now(timezone(timedelta(hours=4)))


def emit(payload):
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()


def deny(reason, event='PreToolUse'):
    emit({'hookSpecificOutput': {'hookEventName': event, 'permissionDecision': 'deny', 'permissionDecisionReason': reason}})
    sys.exit(0)


def ask(reason, event='PreToolUse'):
    emit({'hookSpecificOutput': {'hookEventName': event, 'permissionDecision': 'ask', 'permissionDecisionReason': reason}})
    sys.exit(0)


def context(text, event):
    emit({'hookSpecificOutput': {'hookEventName': event, 'additionalContext': text}})
    sys.exit(0)


def block(reason):
    emit({'decision': 'block', 'reason': reason})
    sys.exit(0)


def truncate(value, limit=MAX_LOG_FIELD):
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    return text if len(text) <= limit else text[:limit] + f'…(+{len(text) - limit} chars)'


def audit_dir(config):
    raw = os.environ.get('WALKTHRU_AUDIT_DIR') or config.get('audit_dir') or '~/.claude/walkthru-audit'
    path = Path(os.path.expanduser(raw))
    path.mkdir(parents=True, exist_ok=True)
    return path


def audit_write(config, record):
    record = {'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'user': os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown', **record}
    path = audit_dir(config) / (time.strftime('%Y-%m-%d') + '.jsonl')
    with path.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(record, default=str) + '\n')
    return path


FILE_TOKEN = re.compile(r'[^\s"\'<>|;&()]+\.[A-Za-z0-9]{2,5}')


def written_files(hook_input, suffixes):
    """Files a Write/Edit call or a shell command produced, filtered by suffix, as absolute paths that exist.

    For Write/Edit the path comes from tool_input. For Bash/PowerShell it is best-effort: every file-like
    token in the command with a matching suffix that exists on disk after the command ran.
    """
    tool = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input') or {}
    cwd = Path(hook_input.get('cwd') or '.')
    if tool in ('Bash', 'PowerShell'):
        candidates = FILE_TOKEN.findall(tool_input.get('command', '') or '')
    else:
        candidates = [tool_input.get('file_path') or '']
    found = []
    for token in candidates:
        if not token.lower().endswith(tuple(suffixes)):
            continue
        path = Path(norm_path(token))
        if not path.is_absolute():
            path = cwd / path
        if path.is_file() and path not in found:
            found.append(path)
    return found


def compile_patterns(patterns):
    return [re.compile(p, re.I) for p in patterns or []]


def run(main):
    """Run a hook body; on an unexpected error report to stderr and exit 0 (fail open, visibly)."""
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - a hook crash must not block the employee
        print(f'walkthru-guardrails: {Path(sys.argv[0]).name} failed: {exc!r}', file=sys.stderr)
        sys.exit(0)
