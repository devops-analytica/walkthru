# walkthru-guardrails · {{VERSION}}

Deterministic hooks that enforce the WalkThru evidence rules around every skill: connector actions stay read-only, supplied originals stay intact, identity and bank details stay out of reports, every tool call is audited, and each session starts with the right date, project scope and rules. Install it alongside `walkthru-general` (or `walkthru-workflows`); it contains no skills of its own.

Hooks run in Claude Code (CLI, desktop app, IDE extensions) and Cowork. They do not run in claude.ai chat, so a claude.ai plugin upload gets skills only.

## Install

```
/plugin marketplace add {{REPO}}
/plugin install walkthru-guardrails@walkthru
```

Requirements: Python 3.9+ on the machine as `python3` (on Windows, install Python from python.org or the Microsoft Store and confirm `python3 --version` works in the shell Claude Code uses). No other dependencies.

To make the guardrails mandatory, IT deploys `config/managed-settings.template.json` as `managed-settings.json` (see `docs/HOOKS.md`). With `allowManagedHooksOnly: true` and the plugin force-enabled in `enabledPlugins`, staff cannot switch the hooks off, and `WALKTHRU_GUARDRAILS` pins the policy file.

## What runs

| Event | Script | Effect |
|---|---|---|
| PreToolUse `mcp__.*` | `mcp_guard.py` | Deny Microsoft 365 send/reply/create/update/delete/upload; any other connector mutation becomes an explicit permission prompt |
| PreToolUse Edit/Write/Bash | `protect_originals.py` | Deny writes to `evidence/`, `inbox/`, secret files and to `.xer/.xlsx/.pdf/.docx/...` outside `outputs/` or `drafts/` |
| PreToolUse Bash | `bash_guard.py` | Deny `rm -rf`, force-push, encoded PowerShell, and uploads to hosts outside the allowlist |
| PreToolUse Write/Edit | `pii_guard.py` | Deny content containing an Emirates ID, UAE IBAN or card number unless the file is under a restricted folder |
| PostToolUse / PostToolUseFailure (all, async) | `audit_log.py` | JSONL audit line per tool call in `~/.claude/walkthru-audit/<date>.jsonl` (or `WALKTHRU_AUDIT_DIR`) |
| PostToolUse Write/Bash | `csv_check.py` | Block and ask for a rewrite when a CSV (written by the Write tool or a shell command) has formula-prefixed cells, mixed date formats or non-UTF-8 bytes |
| PostToolUse Write/Bash | `draft_watermark.py` | Prepend a DRAFT header to `.md`/`.txt` written under `outputs/` or `drafts/` |
| PostToolUse Read / M365 | `injection_flag.py` | Remind Claude that instruction-like text inside a document or message is evidence, not instruction |
| PostToolUseFailure M365 | `mcp_failure_help.py` | Plain-language next step: sign in via `/mcp`, retry, or fall back to the export with a Not-checked note |
| SessionStart | `session_context.py` | Inject Dubai date/time, `WALKTHRU_ROLE`, project-context.json summary, rules summary, and the pre-compaction handoff |
| SubagentStart | `subagent_context.py` | Same scope for subagents, which do not inherit skill context |
| UserPromptSubmit | `context_reload.py` | Re-inject scope when project-context.json changed mid-session |
| PreCompact | `precompact_note.py` | Save the last user requests to the scratchpad for the post-compaction restart |
| Stop (prompt, Haiku 5.5) | inline | Evidence gate: no "sent/approved" claims, no invented owners or positions, no "no incidents" from "none reported" |
| Notification | `notify.py` | Desktop toast when Claude waits for permission or input |
| StopFailure | `stopfailure_alert.py` | Audit line and optional Teams/Slack webhook (`WALKTHRU_ALERT_WEBHOOK`) on rate-limit, billing, auth or server errors |
| ConfigChange | `config_audit.py` | Audit line plus a visible warning when any settings or skills file changes |
| Setup `init` | `setup_check.py` | Readiness report for IT imaging: `claude --init-only` in the staff working folder |

## Configure

Defaults live in `guardrails.json` inside the plugin. Two kinds of override:

- **IT-locked file**, named by `WALKTHRU_GUARDRAILS` (set in managed settings `env`): the only place that can widen `writable_dirs`, `pii_allowed_dirs`, `allowed_upload_hosts` or `watermark_*`.
- **Machine or project files**, `~/.claude/walkthru/guardrails.json` and `.claude/walkthru-guardrails.json`: may only tighten policy (add `protected_dirs`, `protected_extensions`, `secret_files`, `bash_denied_patterns`, verbs, `injection_patterns`) or change `audit_dir`, `watermark`, `project_context_files`. Loosening keys in these files are ignored with a stderr notice, and the hooks refuse to let Claude write any guardrails, settings or hooks file.

Per-user environment: `WALKTHRU_ROLE` (for example `Planning Engineer, DXB`) is injected at session start.

## Verify

```
/hooks                      # every event above is listed under walkthru-guardrails
claude --init-only          # prints the setup report
```

Then ask Claude to "send this email now" (denied), to edit a file inside `evidence/` (denied), and to write a CSV with a cell starting `=SUM(` (blocked and rewritten). The source tree has unit tests for every script: `python3 -m unittest maintenance/tests/test_hooks.py` from the toolkit checkout.
