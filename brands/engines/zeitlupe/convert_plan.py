"""Convert a Revlore week-1 plan (Q1 scenes rv_*) into the Zeitlupe format without touching the spoken text, so the
paid Gemini voice can be reused with --reuse-voice.

    .venv\\Scripts\\python.exe brands\\engines\\zeitlupe\\convert_plan.py data\\direction\\engines-20261110-1-de.json [...]

Writes data\\direction\\<name>.zeitlupe.json next to the input (the input stays unchanged):
- hook rv_hook -> zl_hook: real time (long exposure) for the first 15 % of the beat, then slow motion; claim unchanged;
- middle beats rv_* -> zlx_* (Q1 scene inside the Zeitlupe frame, see zeitlupe/scenes.py section 6); `zl_strip` when
  the voice mentions the strip;
- closing rv_cutaway with chips and cta -> zl_realtime: chips become result rows at their words, the engine speeds up
  and drops into real time at the brand line;
- every scene gets a source line from its first source id.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def _src_line(plan: dict, ids: list[str], lang: str) -> str:
    srcs = {s["id"]: s for s in plan.get("sources", [])}
    for i in ids or []:
        s = srcs.get(i)
        if not s:
            continue
        date = s.get("checked_at", "")
        if lang == "de" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            y, m, d = date.split("-")
            tail = f" · abgerufen {d}.{m}.{y}"
        else:
            tail = f" · retrieved {date}" if date else ""
        label = s.get("label") or s.get("title", "")
        return label[: 64 - len(tail)] + tail
    return ""


def convert(plan: dict, ref_rpm: float | None = None) -> dict:
    lang = plan["language"]
    de = lang == "de"
    p = json.loads(json.dumps(plan))
    p["notes"] = ((p.get("notes") or "") + (" | Zeitlupe-Format (02.11.2026): automatisch umgestellt mit "
                                            "brands/engines/zeitlupe/convert_plan.py, Sprechtext unverändert."))
    lay = p["layout"]
    lay["format"] = "zeitlupe"
    lay["explainer"] = False
    rpm = int(ref_rpm or 3000)
    extra = (f"Zeitlupenfaktor und Millisekunden beziehen sich auf die Beispieldrehzahl {rpm}/min." if de else
             f"Slow-motion factor and milliseconds refer to the example speed of {rpm} rpm.")
    # the export adds the closing sentence itself (prüfrunde 03.11.: it stood twice in Veröffentlichung.md)
    lay["companion_text"] = "\n".join(ln for ln in (lay.get("companion_text") or "").split("\n")
                                      if not ln.startswith(("Folge Revlore", "Follow Revlore")))
    if extra not in (lay.get("companion_text") or ""):
        lay["companion_text"] = ((lay.get("companion_text") or "").rstrip() + " " + extra).strip()
    beats = p["beats"]
    for i, b in enumerate(beats):
        d = b.get("data") or {}
        src = _src_line(p, b.get("source_ids") or [], lang)
        st = b["scene_type"]
        if i == 0 and st == "rv_hook":
            nd = {kk: d[kk] for kk in ("claim", "claim_lines", "claim_highlight", "claim_at", "theta", "fuel", "injector", "knock") if kk in d}
            nd["slow_at"] = 0.15
            n = len(nd.get("claim_lines") or [1])
            if n > 2:
                nd["view"] = {"s": 0.66, "top": 372 + 88 * (n - 1) + 48}
            b["scene_type"] = "zl_hook"
        elif i == len(beats) - 1 and d.get("cta"):
            th = d.get("theta") or [[0, 0], [1, 720]]
            a0 = float(th[0][1])
            cta = d["cta"]
            at = cta.get("at", 0.7)
            nd = {"theta": [[0, a0], [0.3, a0 + 180], [0.5, a0 + 540], [at, a0 + 1260], [1, a0 + 7260]], "real_at": at,
                  "rows": [{"text": ch.get("text", ""), "at": ch.get("at", 0.3)} for ch in d.get("chips", [])],
                  "brand": {"text": f'{cta.get("brand", "Revlore").upper()} · {cta.get("title", "")}', "hl": cta.get("brand", "Revlore").upper(), "at": at}}
            for kk in ("fuel", "injector", "knock"):
                if kk in d:
                    nd[kk] = d[kk]
            b["scene_type"] = "zl_realtime"
        elif st.startswith("rv_") and st != "rv_hook":
            nd = dict(d)
            if re.search(r"\bLeiste\b|\bstrip\b|\bbar (at the )?(bottom|below)\b", b.get("spoken", ""), re.I):
                nd["zl_strip"] = True
            b["scene_type"] = "zlx_" + st[3:]
        else:
            raise ValueError(f"{p['video_id']} beat {b['id']}: no rule for {st}")
        if src:
            nd["source"] = src
        if ref_rpm:
            nd["ref_rpm"] = ref_rpm
        b["data"] = nd
        b["overlay"] = {}
    return p


def main() -> int:
    """Arguments: plan files; `--ref-rpm N` applies to the plans after it (default 3000/min)."""
    ref = None
    args = sys.argv[1:]
    while args:
        arg = args.pop(0)
        if arg == "--ref-rpm":
            ref = float(args.pop(0))
            continue
        src = Path(arg)
        plan = json.loads(src.read_text(encoding="utf-8"))
        out = src.with_name(src.stem + ".zeitlupe.json")
        out.write_text(json.dumps(convert(plan, ref), ensure_ascii=False, indent=1), encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
