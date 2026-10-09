# WalkThru Contracting: Claude Toolkit

Revision 1.1.0 · reviewed 08 Oct 2026. Local automated checks and packaging validated; real-project and authenticated Microsoft 365 acceptance remain pending. See `releases/acceptance-log.json`.

Originally prepared 07 Oct 2026. Online version of the report: https://claude.ai/artifact/4hsqKxDEf6BhCeabqhUdGv (private until shared).

## Contents

```
WalkThru-Skills/                 15 WalkThru skills built from the role profiles (see its README)
  general/ group-4/ dist/ share/ samples/
Group-4/Group-4-Training-Plan.docx   trainer plan for Operations + Planning (session 10 Oct 2026)
Re__Walk_Thru_AI_Program_Presentation_Day_1/   the 13 role profiles (source material)
report/
  WalkThru-Claude-Rollout.docx   Word version of the role-by-role report
  WalkThru-Claude-Rollout.html   Same report, open in a browser
plugins/walkthru-workflows/       generated WalkThru-only pilot plugin (15 maintained skills, M365/export fallback)
plugins/                         remaining folders: upstream reference snapshots; not configured deployment
  finance  legal  human-resources  operations  productivity
  enterprise-search  data  small-business  cowork-plugin-management
  gl-reconciler  month-end-closer          (from financial-services-plugins)
skills/
  skill-creator  internal-comms  mcp-builder     Anthropic (Apache 2.0)
  construction/   27 skills  DataDrivenConstruction, top construction skill repo (MIT)
  business/       12 skills  alirezarezvani/claude-skills, 28k stars (MIT)
  writing/humanizer          blader/humanizer, 54k stars (MIT): strips "AI-sounding" text
```

### Community skills: what they are and where they came from

These are community reference skills, retained with their licenses. Their original upstream commit IDs were not supplied, so `sources.json` records local snapshot hashes and reported origins without inventing commits. Popularity is not an approval criterion. The current review checks structure, Python syntax and the specifically documented runtime tests; it does not validate every community workflow. Several skills instruct Claude to run bundled Python through shell commands. Do not describe them as text-only or universally incapable of side effects. Review the chosen skill and script before deployment.

They were written for US/international practice. Company contract and finance policy must supply the applicable terms; the US AIA payment formats are references, not WalkThru's approved IPA format. No automatic upstream updates: acquire a known commit, review its diff/license and rerun the checks.

| Folder | Skills |
|---|---|
| construction/ (contracts & cost) | contract-clause-analyzer, contract-clause-extractor, change-order-manager, claims-documentation, payment-application-generator, retention-tracker, subcontractor-payment-tracker, budget-variance-analyzer, cash-flow-forecaster, estimate-builder, bid-analysis-comparator, subcontractor-prequalification |
| construction/ (planning) | look-ahead-scheduler, critical-path-analyzer, delay-analysis |
| construction/ (technical & docs) | specification-extractor, drawing-analyzer, submittal-tracker, rfi-management, material-procurement-tracker, document-classification-nlp, meeting-minutes-generator, as-built-tracker, warranty-tracker, punch-list-manager |
| construction/ (dashboards) | project-kpi-dashboard, portfolio-dashboard |
| business/ | ceo-advisor, coo-advisor, cfo-advisor, chro-advisor, board-deck-builder, financial-analyst, senior-pm, meeting-analyzer, procurement-optimizer, vendor-management, process-mapper, rfp-responder |

Looked at and skipped: archify (78k stars; Node.js toolchain for software diagrams), last30days (social-media research, needs API keys), DDC `daily-report-generator` (needs a weather API key), DDC CWICR cost-database skills (the database needs a commercial licence), legal-skills-open (no UAE construction or labour-law skills).

The Word, Excel, PowerPoint and PDF skills are **not** copied here. Their licence forbids keeping copies outside Claude, and they are already built into Claude on every paid plan with no setup.

## What each role gets

| Role | Plugins | Skills |
|---|---|---|
| Managing Director | enterprise-search, operations | ceo-advisor, board-deck-builder, portfolio-dashboard, humanizer |
| General Manager | operations, productivity | coo-advisor, project-kpi-dashboard, vendor-management, process-mapper |
| Chief Financial Officer | finance, month-end-closer | cfo-advisor, financial-analyst, cash-flow-forecaster, budget-variance-analyzer |
| Finance Manager | finance, gl-reconciler | budget-variance-analyzer, subcontractor-payment-tracker, retention-tracker |
| Chief Accountant | finance, month-end-closer | retention-tracker, subcontractor-payment-tracker |
| Contracts / Commercial & Estimation Manager | legal, small-business | contract-clause-analyzer, contract-clause-extractor, change-order-manager, claims-documentation, payment-application-generator, estimate-builder, bid-analysis-comparator, rfp-responder |
| Technical Manager | operations | specification-extractor, drawing-analyzer, submittal-tracker, rfi-management, material-procurement-tracker, procurement-optimizer |
| Planning Manager | data | look-ahead-scheduler, critical-path-analyzer, delay-analysis, senior-pm |
| Projects Coordinator | productivity, operations | meeting-minutes-generator, meeting-analyzer, punch-list-manager, internal-comms |
| HR & Administration Manager | human-resources, small-business | chro-advisor, internal-comms, humanizer |
| Senior Document Controller | enterprise-search, operations | document-classification-nlp, submittal-tracker, rfi-management, as-built-tracker, warranty-tracker |

## Install

1. **Plan:** Claude Team (or higher). Plugins and Office add-ins need a paid plan.
2. **Microsoft 365:** IT grants Entra consent and limits the pilot to authorized users; each user then connects their own work/school account. Start with read-only tools. Follow `config/plugin-setup.md`; consent is not proof that each user is connected.
3. **Office add-ins:** deploy Claude for Excel/Word/PowerPoint, plus Outlook (beta), from the Microsoft 365 admin center.
4. **Plugins (Cowork):** choose one route.
   - **Official, unmodified:** install from https://claude.com/plugins. For the finance agents, go to Settings → Plugins → Add plugin and paste `https://github.com/anthropics/financial-services`.
   - **WalkThru pilot (recommended):** use `releases/walkthru-workflows-1.1.0.zip`, built from the maintained 15 custom skills and one official Microsoft 365 endpoint. IT must complete the authenticated smoke checks in `config/plugin-setup.md`. Upstream role plugins stay reference-only until their selected workflows and connectors are separately tested. A simple replacement of connector names does not adapt tool schemas or permissions.
   - **Claude Code:** `claude plugin marketplace add anthropics/knowledge-work-plugins`, then `claude plugin install finance@knowledge-work-plugins`.
5. **Skills:** zip a skill folder (with `SKILL.md` at its root) and upload it in Claude's Skills settings. Team/Enterprise owners can share it org-wide.

## Not included, on purpose

- **Community MCP servers** (DWG reader, p6xer, AutoCAD COM): unaudited third-party code. IT should review them before anyone installs them. Links are in the report.
- **WhatsApp bridges:** they work only through the WhatsApp Business API and route data through another vendor.
- **financial-analysis plugin:** built for investment banking. It depends on paid market-data feeds (FactSet, PitchBook, S&P and others).

## Licences

`plugins/`: Apache 2.0, see the LICENSE files. Anthropic skills: Apache 2.0, see each `LICENSE.txt`. `skills/construction`, `skills/business`, `skills/writing`: MIT, see the LICENSE file in each folder plus `construction/NOTICE.md`.

## Maintain and validate

- Maintainer role: WalkThru AI lead / trainer. Department reviewers: Planning, Operations, Finance/Commercial; connector acceptance: IT. Named assignments are recorded at acceptance, not guessed.
- Shared project configuration: `config/project-context.example.json`; null means unknown. Supply actual calendars, project aliases, approved templates, review rules and financial terms per project.
- Shared evidence rules: `config/evidence-rules.md`, copied into each standalone skill by the builder. Facts, calculations and recommendations remain distinct and traceable.
- Canonical helpers: `maintenance/lib/`; never edit packaged copies independently.
- Build: `python3 maintenance/build_release.py`. Check: `python3 maintenance/validate_release.py` (tests, packages, metadata, syntax and references). Both work offline and use Python standard library.
- Release notes: `CHANGELOG.md`. Artifact SHA256 values: `releases/SHA256SUMS`; source manifest: `releases/manifest-1.1.0.json`.
- Historical evaluation outputs under `WalkThru-Skills-workspace/iteration-1` are examples, not proof of behavioral evaluation. New deterministic results and pending model/pilot cases are separated under `releases/`.
- Start each participant with two daily skills and one weekly workflow. Use the updated Group 4 plan and `Group-4/Workshop-1.1.0.md`.
