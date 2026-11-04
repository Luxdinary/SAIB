"""Write Plümo's SVG files and render the character sheet PNG (HyperFrames snapshot, code only).

Run: .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\make_sheet.py [--no-snapshot]
Output: brands/brainrot/assets/character/*.svg, plumo_sheet.png, logo/zonkfruit-mark.svg,
        copy of the PNGs to OneDrive\\Business\\02 Marke\\Tintora\\.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))

from plumo import C, POSES, plumo_svg, logo_svg  # noqa: E402
from fn.render import hyperframes  # noqa: E402

BRAND = HERE.parent
CHAR = BRAND / "assets" / "character"
ONEDRIVE = Path(r"C:\Users\Stefa\OneDrive\Business\02 Marke\Tintora")
FONT = BRAND / "assets" / "fonts" / "fredoka" / "Fredoka[wdth,wght].ttf"

LABELS = {"neutral": "neutral (deadpan)", "staunen": "staunen", "stolz": "stolz", "zeigen": "zeigen (Blatt)",
          "verwirrt": "verwirrt", "umgekippt": "umgekippt (der Zonk)"}
SWATCHES = [("Körper", C["body"]), ("Licht", C["body_hi"]), ("Schatten", C["body_lo"]), ("Lid", C["lid"]), ("Kante", C["line"]),
            ("Blatt / Sommersprossen", C["leaf"]), ("Blatt unten", C["leaf_lo"]), ("Stiel", C["stem"]), ("Auge", C["eye"]),
            ("Pupille", C["pupil"]), ("Mund", C["mouth"]), ("Etikett", C["sticker"])]
TRAITS = ["Gummidrop-Silhouette, runder Boden: kippt um und steht wieder auf",
          "Spiralfeder als Stiel, genau drei Windungen",
          "ein magenta Blatt = seine einzige Hand (zeigt, winkt, stützt)",
          "schwere Lider, Grundblick deadpan",
          "drei magenta Sommersprossen nur auf der rechten Wange",
          "Etikett mit „?“ auf dem Rücken: Sorte nicht ermittelbar",
          "keine Arme, keine Beine, keine Kleidung, keine Schrift am Körper",
          "magenta Randlicht rechts, Licht von links oben"]


def write_svgs() -> None:
    CHAR.mkdir(parents=True, exist_ok=True)
    for view in ("front", "side", "back"):
        (CHAR / f"plumo_{view}.svg").write_text(plumo_svg("neutral", view, uid=f"s{view}"), encoding="utf-8")
    for pose in POSES:
        (CHAR / f"plumo_pose_{pose}.svg").write_text(plumo_svg(pose, "front", uid=f"x{pose}"), encoding="utf-8")
    (BRAND / "assets" / "logo").mkdir(parents=True, exist_ok=True)
    (BRAND / "assets" / "logo" / "zonkfruit-mark.svg").write_text(logo_svg(), encoding="utf-8")


def sheet_html(w: int, h: int) -> str:
    views = "".join(f'<div class="view"><div class="fig">{plumo_svg("neutral", v, uid=f"v{v}")}</div><div class="lab">{t}</div></div>'
                    for v, t in (("front", "vorne"), ("side", "Seite (links)"), ("back", "hinten")))
    poses = "".join(f'<div class="pose"><div class="pfig">{plumo_svg(p, "front", uid=f"q{p}")}</div><div class="lab small">{LABELS[p]}</div></div>' for p in POSES)
    sw = "".join(f'<div class="sw"><span class="chip" style="background:{c}"></span><span>{n}</span><code>{c}</code></div>' for n, c in SWATCHES)
    tr = "".join(f"<li>{t}</li>" for t in TRAITS)
    return f"""<!doctype html><html lang="de" data-resolution="landscape"><head><meta charset="utf-8">
<style>
@font-face{{font-family:'FN Fredoka';src:url('assets/fonts/fredoka/Fredoka[wdth,wght].ttf') format('truetype');font-weight:300 700;}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;background:#101010;color:#FFF4FA;font-family:'FN Fredoka',sans-serif;overflow:hidden}}
#root{{position:relative;width:{w}px;height:{h}px;background:radial-gradient(ellipse at 40% 35%,#22162b 0%,#101010 70%)}}
h1{{position:absolute;left:80px;top:56px;font-size:72px;font-weight:700;color:#B7FF00;letter-spacing:-0.01em}}
h1 span{{color:#FF43C0}}
.sub{{position:absolute;left:84px;top:146px;font-size:30px;color:#c9b8c4}}
.views{{position:absolute;left:60px;top:200px;width:1500px;display:flex;gap:10px}}
.view{{flex:1;text-align:center}} .fig svg{{width:470px;height:540px}}
.poses{{position:absolute;left:60px;top:830px;width:1500px;display:flex;gap:6px}}
.pose{{flex:1;text-align:center}} .pfig svg{{width:240px;height:276px}}
.lab{{font-size:34px;font-weight:600;color:#FFF4FA;margin-top:-6px}} .lab.small{{font-size:24px;font-weight:500;color:#e8d8e3;margin-top:4px}}
.side{{position:absolute;left:1600px;top:200px;width:{w - 1680}px}}
.side h2{{font-size:36px;color:#B7FF00;margin:0 0 18px}}
.sw{{display:flex;align-items:center;gap:16px;font-size:24px;margin-bottom:6px}}
.chip{{width:38px;height:38px;border-radius:12px;border:2px solid #3a2a36;flex:0 0 38px}}
code{{margin-left:auto;font-family:monospace;font-size:24px;color:#d6c6d0}}
ul{{margin:20px 0 0 26px;font-size:23px;line-height:1.35;color:#FFF4FA}} li{{margin-bottom:8px}}
.foot{{position:absolute;left:84px;bottom:36px;width:1480px;font-size:22px;color:#9d8a97}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="{w}" data-height="{h}" data-fps="30">
<h1>Plümo <span>·</span> Zonkfruit</h1>
<div class="sub">Charakterblatt, Entwurf 30.10.2026 · nur Code (SVG), kein KI-Bild · Freigabe durch Stefan offen</div>
<div class="views">{views}</div>
<div class="poses">{poses}</div>
<div class="side"><h2>Feste Farben</h2>{sw}<h2 style="margin-top:34px">Unveränderliche Merkmale</h2><ul>{tr}</ul></div>
<div class="foot">Bewegungsstil: elastisch (Squash und Stretch, Feder-Nachschwingen am Stiel, Umkippen und Aufstehen als Loop) · Schrift Fredoka (OFL-1.1)</div>
</div>
<script src="assets/vendor/gsap.min.js"></script>
<script>const tl=gsap.timeline({{paused:true}});tl.to("#root",{{opacity:1,duration:1}},0);window.__timelines={{main:tl}};</script>
</body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-snapshot", action="store_true")
    a = ap.parse_args()
    write_svgs()
    print(f"svgs -> {CHAR}")
    if a.no_snapshot:
        return 0
    w, h = 2400, 1350
    proj = ROOT / "storage" / "brainrot_character_sheet"
    (proj / "assets" / "fonts" / "fredoka").mkdir(parents=True, exist_ok=True)
    (proj / "assets" / "vendor").mkdir(parents=True, exist_ok=True)
    shutil.copy2(FONT, proj / "assets" / "fonts" / "fredoka" / FONT.name)
    gsap = ROOT / "assets" / "vendor" / "gsap.min.js"
    if gsap.exists():
        shutil.copy2(gsap, proj / "assets" / "vendor" / "gsap.min.js")
    (proj / "index.html").write_text(sheet_html(w, h), encoding="utf-8")
    (proj / "hyperframes.json").write_text('{"paths":{"assets":"assets"},"media":{"autoProxy":false}}\n', encoding="utf-8")
    (proj / "meta.json").write_text('{"id":"brainrot_character_sheet","name":"Plümo sheet"}\n', encoding="utf-8")
    shots = hyperframes.snapshot(proj, [0.5], proj / "shots")
    if not shots:
        print("no snapshot written")
        return 2
    dst = CHAR / "plumo_sheet.png"
    shutil.copy2(shots[-1], dst)
    ONEDRIVE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dst, ONEDRIVE / "Plümo Charakterblatt (Entwurf).png")
    print(f"sheet -> {dst}\n       -> {ONEDRIVE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
