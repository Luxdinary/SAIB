"""Render a 10-second placeholder demo per brand and build an overview page.

Run:  .venv\\Scripts\\python.exe scripts\\render_demos.py [--brands a,b] [--quality draft|looks] [--no-mirror] [--skip-existing]

Output: storage/demos/<brand_id>/{project/, demo.mp4, cover.jpg, frames/}, storage/demos/index.html,
mirrored to <FN_STORAGE_MIRROR>\\_Demos.
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fn.brands import all_brand_ids, load_brand  # noqa: E402
from fn.config import STORAGE_DIR, mirror_dir  # noqa: E402
from fn.disk import check_free_space  # noqa: E402
from fn.render import ffmpeg, hyperframes  # noqa: E402
from fn.render.compose import Composition, Scene, Word, build_project, group_words  # noqa: E402

DEMO_SECONDS = 10.0

DEMO_TEXT = {
    "claude_workflows": {
        "de": ("Ein Prompt, der wirklich funktioniert", "Erst Kontext, dann Aufgabe, dann Prüfung. In dieser Reihenfolge spart jeder Lauf Zeit.",
               ["$ claude", "> lies CLAUDE.md", "> baue den Workflow", "✓ Tests grün"]),
        "en": ("One prompt that actually works", "Context first, then the task, then the check. This order saves time on every run.",
               ["$ claude", "> read CLAUDE.md", "> build the workflow", "✓ tests green"]),
    },
    "ai_security": {
        "de": ("Was ein KI-Tool über deinen Betrieb weiß", "Jede Eingabe kann gespeichert werden. Eine Regel dafür schützt mehr als jedes Programm.", []),
        "en": ("What an AI tool knows about your business", "Every input can be stored. One rule for that protects more than any software.", []),
    },
    "engines": {
        "de": ("Warum dieser Kolben nicht rund ist", "Bei Betriebstemperatur dehnt sich Aluminium ungleich aus. Die Form gleicht das aus.", []),
        "en": ("Why this piston is not round", "At operating temperature aluminium expands unevenly. The shape compensates for it.", []),
    },
    "megaconstruction": {
        "de": ("Höher als drei Eiffeltürme", "Vergleiche werden gerechnet, nicht geschätzt. Jede Zahl hat eine Quelle.", []),
        "en": ("Taller than three Eiffel Towers", "Comparisons are computed, not guessed. Every number has a source.", []),
    },
    "menswear": {
        "de": ("Die eine Regel für den Ärmel", "Ein Zentimeter Hemd sichtbar. Alles andere ist Geschmack.", []),
        "en": ("The one rule for the sleeve", "One centimetre of shirt showing. Everything else is taste.", []),
    },
    "motivation": {
        "de": ("Zwei Minuten reichen", "Eine Methode mit Namen und Quelle, nicht nur ein Spruch.", []),
        "en": ("Two minutes are enough", "A method with a name and a source, not just a slogan.", []),
    },
    "military_history": {
        "de": ("Warum der Turm so flach war", "Eine dokumentierte Entscheidung von 1943 und ihre Folgen. Nur Geschichte, keine Taktik.", []),
        "en": ("Why the turret was so flat", "A documented decision from 1943 and its consequences. History only, no tactics.", []),
    },
    "beauty": {
        "de": ("Was Niacinamid wirklich tut", "Inhaltsstoffwissen mit Quelle. Keine Wirkversprechen.", []),
        "en": ("What niacinamide really does", "Ingredient knowledge with a source. No efficacy claims.", []),
    },
    "brainrot": {
        "de": ("Zonk hat den Montag verloren", "Regel eins der Zonk-Welt: Niemand sucht ihn.", []),
        "en": ("Zonk lost Monday", "Rule one of the Zonk world: nobody looks for it.", []),
    },
}


def mock_words(text: str, start: float, end: float) -> list[Word]:
    tokens = text.split()
    if not tokens:
        return []
    weights = [max(1, len(t)) for t in tokens]
    total_w = sum(weights)
    span = end - start
    words, t = [], start
    for tok, w in zip(tokens, weights):
        d = span * w / total_w
        words.append(Word(text=tok, start=round(t, 3), end=round(t + d * 0.92, 3)))
        t += d
    return words


def demo_composition(brand_id: str, language: str) -> Composition:
    brand = load_brand(brand_id)
    brand.outro["seconds"] = 2.5  # short outro for the 10-second demo
    headline, body, code = DEMO_TEXT[brand_id][language]
    intro = float(brand.intro.get("seconds", 1.6))
    outro = float(brand.outro.get("seconds", 4.0))
    hook_start = intro
    outro_start = DEMO_SECONDS - outro
    mid = hook_start + (outro_start - hook_start) * 0.55
    scenes = [
        Scene(id="hook", start=hook_start, duration=mid - hook_start, headline=headline, kind="hook",
              code_lines=code if code else [], source_label=""),
        Scene(id="fact", start=mid, duration=outro_start - mid, headline=body.split(".")[0] + ".", body=".".join(body.split(".")[1:]).strip(),
              kind="code" if code else "fact", code_lines=code, source_label="[S1] Platzhalter · 2026-10-30" if language == "de" else "[S1] placeholder · 2026-10-30"),
    ]
    sub_words = int(brand.subtitle_style.get("group_words", 3))
    words = mock_words(headline + " " + body, hook_start + 0.3, outro_start - 0.2)
    captions = group_words(words, sub_words)
    return Composition(brand=brand, language=language, duration=DEMO_SECONDS, scenes=scenes, captions=captions,
                       title=f"{brand.name} demo {language}")


def build_overview(results: list[dict], out: Path) -> None:
    cards = []
    for r in results:
        status = "ok" if r.get("ok") else "fehlgeschlagen"
        video = f'<video controls preload="metadata" poster="{r["brand_id"]}/cover.jpg" src="{r["brand_id"]}/demo.mp4"></video>' if r.get("ok") else f'<pre>{html.escape(str(r.get("error", "")))[:600]}</pre>'
        cards.append(f"""
<article class="card">
  <header><span class="dot" style="background:{r['accent']}"></span><h2>{html.escape(r['name'])}</h2><span class="id">{r['brand_id']} · {r['style']}</span></header>
  {video}
  <footer>
    <span class="pal"><i style="background:{r['bg']}"></i><i style="background:{r['accent']}"></i><i style="background:{r['text']}"></i></span>
    <span>{html.escape(r.get('fonts', ''))}</span>
    <span>{status} · Render {r.get('render_seconds', 0):.0f} s · {r.get('size_mb', 0):.1f} MB</span>
  </footer>
</article>""")
    page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>Demos – neun Marken</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{margin:0;background:#0d0f14;color:#e8eaf0;font-family:Inter,Segoe UI,sans-serif;padding:24px;}}
h1{{font-size:22px;font-weight:600;margin:0 0 6px}} p.sub{{color:#9aa3b2;margin:0 0 24px;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}
.card{{background:#151923;border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:10px}}
.card header{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}} .card h2{{font-size:18px;margin:0;font-weight:600}}
.id{{color:#9aa3b2;font-size:12px}} .dot{{width:14px;height:14px;border-radius:50%;display:inline-block}}
video{{width:100%;aspect-ratio:9/16;background:#000;border-radius:12px}}
footer{{display:flex;flex-direction:column;gap:6px;color:#9aa3b2;font-size:12px}}
.pal i{{display:inline-block;width:22px;height:22px;border-radius:6px;margin-right:6px;border:1px solid #2a3040}}
pre{{white-space:pre-wrap;font-size:11px;color:#ff8a8a}}
</style></head><body>
<h1>Phase 1 · Demos aller neun Marken (10 s, Platzhalter)</h1>
<p class="sub">Erzeugt {datetime.now().strftime('%Y-%m-%d %H:%M')} · HyperFrames + FFmpeg NVENC · Stimme: Mock (stumm) · Optik zur Beurteilung durch Stefan</p>
<div class="grid">{''.join(cards)}</div>
</body></html>"""
    out.write_text(page, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brands", default="")
    ap.add_argument("--language", default="de")
    ap.add_argument("--quality", default="looks")
    ap.add_argument("--workers", default="4")
    ap.add_argument("--no-mirror", action="store_true")
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--no-gpu", action="store_true")
    args = ap.parse_args()

    space = check_free_space()
    print(f"free on C: {space.free_gb:.1f} GB (min {space.min_gb:.0f})")
    if not space.ok:
        print("ABORT: not enough free space for new renders")
        return 2

    ids = [b.strip() for b in args.brands.split(",") if b.strip()] or all_brand_ids()
    out_root = STORAGE_DIR / "demos"
    out_root.mkdir(parents=True, exist_ok=True)
    results = []
    for bid in ids:
        brand = load_brand(bid)
        bdir = out_root / bid
        video = bdir / "demo.mp4"
        rec = {"brand_id": bid, "name": brand.name, "style": brand.style, "bg": brand.palette["bg"],
               "accent": brand.palette["accent"], "text": brand.palette["text"],
               "fonts": f"{brand.fonts.get('display', {}).get('family')} / {brand.fonts.get('body', {}).get('family')}"}
        if args.skip_existing and video.exists():
            pr = ffmpeg.probe(video)
            rec.update(ok=True, render_seconds=0, size_mb=pr.size_bytes / 1e6, skipped=True)
            results.append(rec)
            print(f"{bid}: skipped (exists)")
            continue
        try:
            comp = demo_composition(bid, args.language)
            voice = bdir / "project" / "assets" / "voice.wav"
            voice.parent.mkdir(parents=True, exist_ok=True)
            ffmpeg.tone_wav(voice, DEMO_SECONDS - comp.intro_seconds - 0.2)
            comp.voice_file = voice
            comp.voice_start = comp.intro_seconds
            project = bdir / "project"
            build_project(comp, project)
            report = hyperframes.check(project)
            (bdir / "check.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            t0 = time.perf_counter()
            raw = bdir / "demo_raw.mp4"
            hyperframes.render(project, raw, quality=args.quality, gpu=not args.no_gpu, workers=args.workers)
            ffmpeg.encode_nvenc(raw, video, loudness_lufs=None)
            cover_at = comp.scenes[0].start + 0.6
            ffmpeg.extract_frame(video, bdir / "cover.jpg", cover_at)
            pr = ffmpeg.probe(video)
            rec.update(ok=True, render_seconds=time.perf_counter() - t0, size_mb=pr.size_bytes / 1e6,
                       duration=pr.duration, width=pr.width, height=pr.height)
            print(f"{bid}: ok {pr.duration:.1f}s {pr.width}x{pr.height} in {rec['render_seconds']:.0f}s")
        except Exception as exc:  # noqa: BLE001
            rec.update(ok=False, error=str(exc))
            print(f"{bid}: FAILED {exc}")
        results.append(rec)
        (bdir / "result.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")

    build_overview(results, out_root / "index.html")
    (out_root / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"overview: {out_root / 'index.html'}")

    if not args.no_mirror:
        target = mirror_dir() / "_Demos"
        target.mkdir(parents=True, exist_ok=True)
        for r in results:
            if not r.get("ok"):
                continue
            (target / r["brand_id"]).mkdir(exist_ok=True)
            for f in ("demo.mp4", "cover.jpg"):
                src = out_root / r["brand_id"] / f
                if src.exists():
                    shutil.copy2(src, target / r["brand_id"] / f)
        shutil.copy2(out_root / "index.html", target / "index.html")
        shutil.copy2(out_root / "results.json", target / "results.json")
        print(f"mirrored to {target}")
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
