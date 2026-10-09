# Synthetic practice requests

Fictional data, not live WalkThru records. Expected outcomes are reviewer criteria.

## Case 1
Request: Check these BOQ lines against the spec.
Input: BOQ 5.1 "Porcelain floor tile 600x600, 10 mm" 420 m2; Spec 09 30 00 cl 2.1: "porcelain tile 600x600, 12 mm, R10 slip rating in wet areas, approved-list brand". Takeoff export (KREO): floor tile 455 m2. Drawing list has a tile schedule A-601 rev C; BOQ says "per A-601 rev B". No BOQ line for tile adhesive or movement joints; spec cl 3.4 requires both.
Expected: thickness conflict (10 vs 12 mm), slip rating and brand not in BOQ text, 35 m2 difference (calculation, 455-420, about 8.3% of BOQ), drawing revision B vs C, adhesive and movement joints as possible omissions to confirm.

## Case 2
Request: Review this dry cost line.
Input: BOQ 7.4 "Chilled water pipe 100 mm, supply and install", rate 310/m = material 140 + manpower 60 + wastage 0 + subcontract (insulation) 70. No quotation reference for insulation.
Expected: sums to 270 not 310 (calculation, 40 unexplained); wastage blank means not stated, not zero; insulation component unsupported by a quote; no claim the rate is wrong, only that the build-up does not reconcile.
