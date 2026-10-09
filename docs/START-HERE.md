# Manage the WalkThru toolkit

Open `../index.html` for the searchable skill catalogue, role filters and current download links.

## One current source per skill
Edit only `skills/<department>/<skill-name>/`. There are 29 unique WalkThru skills across eight department folders: general, site-operations, engineering, procurement, finance-commercial, planning, estimation-commercial and hr-admin. The 13 skills added on 09-Oct-2026 were derived from the employee role profiles in `references/employee-profiles/` (estimation, technical review, finance reporting, HR/PRO).

Use `catalog.json` to track title, department, source and acceptance. Update shared evidence/settings in `config/`; canonical helpers in `maintenance/lib/`. Run `python3 maintenance/build_release.py`, then `python3 maintenance/validate_release.py`, then `claude plugin eval ./plugins/walkthru-workflows --trust-plugin --ablation none --runs 1` and record the result in `releases/<version>/`. Never edit generated plugin/ZIP copies. Both run offline; no live account actions occur.

## Install and assign
Choose one route per person: (a) individual ZIPs in `releases/2.1.0/skills/<department>/` for training and personal claude.ai uploads; (b) Claude Code marketplace — `/plugin marketplace add <repo>` then `walkthru-general@walkthru` plus the department plugin; or (c) the all-in-one `walkthru-workflows` plugin (ZIP under `releases/2.1.0/plugins/` or via the marketplace). Never install two routes that contain the same skill. Replace previously installed matching names; do not add duplicates. Installing and connecting accounts is a separate employee/IT task.

Start employees with the slash-command routines in `config/plugin-setup.md`, or two relevant skills. Coordinators: morning brief + action tracker. Site/operations: daily report + materials tracker. Engineering/document control: engineering follow-up + correspondence. Accounts: invoice checker + action tracker. Planning: P6 review + weekly reporting. Add shared meeting minutes when useful.

Use the employee's actual templates and project facts. No draft template or configuration example is an approved company policy. Follow config/plugin-setup.md for the optional connector setup; exports remain supported. Department/model/tenant acceptance is pending, even when local checks pass.

## What belongs where
- `skills/`: maintained WalkThru source only.
- `commands/<department>/`: starter-routine slash commands; copied into the matching plugin.
- `evals/<skill>-<n>/`: behavioral cases (prompt + graders) for `claude plugin eval`.
- `plugins/`: generated department/all-in-one plugins only.
- `releases/`: versioned outputs, checksums and current local validation.
- `references/`: employee profiles and licensed community/plugin snapshots; reference-only.
- `docs/`: this guide, skill catalogue and clearly labelled historical training/reports.
- `samples/`: synthetic demo files; skill-specific templates/practice stay with each skill.
- `evaluation/`: behavioral cases and acceptance records, separate from automated tests.
- `archive/`: earlier layout, release records and historical evaluations; do not edit as current source.

Earlier Word training/report documents are retained under docs/legacy-* for context. Their original folder names/version claims are historical; use this guide and the current catalogue for paths and packages.
