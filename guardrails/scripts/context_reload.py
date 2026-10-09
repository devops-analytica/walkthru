#!/usr/bin/env python3
"""UserPromptSubmit: when project-context.json changed since it was last injected, re-inject the scope."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt
import scope

STAMP = 'walkthru-context.stamp'


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    path = scope.find_project_context(config, data.get('cwd'))
    if not path or not data.get('scratchpad_dir'):
        return
    stamp = Path(data['scratchpad_dir']) / STAMP
    current = f'{path}:{path.stat().st_mtime_ns}'
    try:
        previous = stamp.read_text(encoding='utf-8')
    except OSError:
        previous = ''
    if previous == current:
        return
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(current, encoding='utf-8')
    if previous:  # first sighting is covered by SessionStart; only announce real changes
        wt.context('Project context file changed since last read. Refreshed scope:\n' + scope.scope_text(config, data, include_rules=False), 'UserPromptSubmit')


if __name__ == '__main__':
    wt.run(main)
