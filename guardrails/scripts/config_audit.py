#!/usr/bin/env python3
"""ConfigChange: log every settings/skills change to the audit log and warn the user in the transcript."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt


def main():
    data = wt.read_input()
    if not data:
        return
    config = wt.load_config(data)
    wt.audit_write(config, {'event': 'ConfigChange', 'session_id': data.get('session_id'), 'source': data.get('source'), 'file': data.get('file_path')})
    wt.emit({'systemMessage': f'WalkThru guardrail: configuration changed ({data.get("source")}: {data.get("file_path")}). Logged to the audit folder.'})


if __name__ == '__main__':
    wt.run(main)
