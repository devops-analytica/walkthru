# Behavioral and pilot acceptance

The 70 cases in behavioral-cases.json are authored review scenarios, not recorded model runs. Deterministic tests validate the helpers; they cannot establish whether Claude invokes a skill correctly, extracts a PDF accurately or follows the evidence rules.

Use the installed 1.1.0 skill/plugin in a fresh conversation per case. Supply the scenario prompt as synthetic evidence with labels/references, plus the actual skill. Record exact prompt/input attachments, model/version, date, active skills, response and artifact paths. Review the expected invariants against the output. Mark Pass only when those invariants hold; Fail and explain otherwise. Never overwrite an expected result to match a failed run. Save normalized outputs under a new dated evaluation directory. Repeat failed cases after a correction and rebuild/revalidate packages.

The invoice/P6/deadline/progress fixture inputs in maintenance/tests/fixtures also run through the helpers without a model. Use them as reproducible workshop fallbacks; use the existing daily reports for the digest.

External acceptance includes a real WalkThru XER and anonymized transaction/register data checked by the departments, plus authenticated tenant checks. Record these in acceptance-log.json. There is no fabricated pilot pass and no claim of production readiness until the responsible reviewers complete them. Use company accounts and preserve the workshop’s draft-only/no-write boundary.
