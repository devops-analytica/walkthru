#!/usr/bin/env python3
"""PreToolUse on Edit|Write|NotebookEdit|Bash|PowerShell: supplied originals and secrets are read-only.

Deny writes to files in protected folders, to protected office/P6 formats outside a writable output folder,
and to secret files. For shell commands the check is best-effort: a command that names a protected file
together with a destructive or redirecting construct is denied.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

SHELL_WRITE = re.compile(r'(>{1,2}|\brm\b|\bmv\b|\bdel\b|\bsed\s+-i|\btee\b|\btruncate\b|\bRemove-Item\b|\bMove-Item\b|\bSet-Content\b|\bOut-File\b|\bcp\b|\bCopy-Item\b)', re.I)
FILE_TOKEN = re.compile(r'[^\s"\'<>|;&]+\.[A-Za-z0-9]{2,5}')


def verdict(path, config, cwd=None):
    """Return a reason string when the (normalized, cwd-anchored) path must not be written, else None."""
    p = wt.norm_path(path, cwd)
    if not p:
        return None
    if wt.path_matches(p, config.get('secret_files')):
        return f'{Path(p).name} is a secret/credential file'
    if wt.path_matches(p, config.get('protected_dirs')):
        return f'{p} is inside a protected evidence folder'
    if wt.path_matches(p, config.get('protected_extensions')) and not wt.path_matches(p, config.get('writable_dirs')):
        return f'{Path(p).name} looks like a supplied original (write such formats only under ' + ', '.join(config.get('writable_dirs', [])) + ')'
    return None


def shell_targets(command):
    if not SHELL_WRITE.search(command or ''):
        return []
    return FILE_TOKEN.findall(command)


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    tool = data.get('tool_name', '')
    tool_input = data.get('tool_input') or {}
    cwd = data.get('cwd')
    if tool in ('Bash', 'PowerShell'):
        for token in shell_targets(tool_input.get('command', '')):
            reason = verdict(token, config, cwd)
            if reason:
                wt.deny(f'WalkThru guardrail: shell command would modify a protected file: {reason}. Leave supplied originals intact; write results to an outputs folder.')
        return
    path = tool_input.get('file_path') or tool_input.get('notebook_path') or ''
    reason = verdict(path, config, cwd)
    if reason:
        wt.deny(f'WalkThru guardrail: {reason}. Leave supplied originals intact; write results to an outputs folder (CSV/Markdown/new XLSX) instead.')


if __name__ == '__main__':
    wt.run(main, fail_closed=True)
