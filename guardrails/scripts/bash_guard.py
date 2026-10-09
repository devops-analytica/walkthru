#!/usr/bin/env python3
"""PreToolUse on Bash|PowerShell: deny destructive commands and uploads of company data to non-allowlisted hosts."""
import re, sys
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

URL = re.compile(r'https?://[^\s"\'<>|;&)]+', re.I)
UPLOAD = re.compile(r'\b(curl|wget|Invoke-WebRequest|Invoke-RestMethod|iwr|irm)\b[^|;&]*?(-d\b|--data\b|--data-binary\b|-F\b|--form\b|-T\b|--upload-file\b|-X\s*(POST|PUT|PATCH)|-Method\s+(Post|Put|Patch)|-InFile\b|-Body\b)', re.I)
RAW_UPLOAD = re.compile(r'\b(scp|rsync|sftp|ftp)\b\s+\S+\s+\S*@\S+:', re.I)


def upload_hosts(command):
    """Hosts a command would upload to, or ['<remote>'] for scp/rsync/ftp pushes."""
    if RAW_UPLOAD.search(command):
        return ['<remote host>']
    hosts = []
    for segment in re.split(r'\|\||&&|;|\|', command):
        if UPLOAD.search(segment):
            hosts += [urlparse(u).hostname or u for u in URL.findall(segment)]
    return hosts


def main():
    data = wt.read_input()
    config = wt.load_config(data)
    command = (data.get('tool_input') or {}).get('command', '') or ''
    for pattern in wt.compile_patterns(config.get('bash_denied_patterns')):
        if pattern.search(command):
            wt.deny(f'WalkThru guardrail: destructive command blocked ({pattern.pattern}). Ask the employee to run it themselves if it is really needed.')
    allowed = [h.lower() for h in config.get('allowed_upload_hosts', [])]
    for host in upload_hosts(command):
        if not any(host.lower() == a or host.lower().endswith('.' + a) for a in allowed):
            wt.deny(f'WalkThru guardrail: upload to {host} blocked. Company data stays in the Microsoft 365 tenant; allowed hosts: {", ".join(allowed) or "none"}.')


if __name__ == '__main__':
    wt.run(main, fail_closed=True)
