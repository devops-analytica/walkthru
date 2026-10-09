#!/usr/bin/env python3
"""Overtime vs supplied limits. Reads normalized JSON, writes JSON to --out (never overwrites input).

Input: {"as_of": "YYYY-MM-DD", "daily_limit_hours": n|null, "weekly_limit_hours": n|null,
        "week_start": 0-6 (Mon=0)|null, "limit_source": "...",
        "records": [{"employee": "...", "project": "...", "date": "YYYY-MM-DD", "ot_hours": n, "source": "..."}]}
Limits are never defaulted: a missing limit or week_start gives "To confirm", not a breach or a pass.
Weekly totals are only what the records show (days_with_records), not proof of a full week.
"""
import argparse
import json
import sys
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path


def num(v, what):
    try:
        n = Decimal(str(v))
    except InvalidOperation:
        raise ValueError(f"{what}: invalid number {v!r}")
    if not n.is_finite() or n < 0:
        raise ValueError(f"{what}: must be a non-negative number, got {v!r}")
    return n


def opt(v, what):
    return None if v is None else num(v, what)


def run(d):
    daily, weekly = opt(d.get("daily_limit_hours"), "daily_limit_hours"), opt(d.get("weekly_limit_hours"), "weekly_limit_hours")
    ws = d.get("week_start")
    if ws is not None and ws not in range(7):
        raise ValueError("week_start must be 0-6 (Mon=0) or null")
    day_tot, srcs = defaultdict(Decimal), defaultdict(list)
    for i, r in enumerate(d["records"]):
        who = r.get("employee_id") or r["employee"]
        day = date.fromisoformat(r["date"])
        day_tot[(who, r["employee"], day)] += num(r["ot_hours"], f"records[{i}].ot_hours")
        srcs[(who, day)].append(r.get("source", "not supplied"))
    out = {"as_of": d.get("as_of"), "limit_source": d.get("limit_source", "not supplied"),
           "daily_limit_hours": None if daily is None else str(daily), "weekly_limit_hours": None if weekly is None else str(weekly),
           "daily": [], "weekly": []}
    wk = defaultdict(lambda: [Decimal(0), set()])
    for (who, name, day), h in sorted(day_tot.items(), key=lambda x: (x[0][0], x[0][2])):
        status = "To confirm (no daily limit supplied)" if daily is None else "Over limit" if h > daily else "Within limit"
        out["daily"].append({"employee": name, "date": day.isoformat(), "ot_hours": str(h), "status": status,
                             "over_by": str(h - daily) if daily is not None and h > daily else None, "sources": srcs[(who, day)]})
        if ws is not None:
            start = day - timedelta(days=(day.weekday() - ws) % 7)
            wk[(who, name, start)][0] += h
            wk[(who, name, start)][1].add(day)
    for (who, name, start), (h, days) in sorted(wk.items(), key=lambda x: (x[0][0], x[0][2])):
        status = "To confirm (no weekly limit supplied)" if weekly is None else "Over limit" if h > weekly else "Within limit"
        out["weekly"].append({"employee": name, "week_start": start.isoformat(), "ot_hours_reported": str(h),
                              "days_with_records": len(days), "status": status,
                              "over_by": str(h - weekly) if weekly is not None and h > weekly else None})
    if ws is None:
        out["weekly_note"] = "To confirm: week_start not supplied, weekly totals not calculated"
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("input")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    if Path(a.out).resolve() == Path(a.input).resolve():
        sys.exit("--out must differ from the input file")
    try:
        result = run(json.loads(Path(a.input).read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as e:
        sys.exit(f"Bad input: {e!r}")
    Path(a.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
