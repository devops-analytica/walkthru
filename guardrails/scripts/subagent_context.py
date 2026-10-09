#!/usr/bin/env python3
"""SubagentStart: subagents do not inherit skill context, so hand them the evidence rules and scope."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt_hooks as wt
import scope


def main():
    data = wt.read_input()
    wt.context(scope.scope_text(wt.load_config(data), data), 'SubagentStart')


if __name__ == '__main__':
    wt.run(main)
