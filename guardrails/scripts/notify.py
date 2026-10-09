#!/usr/bin/env python3
"""Notification (permission_prompt|idle_prompt): desktop toast on macOS, Windows or Linux."""
import os, platform, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt


def toast():
    """Command that reads WT_TITLE / WT_MSG from its environment, so notification text is never spliced into code."""
    system = platform.system()
    if system == 'Darwin' and shutil.which('osascript'):
        return ['osascript', '-e', 'display notification (system attribute "WT_MSG") with title (system attribute "WT_TITLE")']
    if system == 'Windows':
        ps = ("[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null;"
              "$x=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
              "$t=$x.GetElementsByTagName('text');$t.Item(0).AppendChild($x.CreateTextNode($env:WT_TITLE))|Out-Null;$t.Item(1).AppendChild($x.CreateTextNode($env:WT_MSG))|Out-Null;"
              "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show([Windows.UI.Notifications.ToastNotification]::new($x))")
        return ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', ps]
    if shutil.which('notify-send'):
        return ['notify-send', '--', '$WT_TITLE', '$WT_MSG']  # placeholders replaced below; notify-send takes plain arguments
    return None


def main():
    data = wt.read_input()
    title = str(data.get('title') or 'Claude Code')[:80]
    message = str(data.get('message') or 'Claude Code needs your attention')[:200]
    cmd = toast()
    if not cmd:
        return
    cmd = [title if c == '$WT_TITLE' else message if c == '$WT_MSG' else c for c in cmd]
    subprocess.run(cmd, check=False, timeout=10, capture_output=True, env={**os.environ, 'WT_TITLE': title, 'WT_MSG': message})


if __name__ == '__main__':
    wt.run(main)
