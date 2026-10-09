#!/usr/bin/env python3
"""PreToolUse on Write|Edit: identity numbers, IBANs and card numbers do not go into general reports.

Evidence rule: work with the minimum necessary employee/vendor data; do not reproduce bank details or
identity documents in general reports. Files under a configured restricted folder are exempt.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

PATTERNS = {
    'Emirates ID': re.compile(r'\b784-?\d{4}-?\d{7}-?\d\b'),
    'UAE IBAN': re.compile(r'\bAE\d{2}(?:\s?\d{4}){4}\s?\d{3}\b', re.I),
    'card number': re.compile(r'\b(?:\d[ -]?){15}\d\b'),
}


def luhn(digits):
    total, alt = 0, False
    for ch in reversed(digits):
        n = int(ch)
        if alt:
            n = n * 2 - 9 if n > 4 else n * 2
        total += n
        alt = not alt
    return total % 10 == 0


def findings(text):
    hits = []
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text or ''):
            if label == 'card number' and not luhn(re.sub(r'\D', '', match.group())):
                continue
            hits.append(label)
    return sorted(set(hits))


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    tool_input = data.get('tool_input') or {}
    path = tool_input.get('file_path') or tool_input.get('notebook_path') or ''
    if wt.path_matches(path, config.get('pii_allowed_dirs'), data.get('cwd')):
        return
    texts = [tool_input.get('content'), tool_input.get('new_string'), tool_input.get('new_source')]
    texts += [e.get('new_string') for e in tool_input.get('edits') or [] if isinstance(e, dict)]
    hits = findings('\n'.join(t for t in texts if isinstance(t, str)))
    if hits:
        wt.deny(f'WalkThru guardrail: output contains {", ".join(hits)}. Do not reproduce identity or bank details in reports; refer to the record ID and keep the detail in the restricted source. Restricted folders: ' + ', '.join(config.get('pii_allowed_dirs', [])) + '.')


if __name__ == '__main__':
    wt.run(main, fail_closed=True)
