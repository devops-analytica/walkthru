#!/usr/bin/env python3
"""PostToolUse on Write|Bash|PowerShell: Markdown/text drafts written to an outputs folder get a visible DRAFT header."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt


def stamp(target, mark):
    try:
        text = target.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return False
    if mark in text:
        return False
    banner = f'> {mark}\n\n' if target.suffix.lower() == '.md' else f'{mark}\n\n'
    target.write_text(banner + text, encoding='utf-8')
    return True


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    mark = config.get('watermark', '').strip()
    if not mark:
        return
    stamped = [p.name for p in wt.written_files(data, tuple(config.get('watermark_extensions', []))) if wt.path_matches(p, config.get('watermark_dirs'), data.get('cwd')) and stamp(p, mark)]
    if stamped:
        wt.context(f'WalkThru guardrail: DRAFT header added to {", ".join(stamped)}. Leave it in place until the responsible person reviews and approves the document.', 'PostToolUse')


if __name__ == '__main__':
    wt.run(main)
