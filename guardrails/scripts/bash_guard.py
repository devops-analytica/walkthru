#!/usr/bin/env python3
"""PreToolUse on Bash|PowerShell: deny destructive commands and uploads of company data to non-allowlisted hosts."""
import re, shlex, sys
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

HTTP_TOOLS = {'curl', 'wget', 'invoke-webrequest', 'invoke-restmethod', 'iwr', 'irm', 'http', 'https', 'xh'}
UPLOAD_FLAGS = re.compile(r'^(-d|--data(-\w+)?|--json|-F|--form(-string)?|-T|--upload(-file)?|--post-data|--post-file|-K|--config|-InFile|-Body|--body)$', re.I)
METHOD_FLAGS = re.compile(r'^(-X|--request|-Method)$', re.I)
MUTATING_METHODS = {'post', 'put', 'patch', 'delete'}
HOSTLIKE = re.compile(r'^(?:[a-z][a-z0-9+.-]*://)?(?:[\w-]+\.)+[a-z]{2,}(?::\d+)?(?:/|$)', re.I)
VALUE_FLAGS = re.compile(r'^(-[dFTXoHuAbcexK]|--(data(-\w+)?|form(-string)?|upload(-file)?|json|post-\w+|request|output|header|user|proxy|cookie|config|body|method)|-InFile|-Body|-Method|-Uri|-OutFile|-Headers)$', re.I)
FILE_EXT = re.compile(r'\.(pdf|csv|xlsx?|xlsm|json|txt|md|zip|xer|docx?|png|jpe?g|xml|html?|py|sh|ps1|log|eml|msg)$', re.I)
RAW_UPLOAD = re.compile(r'\b(scp|rsync|sftp|ftp)\b\s+\S+\s+\S*@\S+:', re.I)
NO_HOST = '<no host could be determined>'


def _tokens(segment):
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def upload_hosts(command):
    """Destinations a command would upload to. Returns NO_HOST when an upload flag is present but no host parses."""
    if RAW_UPLOAD.search(command):
        return ['<remote host>']
    hosts = []
    for segment in re.split(r'\|\||&&|;|\|', command):
        tokens = _tokens(segment)
        if not tokens or tokens[0].rsplit('/', 1)[-1].lower() not in HTTP_TOOLS:
            continue
        uploading, destinations, skip = False, [], False
        for i, tok in enumerate(tokens[1:], start=1):
            if skip:  # value of the previous flag (file name, header, method...), never a destination
                skip = False
                continue
            bare = tok.split('=', 1)[0]
            if UPLOAD_FLAGS.match(bare) or re.match(r'^-\w*[dFT]\w*$', tok) and not tok.startswith('--'):
                uploading = True
            elif METHOD_FLAGS.match(bare):
                method = tok.split('=', 1)[1] if '=' in tok else (tokens[i + 1] if i + 1 < len(tokens) else '')
                uploading = uploading or method.lower() in MUTATING_METHODS
            elif re.match(r'^-X(POST|PUT|PATCH|DELETE)$', tok, re.I):
                uploading = True
            elif not tok.startswith('-') and HOSTLIKE.match(tok) and not ('://' not in tok and FILE_EXT.search(tok)):
                destinations.append(urlparse(tok if '://' in tok else 'http://' + tok).hostname or tok)
            skip = bool(VALUE_FLAGS.match(bare)) and '=' not in tok
        if uploading:
            hosts += destinations or [NO_HOST]
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
        if host == NO_HOST:
            wt.ask('WalkThru guardrail: this command uploads data but the destination could not be determined (variable, config file or quoted URL). Confirm the destination is inside the company tenant.')
        if not any(host.lower() == a or host.lower().endswith('.' + a) for a in allowed):
            wt.deny(f'WalkThru guardrail: upload to {host} blocked. Company data stays in the Microsoft 365 tenant; allowed hosts: {", ".join(allowed) or "none"}.')


if __name__ == '__main__':
    wt.run(main, fail_closed=True)
