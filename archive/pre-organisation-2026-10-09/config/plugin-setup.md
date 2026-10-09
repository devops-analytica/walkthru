# WalkThru workflow plugin · 1.1.0

This package contains only the 15 WalkThru-specific workflows. The other folders under `plugins/` are upstream reference snapshots, not a configured WalkThru deployment. Install the role's minimum starter set of standalone skills for training, or this plugin for a managed pilot; avoid installing both routes together because the same skills will be discoverable twice.

## Connection and permissions

The plugin has one non-empty HTTP MCP entry: `microsoft365`, pointing to the official `https://microsoft365.mcp.claude.com/mcp` endpoint. There are no Slack/Gmail/Notion or empty placeholder endpoints in this custom plugin. This configuration does not grant tenant consent, authenticate users, or enforce a tool allowlist by itself.

1. IT grants Microsoft Entra admin consent for the official connector and restricts the rollout to the pilot group. Keep write scopes/tools disabled for this workshop. If writes were already enabled, disable/restrict them in the tenant and Claude tool settings; skill instructions are not an access-control boundary.
2. Each participant connects their own work/school Microsoft 365 account in Claude. Tenant consent alone does not connect everybody. No personal account for company data.
3. Use available Outlook email search, calendar search, SharePoint search, Teams message search and resource-read tools. Do not assume Gmail/Slack tool names can simply be replaced. Full message/document evidence is required after search hits.
4. If the connector cannot authenticate, a tool is absent, pagination is incomplete or access is denied, record partial coverage and use a supplied export. No claims of tenant-wide completeness and no invented results.
5. ePromis and P6 remain export-based. There is no direct ERP approval or P6 write integration in this package.

## Installation smoke check (IT and trainer)

Record environment, account, date, plugin version and result for each check in `releases/acceptance-log.json` (use the toolkit copy if this plugin was uploaded by itself):

- Upload `releases/walkthru-workflows-1.1.0.zip` using the organization's supported plugin upload route. Confirm metadata and all 15 skills are visible. Not authenticated/tested by the local build.
- Search for a known synthetic test email, read the full message and confirm the correct time window/source reference. Follow pagination or show a partial-coverage warning.
- Search/read a known pilot SharePoint document, then confirm another user cannot access a restricted test document.
- Confirm write tools are unavailable to the pilot; do not send a message as a smoke test. Draft an email locally and verify no external action occurred.
- Disconnect/deny the connector and verify the uploaded-export fallback explicitly says it has no mailbox access.
- Remove any duplicate standalone installs if using the plugin route. Re-check skill discovery after restart.

Local package/configuration checks are automated. These authenticated checks are **pending** until IT runs them; a valid URL and JSON file are not proof of working tenant integration.

Sources checked 08 Oct 2026:
- https://claude.com/marketplace/connectors/microsoft-365
- https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector

## Starter routines

- Hosam: daily Morning Brief + Action Tracker; weekly Planning Weekly Report (which can invoke the schedule helper).
- Menna (role still to confirm): daily Morning Brief + Chat to Actions; weekly P6 Schedule Health Review.
- Wissam: daily Morning Brief + Daily Site Report Digest; weekly Invoice vs PO Check.
- Rami: daily Morning Brief + Daily Site Report Digest; weekly Submittal/WIR Tracker.

Additional skills are introduced after each participant completes one reviewed result on those routines. Contractual, tax, payroll or certification decisions remain with the responsible department.
