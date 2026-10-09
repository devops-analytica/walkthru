# Organisation release 2.1.0 — 09-Oct-2026

- Rewrote all 16 skill descriptions with explicit "Use when" trigger phrases and WalkThru vocabulary (DPR, LPO, WIR, MOM, IPA, XER…) so skills fire from ordinary requests; validator now requires a trigger clause and allows up to 1024 characters.
- Helpers invoked as `python3`; the four script-bearing skills declare `allowed-tools: Bash(python3 *) Read Write`.
- Added five starter-routine slash commands (`/walkthru-general:morning`, `site-day`, `planning-week`, `invoice-check`, `engineering-week`).
- Build now emits `walkthru-general` + five department plugins and the all-in-one `walkthru-workflows`, plus a root `.claude-plugin/marketplace.json` for Claude Code installs.
- Added 24 behavioral eval cases (`evals/`) runnable with `claude plugin eval`; each asserts the correct skill fired and an LLM-judged reviewer criterion.
- Repository initialised with git and `.gitignore`; generated `__pycache__`, `.DS_Store` and eval results excluded.
- Departmental/model and tenant acceptance stays pending. No upstream downloads or live account changes.

# Organisation release 2.0.0 — 09-Oct-2026

- Consolidated the 15-skill toolkit and eight-skill daily pack into 16 unique current skills. Seven overlapping names use the newer everyday instructions; eight other workflows remain, plus the new materials tracker.
- Grouped sources by department and added a searchable catalogue and management guide.
- Isolated byte-preserved third-party/employee references from maintained sources and generated deployment copies.
- Updated build and validation for the catalog-driven 16-skill release; old releases/layout retained for traceability.
- Departmental/model and tenant acceptance stays pending. No new upstream downloads or live account changes.
