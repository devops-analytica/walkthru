#!/usr/bin/env python3
"""PostToolUse on Write|Bash|PowerShell: a CSV register must be safe to open in Excel and sortable.

Blocks (so Claude rewrites the file) when a cell starts with = + - @ or a tab/CR (formula injection), when a
column of dates mixes formats, or when the file is not UTF-8. Numeric negatives such as -1250.00 are allowed.
"""
import csv, io, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

NUMBER = re.compile(r'^-?\d[\d,]*(\.\d+)?%?$')
DATE_SHAPES = {
    'ISO': re.compile(r'^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$'),
    'DMY': re.compile(r'^\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}$'),
    'text': re.compile(r'^\d{1,2}[ -][A-Za-z]{3}[a-z]*[ -]\d{2,4}$'),
}


def problems(text):
    issues = []
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return issues
    header = rows[0]
    shapes = {}
    for r, row in enumerate(rows[1:], start=2):
        for c, cell in enumerate(row):
            value = cell.strip()
            if not value:
                continue
            if value[0] in '=+@' or value[0] in '\t\r' or (value[0] == '-' and not NUMBER.match(value)):
                issues.append(f'row {r} col {c + 1}: "{wt.truncate(value, 40)}" would be read as a formula; prefix with an apostrophe or reword')
            for name, shape in DATE_SHAPES.items():
                if shape.match(value):
                    shapes.setdefault(c, set()).add(name)
    for c, kinds in shapes.items():
        if len(kinds) > 1:
            title = header[c] if c < len(header) else f'column {c + 1}'
            issues.append(f'column "{title}" mixes date formats {sorted(kinds)}; use ISO yyyy-mm-dd throughout')
    return issues[:12]


def main():
    data = wt.read_input()
    tool_input = data.get('tool_input') or {}
    content = tool_input.get('content') if data.get('tool_name') == 'Write' else None
    if content is not None:  # Write hands us the bytes; no need for the file to be readable from here
        paths = [Path(wt.norm_path(tool_input.get('file_path', '')))] if wt.norm_path(tool_input.get('file_path', '')).lower().endswith('.csv') else []
    else:
        paths = wt.written_files(data, ('.csv',))
    for path in paths:
        text = content
        if text is None:
            try:
                text = path.read_bytes().decode('utf-8')
            except UnicodeDecodeError:
                wt.block(f'WalkThru guardrail: {path.name} is not UTF-8; rewrite the CSV as UTF-8.')
            except OSError:
                continue
        issues = problems(text)
        if issues:
            wt.block(f'WalkThru guardrail: CSV {path.name} is not spreadsheet-safe. Fix and rewrite: ' + '; '.join(issues))


if __name__ == '__main__':
    wt.run(main)
