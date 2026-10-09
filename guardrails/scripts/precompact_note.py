#!/usr/bin/env python3
"""PreCompact: save the last user requests from the transcript so SessionStart(compact) can restore them."""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt

HANDOFF = 'walkthru-handoff.md'
KEEP = 6


def user_messages(transcript_path):
    """Last KEEP plain-text user messages from a Claude Code JSONL transcript."""
    texts = []
    try:
        lines = Path(transcript_path).read_text(encoding='utf-8', errors='replace').splitlines()
    except OSError:
        return texts
    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get('type') != 'user':
            continue
        content = (entry.get('message') or {}).get('content')
        if isinstance(content, list):
            content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict) and c.get('type') == 'text')
        if isinstance(content, str) and content.strip() and not content.lstrip().startswith('<'):
            texts.append(wt.truncate(content.strip(), 300))
    return texts[-KEEP:]


def main():
    data = wt.read_input()
    if not data.get('scratchpad_dir'):
        return
    note = Path(data['scratchpad_dir']) / HANDOFF
    note.parent.mkdir(parents=True, exist_ok=True)
    msgs = user_messages(data.get('transcript_path', ''))
    body = [f'Saved {datetime.now(timezone.utc).isoformat(timespec="seconds")} UTC before {data.get("trigger", "auto")} compaction, cwd {data.get("cwd")}.']
    body += ['Recent user requests:'] + [f'- {m}' for m in msgs] if msgs else ['No user requests could be recovered from the transcript.']
    body.append('Re-confirm project ID, as-of date, source revisions and open action IDs before continuing.')
    note.write_text('\n'.join(body) + '\n', encoding='utf-8')


if __name__ == '__main__':
    wt.run(main)
