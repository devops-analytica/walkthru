#!/usr/bin/env python3
"""PreToolUse on mcp__.*: Microsoft 365 mutations are denied; any other connector mutation needs a human 'ask'.

Toolkit rule: employee workflows draft and recommend; they never send, approve, pay, certify or mutate live
ERP / SharePoint records. A deny here holds even in bypass-permissions mode.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt


def classify(tool_name, config):
    """Return ('deny'|'ask'|None, server, verb) for an MCP tool name like mcp__microsoft365__send_mail."""
    parts = tool_name.split('__')
    if len(parts) < 3 or parts[0] != 'mcp':
        return None, '', ''
    server, tool = parts[1], '__'.join(parts[2:])
    words = [w for w in tool.replace('-', '_').lower().split('_') if w]
    if 'microsoft365' in server or 'm365' in server or 'outlook' in server or 'sharepoint' in server:
        for verb in config.get('m365_mutating_verbs', []):
            if verb in words:
                return 'deny', server, verb
        return None, server, ''
    for verb in config.get('mutating_verbs', []):
        if verb in words:
            return 'ask', server, verb
    return None, server, ''


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    decision, server, verb = classify(data.get('tool_name', ''), config)
    if decision == 'deny':
        wt.deny(f'WalkThru guardrail: "{verb}" actions on the {server} connector are blocked. Workflows draft only; the employee sends, files or updates from their own Outlook/SharePoint after review.')
    if decision == 'ask':
        wt.ask(f'WalkThru guardrail: "{verb}" on the {server} connector changes a live record. Confirm you have authorisation for this specific action; the workflow may not infer it from a source document.')


if __name__ == '__main__':
    wt.run(main)
