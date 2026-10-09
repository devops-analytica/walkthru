#!/usr/bin/env python3
"""PostToolUse / PostToolUseFailure (async): one JSON line per tool call in the local audit log.

Records who, when, which tool, a truncated input summary, duration and failure text. File contents and
full message bodies are never logged. Mirror the folder to a central store for a tamper-resistant record.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

SUMMARY_KEYS = ('command', 'file_path', 'notebook_path', 'pattern', 'query', 'url', 'skill', 'description', 'subject', 'to', 'path', 'id')


def summarize(tool_input):
    if not isinstance(tool_input, dict):
        return wt.truncate(tool_input)
    picked = {k: wt.truncate(v, 200) for k, v in tool_input.items() if k in SUMMARY_KEYS}
    return picked or {'keys': sorted(tool_input)[:12]}


def record_for(data):
    rec = {
        'event': data.get('hook_event_name'),
        'session_id': data.get('session_id'),
        'cwd': data.get('cwd'),
        'permission_mode': data.get('permission_mode'),
        'tool': data.get('tool_name'),
        'tool_use_id': data.get('tool_use_id'),
        'input': summarize(data.get('tool_input')),
    }
    if data.get('agent_id'):
        rec['agent'] = {'id': data['agent_id'], 'type': data.get('agent_type')}
    if data.get('duration_ms') is not None:
        rec['duration_ms'] = data['duration_ms']
    if data.get('hook_event_name') == 'PostToolUseFailure':
        rec['error'] = wt.truncate(data.get('error') or data.get('tool_response') or '')
    return rec


def main():
    data = wt.read_input()
    if not data:
        return
    wt.audit_write(wt.load_config(data), record_for(data))


if __name__ == '__main__':
    wt.run(main)
