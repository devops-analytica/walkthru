#!/usr/bin/env python3
"""Setup (init): machine readiness report for IT imaging. Run with `claude --init-only` in the staff working folder."""
import os, platform, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt
import scope


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    lines = [f'WalkThru guardrails setup check on {platform.system()} {platform.release()}, Python {platform.python_version()}']
    lines.append('python3 on PATH: ' + ('yes' if shutil.which('python3') or shutil.which('python') else 'NO - helper scripts and hooks need Python 3.9+'))
    lines.append('jq on PATH: ' + ('yes' if shutil.which('jq') else 'no (optional)'))
    try:
        lines.append(f'audit folder writable: {wt.audit_dir(config)}')
    except OSError as exc:
        lines.append(f'audit folder NOT writable: {exc}')
    ctx = scope.find_project_context(config, data.get('cwd'))
    lines.append(f'project context: {ctx}' if ctx else 'project context: none found (copy config/project-context.example.json to .claude/project-context.json)')
    cwd = Path(data.get('cwd') or '.')
    outputs = [d for d in config.get('writable_dirs', []) if (cwd / d.rstrip('/')).is_dir()]
    lines.append('output folders present: ' + (', '.join(outputs) if outputs else 'none (create outputs/ for drafts)'))
    lines.append('policy lock (WALKTHRU_GUARDRAILS): ' + (os.environ.get('WALKTHRU_GUARDRAILS') or 'not set'))
    lines.append('alert webhook: ' + ('configured' if os.environ.get(config.get('alert_webhook_env', 'WALKTHRU_ALERT_WEBHOOK')) else 'not set'))
    print('\n'.join(lines))


if __name__ == '__main__':
    wt.run(main)
