# Toolkit changes

## 1.1.0 · 08 Oct 2026

- Fixed fractional positive/negative float classification by comparing unrounded values; project-specific data dates; primary and secondary constraints; original/remaining duration; in-progress finish look-ahead. Explicit calendar/unit warnings and invalid-input errors. Schedule outputs are health/float indicators, not an ordered driving path or baseline proof.
- Introduced one canonical source for helpers and shared evidence/configuration references, automatically copied into standalone skills and the WalkThru plugin.
- Added Decimal material-invoice reconciliation, cumulative accepted deliveries minus prior billing, single-counted line differences, duplicate/evidence states, confirmed tax inputs and no approval claims. Expiry logic distinguishes approved/renewed permits from completed tasks. Progress variance is actual−planned in percentage points.
- Programme responses distinguish Proposed/Implemented/Verified and remain Open until verified. Cover letters report actual closed/open counts. No assumed contractual review periods or universal tax bases.
- Added evidence references, project configuration examples, template/revision precedence, source conflict handling and explicit data coverage to all 15 maintained skills.
- Built a WalkThru-only plugin with one official M365 endpoint, per-user/admin setup, export fallback, no-write workshop instructions and authenticated smoke-check requirements. Unmodified upstream plugins remain reference snapshots, not an approved deployment.
- Updated both Word documents, the HTML rollout report, READMEs and sample invoice evidence wording. Sequential one-trainer workshops start with two daily skills and one weekly workflow per person; quality and review time count in adoption metrics.
- Added automated helper/CLI tests, package/reference/checksum checks, 70 pending behavioral scenarios and an honest external acceptance log. Historical sample outputs are labeled illustrative, not reproducible benchmark evidence.
- Recorded artifact/source SHA256 values and reported vendor origins. Original upstream commit IDs were not available and have not been invented. Future refreshes require a verified commit and reviewed diff/license.

## Original snapshot · 07–08 Oct 2026

15 custom skills, upstream skill/plugin collections, two illustrative evaluation outputs, source role profiles, training plan and rollout report. Source profiles and upstream licenses remain unchanged.
