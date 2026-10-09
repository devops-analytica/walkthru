# walkthru-planning · 2.1.0

Skills in this plugin:
- `p6-programme-review` — P6 Schedule Health and Float Review
- `planning-weekly-report` — Planning Weekly / Monthly Report
- `programme-comment-response` — Programme Comment Response Sheet
- `project-setup-brief` — Project Setup Brief

The toolkit ships one plugin per department plus `walkthru-general` (skills every role uses) and `walkthru-workflows` (everything in one package). Install **either** `walkthru-workflows` **or** `walkthru-general` + your department plugin — not both, or the same skills are discoverable twice. Standalone skill ZIPs (`releases/<version>/skills/`) are for training and claude.ai personal uploads; do not mix them with a plugin install of the same skills.

## Install

Claude Code (2.1.275 or later), from the published repository:

```
/plugin marketplace add analytica-data/WalkThru-Claude-Toolkit
/plugin install walkthru-planning@walkthru
```

From a local checkout of the toolkit:

```
/plugin marketplace add /path/to/WalkThru-Claude-Toolkit
/plugin install walkthru-planning@walkthru
```

claude.ai / Claude Desktop (organisation plugin upload): upload `releases/2.1.0/plugins/walkthru-planning-2.1.0.zip` through the organisation's supported plugin route. Confirm the metadata and every skill above is visible after install.

Slash commands bundled with the department plugins run the starter routines (for example `/walkthru-general:morning`, `/walkthru-planning:planning-week`). Skills also trigger on their own from ordinary requests ("what's expiring", "draft the DPR", "check this invoice").

## Connection and permissions

The plugin has one HTTP MCP entry: `microsoft365`, pointing to the official `https://microsoft365.mcp.claude.com/mcp` endpoint. This configuration does not grant tenant consent, authenticate users, or enforce a tool allowlist by itself.

1. IT grants Microsoft Entra admin consent for the official connector and restricts the rollout to the pilot group. Keep write scopes/tools disabled for the pilot. If writes were already enabled, disable/restrict them in the tenant and Claude tool settings; skill instructions are not an access-control boundary.
2. Each participant connects their own work/school Microsoft 365 account in Claude. Tenant consent alone does not connect everybody. No personal account for company data.
3. Use available Outlook email search, calendar search, SharePoint search, Teams message search and resource-read tools. Full message/document evidence is required after search hits.
4. If the connector cannot authenticate, a tool is absent, pagination is incomplete or access is denied, record partial coverage and use a supplied export. No claims of tenant-wide completeness and no invented results.
5. ePromis and P6 remain export-based. There is no direct ERP approval or P6 write integration in this package.

Skills that run a bundled helper (`invoice-po-check`, `walkthru-deadline-watch`, `p6-programme-review`, `planning-weekly-report`) need `python3` on the machine or in the Claude sandbox; the helpers use the standard library only.

## Installation smoke check (IT and trainer)

Record environment, account, date, plugin version and result for each check in `evaluation/tenant-acceptance.json`:

- Install the plugin by one of the routes above. Confirm metadata, all skills and (Claude Code) the slash commands are visible.
- Run the bundled evals: `claude plugin eval ./plugins/walkthru-planning` from the toolkit checkout. Every case asserts the right skill fired and the answer respects the evidence rules.
- Search for a known synthetic test email, read the full message and confirm the correct time window/source reference. Follow pagination or show a partial-coverage warning.
- Search/read a known pilot SharePoint document, then confirm another user cannot access a restricted test document.
- Confirm write tools are unavailable to the pilot; do not send a message as a smoke test. Draft an email locally and verify no external action occurred.
- Disconnect/deny the connector and verify the uploaded-export fallback explicitly says it has no mailbox access.

Local package/configuration checks are automated. Authenticated tenant checks are **pending** until IT runs them; a valid URL and JSON file are not proof of working tenant integration.

Sources checked 08 Oct 2026:
- https://claude.com/marketplace/connectors/microsoft-365
- https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector

## Starter routines

- Hosam (planning): `/walkthru-general:morning` daily; `/walkthru-planning:planning-week` weekly.
- Menna (role to confirm): `/walkthru-general:morning` daily + Chat to Actions as chats arrive; weekly P6 Schedule Health Review.
- Wissam (operations, AUH): `/walkthru-general:morning` + `/walkthru-site-operations:site-day` daily; `/walkthru-finance-commercial:invoice-check` weekly.
- Kareem (estimation/commercial): `/walkthru-estimation-commercial:tender-week` weekly; quotation comparison and BOQ/spec check per tender.
- Salah (technical): `/walkthru-engineering:technical-review` daily.
- Rawad / Hady / Islam (finance): `/walkthru-finance-commercial:finance-day` daily; `monthly-owners-report` at month-end.
- Chadi / George (PRO, HR): `/walkthru-hr-admin:pro-day` daily; attendance/OT check and MOHRE renewal batches as needed.
- Rami (operations, DXB): `/walkthru-general:morning` + `/walkthru-site-operations:site-day` daily; `/walkthru-engineering:engineering-week` weekly.

Additional skills are introduced after each participant completes one reviewed result on those routines. Contractual, tax, payroll or certification decisions remain with the responsible department.
