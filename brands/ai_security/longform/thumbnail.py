"""Scutoria YouTube thumbnails (1280x720 PNG) from a Higgsfield background and at most five words.

Rules: OneDrive\\Business\\02 Marke\\Scutoria\\YouTube-Konzept.md section 5. The picture sits on the right and fades
into the dark ground; words on the left in Manrope 800, one word may be accent blue (*Wort*); number top left,
"Stand ..." bottom left, Scutum mark bottom right. Rendered with HyperFrames snapshot (same fonts as the videos).

  .venv\\Scripts\\python.exe brands\\ai_security\\longform\\thumbnail.py --num 01 --text "Womit fangen *KI-Regeln* an?" \\
      --bg yt/thumb_01_a.png --stand "Stand Nov. 2026" --out <file.png>
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE.parent))

from fn.render import hyperframes  # noqa: E402
from longform.compose import FONTS, LIB, LOGO, PAL  # noqa: E402


def build(num: str, text: str, bg: str, stand: str, out: Path, *, focus: str = "right") -> Path:
    words = len(re.sub(r"\*", "", text).split())
    if words > 5:
        raise SystemExit(f"thumbnail text has {words} words; at most five")
    tmp = Path(tempfile.mkdtemp(prefix="thumb_"))
    (tmp / "assets").mkdir()
    for p in FONTS.values():
        shutil.copy2(p, tmp / "assets" / p.name)
    shutil.copy2(LOGO, tmp / "assets" / "logo.svg")
    src = LIB / bg if not Path(bg).is_absolute() else Path(bg)
    shutil.copy2(src, tmp / "assets" / ("bg" + src.suffix))
    t = re.sub(r"\*(.+?)\*", r'<em>\1</em>', html.escape(text))
    size = 108 if len(re.sub(r"\*", "", text)) <= 22 else 86
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1280, height=720">
<style>
@font-face{{font-family:'D';src:url('assets/{FONTS['Display'].name}') format('woff2');font-weight:100 900;}}
@font-face{{font-family:'D';src:url('assets/{FONTS['DisplayExt'].name}') format('woff2');font-weight:100 900;unicode-range:U+0100-024F;}}
@font-face{{font-family:'M';src:url('assets/{FONTS['Mono'].name}') format('truetype');}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body,#root{{width:1280px;height:720px;overflow:hidden;background:{PAL['bg']}}}
#root{{position:relative}}
.bg{{position:absolute;top:0;{'right' if focus == 'right' else 'left'}:0;width:820px;height:720px;object-fit:cover;object-position:{focus} center;
 -webkit-mask-image:linear-gradient(to {'right' if focus == 'right' else 'left'},transparent 0%,#000 38%);mask-image:linear-gradient(to {'right' if focus == 'right' else 'left'},transparent 0%,#000 38%)}}
.n{{position:absolute;left:64px;top:52px;font-family:'M';font-size:34px;color:{PAL['accent']};letter-spacing:0.08em}}
.t{{position:absolute;left:64px;top:0;bottom:0;width:590px;display:flex;align-items:center;font-family:'D';font-weight:800;font-size:{size}px;
 line-height:1.02;letter-spacing:-0.03em;color:#fff}}
.t em{{font-style:normal;color:{PAL['accent']}}}
.s{{position:absolute;left:64px;bottom:50px;font-family:'M';font-size:30px;color:{PAL['muted']}}}
.l{{position:absolute;right:52px;bottom:44px;width:56px;height:56px}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1280" data-height="720" data-fps="30">
<img class="bg" src="assets/bg{src.suffix}" alt=""><div class="n">{html.escape(num)}</div><div class="t"><div>{t}</div></div>
<div class="s">{html.escape(stand)}</div><img class="l" src="assets/logo.svg" alt="">
</div><script>window.__timelines={{}};</script></body></html>"""
    (tmp / "index.html").write_text(page, encoding="utf-8")
    shots = hyperframes.snapshot(tmp, [0.5], tmp / "shot")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shots[0], out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--num", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--bg", required=True)
    ap.add_argument("--stand", default="Stand Nov. 2026")
    ap.add_argument("--focus", default="right")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    print(build(a.num, a.text, a.bg, a.stand, Path(a.out), focus=a.focus))
