# Synthetic practice requests

Fictional data, not live WalkThru records. Expected outcomes are reviewer criteria.

## Case 1
Request: As of 2026-10-09 update my tender list.
Input: T-101 Hotel fit-out, AUH, submission 2026-10-08, status pricing, estimator Sara. T-102 Villa cluster, DXB, site visit 2026-10-12, clarifications 2026-10-14, submission 2026-10-20, no estimator. T-103 Office tower, DXB, submission blank, status "waiting quotes". T-104 Clinic, AUH, submitted 2026-10-02.
Expected: T-101 overdue 1 day (not Submitted; confirm whether it was submitted); T-102 driven by site visit in 3 days, unassigned flagged "To confirm"; T-103 missing date; T-104 Submitted, closed from deadline watch; no invented estimators.

## Case 2
Request: Pipeline summary for the Saturday report.
Input: 3 rows Submitted (values 12M, 40M, blank), 1 Awarded 25M, 2 Lost, 2 forecast tenders "approx 60M" and "TBC".
Expected: counts by status, submitted value total stated as 52M with one value unknown (not zero), forecast listed separately, no win rate claimed beyond supplied outcomes.
