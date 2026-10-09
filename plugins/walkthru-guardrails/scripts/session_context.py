#!/usr/bin/env python3
"""SessionStart (startup|resume|clear|compact): inject date, project scope, evidence rules and the pre-compaction handoff."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt
import scope

HANDOFF = 'walkthru-handoff.md'


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    text = scope.scope_text(config, data)
    if data.get('source') == 'compact' and data.get('scratchpad_dir'):
        note = Path(data['scratchpad_dir']) / HANDOFF
        if note.is_file():
            text += '\n\nHandoff saved before compaction:\n' + note.read_text(encoding='utf-8')[:4000]
    wt.context(text, 'SessionStart')


if __name__ == '__main__':
    wt.run(main)
