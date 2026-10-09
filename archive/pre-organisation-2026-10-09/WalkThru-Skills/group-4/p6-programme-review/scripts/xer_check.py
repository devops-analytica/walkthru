#!/usr/bin/env python3
"""P6 schedule-health and float review; not a scheduling or longest-path engine.

Canonical source. build_release.py copies this into standalone skill packages.
Stdlib only. Input is never modified. Output files are written only to --out-dir.
"""
import argparse
import csv
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

HARD_CONSTRAINTS = {'CS_MSO', 'CS_MEO', 'CS_MANDSTART', 'CS_MANDFIN'}
SUMMARY_TYPES = {'TT_LOE', 'TT_WBS'}
MILESTONE_TYPES = {'TT_Mile', 'TT_FinMile'}
LONG_DURATION_DAYS = 44


def parse_xer(path):
    raw = Path(path).read_bytes()
    for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    tables, current, fields = defaultdict(list), None, []
    for number, line in enumerate(text.splitlines(), 1):
        parts = line.split('\t')
        tag = parts[0]
        if tag == '%T':
            if len(parts) != 2 or not parts[1]:
                raise ValueError(f'Line {number}: malformed table header')
            current, fields = parts[1], []
        elif tag == '%F':
            if not current or len(parts) < 2 or len(set(parts[1:])) != len(parts[1:]):
                raise ValueError(f'Line {number}: invalid field header')
            fields = parts[1:]
        elif tag == '%R':
            if not current or not fields:
                raise ValueError(f'Line {number}: row without table/fields')
            if len(parts[1:]) > len(fields):
                raise ValueError(f'Line {number}: too many values for {current}')
            values = parts[1:] + [''] * (len(fields) - len(parts[1:]))
            tables[current].append(dict(zip(fields, values)))
    return tables


def to_date(value):
    if not value or not str(value).strip():
        return None
    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f'Invalid P6 date: {value!r}')


def hours(value):
    if value is None or str(value).strip() == '':
        return None
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'Invalid numeric value: {value!r}') from exc
    if not math.isfinite(result):
        raise ValueError(f'Non-finite numeric value: {value!r}')
    return result


def build_activities(tables, fallback_hours_per_day=8.0):
    if not math.isfinite(fallback_hours_per_day) or fallback_hours_per_day <= 0:
        raise ValueError('Fallback hours per day must be positive and finite')
    warnings, calendars = [], {}
    for row in tables.get('CALENDAR', []):
        value = hours(row.get('day_hr_cnt'))
        if value is not None and value <= 0:
            raise ValueError(f"Calendar {row.get('clndr_id')} has non-positive hours/day")
        calendars[row.get('clndr_id')] = value
    projects = {}
    for row in tables.get('PROJECT', []):
        pid = row.get('proj_id')
        if not pid or pid in projects:
            raise ValueError('PROJECT requires unique, non-empty proj_id values')
        projects[pid] = {'id': pid, 'name': row.get('proj_short_name', pid),
                         'data_date': to_date(row.get('last_recalc_date'))}
    if not projects:
        raise ValueError('PROJECT table missing; project data dates cannot be established')
    wbs = {row.get('wbs_id'): row.get('wbs_name', '') for row in tables.get('PROJWBS', [])}
    activities, seen = [], set()
    for row in tables.get('TASK', []):
        tid, pid = row.get('task_id'), row.get('proj_id')
        if not tid or tid in seen:
            raise ValueError('TASK requires unique, non-empty task_id values')
        seen.add(tid)
        if pid not in projects:
            raise ValueError(f'Task {tid}: unknown project {pid!r}')
        hpd = calendars.get(row.get('clndr_id'))
        assumed = hpd is None
        if assumed:
            hpd = fallback_hours_per_day
            warnings.append(f'Task {tid}: hours/day unavailable; assumed {hpd:g}. Confirm P6 display units.')
        def days(field):
            value = hours(row.get(field))
            return None if value is None else value / hpd  # Never round before checks.
        activities.append({
            'task_id': tid, 'project_id': pid, 'project': projects[pid]['name'],
            'data_date': projects[pid]['data_date'], 'id': row.get('task_code', tid),
            'name': row.get('task_name', ''), 'wbs': wbs.get(row.get('wbs_id'), ''),
            'type': row.get('task_type'), 'status': row.get('status_code'),
            'pct': row.get('phys_complete_pct'), 'hours_per_day': hpd,
            'calendar_assumed': assumed, 'total_float_hr_cnt': hours(row.get('total_float_hr_cnt')),
            'target_drtn_hr_cnt': hours(row.get('target_drtn_hr_cnt')),
            'remain_drtn_hr_cnt': hours(row.get('remain_drtn_hr_cnt')), 'orig_dur_d': days('target_drtn_hr_cnt'),
            'rem_dur_d': days('remain_drtn_hr_cnt'), 'total_float_d': days('total_float_hr_cnt'),
            'start': to_date(row.get('act_start_date') or row.get('early_start_date') or row.get('target_start_date')),
            'finish': to_date(row.get('act_end_date') or row.get('early_end_date') or row.get('target_end_date')),
            'planned_finish': to_date(row.get('target_end_date')),
            'act_start': to_date(row.get('act_start_date')), 'act_finish': to_date(row.get('act_end_date')),
            'constraint': row.get('cstr_type', ''), 'constraint_date': to_date(row.get('cstr_date')),
            'constraint2': row.get('cstr_type2', ''), 'constraint2_date': to_date(row.get('cstr_date2')),
            'source': f"TASK task_id={tid}; project_id={pid}",
        })
    for pid, project in projects.items():
        if project['data_date'] is None:
            warnings.append(f'Project {pid}: data date missing; overdue-start and look-ahead checks not performed.')
    return activities, projects, sorted(set(warnings))


def check(tables, activities, projects, near_days=10, lookahead_days=21, critical_days=0):
    if not all(math.isfinite(v) for v in (near_days, critical_days)) or critical_days < 0 or near_days < critical_days or lookahead_days < 0:
        raise ValueError('Use 0 <= critical_days <= near_days and a non-negative lookahead')
    preds, succs, findings = defaultdict(list), defaultdict(list), []
    by_task = {a['task_id']: a for a in activities}
    for rel in tables.get('TASKPRED', []):
        preds[rel.get('task_id')].append(rel)
        succs[rel.get('pred_task_id')].append(rel)
    for a in activities:
        if a['status'] == 'TK_Complete' or a['type'] in SUMMARY_TYPES:
            continue
        dd = projects[a['project_id']]['data_date']
        tf = a['total_float_d']
        if tf is None:
            findings.append(('Total float not checked (missing)', a))
        elif tf < 0:
            findings.append(('Negative float', a))
        elif tf <= critical_days:
            findings.append((f'Float at/below critical threshold ({critical_days:g}d)', a))
        elif tf <= near_days:
            findings.append((f'Near-critical float (<= {near_days:g}d)', a))
        if not preds[a['task_id']] and a['type'] != 'TT_Mile':
            findings.append(('Open start (no predecessor)', a))
        if not succs[a['task_id']] and a['type'] != 'TT_FinMile':
            findings.append(('Open finish (no successor)', a))
        for field, label in [('constraint', 'primary'), ('constraint2', 'secondary')]:
            if a[field] in HARD_CONSTRAINTS:
                findings.append((f'Hard constraint ({label}: {a[field]})', a))
        if a['type'] not in MILESTONE_TYPES and a['orig_dur_d'] is not None and a['orig_dur_d'] > LONG_DURATION_DAYS:
            findings.append((f'Long original duration (> {LONG_DURATION_DAYS}d)', a))
        if a['type'] not in MILESTONE_TYPES and a['rem_dur_d'] is not None and a['rem_dur_d'] > LONG_DURATION_DAYS:
            findings.append((f'Long remaining duration (> {LONG_DURATION_DAYS}d)', a))
        if dd and not a['act_start'] and a['start'] and a['start'] < dd:
            findings.append(('Should have started (start before project data date)', a))
        if a['finish'] and a['planned_finish'] and a['finish'] > a['planned_finish']:
            a['slip_d'] = (a['finish'] - a['planned_finish']).total_seconds() / 86400
            findings.append(('Finish later than current planned finish (not baseline)', a))
        if dd and a['start'] and dd <= a['start'] <= dd + timedelta(days=lookahead_days) and not a['act_start']:
            findings.append((f'Starts in next {lookahead_days} calendar days', a))
        if dd and a['finish'] and dd <= a['finish'] <= dd + timedelta(days=lookahead_days):
            findings.append((f'Finishes in next {lookahead_days} calendar days', a))
    for rel in tables.get('TASKPRED', []):
        a = by_task.get(rel.get('task_id'))
        if not a or a['status'] == 'TK_Complete':
            continue
        lag = hours(rel.get('lag_hr_cnt'))
        if lag is not None and lag < 0:
            findings.append(('Negative lag (lead) on predecessor', a))
        if rel.get('pred_type') == 'PR_SF':
            findings.append(('Start-to-finish relationship', a))
    return findings


def csv_value(value):
    if isinstance(value, datetime):
        return value.isoformat(sep=' ', timespec='minutes')
    if isinstance(value, float):
        return format(value, '.12g')
    if isinstance(value, str) and value.lstrip().startswith(('=', '+', '-', '@')):
        return "'" + value  # Keep untrusted names as text in spreadsheet applications.
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xer')
    parser.add_argument('--near-critical-days', type=float, default=10)
    parser.add_argument('--critical-float-days', type=float, default=0)
    parser.add_argument('--lookahead-days', type=int, default=21)
    parser.add_argument('--fallback-hours-per-day', type=float, default=8)
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    try:
        tables = parse_xer(args.xer)
        if not tables.get('TASK'):
            raise ValueError('No TASK table found; provide a P6 XER export')
        activities, projects, warnings = build_activities(tables, args.fallback_hours_per_day)
        findings = check(tables, activities, projects, args.near_critical_days, args.lookahead_days, args.critical_float_days)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        columns = ['project_id', 'project', 'data_date', 'task_id', 'id', 'name', 'wbs', 'type', 'status', 'pct',
                   'hours_per_day', 'calendar_assumed', 'total_float_hr_cnt', 'target_drtn_hr_cnt', 'remain_drtn_hr_cnt', 'orig_dur_d', 'rem_dur_d', 'total_float_d', 'start',
                   'finish', 'planned_finish', 'constraint', 'constraint_date', 'constraint2', 'constraint2_date', 'source']
        with (out / 'activities.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f); writer.writerow(columns)
            for a in activities:
                writer.writerow([csv_value(a[c]) for c in columns])
        columns = ['project_id', 'data_date', 'task_id', 'id', 'name', 'total_float_d', 'start', 'finish', 'planned_finish', 'slip_d', 'source']
        with (out / 'findings.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f); writer.writerow(['check'] + columns)
            for name, a in findings:
                writer.writerow([name] + [csv_value(a.get(c, '')) for c in columns])
        print('# Schedule health and float review')
        print('Not an ordered critical path, baseline comparison, or P6 reschedule. Confirm P6 critical settings and hours/day.\n')
        for pid, project in projects.items():
            date = csv_value(project['data_date']) or 'unknown'
            print(f"## Project {pid}: {project['name']} — data date {date}")
            for name, count in sorted(Counter(n for n, a in findings if a['project_id'] == pid).items()):
                print(f'- {name}: {count}')
        for warning in warnings:
            print('WARNING: ' + warning)
        print(f'\nDetail: {out / "findings.csv"}; all activities: {out / "activities.csv"}')
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Input/output error: {exc}\n')


if __name__ == '__main__':
    main()
