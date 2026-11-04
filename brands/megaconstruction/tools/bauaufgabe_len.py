"""Estimate the Gemini voice length of Gigastruct plans (calibrated 02.11.2026 on three real voices):
DE 15.0 characters/s plus 0.32 s per digit, EN 15.2 characters/s plus 0.41 s per digit (digits are read out slowly).
Target: estimate + 2.6 s tail between 70 and 84 s.  Run: ... bauaufgabe_len.py <plan.json> ..."""
import json
import re
import sys

for f in sys.argv[1:]:
    p = json.load(open(f, encoding="utf-8"))
    txt = " ".join(b["spoken"] for b in p["beats"])
    rate, dig = (15.2, 0.41) if p["language"] == "en" else (15.0, 0.32)
    est = len(txt) / rate + dig * len(re.findall(r"\d", txt)) + 2.6
    flag = "ok" if 70 <= est <= 84 else ("SHORT" if est < 70 else "LONG")
    print(f"{f.split('/')[-1]:45s} {len(txt.split()):4d} words {est:5.1f} s {flag}")
