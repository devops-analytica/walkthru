# WalkThru contracting toolkit

Organisation release 2.1.0 · 09-Oct-2026. **Start with [index.html](index.html)** or [docs/START-HERE.md](docs/START-HERE.md).

29 unique maintained WalkThru skills across 8 departments, shipped three ways from one source tree: standalone skill ZIPs, one Claude plugin per department (plus `walkthru-general` for every role), and an all-in-one plugin — all listed in a Claude Code marketplace at the repo root. Only `skills/`, `commands/`, `evals/` and `config/` are source; `plugins/` and `releases/` are generated.

```
index.html                 searchable current skill catalogue
catalog.json               maintained source/department/acceptance map
.claude-plugin/            marketplace.json (generated) — /plugin marketplace add <this repo>
skills/<department>/       general · site-operations · engineering · procurement
                           finance-commercial · planning · estimation-commercial · hr-admin
commands/<department>/     starter-routine slash commands (/walkthru-general:morning …)
evals/                     behavioral eval cases for `claude plugin eval`
config/                    shared evidence rules, project settings, plugin README template
maintenance/               build, validation, canonical helpers and tests
plugins/                   generated plugins; do not edit
releases/<version>/        skill ZIPs, bundles, plugin ZIPs, checksums, validation, eval results
references/                employee profiles, community skills, upstream plugins
samples/                   synthetic demonstrations
evaluation/                behavioral case sources and acceptance records
docs/                      current management guide and historical reports
archive/                   original layout and historical results
```

Build: `python3 maintenance/build_release.py`
Validate: `python3 maintenance/validate_release.py`
Behavioral evals: `claude plugin eval ./plugins/walkthru-workflows --trust-plugin --ablation none --runs 1`

Install (Claude Code): `/plugin marketplace add devops-analytica/walkthru` then `/plugin install walkthru-general@walkthru` + `walkthru-<department>@walkthru`, **or** `walkthru-workflows@walkthru` alone. See `config/plugin-setup.md`.

Local tests and evals are separate from real employee/project acceptance, which remains pending. No live integration, org-wide deployment or email sending was performed. The earlier layout is preserved in archive/pre-organisation-2026-10-09; do not install duplicate archived skills.
