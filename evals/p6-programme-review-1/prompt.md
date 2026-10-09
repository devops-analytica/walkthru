---
max_turns: 10
timeout_seconds: 600
runs: 1
allowed_tools: [Read, Glob, Grep, Skill]
tags: [p6, p6-programme-review]
---

I exported our tower project programme from P6 to Excel. Columns: Activity ID, Activity Name, Total Float, Start, Finish, Activity Status, Primary Constraint. Rows:
A100 | Mobilise | 0 | 2026-09-01 | 2026-09-10 | Completed | -
A200 | Excavation | -3 | 2026-09-11 | 2026-10-05 | In Progress | -
A300 | Raft slab | 2 | 2026-10-06 | 2026-10-20 | Not Started | Must Finish On
A400 | Columns L1 | 15 | 2026-10-21 | 2026-11-05 | Not Started | -
Data date 09-Oct-2026. What's critical and what's delayed?
