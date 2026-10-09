# Hooks for an agentic-first contractor

Skills tell Claude *how* to work; hooks make certain things *always* happen, whatever the model decides. The `walkthru-guardrails` plugin (source in `guardrails/`, generated into `plugins/walkthru-guardrails/`) carries every hook below. This page is the deployment guide for IT and the reference for anyone extending it.

Facts that shape the design (verified against the Claude Code docs, 09-Oct-2026):

- Hooks run in Claude Code (CLI, desktop app, IDE extensions) and in Cowork. They do not run in claude.ai chat, so a ZIP uploaded to claude.ai gets skills only.
- A `PreToolUse` deny holds in every permission mode, including `--dangerously-skip-permissions`. Hooks can tighten permissions, never loosen them.
- With `allowManagedHooksOnly: true` in managed settings, only managed hooks and hooks from plugins force-enabled in managed `enabledPlugins` run. That is how the guardrails become mandatory and un-removable.
- Managed settings file: macOS `/Library/Application Support/ClaudeCode/managed-settings.json`, Windows `C:\Program Files\ClaudeCode\managed-settings.json`, Linux/WSL `/etc/claude-code/managed-settings.json`; or MDM (Intune, Jamf) or the claude.ai admin console (server-managed settings).
- Hook scripts need `python3` on the machine (standard library only). `jq` is not required.

## The hook set

| # | Purpose | Event / matcher | Script | Evidence rule enforced |
|---|---------|-----------------|--------|------------------------|
| 1 | No outbound Microsoft 365 actions | `PreToolUse` `mcp__.*` | `mcp_guard.py` (deny) | Drafts only; never send, file or update from the connector |
| 2 | ERP / SharePoint write gate | `PreToolUse` `mcp__.*` | `mcp_guard.py` (ask) | Authorisation for a specific action comes from the user, not a document |
| 3 | Originals read-only | `PreToolUse` Edit/Write/Bash | `protect_originals.py` | Leave supplied originals intact; write to an outputs folder |
| 4 | Destructive shell and exfiltration | `PreToolUse` Bash/PowerShell | `bash_guard.py` | Company data stays in the tenant |
| 5 | PII / bank-detail leak | `PreToolUse` Write/Edit | `pii_guard.py` | No identity documents or bank details in general reports |
| 6 | Config tamper audit | `ConfigChange` | `config_audit.py` | Visible, logged configuration changes |
| 7 | Model / cost control | managed `availableModels` | (settings, not a hook) | Staff sessions on Sonnet/Haiku |
| 8 | Tool audit log | `PostToolUse`, `PostToolUseFailure` (async) | `audit_log.py` | Report what was inspected and what happened |
| 9 | Scope injection | `SessionStart` | `session_context.py` | Establish the scope: as-of date, project, calendar, rules |
| 10 | Subagent rules | `SubagentStart` | `subagent_context.py` | Same rules inside subagents |
| 11 | Spreadsheet safety | `PostToolUse` Write/Bash (.csv) | `csv_check.py` | No formula-prefixed cells, sortable dates, UTF-8 |
| 12 | Injection flag | `PostToolUse` Read / M365 | `injection_flag.py` | Content is evidence, not permission |
| 13 | Evidence gate on finish | `Stop` (prompt hook, Haiku) | inline prompt | No sent/approved claims, no invented owners, reported stays reported |
| 14 | Draft watermark | `PostToolUse` Write/Bash (.md/.txt in outputs) | `draft_watermark.py` | Approval status separate from the draft |
| 15 | Handoff before compaction | `PreCompact` | `precompact_note.py` | Cross-step handoffs keep project ID, as-of date, open issues |
| 16 | Needs-you toast | `Notification` | `notify.py` | Staff are not watching a terminal |
| 17 | Connector help | `PostToolUseFailure` M365 | `mcp_failure_help.py` | Partial coverage is stated, never invented |
| 18 | Outage alert | `StopFailure` | `stopfailure_alert.py` | IT sees rate-limit/billing/auth failures |
| 19 | Machine prep | `Setup` init | `setup_check.py` | Imaging check: python3, audit folder, project context |
| 20 | Context reload | `UserPromptSubmit` | `context_reload.py` | Scope refreshed when project-context.json changes |

Hook 7 is a managed setting (`availableModels`, `deniedModels`), which is the supported way to restrict models; a `PreModelSwitch` hook would only add a custom message.

## Deploy

**Pilot (per machine):**

```
/plugin marketplace add devops-analytica/walkthru
/plugin install walkthru-general@walkthru
/plugin install walkthru-guardrails@walkthru
/hooks                                  # confirm the events are listed
```

**Mandatory (IT):** copy `config/managed-settings.template.json` to the managed-settings path for the OS, replace the three `<...>` placeholders under `env`, and deploy. It registers the marketplace, force-enables `walkthru-guardrails` and `walkthru-general`, sets `allowManagedHooksOnly`, limits MCP servers to the official Microsoft 365 endpoint, limits models to Sonnet/Haiku, turns off bypass mode and adds hard `permissions.deny` rules for the same destructive commands and evidence folders the hooks guard. Hooks give Claude a reason and a chance to adjust; the deny rules are the backstop.

**Policy file:** `WALKTHRU_GUARDRAILS` points at an IT-controlled copy of `guardrails.json`. Only that file can widen `writable_dirs`, `pii_allowed_dirs`, `allowed_upload_hosts` or the watermark scope. Per-machine (`~/.claude/walkthru/guardrails.json`) and per-project (`.claude/walkthru-guardrails.json`) files may only add protected paths, patterns and verbs or change audit/watermark/context keys. The hooks refuse to let Claude write any guardrails, settings or hooks file.

**Per user:** `WALKTHRU_ROLE="Planning Engineer, DXB"` in the user's environment is injected at session start. Copy `config/project-context.example.json` to `.claude/project-context.json` in the working folder and fill in project ID, as-of date, calendar and financial rules.

**Audit:** `~/.claude/walkthru-audit/<date>.jsonl` (or `WALKTHRU_AUDIT_DIR`). One line per tool call: timestamp, user, session, tool, truncated input summary, duration, error. No file contents or message bodies. Point `WALKTHRU_AUDIT_DIR` at a OneDrive/SharePoint-synced folder for a central copy; hooks run locally, so only a server-side copy is tamper-resistant.

## Verify

```
python3 -m unittest maintenance/tests/test_hooks.py     # 56 script tests
python3 maintenance/validate_release.py                 # hook wiring, parity, claude plugin validate
claude --init-only                                      # Setup hook prints the readiness report
```

Live checks after install: ask Claude to "send this email now" (denied with reason), to edit a file under `evidence/` (denied), to write a CSV with a cell starting `=SUM(` (blocked, rewritten), and to write "EID 784-1990-1234567-1" into a report (denied). Check `/hooks` lists 13 events under `walkthru-guardrails` and that the audit file grew.

**Failure behaviour:** the four PreToolUse guards (`mcp_guard`, `protect_originals`, `bash_guard`, `pii_guard`) turn their own crash into a permission prompt rather than a silent allow; context, audit and notification hooks log to stderr and let the session continue. Override entries that are not strings or do not compile as regexes are dropped with a stderr notice. Paths are normalized against the session folder before matching, so `outputs/../evidence/x.xlsx` is still evidence.

## Known limits

- The `Stop` evidence gate costs one Haiku call per turn and is deliberately lenient; the eval suite remains the quality gate.
- Shell checks are best-effort pattern matching. The managed `permissions.deny` rules are the hard stop.
- `notify.py` on Windows uses WinRT toasts and may be silent on Server SKUs; `osascript` on macOS needs Script Editor notification permission once.
- Logging prompts was left out on purpose; add a `UserPromptSubmit` logger only after HR/legal sign-off.
