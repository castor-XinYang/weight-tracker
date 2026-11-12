# Weight Tracking (Public)

- Author: Xin Yang
- Session 1: 2025-07-11 to 2025-10-31 (extreme diet + re-feed), archived in `sessions/s1-2025-07/` (tag `v1-session1`)
- Session 2: started 2026-11-12, in `sessions/s2-2026-11/`

## Structure
```
data/                 numbers only (append-only CSV, all sessions)
  weight.csv          date, time, weight_lb, session (s1 / gap / s2), note
  daily.csv           date, sleep_h, energy_10, kcal, protein_g, cardio, strength, note
  sessions.csv        id, start, end, start_lb, target_lb, goal
scripts/build.py      CSV -> LaTeX pieces (table, trend data, daily log, stats)
shared/preamble.tex   packages shared by every report
sessions/
  s1-2025-07/         original report, frozen
  s2-2026-11/         main.tex + plan.tex, summary.tex, retro-s1.tex (hand-written)
```

## Log a day
1. Append a row to `data/weight.csv`, e.g. `2026-11-12,06:30,250.0,s2,`
2. Optionally append to `data/daily.csv`.
3. `make s2` (or `make open`) to rebuild `sessions/s2-2026-11/main.pdf`.

## Start a new session
Add a row to `data/sessions.csv`, copy `sessions/s2-2026-11/` to `sessions/s3-YYYY-MM/`, and add a target to the Makefile.
