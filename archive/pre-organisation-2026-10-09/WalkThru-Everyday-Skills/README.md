# WalkThru everyday skills — first batch

Eight standalone employee workflows, version 1.0.0, built 09-Oct-2026 from the supplied WalkThru role profiles and maintained toolkit drafts. Source is in `skills/`; upload packages are in `dist/`. This is a separate pilot pack, not an installation or an update to the original toolkit.

## Included
1. **Morning priorities and email triage** — `walkthru-morning-brief`
2. **Action tracker and follow-up assistant** — `walkthru-action-tracker`
3. **Meeting minutes and actions** — `walkthru-meeting-minutes`
4. **Project correspondence assistant** — `walkthru-letters`
5. **Daily site report and next-day priorities** — `daily-site-report-digest`
6. **Submittal, RFI and inspection follow-up** — `submittal-wir-tracker`
7. **Materials and delivery tracker** — `walkthru-material-delivery-tracker`
8. **Invoice and payment-request pre-check** — `invoice-po-check`

## Use and rollout
Upload the individual skill ZIP from `dist/` to the employee's skill-capable environment. The all-skills bundle is for transfer: unpack it first; do not upload that outer bundle as one skill. For a filesystem-based skill runner, copy the relevant folder from `skills/` into its configured skills directory. No account connection or org-wide deployment has been performed.

Seven skills reuse existing names. Replace an older installed skill of the same name rather than keeping duplicates; `walkthru-material-delivery-tracker` is new. Existing chat-to-actions, management-update and other toolkit skills are outside this eight-skill batch and remain separate.

Start each employee with two relevant skills, not all eight. Office/coordinators: morning brief + action tracker. Site/operations: site report + materials tracker. Technical/document control: engineering tracker + correspondence. Finance/accounts: invoice pre-check + action tracker. Meeting minutes can be shared across teams as needed.

Each skill includes concise instructions, a fallback editable template, common evidence/project-context guidance, and two synthetic practice requests with expected review outcomes. Invoice pre-check additionally includes the maintained Decimal-based Python helper and a synthetic normalized invoice.

Supply the department's actual template and project context: legal entity, status legend, working calendar, review terms, authority matrix and required data. Null values in the example configuration mean unknown. Templates are fallback formats, not claimed approved WalkThru forms. Use exports first; live access is optional and no direct ePromis integration is assumed.

## Acceptance before employee rollout
Run both practice cases per skill, then a department reviewer should test anonymised real records and record results in `evaluation-cases.json` or a separate acceptance log. Check factual accuracy, retained IDs/revisions, due-date basis, missing-evidence handling, usefulness and output template fit. No model-driven or real-project acceptance has been claimed. Deterministic script and package results are recorded in `validation-report.json`.

Rebuild and check: `python3 maintenance/validate_and_package.py`. This validates skill structure, references, assets, invoice regression tests and ZIP parity using Python standard library. Skill-creator format validation is recorded separately when available. No network, live changes or email sending is needed.
