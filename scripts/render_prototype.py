"""Render the 15-second Scutoria direction prototype and a before/after comparison.

Uses the existing Gemini voice of the reference video (no new TTS cost), the prototype plan in
data/direction/ai_security-20261105-1-de.prototype.json and the new director composer.

Run:  .venv\\Scripts\\python.exe scripts\\render_prototype.py [--seconds 15] [--no-render]
Output: storage/prototypes/scutoria-regie/ and the mirror OneDrive\\Business\\05 Produktion\\_Demos\\scutoria-regie\\
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from fn import compliance  # noqa: E402
from fn.brands import load_brand  # noqa: E402
from fn.config import ASSETS_DIR, STORAGE_DIR, mirror_dir  # noqa: E402
from fn.direction import checks, story  # noqa: E402
from fn.render import ffmpeg, hyperframes  # noqa: E402
from fn.render.compose import Word, group_words  # noqa: E402
from fn.render.director import build_direction_project  # noqa: E402

REF_ID = "ai_security-20261105-1-de"
REF_VOICE_START = 2.05          # first spoken word in the reference video (intro 1.8 s + lead 0.25)
NEW_VOICE_START = 0.4


def _ref_dir() -> Path:
    for stage in ("approved", "drafts", "published"):
        d = STORAGE_DIR / stage / REF_ID
        if (d / "video.mp4").exists():
            return d
    raise SystemExit(f"reference video {REF_ID} not found in storage")


def _ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def _label_font(size: int) -> ImageFont.FreeTypeFont:
    f = ASSETS_DIR / "fonts" / "inter" / "Inter[opsz,wght].ttf"
    try:
        font = ImageFont.truetype(str(f), size)
        try:
            font.set_variation_by_axes([size, 700])
        except Exception:  # noqa: BLE001
            pass
        return font
    except OSError:
        return ImageFont.load_default()


def side_by_side(before: Path, after: Path, dst: Path, *, t: float, titles=("Vorher (Phase 1)", "Nachher (Regie-Prototyp)")) -> None:
    a, b = Image.open(before).convert("RGB"), Image.open(after).convert("RGB")
    w, h = 540, 960
    a, b = a.resize((w, h), Image.LANCZOS), b.resize((w, h), Image.LANCZOS)
    pad, top = 40, 110
    canvas = Image.new("RGB", (w * 2 + pad * 3, h + top + pad), "#0d0f14")
    canvas.paste(a, (pad, top))
    canvas.paste(b, (w + pad * 2, top))
    d = ImageDraw.Draw(canvas)
    f = _label_font(34)
    f2 = _label_font(24)
    for i, title in enumerate(titles):
        x = pad + i * (w + pad)
        d.text((x, 28), title, fill="#F4F7FB", font=f)
        d.text((x, 72), f"t = {t:.1f} s", fill="#8B909D", font=f2)
    canvas.save(dst, quality=92)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=15.0)
    ap.add_argument("--plan", default=str(Path("data/direction") / f"{REF_ID}.prototype.json"))
    ap.add_argument("--no-render", action="store_true", help="build the project and checks only")
    ap.add_argument("--quality", default="looks")
    ap.add_argument("--workers", default="4")
    a = ap.parse_args()

    total = float(a.seconds)
    ref = _ref_dir()
    plan = story.load_plan(Path(a.plan))
    problems = story.validate(plan, partial=True)
    if problems:
        print("plan problems:", *problems, sep="\n  ")
        return 2
    brand = load_brand(plan.brand_id)
    out_dir = STORAGE_DIR / "prototypes" / "scutoria-regie"
    project = out_dir / "project"
    if project.exists():
        shutil.rmtree(project)
    (project / "assets").mkdir(parents=True)

    # voice: first N seconds of the reference recording, soft fade at the end
    shift = NEW_VOICE_START - REF_VOICE_START
    voice_len = total - NEW_VOICE_START - 0.3
    voice = project / "assets" / "voice.wav"
    _ffmpeg(["-i", str(ref / "project" / "assets" / "voice.wav"), "-t", f"{voice_len:.3f}",
             "-af", f"afade=t=out:st={voice_len - 0.6:.3f}:d=0.6", "-c:a", "pcm_s16le", str(voice)])

    # captions: reference word timings shifted to the new voice start
    caps = json.loads((ref / "captions.json").read_text(encoding="utf-8"))
    words = [Word(w["text"], round(w["start"] + shift, 3), round(w["end"] + shift, 3))
             for g in caps for w in g["words"] if w["end"] + shift <= total - 0.4]
    captions = group_words(words, int(brand.subtitle_style.get("group_words", 3)))

    build = build_direction_project(plan, brand, captions, total=total, project_dir=project, voice_file=voice,
                                    voice_start=NEW_VOICE_START, outro=False, title=plan.title)
    check = hyperframes.check(project)
    (out_dir / "check.json").write_text(json.dumps(check, indent=2, ensure_ascii=False), encoding="utf-8")
    lint = check.get("lint", {})
    print(f"hyperframes check: {lint.get('errorCount', '?')} errors, {lint.get('warningCount', '?')} warnings")
    if lint.get("errorCount", 0):
        for item in lint.get("errors", lint.get("issues", []))[:10]:
            print("  ", item)
        return 3

    video = out_dir / "nachher.mp4"
    if not a.no_render:
        t0 = time.perf_counter()
        raw = out_dir / "render_raw.mp4"
        hyperframes.render(project, raw, quality=a.quality, gpu=True, workers=a.workers)
        ffmpeg.encode_nvenc(raw, video, loudness_lufs=-16.0)
        raw.unlink(missing_ok=True)
        print(f"render + encode: {time.perf_counter() - t0:.0f} s -> {video}")
        # reference clip trimmed to the same length
        before = out_dir / "vorher.mp4"
        _ffmpeg(["-i", str(ref / "video.mp4"), "-t", f"{total:.3f}", "-c:v", "h264_nvenc", "-preset", "p5", "-cq", "23",
                 "-c:a", "aac", "-b:a", "160k", str(before)])
        for t in (4.9, 11.0):
            fa, fb = out_dir / f"vorher_{t:.0f}s.jpg", out_dir / f"nachher_{t:.0f}s.jpg"
            ffmpeg.extract_frame(before, fa, t)
            ffmpeg.extract_frame(video, fb, t)
            side_by_side(fa, fb, out_dir / f"vorher-nachher_{t:.0f}s.jpg", t=t)

    # direction report
    report = compliance.Report(plan.video_id)
    checks.check_direction(report, plan, build.events, total, template_problems=build.problems,
                           caption_font_px=int(brand.subtitle_style.get("font_size_px", 58)),
                           video=video if video.exists() else None)
    compliance.write_report(report, out_dir / "report.json")
    for f in report.findings:
        print(f"  [{f.severity:6}] {'ok ' if f.ok else 'NOT'} {f.id}: {f.detail}")

    # mirror
    target = mirror_dir() / "_Demos" / "scutoria-regie"
    target.mkdir(parents=True, exist_ok=True)
    files = [p for p in out_dir.iterdir() if p.suffix in (".mp4", ".jpg", ".json")]
    for p in files:
        shutil.copy2(p, target / p.name)
    plan_src = Path(a.plan)
    shutil.copy2(plan_src, target / plan_src.name)
    full_plan = Path("data/direction") / f"{REF_ID}.json"
    if full_plan.exists():
        shutil.copy2(full_plan, target / full_plan.name)
    rows = "".join(f"<li><b>{f.id}</b> · {'ok' if f.ok else 'NICHT ok'} ({f.severity}) · {f.detail}</li>" for f in report.findings)
    imgs = "".join(f'<figure><img src="vorher-nachher_{t:.0f}s.jpg" alt=""><figcaption>Vorher / Nachher bei t = {t:.1f} s</figcaption></figure>' for t in (4.9, 11.0))
    page = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Scutoria Regie-Prototyp</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{{margin:0;background:#0d0f14;color:#e8eaf0;font-family:Inter,Segoe UI,sans-serif;padding:24px}}h1{{font-size:22px;margin:0 0 6px}}p.sub{{color:#9aa3b2;font-size:14px;margin:0 0 20px}}
.row{{display:flex;gap:20px;flex-wrap:wrap}}.row>div{{flex:1 1 300px;background:#151923;border-radius:16px;padding:14px}}video{{width:100%;aspect-ratio:9/16;background:#000;border-radius:12px}}
figure{{margin:20px 0}}img{{max-width:100%;border-radius:12px}}figcaption{{color:#9aa3b2;font-size:13px}}ul{{font-size:14px;line-height:1.5}}h2{{font-size:17px}}</style></head>
<body><h1>Scutoria · Regie-Prototyp (15 s, Hook + Problem)</h1><p class="sub">Stand {time.strftime('%Y-%m-%d %H:%M')} · Stimme: vorhandene Gemini-Aufnahme des Bezugsvideos · nichts veröffentlicht</p>
<div class="row"><div><h2>Vorher (Phase 1)</h2><video controls preload="metadata" src="vorher.mp4"></video></div><div><h2>Nachher (Regie-System)</h2><video controls preload="metadata" src="nachher.mp4"></video></div></div>
{imgs}<h2>Regie-Prüfungen</h2><ul>{rows}</ul>
<p class="sub">Szenenplan der Vollfassung: {full_plan.name} · Prototyp-Plan: {plan_src.name}</p></body></html>"""
    (target / "index.html").write_text(page, encoding="utf-8")
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"mirror -> {target / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
