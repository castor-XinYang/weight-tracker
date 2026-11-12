#!/usr/bin/env python3
"""Generate LaTeX pieces for a session progress report from data/*.csv.

Usage: python3 scripts/build.py s2

Writes into sessions/<id>-*/generated/:
  weight_table.tex  - longtable of this session's readings
  trend.dat         - this session's readings (day, weight, body fat) for pgfplots
  stats.tex         - \\newcommand macros for the summary block
"""
import csv
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def fmt(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def main():
    sid = sys.argv[1] if len(sys.argv) > 1 else "s2"
    sess = {r["id"]: r for r in load("sessions.csv")}[sid]
    start = date.fromisoformat(sess["start"])
    target = float(sess["target_lb"])

    sdir = next(p for p in (ROOT / "sessions").iterdir() if p.name.startswith(sid + "-"))
    out = sdir / "generated"
    out.mkdir(exist_ok=True)

    rows = [r for r in load("weight.csv") if r["session"] == sid]
    w0 = float(rows[0]["weight_lb"]) if rows else None

    # Weight log table
    if rows:
        lines = [
            r"\begin{longtable}{|c|c|r|r|r|r|}",
            r"\hline",
            r"\textbf{Date} & \textbf{Time} & \textbf{Weight (lb)} & \textbf{Body fat (\%)} "
            r"& \textbf{Change (lb)} & \textbf{To target (lb)} \\",
            r"\hline\endhead",
            r"\hline\endfoot",
        ]
        for r in rows:
            w = float(r["weight_lb"])
            bf = r["body_fat_pct"] or "--"
            lines.append(f"{r['date']} & {r['time'] or '--'} & {fmt(w)} & {bf} & "
                         f"{w - w0:+.1f} & {fmt(w - target)} \\\\")
        lines.append(r"\end{longtable}")
        table = "\n".join(lines) + "\n"
    else:
        table = "\\textit{No readings yet.}\n"
    (out / "weight_table.tex").write_text(table)

    # Trend data: this session only
    with open(out / "trend.dat", "w") as f:
        f.write("day weight bodyfat\n")
        for r in rows:
            day = (date.fromisoformat(r["date"]) - start).days
            f.write(f"{day} {float(r['weight_lb']):g} {r['body_fat_pct'] or 'nan'}\n")

    # Summary macros
    if rows:
        ws = [float(r["weight_lb"]) for r in rows]
        latest = ws[-1]
        days = (date.fromisoformat(rows[-1]["date"]) - start).days
        rate = (latest - w0) / days * 7 if days >= 7 else None
        bfs = [r["body_fat_pct"] for r in rows if r["body_fat_pct"]]
        stats = {
            "StartWeight": fmt(w0), "LatestWeight": fmt(latest), "LatestDate": rows[-1]["date"],
            "Change": f"{latest - w0:+.1f}", "ChangePct": f"{(latest - w0) / w0 * 100:+.1f}",
            "ToTarget": fmt(latest - target), "WeeklyRate": f"{rate:+.1f}" if rate is not None else "--",
            "StartBF": bfs[0] if bfs else "--", "LatestBF": bfs[-1] if bfs else "--",
            "Days": str(days), "NReadings": str(len(ws)), "XMax": str(max(days, 7)),
        }
    else:
        stats = {k: "--" for k in ["StartWeight", "LatestWeight", "LatestDate", "Change", "ChangePct",
                                   "ToTarget", "WeeklyRate", "StartBF", "LatestBF", "Days"]}
        stats.update(NReadings="0", XMax="7")
    stats.update(Target=fmt(target), SessionStart=sess["start"])
    (out / "stats.tex").write_text(
        "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in stats.items()))

    print(f"{sid}: {len(rows)} readings -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
