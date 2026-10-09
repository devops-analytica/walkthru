#!/usr/bin/env python3
"""StopFailure (rate_limit|billing|auth|server errors): post to the IT Teams/Slack webhook when configured, always audit."""
import json, os, sys, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt


def post(url, payload):
    body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=8) as resp:  # noqa: S310 - IT-configured webhook only
        return resp.status


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    record = {'event': 'StopFailure', 'session_id': data.get('session_id'), 'error_type': data.get('error_type') or data.get('matcher'), 'error': wt.truncate(data.get('error') or data.get('message') or '', 300)}
    wt.audit_write(config, record)
    url = os.environ.get(config.get('alert_webhook_env', 'WALKTHRU_ALERT_WEBHOOK'))
    if not url:
        return
    user = os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'
    text = f'Claude Code failure for {user}: {record["error_type"]} — {record["error"]}'
    try:
        post(url, {'text': text})  # Teams incoming webhooks and Slack both accept {"text": ...}
    except Exception as exc:  # noqa: BLE001
        print(f'walkthru-guardrails: alert webhook failed: {exc}', file=sys.stderr)


if __name__ == '__main__':
    wt.run(main)
