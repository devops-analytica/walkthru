# Behavioral evals

One directory per case: `prompt.md` (the employee's request, natural phrasing) + `graders/skill-fired.md` (asserts the right skill was invoked) + `graders/rubric.md` (LLM-judged reviewer criterion from `evaluation/everyday-cases.json`). Case directories are named `<skill-name>-<n>`; the build copies each case into every plugin that ships that skill.

Run from the toolkit root (needs the `claude` CLI and your own credentials):

```
claude plugin eval ./plugins/walkthru-workflows --trust-plugin --ablation none --runs 1 --json releases/<version>/evals.json
claude plugin eval ./plugins/walkthru-general --case 'walkthru-morning-brief-*'
```

A passing run is model-behaviour evidence for the model named in the results, not departmental or tenant acceptance.
