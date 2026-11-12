# Weight Tracking (Public)

- Author: Xin Yang
- Session 1: 2025-07-11 to 2025-10-31, archived in `sessions/s1-2025-07/` (tag `v1-session1`)
- Session 2: started 2026-11-12, progress report in `sessions/s2-2026-11/main.pdf`

## Structure
```
data/
  weight.csv          date, time, weight_lb, body_fat_pct, session (s1 / gap / s2), note
  sessions.csv        id, start, end, start_lb, target_lb, goal
scripts/build.py      CSV -> report pieces (summary stats, trend data, weight log table)
shared/preamble.tex   packages shared by every report
sessions/
  s1-2025-07/         original report, frozen
  s2-2026-11/         progress report (summary, trend, weight log)
```

## Log a reading
1. Append a row to `data/weight.csv`, e.g. `2026-11-12,06:30,250.0,31.5,s2,`
2. `make s2` (or `make open`) to rebuild `sessions/s2-2026-11/main.pdf`.

## Start a new session
Add a row to `data/sessions.csv`, copy `sessions/s2-2026-11/` to `sessions/s3-YYYY-MM/`, and add a target to the Makefile.
