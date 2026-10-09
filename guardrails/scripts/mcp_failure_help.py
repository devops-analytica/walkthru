#!/usr/bin/env python3
"""PostToolUseFailure on mcp__microsoft365__.*: plain-language next step for a connector failure."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt


def main():
    data = wt.read_input()
    error = wt.truncate(data.get('error') or data.get('tool_response') or '', 300).lower()
    if any(k in error for k in ('auth', 'unauthori', '401', 'token', 'login', 'consent', 'forbidden', '403')):
        hint = 'The Microsoft 365 connector is not authenticated or lacks consent. Tell the user: run /mcp, select microsoft365 and sign in with the work account; if consent is denied, IT must grant it.'
    elif any(k in error for k in ('timeout', 'timed out', '503', '502', 'unavailable', 'rate')):
        hint = 'The Microsoft 365 connector is temporarily unavailable. Retry once; if it fails again, continue with the uploaded export and state the partial coverage.'
    else:
        hint = 'The Microsoft 365 call failed. Do not invent results: say the mailbox/SharePoint check could not be completed, continue with any supplied export, and list the gap under Not checked.'
    wt.context('WalkThru guardrail: ' + hint, 'PostToolUseFailure')


if __name__ == '__main__':
    wt.run(main)
