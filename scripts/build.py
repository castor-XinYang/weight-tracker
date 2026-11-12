#!/usr/bin/env python3
"""Generate LaTeX pieces for a session report from data/*.csv.

Usage: python3 scripts/build.py s2

Writes into sessions/<dir>/generated/:
  weight_table.tex  - longtable rows for this session
  trend.dat         - all readings (days since first reading, weight, session) for pgfplots
  daily.tex         - itemize entries from data/daily.csv within the session dates
  stats.tex         - \newcommand macros (start/latest/min weight, change, to-target)
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


def d(s):
    return date.fromisoformat(s) if s else None


def tex_escape(s):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(a, b)
    return s


def main():
    sid = sys.argv[1] if len(sys.argv) > 1 else "s2"
    sessions = {r["id"]: r for r in load("sessions.csv")}
    sess = sessions[sid]
    start, end = d(sess["start"]), d(sess["end"])
    target = float(sess["target_lb"])

    sdir = next(p for p in (ROOT / "sessions").iterdir() if p.name.startswith(sid + "-"))
    out = sdir / "generated"
    out.mkdir(exist_ok=True)

    weights = load("weight.csv")
    in_sess = [r for r in weights if r["session"] == sid]

    # Weight table rows
    lines = []
    for r in in_sess:
        w = float(r["weight_lb"])
        lines.append(f"{d(r['date']).strftime('%Y-%m-%d')} & {r['time']} & {w:g} & {w - target:+g} \\\\")
    head = ("\\begin{longtable}{|c|c|c|c|}\n\\hline\n"
            "Date & Time & Weight (lb) & vs.\\ target (lb) \\\\\n\\hline\\endhead\n\\hline\\endfoot\n")
    table = head + "\n".join(lines) + "\n\\end{longtable}\n" if lines else "\\textit{No readings yet.}\n"
    (out / "weight_table.tex").write_text(table)

    # Trend data: every reading, all sessions
    first = d(weights[0]["date"])
    with open(out / "trend.dat", "w") as f:
        f.write("day weight session\n")
        for r in weights:
            f.write(f"{(d(r['date']) - first).days} {float(r['weight_lb']):g} {r['session']}\n")

    # Daily log
    items = []
    for r in load("daily.csv"):
        dt = d(r["date"])
        if dt < start or (end and dt > end):
            continue
        parts = []
        if r["sleep_h"]:
            parts.append(f"Sleep {r['sleep_h']} h")
        if r["energy_10"]:
            parts.append(f"Energy {r['energy_10']}/10")
        if r["kcal"]:
            parts.append(f"{r['kcal']} kcal")
        if r["protein_g"]:
            parts.append(f"{r['protein_g']} g protein")
        if r["cardio"]:
            parts.append("Cardio: " + r["cardio"])
        if r["strength"]:
            parts.append("Strength: " + r["strength"])
        if r["note"]:
            parts.append(r["note"])
        items.append(f"\\item[{dt.strftime('%b %d')}] " + tex_escape("; ".join(parts)))
    body = "\\begin{itemize}\n" + "\n".join(reversed(items)) + "\n\\end{itemize}\n" if items \
        else "\\textit{No daily entries yet.}\n"
    (out / "daily.tex").write_text(body)

    # Stats macros
    if in_sess:
        ws = [float(r["weight_lb"]) for r in in_sess]
        s0, s1, mn = ws[0], ws[-1], min(ws)
        stats = {
            "StartWeight": f"{s0:g}", "LatestWeight": f"{s1:g}", "MinWeight": f"{mn:g}",
            "Change": f"{s1 - s0:+g}", "ToTarget": f"{s1 - target:g}", "NReadings": str(len(ws)),
            "LatestDate": in_sess[-1]["date"],
        }
    else:
        stats = {k: "--" for k in ["StartWeight", "LatestWeight", "MinWeight", "Change",
                                   "ToTarget", "LatestDate"]}
        stats["NReadings"] = "0"
    stats["Target"] = f"{target:g}"
    stats["SessionStart"] = sess["start"]
    (out / "stats.tex").write_text(
        "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in stats.items()))

    print(f"{sid}: {len(in_sess)} readings, {len(items)} daily entries -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
