"""Zonkfruit scene templates (brand_id brainrot): Plümo on a surreal checker stage.

Exposed to the shared renderer through `brands/brainrot/scenes.py` (fn.render.brand_scenes; types apply to this
brand only). Same contract as the shared templates: each function gets a SceneCtx and the beat's data and returns
SceneOut(html, tl, events, problems). Motion only on children of the scene clip. Timings follow the spoken words:
`cue(c, "Banane")` returns the time the word starts inside the beat (SceneCtx.words), with a fraction of the beat
as fallback. Sound effects (own work, assets/sfx) are emitted as <audio class="clip"> inside the scene.

Scene types:
  zonk_scan     door "NUR BEEREN" with scanner; modes hook | reject | accept | unknown (also the hook scene type)
  zonk_word     a word card, one part struck out, two verdict chips
  zonk_diagram  cross-section of a berry with labels; Plümo points with his leaf
  zonk_zoom     magnifier over a big fruit, callouts and a term stamp
  zonk_loop     Plümo gets up, CTA chip, ends on the exact first frame of the hook (seamless loop)
"""
from __future__ import annotations

import html
import math
import re
import shutil
import wave
from pathlib import Path

from fn.render.templates import SceneCtx, SceneOut

from plumo import C as PC, POSES, MOUTHS, plumo_svg, lid_attrs
import zonk_props as zp

WORDS: list = []          # fallback word list (absolute times) when SceneCtx.words is empty
SFX: list[tuple[float, str, float]] = []   # (time, sound name, volume) of the whole video, for MANIFEST_EXTRA
_PENDING: list[tuple[float, str, float]] = []   # cues of the scene being built
_LANES: list[float] = []                         # end time per audio track 20.. (no overlap on one track)
SFX_DIR = Path(__file__).resolve().parent.parent / "assets" / "sfx"
SFX_TRACK0 = 20           # shared sound-effect track uses 8..11, the voice 7, the explainer layer 13..17
TOTAL = [0.0]             # video length, set by scenes.LAYER before the scenes are built: period of the backdrop motion

LIMITS = {"head": 44, "h2": 40, "sign": 14, "stamp": 16, "display": 26, "label": 28, "word": 12, "chip": 26, "cta": 30, "value": 14}

# stage geometry (1080 x 1920, scene zone y 290..1100)
FLOOR_Y = 1060
PL_LEFT, PL_TOP, PL_W = 40, 590, 420          # Plümo standing left of the door
DOOR_X = 590          # door frame right edge 922: x from 930 stays free for the platform icons


def _e(s) -> str:
    return html.escape(str(s))


def _rich(s: str) -> str:
    """*word* -> lime highlight."""
    return re.sub(r"\*(.+?)\*", r'<span class="zhl">\1</span>', _e(s))


def _lim(problems: list, scene: str, key: str, val: str) -> None:
    n = len(re.sub(r"\*", "", str(val)))
    if n > LIMITS[key]:
        problems.append(f"{scene}.{key}: {n} chars > {LIMITS[key]}")


def _norm(w: str) -> str:
    return re.sub(r"[^a-zäöüß0-9]", "", w.lower())


def cue(c: SceneCtx, word: str | None, frac: float, *, after: float | None = None) -> float:
    """Start time of the first spoken word inside this beat that starts with `word` (case/punctuation-insensitive)."""
    if word:
        key = _norm(word)
        lo = c.start if after is None else after
        for w in (getattr(c, "words", None) or WORDS):
            if lo - 0.01 <= w.start < c.end and _norm(w.text).startswith(key):
                return round(max(c.start, w.start - 0.05), 3)
    return c.t(frac * c.duration)


def sfx(t: float, name: str, vol: float = 0.35) -> None:
    SFX.append((round(t, 3), name, vol))
    _PENDING.append((round(t, 3), name, vol))


def _begin(c: SceneCtx) -> None:
    if c.start < 0.01:          # first beat: a new build starts
        SFX.clear()
        _LANES.clear()
    _PENDING.clear()


def _wav_seconds(p: Path) -> float:
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def _audio(c: SceneCtx) -> str:
    """<audio> clips for this scene's cues, cut at the scene end; files are copied by scenes.LAYER."""
    tags = []
    for k, (t, name, vol) in enumerate(sorted(_PENDING)):
        src = SFX_DIR / f"{name}.wav"
        if not src.exists() or t >= c.end - 0.05:
            continue
        dur = round(min(_wav_seconds(src), c.end - t), 3)
        lane = next((i for i, end in enumerate(_LANES) if end <= t), None)
        if lane is None:
            _LANES.append(0.0)
            lane = len(_LANES) - 1
        _LANES[lane] = t + dur + 0.02
        tags.append(f'<audio id="{c.sid}-sfx{k}" class="clip" src="assets/sfx/{src.name}" data-start="{t:.3f}" '
                    f'data-duration="{dur:.3f}" data-track-index="{SFX_TRACK0 + lane}" data-volume="{vol:.2f}"></audio>')
    _PENDING.clear()
    return "".join(tags)


def copy_sfx(project_assets: Path) -> None:
    (project_assets / "sfx").mkdir(parents=True, exist_ok=True)
    for p in list(SFX_DIR.glob("*.wav")) + [SFX_DIR / "LICENSE.md"]:
        if p.exists():
            shutil.copy2(p, project_assets / "sfx" / p.name)


def _out(c: SceneCtx, parts: list[str], tl: list[str], events: list[float], problems: list[str], *,
         cam: tuple[float, float] = (1.0, 1.035), origin: tuple[int, int] = (540, 820), cam_end: float | None = None) -> SceneOut:
    """parts[0] is the backdrop (stage); the rest sits in a camera wrapper that pushes in (or out) during the scene.
    Scenes that cut hard into each other (door scenes) chain their cam values so the cut stays continuous."""
    end = c.end if cam_end is None else cam_end
    tl = list(tl) + [f'tl.fromTo("#{c.sid}-cam",{{scale:{cam[0]}}},{{scale:{cam[1]},duration:{max(0.3, end - c.start):.3f},ease:"sine.inOut"}},{c.start:.3f});']
    body = (f'{parts[0]}<div class="zcam" id="{c.sid}-cam" style="transform-origin:{origin[0]}px {origin[1]}px">{"".join(parts[1:])}</div>')
    return SceneOut(html=f'<div class="zs" id="{c.sid}-zs">{body}</div>{_audio(c)}', tl=tl, events=events, problems=problems)


# --- Plümo helpers --------------------------------------------------------------------------------

def plumo(uid: str, pose: str = "neutral", *, left: int = PL_LEFT, top: int = PL_TOP, width: int = PL_W, back: bool = False) -> str:
    front = plumo_svg(pose, "front", uid=uid, width=width, all_mouths=True)
    b = f'<div class="zpb" id="{uid}-backwrap">{plumo_svg("neutral", "back", uid=uid + "k", width=width)}</div>' if back else ""
    return f'<div class="zpl" id="{uid}-wrap" style="left:{left}px;top:{top}px;width:{width}px;height:{int(width * 600 / 520)}px">{front}{b}</div>'


def expr(uid: str, pose: str, at: float, d: float = 0.14) -> list[str]:
    """Tween every face part of Plümo `uid` to `pose` at absolute time `at`."""
    p = POSES[pose]
    out = []
    for side, cx, lid in (("L", 158, p["lid_l"]), ("R", 244, p["lid_r"])):
        h, ly = lid_attrs(lid)
        out.append(f'tl.to("#{uid}-lid{side}",{{attr:{{height:{h}}},duration:{d}}},{at:.3f});')
        out.append(f'tl.to("#{uid}-lin{side}",{{attr:{{y1:{ly},y2:{ly}}},duration:{d}}},{at:.3f});')
        out.append(f'tl.to("#{uid}-pup{side}",{{attr:{{transform:"translate({p["pdx"]},{p["pdy"]})"}},duration:{d}}},{at:.3f});')
        out.append(f'tl.to("#{uid}-pc{side}",{{attr:{{r:{p["pr"]}}},duration:{d}}},{at:.3f});')
    for m in MOUTHS:
        out.append(f'tl.set("#{uid}-m-{m}",{{opacity:{1 if m == p["mouth"] else 0}}},{at:.3f});')
    out.append(f'tl.to("#{uid}-leaf",{{attr:{{transform:"rotate({p["leaf"]},206,10)"}},duration:{d + 0.1},ease:"back.out(2)"}},{at:.3f});')
    out.append(f'tl.to("#{uid}-stem",{{attr:{{transform:"translate(200,96) scale(1,{p["stem"]}) translate(-200,-96)"}},duration:{d + 0.25},ease:"elastic.out(1,0.35)"}},{at:.3f});')
    return out


def leaf_to(uid: str, angle: float, at: float) -> str:
    return f'tl.to("#{uid}-leaf",{{attr:{{transform:"rotate({angle},206,10)"}},duration:0.25,ease:"back.out(2.5)"}},{at:.3f});'


def blink(uid: str, at: float, pose: str = "neutral") -> list[str]:
    p = POSES[pose]
    out = []
    for side in ("L", "R"):
        h0, l0 = lid_attrs(p[f"lid_{side.lower()}"])
        h1, l1 = lid_attrs(1.0)
        out += [f'tl.to("#{uid}-lid{side}",{{attr:{{height:{h1}}},duration:0.06}},{at:.3f});',
                f'tl.to("#{uid}-lin{side}",{{attr:{{y1:{l1},y2:{l1}}},duration:0.06}},{at:.3f});',
                f'tl.to("#{uid}-lid{side}",{{attr:{{height:{h0}}},duration:0.08}},{at + 0.1:.3f});',
                f'tl.to("#{uid}-lin{side}",{{attr:{{y1:{l0},y2:{l0}}},duration:0.08}},{at + 0.1:.3f});']
    return out


def hop(sel: str, at: float, *, x0: float | None = None, x1: float | None = None, height: float = 70) -> list[str]:
    """Elastic hop of a wrapper div: squash, jump, land with squash (transform-origin bottom). x0 -> x1 absolute (px)."""
    xm = "" if x0 is None else f"x:{(x0 + x1) / 2:.0f},"
    xe = "" if x0 is None else f"x:{x1:.0f},"
    return [f'tl.to("{sel}",{{scaleY:0.86,scaleX:1.1,duration:0.08,ease:"power2.out"}},{at:.3f});',
            f'tl.to("{sel}",{{y:-{height},{xm}scaleY:1.1,scaleX:0.92,duration:0.18,ease:"power2.out"}},{at + 0.08:.3f});',
            f'tl.to("{sel}",{{y:0,{xe}scaleY:0.88,scaleX:1.1,duration:0.16,ease:"power2.in"}},{at + 0.26:.3f});',
            f'tl.to("{sel}",{{scaleY:1,scaleX:1,duration:0.35,ease:"elastic.out(1,0.4)"}},{at + 0.42:.3f});']


def idle(sel: str, c: SceneCtx, start: float | None = None, end: float | None = None) -> list[str]:
    """Breathing squash every ~1.6 s so Plümo is never frozen (until `end`, default the scene end)."""
    out, t = [], (start if start is not None else c.start + 0.4)
    k = 0
    stop = (end if end is not None else c.end) - 0.6
    while t < stop:
        s = 1.025 if k % 2 == 0 else 0.985
        out.append(f'tl.to("{sel} svg",{{scaleY:{s},scaleX:{2 - s:.3f},transformOrigin:"50% 92%",duration:0.8,ease:"sine.inOut"}},{t:.3f});')
        t += 0.8
        k += 1
    return out


def _js(props: dict) -> str:
    return "{" + ",".join(f"{k}:{v:.2f}" if isinstance(v, (int, float)) else f'{k}:"{v}"' for k, v in props.items()) + "}"


def drift(c: SceneCtx, sel: str, fn, step: float = 2.4) -> list[str]:
    """Move `sel` along fn(t) -> props (absolute time t) through this scene in short linear pieces. Every scene samples
    the same functions, so the backdrop runs on without a jump over hard cuts, and because all functions are periodic
    in the video length the last frame equals the first (loop)."""
    n = max(1, round(c.duration / step))
    ts = [c.start + c.duration * k / n for k in range(n + 1)]
    return [f'tl.fromTo("{sel}",{_js(fn(a))},{{...{_js(fn(b))},duration:{b - a:.3f},ease:"none"}},{a:.3f});' for a, b in zip(ts, ts[1:])]


# far landscape: dunes, an aqueduct of arches, a half-sunk sphere and two floating rocks (plum on plum, lime rim light)
_ARCHES = "".join(f'<path d="M{x},300 L{x},214 A34,34 0 0 1 {x + 68},214 L{x + 68},300 Z" fill="#160b1c"/>' for x in range(150, 560, 92))
FAR_SVG = (
    '<svg viewBox="0 0 1240 420" width="1240" height="420" xmlns="http://www.w3.org/2000/svg">'
    '<defs><radialGradient id="zfs" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#7A3CFF"/><stop offset="0.6" stop-color="#3a1a5c"/>'
    '<stop offset="1" stop-color="#1c0f2a"/></radialGradient>'
    '<linearGradient id="zfd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1c46"/><stop offset="1" stop-color="#1b0f22"/></linearGradient></defs>'
    '<circle cx="1000" cy="330" r="150" fill="url(#zfs)" opacity="0.9"/>'
    '<path d="M0,300 C180,250 330,262 520,286 C700,308 860,250 1240,276 L1240,420 L0,420 Z" fill="url(#zfd)"/>'
    '<path d="M120,190 L620,190 L620,206 L120,206 Z" fill="#160b1c"/>' + _ARCHES +
    '<path d="M120,190 L620,190" stroke="#B7FF00" stroke-opacity="0.28" stroke-width="3"/>'
    '<path d="M0,300 C180,250 330,262 520,286 C700,308 860,250 1240,276" fill="none" stroke="#FF43C0" stroke-opacity="0.35" stroke-width="3"/>'
    '<g opacity="0.85"><ellipse cx="760" cy="96" rx="70" ry="20" fill="#2a1536"/><path d="M700,96 Q760,170 820,96 Z" fill="#22112c"/>'
    '<ellipse cx="760" cy="92" rx="70" ry="14" fill="none" stroke="#B7FF00" stroke-opacity="0.3" stroke-width="3"/>'
    '<ellipse cx="300" cy="60" rx="40" ry="12" fill="#2a1536"/><path d="M266,60 Q300,104 334,60 Z" fill="#22112c"/></g>'
    '<rect x="900" y="150" width="16" height="150" rx="8" fill="#1d1026"/><rect x="940" y="196" width="12" height="104" rx="6" fill="#1d1026"/>'
    '</svg>')


def stage(c: SceneCtx) -> tuple[str, list[str]]:
    """Backdrop with depth, code only: night sky with key light (upper left) and magenta neon haze (right), a small
    ringed planet, far surreal landscape (parallax), three spotlight cones, perspective checker floor with light pool
    and horizon fog, two dust layers rising at different speeds, floating spheres, soft out-of-focus orbs, vignette.
    All motion is a periodic function of the absolute time (see drift)."""
    sid = c.sid
    T = TOTAL[0] if TOTAL[0] > 5 else max(60.0, c.end)
    w = 2 * math.pi / T
    orbs = [(90, 480, 40, PC["leaf"], 1, 0.0), (985, 610, 26, PC["body"], 2, 1.7), (990, 780, 56, "#7A3CFF", 1, 3.1)]
    html_ = ['<div class="zbg"></div><div class="zkey"></div><div class="zneon"></div>',
             f'<div class="zplanet" id="{sid}-pt"><i></i></div>',
             f'<div class="zfar" id="{sid}-far">{FAR_SVG}</div>',
             f'<div class="zbeam3" id="{sid}-bm0" style="left:150px;background:linear-gradient(rgba(255,242,199,0.20),rgba(255,242,199,0) 92%)"></div>'
             f'<div class="zbeam3" id="{sid}-bm1" style="left:420px;background:linear-gradient(rgba(255,67,192,0.16),rgba(255,67,192,0) 92%)"></div>'
             f'<div class="zbeam3" id="{sid}-bm2" style="left:690px;background:linear-gradient(rgba(183,255,0,0.13),rgba(183,255,0,0) 92%)"></div>',
             f'<div class="zfloorw" id="{sid}-fw"><div class="zfloor"></div></div><div class="zfog"></div><div class="zpool" id="{sid}-pool"></div>',
             f'<div class="zdust zd1" id="{sid}-d1"></div><div class="zdust zd2" id="{sid}-d2"></div>']
    for k, (x, y, r, col, _, _) in enumerate(orbs):
        html_.append(f'<div class="zorb" id="{sid}-o{k}" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;'
                     f'background:radial-gradient(circle at 35% 30%,#ffffff 0%,{col} 30%,color-mix(in srgb,{col} 45%,#101010) 100%)"></div>')
    html_.append(f'<div class="zbokeh" id="{sid}-k1" style="left:-170px;top:150px;width:340px;height:340px;--c:rgba(255,67,192,0.30)"></div>'
                 f'<div class="zbokeh" id="{sid}-k2" style="left:880px;top:880px;width:380px;height:380px;--c:rgba(122,60,255,0.30)"></div>'
                 '<div class="zvig"></div>')
    tl: list[str] = []
    tl += drift(c, f"#{sid}-far", lambda t: {"x": 34 * math.sin(w * t)})
    tl += drift(c, f"#{sid}-fw", lambda t: {"x": -70 * math.sin(w * t)})
    tl += drift(c, f"#{sid}-pt", lambda t: {"x": 14 * math.sin(w * t), "y": 8 * math.sin(2 * w * t), "rotation": 6 * math.sin(w * t)})
    for k, ph in enumerate((0.0, 2.1, 4.2)):
        tl += drift(c, f"#{sid}-bm{k}", lambda t, ph=ph, k=k: {"rotation": (k - 1) * 9 + 6 * math.sin(2 * w * t + ph)})
    tl += drift(c, f"#{sid}-pool", lambda t: {"opacity": 0.75 + 0.25 * math.sin(3 * w * t), "x": -40 * math.sin(w * t)})
    tl += drift(c, f"#{sid}-d1", lambda t: {"y": -300 * t / T}, step=c.duration)          # 300 px tile: seamless
    tl += drift(c, f"#{sid}-d2", lambda t: {"y": -900 * t / T, "x": 20 * math.sin(w * t)})  # 3 tiles of 300 px, nearer, faster
    for k, (_, _, _, _, m, ph) in enumerate(orbs):
        tl += drift(c, f"#{sid}-o{k}", lambda t, m=m, ph=ph, k=k: {"y": (38 if k % 2 else -34) * math.sin(m * w * t + ph),
                                                                  "rotation": 18 * math.sin(m * w * t + ph)})
    tl += drift(c, f"#{sid}-k1", lambda t: {"x": 40 * math.sin(w * t + 1), "y": 30 * math.sin(2 * w * t)})
    tl += drift(c, f"#{sid}-k2", lambda t: {"x": -36 * math.sin(w * t), "y": -40 * math.sin(2 * w * t + 2)})
    return "".join(html_), tl


def door(sid: str, sign: str) -> str:
    return (f'<div class="zsign" id="{sid}-sign">{_e(sign)}</div>'
            f'<div class="zdoor" id="{sid}-door"><div class="zdoor-in"></div><div class="zlamp" id="{sid}-lamp"></div></div>'
            f'<div class="zbeam" id="{sid}-beam"></div>')


# --- fruit drawings (plain fruits, never with faces: only Plümo has a face) --------------------------

def fruit_svg(kind: str, uid: str, size: int = 220) -> str:
    if kind == "strawberry":
        dots = "".join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="8" fill="#FFD84D" transform="rotate({r},{x},{y})"/>'
                       for x, y, r in [(70, 92, -20), (100, 84, 0), (130, 92, 20), (58, 122, -25), (88, 118, -8), (116, 118, 8), (144, 122, 25),
                                       (70, 150, -20), (100, 148, 0), (130, 150, 20), (86, 178, -10), (114, 178, 10), (100, 204, 0)])
        body = (f'<defs><radialGradient id="{uid}-sg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FF7A8E"/>'
                f'<stop offset="0.45" stop-color="#F0213F"/><stop offset="1" stop-color="#8E0B24"/></radialGradient></defs>'
                f'<path d="M100,228 C52,196 30,140 36,104 C42,72 70,62 100,64 C130,62 158,72 164,104 C170,140 148,196 100,228 Z" fill="url(#{uid}-sg)"/>'
                f'{dots}<path d="M100,70 L70,46 L92,58 L84,30 L100,54 L116,30 L108,58 L130,46 Z" fill="#3FAF3A"/>'
                f'<rect x="96" y="22" width="8" height="26" rx="4" fill="#2E7D2A"/>')
    elif kind == "banana":
        body = ('<defs><linearGradient id="%s-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF08A"/><stop offset="1" stop-color="#E6B800"/></linearGradient></defs>'
                '<path d="M30,70 C40,170 130,210 196,150 C200,146 200,138 194,138 C140,170 80,140 58,62 Z" fill="url(#%s-bg)"/>'
                '<path d="M30,70 L22,52 L40,48 L58,62 Z" fill="#6B4A1A"/><circle cx="196" cy="144" r="6" fill="#4A3210"/>') % (uid, uid)
    elif kind == "tomato":
        body = (f'<defs><radialGradient id="{uid}-tg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FF8A7A"/>'
                f'<stop offset="0.5" stop-color="#F23A2A"/><stop offset="1" stop-color="#9A1408"/></radialGradient></defs>'
                f'<ellipse cx="110" cy="130" rx="84" ry="74" fill="url(#{uid}-tg)"/>'
                f'<path d="M110,62 L84,50 L100,66 L78,78 L106,72 L110,92 L114,72 L142,78 L120,66 L136,50 Z" fill="#3FAF3A"/>')
    elif kind == "grape":
        grapes = "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="url(#{uid}-gg)"/>'
                         for x, y in [(80, 70), (124, 70), (60, 108), (102, 108), (144, 108), (80, 146), (124, 146), (102, 184)])
        body = (f'<defs><radialGradient id="{uid}-gg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#D6A8FF"/>'
                f'<stop offset="0.5" stop-color="#8E44D9"/><stop offset="1" stop-color="#4A1A80"/></radialGradient></defs>'
                f'<path d="M102,46 L102,20" stroke="#5A3A1A" stroke-width="7" stroke-linecap="round"/>{grapes}')
    elif kind in zp.PROPS:
        body = zp.PROPS[kind](uid)
    else:
        raise ValueError(f"unknown prop {kind!r}; add it to zonk_props.PROPS")
    return f'<svg viewBox="0 0 220 240" width="{size}" height="{int(size * 240 / 220)}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def embed(kind: str, uid: str, x: float, y: float, w: float) -> str:
    """A prop as nested <svg> inside another SVG (x, y top-left, width w, height from the 220 x 240 box)."""
    inner = re.sub(r"^<svg[^>]*>|</svg>$", "", fruit_svg(kind, uid, 220))
    return f'<svg x="{x}" y="{y}" width="{w}" height="{w * 240 / 220:.0f}" viewBox="0 0 220 240" overflow="visible">{inner}</svg>'


# --- 1. zonk_scan ----------------------------------------------------------------------------------

def zonk_scan(c: SceneCtx, d: dict) -> SceneOut:
    """Door 'NUR BEEREN' with a scanner. d: mode (hook|reject|accept|unknown), sign, head, items[{kind, word, verdict}],
    stamp_reject, stamp_accept, display, counter, merke, cues {...}."""
    _begin(c)
    mode = d.get("mode", "reject")
    sid, u = c.sid, f"{c.sid}p"
    problems: list[str] = []
    sign = d.get("sign", "NUR BEEREN")
    _lim(problems, "zonk_scan", "sign", sign)
    bg, tl = stage(c)
    events: list[float] = []
    parts = [bg, door(sid, sign)]
    head = d.get("head", "")
    if head:
        _lim(problems, "zonk_scan", "head", head)
        parts.append(f'<div class="zhead" id="{sid}-head">{_rich(head)}</div>')
    parts.append(plumo(u, "neutral", back=(mode == "unknown")))
    wrap = f"#{u}-wrap"
    tl += idle(wrap, c)

    if mode in ("hook", "reject"):
        item = (d.get("items") or [{"kind": "strawberry"}])[0]
        stamp = d.get("stamp_reject", "ABGELEHNT")
        _lim(problems, "zonk_scan", "stamp", stamp)
        parts.append(f'<div class="zitem" id="{sid}-i0">{fruit_svg(item["kind"], sid + "f0")}</div>')
        parts.append(f'<div class="zstamp zreject" id="{sid}-stamp">{_e(stamp)}</div>')
        t_in = c.start + 0.15
        if mode == "reject":
            t_scan = cue(c, item.get("word_scan"), 0.22)
            t_verdict = cue(c, item.get("word_verdict"), 0.4)
        else:   # hook: scan on the fruit's name, verdict on the negation, but the visual punchline within ~2 s
            t_scan = max(t_in + 0.45, min(cue(c, d.get("cue_scan"), 0.9 / c.duration), c.start + 1.2))
            t_verdict = max(t_scan + 0.6, min(cue(c, d.get("cue_verdict"), min(1.9, c.duration * 0.45) / c.duration), c.start + 2.1))
        tl += [f'tl.fromTo("#{sid}-i0",{{x:520,y:-160,rotation:40,opacity:1}},{{x:0,y:0,rotation:0,duration:0.5,ease:"bounce.out"}},{t_in:.3f});',
               f'tl.fromTo("#{sid}-beam",{{opacity:0,y:0}},{{opacity:1,y:440,duration:0.55,ease:"sine.inOut"}},{t_scan:.3f});',
               f'tl.to("#{sid}-beam",{{opacity:0,duration:0.15}},{t_scan + 0.55:.3f});',
               f'tl.fromTo("#{sid}-lamp",{{background:"#3a2a36"}},{{background:"{PC["leaf"]}",duration:0.1}},{t_verdict:.3f});',
               f'tl.fromTo("#{sid}-stamp",{{opacity:0,scale:2.4,rotation:-18}},{{opacity:1,scale:1,rotation:-9,duration:0.22,ease:"back.out(2)"}},{t_verdict:.3f});',
               f'tl.to("#{sid}-i0",{{x:640,y:-420,rotation:260,duration:0.7,ease:"power2.in"}},{t_verdict + 0.55:.3f});']
        tl += expr(u, "staunen", t_verdict + 0.05) + expr(u, "neutral", t_verdict + 1.3)
        sfx(t_in, "pop", 0.3); sfx(t_in + 0.25, "boing", 0.25); sfx(t_scan, "scan", 0.18); sfx(t_verdict, "buzz", 0.22); sfx(t_verdict + 0.55, "whoosh", 0.3)
        events += [t_in, t_scan, t_verdict, t_verdict + 0.55, t_verdict + 1.3]
        if head:
            t_head = c.t(d.get("head_at", 0.25))
            tl.append(f'tl.fromTo("#{sid}-head",{{opacity:0,y:30,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(2)"}},{t_head:.3f});')
            tl.append(f'tl.fromTo("#{sid}-head .zhl",{{scale:1}},{{scale:1.18,duration:0.14,yoyo:true,repeat:1,ease:"power2.out"}},{t_verdict:.3f});')
            events.append(t_head)
        if mode == "hook" and d.get("cue_club"):     # "... der Beerenclub weiß das auch": sign jumps, lamp blinks, Plümo smug
            t_club = cue(c, d.get("cue_club"), 0.62, after=t_verdict + 0.5)
            t_know = cue(c, d.get("cue_know"), 0.75, after=t_club + 0.2)
            tl += [f'tl.fromTo("#{sid}-sign",{{y:0,rotation:0}},{{y:-26,rotation:-4,duration:0.16,yoyo:true,repeat:1,ease:"power2.out"}},{t_club:.3f});',
                   f'tl.to("#{sid}-lamp",{{background:"{PC["leaf"]}",duration:0.06,yoyo:true,repeat:3}},{t_club:.3f});',
                   f'tl.fromTo("#{sid}-door",{{boxShadow:"inset 0 0 60px rgba(0,0,0,0.8),0 0 0 rgba(255,67,192,0)"}},'
                   f'{{boxShadow:"inset 0 0 60px rgba(0,0,0,0.8),0 0 60px rgba(255,67,192,0.7)",duration:0.25,yoyo:true,repeat:1}},{t_club:.3f});']
            tl += expr(u, "stolz", t_know) + [leaf_to(u, 140, t_know + 0.1), leaf_to(u, 118, t_know + 0.4)]
            sfx(t_club, "pop", 0.22)
            events += [t_club, t_know]
        if mode == "reject":
            t2 = cue(c, d.get("cue_blink"), 0.75)
            tl += expr(u, "verwirrt", t2) + [leaf_to(u, 40, t2 + 0.3), leaf_to(u, 80, t2 + 0.6), leaf_to(u, 40, t2 + 0.9)]
            events.append(t2)
    elif mode == "accept":
        items = d.get("items", [])
        stamp = d.get("stamp_accept", "EINLASS")
        _lim(problems, "zonk_scan", "stamp", stamp)
        parts.append(f'<div class="zstamp zaccept" id="{sid}-stamp">{_e(stamp)}</div>')
        parts.append(f'<div class="zcounter" id="{sid}-cnt">{_e(d.get("counter", "Echte Beeren:"))} <span class="zcn">{"".join(f'<b id="{sid}-cn{k}" style="opacity:{1 if k == 0 else 0}">{k}</b>' for k in range(len(d.get("items", [])) + 1))}</span></div>')
        tl.append(f'tl.fromTo("#{sid}-cnt",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.25}},{c.t(0.2):.3f});')
        events.append(c.t(0.2))
        prev = c.start + 0.3
        for k, it in enumerate(items):
            parts.append(f'<div class="zitem" id="{sid}-i{k}">{fruit_svg(it["kind"], f"{sid}f{k}")}</div>')
            t = max(prev, cue(c, it.get("word"), 0.15 + 0.22 * k))
            tl += [f'tl.fromTo("#{sid}-i{k}",{{x:520,y:-160,rotation:30,opacity:1}},{{x:0,y:0,rotation:0,duration:0.42,ease:"bounce.out"}},{t:.3f});',
                   f'tl.to("#{sid}-lamp",{{background:"{PC["body"]}",duration:0.08}},{t + 0.45:.3f});',
                   f'tl.fromTo("#{sid}-stamp",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,rotation:-6,duration:0.18,ease:"back.out(2)"}},{t + 0.45:.3f});',
                   f'tl.set("#{sid}-cn{k}",{{opacity:0}},{t + 0.5:.3f});', f'tl.set("#{sid}-cn{k + 1}",{{opacity:1}},{t + 0.5:.3f});',
                   f'tl.to("#{sid}-stamp",{{opacity:0,duration:0.12}},{t + 0.95:.3f});',
                   f'tl.to("#{sid}-i{k}",{{x:-40,scale:0.2,opacity:0,duration:0.3,ease:"power2.in"}},{t + 0.95:.3f});']
            sfx(t, "pop", 0.28); sfx(t + 0.45, "chime", 0.22)
            events += [t, t + 0.45, t + 0.95]
            prev = t + 1.2
        tl += expr(u, "verwirrt", c.t(0.3)) + expr(u, "staunen", prev - 0.6)
        if d.get("cue_all"):        # "Alles echte Beeren": counter pulses in mint (reached)
            t_all = cue(c, d.get("cue_all"), 0.55, after=prev - 0.4)
            tl += [f'tl.fromTo("#{sid}-cnt",{{scale:1}},{{scale:1.12,duration:0.16,yoyo:true,repeat:1,ease:"power2.out"}},{t_all:.3f});',
                   f'tl.to("#{sid}-cnt .zcn",{{color:"#3EE08F",duration:0.15}},{t_all:.3f});']
            sfx(t_all, "chime", 0.2)
            events.append(t_all)
        t_end = cue(c, d.get("cue_react"), 0.82, after=prev - 0.3)
        tl += expr(u, "stolz", t_end) if d.get("react") == "stolz" else expr(u, "neutral", t_end)
        events.append(t_end)
        if d.get("cue_why"):        # "... gefragt, warum": Plümo asks; "Sie wusste es auch nicht": deadpan blink
            t_why = cue(c, d.get("cue_why"), 0.85, after=t_end)
            t_no = cue(c, d.get("cue_shrug"), 0.95, after=t_why + 0.2)
            tl += expr(u, "verwirrt", t_why) + [leaf_to(u, 60, t_why + 0.1), leaf_to(u, 100, t_why + 0.35), leaf_to(u, 60, t_why + 0.6)]
            tl += expr(u, "neutral", t_no) + blink(u, t_no + 0.25)
            tl.append(f'tl.fromTo("#{sid}-sign",{{rotation:0}},{{rotation:5,duration:0.12,yoyo:true,repeat:3}},{t_no:.3f});')
            events += [t_why, t_no]
    elif mode == "unknown":
        disp = d.get("display", "Sorte: nicht ermittelbar")
        _lim(problems, "zonk_scan", "display", disp)
        merke = d.get("merke", "")
        if merke:
            _lim(problems, "zonk_scan", "head", merke)
            parts.append(f'<div class="zmerke" id="{sid}-merke"><span class="zmk">Merke</span>{_rich(merke)}</div>')
            tl.append(f'tl.fromTo("#{sid}-merke",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.6)"}},{c.t(0.1):.3f});')
            events.append(c.t(0.1))
        parts.append(f'<div class="zdisplay" id="{sid}-disp">{_e(disp)}</div>')
        parts.append(f'<div class="zplumps" id="{sid}-pl">{_e(d.get("plumps", "PLUMPS"))}</div>')
        t_go = cue(c, d.get("cue_go"), 0.35)
        t_scan = cue(c, d.get("cue_scan"), 0.5, after=t_go)
        t_res = cue(c, d.get("cue_result"), 0.62, after=t_scan)
        t_back = cue(c, d.get("cue_back"), 0.78, after=t_res)
        t_fall = min(c.end - 0.7, t_back + 1.4)
        if merke:
            if d.get("cue_build"):      # "... wie die Frucht gebaut ist": the highlighted word in the Merke line pops
                t_b = cue(c, d.get("cue_build"), 0.3)
                tl.append(f'tl.fromTo("#{sid}-merke .zhl",{{scale:1}},{{scale:1.25,duration:0.16,yoyo:true,repeat:1,ease:"power2.out"}},{t_b:.3f});')
                events.append(t_b)
            tl.append(f'tl.to("#{sid}-merke",{{opacity:0,y:-20,duration:0.2}},{t_go - 0.1:.3f});')
        tl += expr(u, "stolz", t_go - 0.4) + hop(wrap, t_go, x0=0, x1=210) + hop(wrap, t_go + 0.75, x0=210, x1=420)
        tl += [f'tl.fromTo("#{sid}-beam",{{opacity:0,y:0}},{{opacity:1,y:440,duration:0.6,ease:"sine.inOut"}},{t_scan:.3f});',
               f'tl.to("#{sid}-beam",{{opacity:0,duration:0.15}},{t_scan + 0.6:.3f});',
               f'tl.to("#{sid}-lamp",{{background:"{PC["sticker"]}",duration:0.1}},{t_res:.3f});',
               f'tl.fromTo("#{sid}-disp",{{opacity:0,scaleY:0.2}},{{opacity:1,scaleY:1,duration:0.2,ease:"back.out(2)"}},{t_res:.3f});']
        tl += expr(u, "staunen", t_res + 0.2)
        # turn around: the back view with the "?" sticker, then front again
        tl += [f'tl.to("#{u}",{{opacity:0,duration:0.12}},{t_back:.3f});', f'tl.to("#{u}-backwrap",{{opacity:1,duration:0.12}},{t_back:.3f});',
               f'tl.to("#{u}-backwrap",{{opacity:0,duration:0.12}},{t_back + 1.0:.3f});', f'tl.to("#{u}",{{opacity:1,duration:0.12}},{t_back + 1.0:.3f});']
        tl += expr(u, "umgekippt", t_fall)
        tl += [f'tl.to("{wrap}",{{rotation:-90,transformOrigin:"20% 92%",duration:0.42,ease:"bounce.out"}},{t_fall:.3f});',
               f'tl.fromTo("#{sid}-pl",{{opacity:0,scale:0.4,rotation:-12}},{{opacity:1,scale:1,rotation:-6,duration:0.2,ease:"back.out(3)"}},{t_fall + 0.3:.3f});',
               f'tl.to("#{sid}-pl",{{opacity:0,duration:0.2}},{min(c.end - 0.2, t_fall + 1.2):.3f});']
        sfx(t_go, "boing", 0.25); sfx(t_go + 0.75, "boing", 0.25); sfx(t_scan, "scan", 0.18); sfx(t_res, "unknown", 0.3); sfx(t_back, "whoosh", 0.25); sfx(t_fall + 0.25, "plumps", 0.4)
        events += [t_go, t_go + 0.75, t_scan, t_res, t_back, t_back + 1.0, t_fall, t_fall + 0.3]
    # camera: door scenes cut hard into each other (accept -> unknown -> loop), so their values chain (see zonk_loop)
    cam = {"hook": (1.0, 1.05), "reject": (1.0, 1.04), "accept": (1.0, 1.035), "unknown": (1.035, 1.08)}[mode]
    return _out(c, parts, tl, events, problems, cam=cam, origin=(860, 860))


# --- 2. zonk_word ----------------------------------------------------------------------------------

def zonk_word(c: SceneCtx, d: dict) -> SceneOut:
    """d: word_a, word_b (struck), left{text}, right{text}, cues {strike, left, right}."""
    _begin(c)
    sid, u = c.sid, f"{c.sid}p"
    problems: list[str] = []
    a, b = d.get("word_a", ""), d.get("word_b", "")
    _lim(problems, "zonk_word", "word", a + b)
    lt, rt = d.get("left", ""), d.get("right", "")
    _lim(problems, "zonk_word", "chip", lt)
    _lim(problems, "zonk_word", "chip", rt)
    bg, tl = stage(c)
    parts = [bg, f'<div class="zword" id="{sid}-w"><span>{_e(a)}</span><span class="zwb" id="{sid}-wb">{_e(b)}<i class="zstrike" id="{sid}-st"></i></span></div>',
             f'<div class="zchip zchip-c" id="{sid}-cl">{_rich(lt)}</div>', f'<div class="zchip zchip-m" id="{sid}-cr">{_rich(rt)}</div>',
             plumo(u, "verwirrt", left=20, top=640, width=400)]
    wrap = f"#{u}-wrap"
    t0 = c.t(0.12)
    t_l = cue(c, d.get("cue_left"), 0.3)
    t_s = cue(c, d.get("cue_strike"), 0.5, after=t_l)
    t_r = max(t_s + 0.2, cue(c, d.get("cue_right"), 0.58, after=t_s))
    t_x = cue(c, d.get("cue_react"), 0.82, after=t_r)
    events = [t0, t_l, t_s, t_r, t_x]
    if d.get("item"):       # "... genauso geschockt wie die Erdbeere. Und die ist sonst nie geschockt.": the fruit itself
        parts.append(f'<div class="zwitem" id="{sid}-it">{fruit_svg(d["item"], sid + "wf", size=190)}</div>')
        t_sh = cue(c, d.get("cue_shock"), 0.86, after=t_x)
        t_it = max(t_sh + 0.3, cue(c, d.get("cue_item"), 0.9, after=t_sh))
        t_nv = max(t_it + 0.5, cue(c, d.get("cue_never"), 0.96, after=t_it))
        tl += expr(u, "staunen", t_sh) + [f'tl.fromTo("{wrap}",{{x:0}},{{x:12,duration:0.05,yoyo:true,repeat:5}},{t_sh:.3f});']
        tl += [f'tl.fromTo("#{sid}-it",{{opacity:0,y:-200,rotation:-30}},{{opacity:1,y:0,rotation:0,duration:0.4,ease:"bounce.out"}},{t_it:.3f});',
               f'tl.fromTo("#{sid}-it svg",{{x:0}},{{x:9,duration:0.04,yoyo:true,repeat:9}},{t_it + 0.4:.3f});',
               f'tl.to("#{sid}-it",{{rotation:14,duration:0.25,ease:"back.out(2)"}},{t_nv:.3f});']
        tl += expr(u, "neutral", t_nv) + blink(u, t_nv + 0.4)
        sfx(t_sh, "boing", 0.2); sfx(t_it, "pop", 0.28)
        events += [t_sh, t_it, t_nv]
    tl += [f'tl.fromTo("#{sid}-w",{{opacity:0,y:-60,rotation:-4}},{{opacity:1,y:0,rotation:0,duration:0.35,ease:"back.out(2)"}},{t0:.3f});',
           f'tl.fromTo("#{sid}-cl",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.25}},{t_l:.3f});',
           f'tl.fromTo("#{sid}-st",{{scaleX:0}},{{scaleX:1,duration:0.25,ease:"power2.out"}},{t_s:.3f});',
           f'tl.to("#{sid}-wb",{{color:"#7d6a78",duration:0.2}},{t_s:.3f});',
           f'tl.fromTo("#{sid}-cr",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.22,ease:"back.out(2)"}},{t_r:.3f});']
    tl += idle(wrap, c) + [leaf_to(u, 60, t0 + 0.4), leaf_to(u, 95, t0 + 0.7), leaf_to(u, 60, t0 + 1.0)]
    tl += expr(u, "staunen", t_s + 0.05) + expr(u, "neutral", t_x) + blink(u, t_x + 0.6)
    sfx(t0, "pop", 0.3); sfx(t_s, "whoosh", 0.22); sfx(t_r, "buzz", 0.15)
    return _out(c, parts, tl, events, problems, cam=(1.0, 1.04), origin=(540, 700))


# --- 3. zonk_diagram -------------------------------------------------------------------------------

def zonk_diagram(c: SceneCtx, d: dict) -> SceneOut:
    """d: headline, labels[{text, pos: tr|l|b, cue}]; cross-section of a berry, Plümo points at each label."""
    _begin(c)
    sid, u = c.sid, f"{c.sid}p"
    problems: list[str] = []
    h2 = d.get("headline", "")
    _lim(problems, "zonk_diagram", "h2", h2)
    bg, tl = stage(c)
    seeds = "".join(f'<path d="M0,-26 C14,-10 14,14 0,26 C-14,14 -14,-10 0,-26 Z" fill="#6B4220" transform="translate({x},{y}) rotate({r})"/>'
                    for x, y, r in [(-60, -40, -30), (52, -48, 30), (-44, 56, 200), (60, 44, 150), (0, 0, 90)])
    if d.get("inner"):          # any prop inside the disc instead of the berry seeds (zonk_props)
        seeds = embed(d["inner"], sid + "in", -165, -180, 330)
    rim, hi, lo = d.get("disc", ["#6B2FA8", "#F4E2FF", "#C79AF0"])
    xs = (f'<svg class="zxs" id="{sid}-xs" viewBox="-260 -260 520 520" width="620" height="620">'
          f'<defs><radialGradient id="{sid}-fl" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="{hi}"/><stop offset="1" stop-color="{lo}"/></radialGradient></defs>'
          f'<circle r="236" fill="{rim}"/><circle r="214" fill="url(#{sid}-fl)" id="{sid}-flesh"/>'
          f'<circle r="214" fill="none" stroke="{PC["body"]}" stroke-width="10" id="{sid}-ring" stroke-dasharray="1345" stroke-dashoffset="1345"/>'
          f'<g id="{sid}-seeds">{seeds}</g></svg>')
    parts = [bg, f'<div class="zh2" id="{sid}-h">{_rich(h2)}</div>', xs, plumo(u, "zeigen", left=10, top=800, width=280)]
    # labels stay left of x 930 (platform icons): top-right label is right-aligned
    pos_css = {"tr": "right:150px;top:440px", "l": "left:60px;top:650px", "b": "left:310px;top:1000px"}
    leaf_angle = {"tr": -40, "l": -150, "b": 20}
    wrap = f"#{u}-wrap"
    t0 = c.t(0.08)
    tl += [f'tl.fromTo("#{sid}-h",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t0:.3f});',
           f'tl.fromTo("#{sid}-xs",{{opacity:0,scale:0.3,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:0.55,ease:"back.out(1.6)"}},{t0 + 0.15:.3f});',
           f'tl.fromTo("#{sid}-xs",{{rotation:0}},{{rotation:8,duration:{max(1.0, c.duration - 1.0):.2f},ease:"sine.inOut"}},{t0 + 0.7:.3f});']
    events = [t0, t0 + 0.15]
    sfx(t0 + 0.15, "pop", 0.3)
    if d.get("cue_q"):          # "... was ist eine Beere?": the highlighted word in the headline pops
        t_q = cue(c, d.get("cue_q"), 0.12)
        tl.append(f'tl.fromTo("#{sid}-h .zhl",{{scale:1}},{{scale:1.22,duration:0.15,yoyo:true,repeat:1,ease:"power2.out"}},{t_q:.3f});')
        events.append(t_q)
    prev = t0 + 0.7
    for k, lab in enumerate(d.get("labels", [])):
        _lim(problems, "zonk_diagram", "label", lab["text"])
        parts.append(f'<div class="zlabel" id="{sid}-l{k}" style="{pos_css[lab.get("pos", "tr")]}">{_rich(lab["text"])}</div>')
        t = max(prev, cue(c, lab.get("cue"), 0.25 + 0.22 * k))
        tl += [f'tl.fromTo("#{sid}-l{k}",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.22,ease:"back.out(2.4)"}},{t:.3f});',
               leaf_to(u, leaf_angle[lab.get("pos", "tr")], t)]
        if lab.get("pos") == "l":
            tl.append(f'tl.to("#{sid}-ring",{{attr:{{"stroke-dashoffset":0}},duration:0.6,ease:"power2.out"}},{t:.3f});')
        if lab.get("pos") == "b":
            tl.append(f'tl.fromTo("#{sid}-seeds",{{scale:1}},{{scale:1.18,transformOrigin:"50% 50%",duration:0.18,yoyo:true,repeat:3}},{t:.3f});')
        tl += hop(wrap, t, height=30)
        sfx(t, "pop", 0.25)
        events.append(t)
        prev = t + 0.5
    if d.get("cue_hands"):      # "Ich hab keine Hände, also zeige ich mit meinem Blatt.": shrug, then a big leaf point
        t_h = cue(c, d.get("cue_hands"), 0.75, after=prev - 0.3)
        t_bl = max(t_h + 0.5, cue(c, d.get("cue_leaf"), 0.9, after=t_h))
        tl += expr(u, "verwirrt", t_h) + [leaf_to(u, 150, t_h + 0.05), leaf_to(u, 90, t_h + 0.3), leaf_to(u, 150, t_h + 0.55)]
        tl += expr(u, "stolz", t_bl) + [leaf_to(u, -40, t_bl + 0.1), leaf_to(u, -10, t_bl + 0.35), leaf_to(u, -40, t_bl + 0.6)]
        tl += hop(wrap, t_bl, height=36)
        sfx(t_bl, "boing", 0.22)
        events += [t_h, t_bl]
    tl += idle(wrap, c)
    return _out(c, parts, tl, events, problems, cam=(1.0, 1.045), origin=(540, 730))


# --- 4. zonk_zoom ----------------------------------------------------------------------------------

def zonk_zoom(c: SceneCtx, d: dict) -> SceneOut:
    """d: kind (strawberry), callouts[{text, cue}], stamp{text, cue}; magnifier slides over the fruit."""
    _begin(c)
    sid, u = c.sid, f"{c.sid}p"
    problems: list[str] = []
    bg, tl = stage(c)
    mag_in = (f'<div class="zmag" id="{sid}-mag"><div class="zmag-in"><svg viewBox="-190 -190 380 380" width="318" height="318">'
              f'<circle r="190" fill="#E5163F"/><circle r="190" fill="url(#{sid}-mg)"/>'
              f'<defs><radialGradient id="{sid}-mg" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FF8A9C" stop-opacity="0.8"/><stop offset="1" stop-color="#8E0B24" stop-opacity="0.6"/></radialGradient></defs>'
              f'<ellipse rx="66" ry="104" fill="#FFD84D" transform="rotate(-14)"/><ellipse rx="40" ry="66" fill="none" stroke="#C99A1A" stroke-width="5" stroke-dasharray="10 8" transform="rotate(-14)"/>'
              f'<ellipse cx="-118" cy="-110" rx="30" ry="46" fill="#FFD84D" transform="rotate(-30,-118,-110)"/><ellipse cx="130" cy="120" rx="30" ry="46" fill="#FFD84D" transform="rotate(20,130,120)"/>'
              f'</svg></div><div class="zmag-h"></div></div>')
    if d.get("lens"):           # any prop, enlarged, inside the lens (default: the strawberry nutlet)
        lens_bg = d.get("lens_bg", "#2C1638")
        mag_in = (f'<div class="zmag" id="{sid}-mag"><div class="zmag-in" style="background:{lens_bg}"><svg viewBox="-190 -190 380 380" width="318" height="318">'
                  f'<circle r="190" fill="{lens_bg}"/>{embed(d["lens"], sid + "ln", -165, -180, 330)}'
                  f'</svg></div><div class="zmag-h"></div></div>')
    # x from 930 stays free (platform icons): magnifier ends at x 900, Plümo at x 910 (also at camera scale 1.04)
    parts = [bg, f'<div class="zbig" id="{sid}-fruit">{fruit_svg(d.get("kind", "strawberry"), sid + "bf", size=580)}</div>', mag_in,
             plumo(u, "staunen", left=650, top=850, width=260)]
    pos = ["left:70px;top:340px", "left:70px;top:980px"]
    t0 = c.t(0.05)
    t_mag = cue(c, d.get("cue_mag"), 0.12)
    tl += [f'tl.fromTo("#{sid}-fruit",{{opacity:0,scale:0.6,y:60}},{{opacity:1,scale:1,y:0,duration:0.4,ease:"back.out(1.8)"}},{t0:.3f});',
           f'tl.fromTo("#{sid}-mag",{{x:520,y:-300,rotation:30,opacity:0}},{{x:0,y:0,rotation:0,opacity:1,duration:0.55,ease:"power3.out"}},{t_mag:.3f});',
           f'tl.fromTo("#{sid}-mag .zmag-in svg",{{scale:0.5}},{{scale:1,duration:0.6,ease:"power2.out"}},{t_mag + 0.3:.3f});',
           f'tl.fromTo("#{sid}-fruit",{{scale:1}},{{scale:1.06,duration:{max(0.5, c.duration - 1):.2f},ease:"none"}},{t0 + 0.4:.3f});']
    events = [t0, t_mag, t_mag + 0.3]
    sfx(t0, "pop", 0.3); sfx(t_mag, "whoosh", 0.3)
    prev = t_mag + 0.8
    for k, co in enumerate(d.get("callouts", [])):
        _lim(problems, "zonk_zoom", "label", co["text"])
        # the close-up vignette of the explainer layer (translucent, z 12) lies over the callouts on purpose
        parts.append(f'<div class="zlabel" id="{sid}-c{k}" style="{pos[k % 2]}" data-layout-allow-occlusion>{_rich(co["text"]).replace('class="zhl"', 'class="zhl" data-layout-allow-occlusion')}</div>')
        t = max(prev, cue(c, co.get("cue"), 0.3 + 0.25 * k))
        tl.append(f'tl.fromTo("#{sid}-c{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25,ease:"back.out(2)"}},{t:.3f});')
        if k == 1:      # second callout is about the red flesh: magnifier moves off the nutlet, the fruit squishes
            tl.append(f'tl.to("#{sid}-mag",{{x:-80,y:180,duration:0.5,ease:"power2.inOut"}},{t:.3f});')
            tl.append(f'tl.fromTo("#{sid}-fruit svg",{{scaleX:1,scaleY:1}},{{scaleX:1.07,scaleY:0.93,transformOrigin:"50% 90%",duration:0.14,yoyo:true,repeat:1}},{t + 0.3:.3f});')
        sfx(t, "pop", 0.25)
        events.append(t)
        prev = t + 0.6
        if k == 0 and d.get("cue_nut"):     # "... kleine Nüsschen": the nutlet in the lens pulses
            t_n = max(t + 0.4, cue(c, d.get("cue_nut"), 0.45, after=t))
            tl.append(f'tl.fromTo("#{sid}-mag .zmag-in svg",{{scale:1}},{{scale:1.16,duration:0.16,yoyo:true,repeat:3,ease:"power2.out"}},{t_n:.3f});')
            sfx(t_n, "pop", 0.18)
            events.append(t_n)
            prev = t_n + 0.5
    st = d.get("stamp") or {}
    if st:
        _lim(problems, "zonk_zoom", "stamp", st["text"])
        parts.append(f'<div class="zterm" id="{sid}-term">{_e(st["text"])}</div>')
        t = max(prev, cue(c, st.get("cue"), 0.75))
        tl += [f'tl.to("#{sid}-mag",{{x:0,y:-30,duration:0.35,ease:"power2.inOut"}},{t - 0.2:.3f});',   # lens clears the stamp line
               f'tl.fromTo("#{sid}-term",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.25,ease:"back.out(2)"}},{t:.3f});']
        tl += expr(u, "stolz", t + 0.3)
        t_end = cue(c, d.get("cue_react"), 0.9, after=t + 0.5)
        tl += expr(u, "verwirrt", t_end) + hop(f"#{u}-wrap", t_end, height=40)
        sfx(t, "boing", 0.3)
        events += [t, t_end]
        if d.get("cue_fast"):       # "... dreimal schnell sagen": the stamp wobbles three times, fast
            t_f = max(t_end + 0.2, cue(c, d.get("cue_fast"), 0.95, after=t_end))
            tl.append(f'tl.fromTo("#{sid}-term",{{rotation:-5}},{{rotation:3,duration:0.07,yoyo:true,repeat:5}},{t_f:.3f});')
            events.append(t_f)
    tl += blink(u, c.t(0.4), "staunen") + idle(f"#{u}-wrap", c)
    return _out(c, parts, tl, events, problems, cam=(1.0, 1.04), origin=(560, 700))


# --- 4b. zonk_compare -----------------------------------------------------------------------------

def zonk_compare(c: SceneCtx, d: dict) -> SceneOut:
    """Bars that grow on their word: d: headline, bars[{label, value, h (0..1), kind, cue, color}], stamp{text, cue},
    cue_react, fall (Plümo tips over on cue_react). Plümo stands left, next to the bars; bars end left of x 920."""
    _begin(c)
    sid, u = c.sid, f"{c.sid}p"
    problems: list[str] = []
    h2 = d.get("headline", "")
    _lim(problems, "zonk_compare", "h2", h2)
    bg, tl = stage(c)
    parts = [bg, f'<div class="zh2" id="{sid}-h">{_rich(h2)}</div>', plumo(u, "neutral", left=10, top=760, width=300)]
    wrap = f"#{u}-wrap"
    bars = d.get("bars", [])
    n = max(1, len(bars))
    x0, x1, base, hmax = 330, 915, 1060, 500
    slot = (x1 - x0) / n
    bw = min(220, slot - 26)
    t0 = c.t(0.06)
    tl.append(f'tl.fromTo("#{sid}-h",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t0:.3f});')
    events = [t0]
    prev = t0 + 0.4
    for k, bar in enumerate(bars):
        _lim(problems, "zonk_compare", "chip", bar.get("label", ""))
        _lim(problems, "zonk_compare", "value", bar.get("value", ""))
        H = int(hmax * max(0.06, min(1.0, float(bar.get("h", 0.5)))))
        x = int(x0 + slot * k + (slot - bw) / 2)
        col = bar.get("color", PC["body"] if k == n - 1 else "#B04A92")    # the record holder in lime
        ps = int(min(bw, 170))
        prop = f'<div class="zcp" id="{sid}-p{k}" style="left:{x + (bw - ps) / 2:.0f}px;top:{base - H - ps * 240 / 220 + 6:.0f}px;width:{ps}px">{fruit_svg(bar["kind"], f"{sid}c{k}", size=ps)}</div>' if bar.get("kind") else ""
        parts.append(f'<div class="zbar" id="{sid}-b{k}" style="left:{x}px;top:{base - H}px;width:{bw:.0f}px;height:{H}px;background:linear-gradient(180deg,{col},color-mix(in srgb,{col} 55%,#101010))">'
                     f'<span class="zbv" id="{sid}-v{k}">{_e(bar.get("value", ""))}</span></div>{prop}'
                     f'<div class="zbl" id="{sid}-l{k}" style="left:{x - 20}px;width:{bw + 40:.0f}px;top:{base + 10}px">{_e(bar.get("label", ""))}</div>')
        t = max(prev, cue(c, bar.get("cue"), 0.2 + 0.25 * k))
        tl += [f'tl.fromTo("#{sid}-b{k}",{{scaleY:0}},{{scaleY:1,transformOrigin:"50% 100%",duration:0.6,ease:"back.out(1.4)"}},{t:.3f});',
               f'tl.fromTo("#{sid}-v{k}",{{opacity:0}},{{opacity:1,duration:0.2}},{t + 0.45:.3f});',
               f'tl.fromTo("#{sid}-l{k}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.2}},{t:.3f});']
        if prop:
            tl.append(f'tl.fromTo("#{sid}-p{k}",{{opacity:0,y:{H}}},{{opacity:1,y:0,duration:0.6,ease:"back.out(1.4)"}},{t:.3f});')
        tl += expr(u, "staunen" if k == n - 1 else "zeigen", t + 0.1) + [leaf_to(u, -40, t + 0.15)]
        sfx(t, "whoosh" if k == n - 1 else "pop", 0.25)
        events.append(t)
        prev = t + 0.7
    st = d.get("stamp") or {}
    if st:
        _lim(problems, "zonk_compare", "stamp", st["text"])
        parts.append(f'<div class="zterm zcst" id="{sid}-st">{_e(st["text"])}</div>')
        t = max(prev, cue(c, st.get("cue"), 0.7))
        tl.append(f'tl.fromTo("#{sid}-st",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.25,ease:"back.out(2)"}},{t:.3f});')
        sfx(t, "boing", 0.3)
        events.append(t)
        prev = t + 0.5
    t_end = cue(c, d.get("cue_react"), 0.88, after=prev - 0.2)
    if d.get("fall"):
        tl += expr(u, "umgekippt", t_end) + [f'tl.to("{wrap}",{{rotation:-90,transformOrigin:"20% 92%",duration:0.42,ease:"bounce.out"}},{t_end:.3f});']
        sfx(t_end + 0.25, "plumps", 0.35)
    else:
        tl += expr(u, "verwirrt", t_end) + hop(wrap, t_end, height=40)
    events.append(t_end)
    tl += idle(wrap, c, end=t_end - 0.1) if d.get("fall") else idle(wrap, c)
    return _out(c, parts, tl, events, problems, cam=(1.0, 1.04), origin=(620, 760))


# --- 5. zonk_loop ----------------------------------------------------------------------------------

def zonk_loop(c: SceneCtx, d: dict) -> SceneOut:
    """Plümo lies where he fell, CTA chip, he gets up and hops back; the last 0.6 s equal the hook's first frame."""
    _begin(c)
    sid, u = c.sid, f"{c.sid}p"
    problems: list[str] = []
    cta = d.get("cta", "Mehr Zonkfruit? Folgen.")
    _lim(problems, "zonk_loop", "cta", cta)
    bg, tl = stage(c)
    parts = [bg, door(sid, d.get("sign", "NUR BEEREN")), f'<div class="zcta" id="{sid}-cta">{_rich(cta)}</div>', plumo(u, "neutral")]
    wrap = f"#{u}-wrap"
    t_cta = cue(c, d.get("cue_cta"), 0.35)
    t_up = cue(c, d.get("cue_up"), 0.62, after=t_cta)
    t_up = min(t_up, c.end - 2.2)
    end_still = c.end - 0.6
    tl += [f'tl.set("{wrap}",{{x:420,rotation:-90,transformOrigin:"20% 92%"}},{c.start:.3f});',
           f'tl.fromTo("#{sid}-cta",{{opacity:0,y:30,scale:0.85}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(2)"}},{t_cta:.3f});',
           f'tl.to("{wrap}",{{rotation:0,duration:0.55,ease:"elastic.out(1,0.45)"}},{t_up:.3f});']
    # lying = upright drawing in a wrapper rotated -90 deg (same as the end of zonk_scan/unknown), face set to "umgekippt"
    tl += expr(u, "umgekippt", c.start, d=0.01) + expr(u, "staunen", t_up) + hop(wrap, t_up + 0.6, x0=420, x1=210) + hop(wrap, t_up + 1.2, x0=210, x1=0)
    tl += expr(u, "neutral", t_up + 1.75)
    tl += [f'tl.to("#{sid}-cta",{{opacity:0,y:-20,duration:0.25}},{end_still - 0.3:.3f});',
           f'tl.set("{wrap}",{{x:0,y:0,rotation:0,scaleX:1,scaleY:1}},{end_still:.3f});']
    sfx(t_cta, "pop", 0.3); sfx(t_up, "boing", 0.35); sfx(t_up + 0.6, "boing", 0.2); sfx(t_up + 1.2, "boing", 0.2)
    events = [c.t(0.3), t_cta, t_up, t_up + 0.6, t_up + 1.2, end_still - 0.3]
    if d.get("cue_lie"):        # "Ich bleib dann mal liegen.": one eye opens, closes again; leaf flops
        t_l = cue(c, d.get("cue_lie"), 0.12)
        (h5, y5), (h1, y1) = lid_attrs(0.5), lid_attrs(1.0)
        tl += [f'tl.to("#{u}-lidR",{{attr:{{height:{h5}}},duration:0.1}},{t_l:.3f});',
               f'tl.to("#{u}-linR",{{attr:{{y1:{y5},y2:{y5}}},duration:0.1}},{t_l:.3f});',
               f'tl.to("#{u}-lidR",{{attr:{{height:{h1}}},duration:0.12}},{t_l + 0.7:.3f});',
               f'tl.to("#{u}-linR",{{attr:{{y1:{y1},y2:{y1}}},duration:0.12}},{t_l + 0.7:.3f});',
               leaf_to(u, 175, t_l + 0.75), leaf_to(u, 150, t_l + 1.0)]
        events.append(t_l)
    if d.get("cue_ch"):         # "Folge dem Kanal.": the CTA chip pulses
        t_k = max(t_cta + 0.4, cue(c, d.get("cue_ch"), 0.5, after=t_cta))
        tl.append(f'tl.fromTo("#{sid}-cta",{{scale:1}},{{scale:1.08,duration:0.15,yoyo:true,repeat:1,ease:"power2.out"}},{t_k:.3f});')
        sfx(t_k, "chime", 0.18)
        events.append(t_k)
    # camera pulls back from the end of zonk_scan/unknown (1.08) to the hook's first frame (1.0) before the still end
    return _out(c, parts, tl, events, problems, cam=(1.08, 1.0), origin=(860, 860), cam_end=t_up + 1.6)


ZONK_TEMPLATES = {"zonk_scan": zonk_scan, "zonk_word": zonk_word, "zonk_diagram": zonk_diagram, "zonk_zoom": zonk_zoom,
                  "zonk_compare": zonk_compare, "zonk_loop": zonk_loop}


def zonk_css(display: str, body: str) -> str:
    acc, pop, text, bg = PC["body"], PC["leaf"], "#FFF4FA", "#101010"
    REACHED, OPEN = "#3EE08F", "#FFD84D"   # fixed meanings (brand.yaml explainer.colors): mint = reached, amber = open
    dots1 = ",".join(f"radial-gradient(circle at {x}px {y}px,rgba(255,244,250,{a}) 0 {r}px,transparent {r + 1.5}px)"
                     for x, y, r, a in [(30, 40, 1.6, 0.5), (170, 110, 1.2, 0.4), (250, 230, 1.8, 0.45), (90, 260, 1.1, 0.35), (210, 20, 1.0, 0.3)])
    dots2 = ",".join(f"radial-gradient(circle at {x}px {y}px,rgba({c},{a}) 0 {r}px,transparent {r + 2.5}px)"
                     for x, y, r, c, a in [(60, 80, 3.0, "183,255,0", 0.35), (220, 190, 2.6, "255,67,192", 0.35), (140, 280, 2.2, "255,242,199", 0.4)])
    # status bar (shared #status from plan.layout.status_bar) in Zonkfruit style: the club door instead of the file icon
    door = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 38'%3E%3Cpath d='M3 38V15a12 12 0 0 1 24 0v23' "
            "fill='%23140e19' stroke='%23FF43C0' stroke-width='4'/%3E%3Ccircle cx='15' cy='5' r='4' fill='%23B7FF00'/%3E%3C/svg%3E")
    return f"""
.zs{{position:absolute;inset:0;overflow:hidden;}}
.zcam{{position:absolute;inset:0;}}
.zbg{{position:absolute;inset:0;background:linear-gradient(180deg,#120a18 0%,#2C1638 38%,#3a1a44 47%,#1a1020 62%,{bg} 100%);}}
.zkey{{position:absolute;left:-300px;top:-260px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle,rgba(255,242,199,0.16) 0%,rgba(255,242,199,0.05) 40%,transparent 68%);}}
.zneon{{position:absolute;right:-380px;top:260px;width:900px;height:1000px;border-radius:50%;background:radial-gradient(circle,rgba(255,67,192,0.22) 0%,rgba(255,67,192,0.06) 45%,transparent 70%);}}
.zplanet{{position:absolute;left:806px;top:196px;width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 34% 30%,#ffd2f0 0%,{pop} 38%,#5a1046 100%);box-shadow:0 0 40px rgba(255,67,192,0.45);}}
.zplanet i{{position:absolute;left:-22px;top:26px;width:108px;height:14px;border-radius:50%;border:3px solid rgba(183,255,0,0.75);transform:rotate(-14deg);}}
.zfar{{position:absolute;left:-80px;top:560px;width:1240px;height:420px;}}
.zfar svg{{display:block;}}
.zbeam3{{position:absolute;top:-80px;width:240px;height:1260px;transform-origin:50% 0;clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);mix-blend-mode:screen;}}
.zfloorw{{position:absolute;left:0;top:0;width:1080px;height:1920px;}}
.zfloor{{position:absolute;left:-560px;width:2200px;top:860px;height:1150px;transform:perspective(700px) rotateX(62deg);transform-origin:50% 0;
  background:linear-gradient(rgba(255,67,192,0.10),transparent 30%),repeating-conic-gradient(#3a2244 0 25%,#1c1324 0 50%) 0 0/150px 150px;
  -webkit-mask-image:linear-gradient(transparent 0%,#000 8%,#000 60%,transparent 100%);}}
.zfog{{position:absolute;left:0;right:0;top:800px;height:220px;background:linear-gradient(transparent,rgba(122,60,255,0.22) 45%,rgba(75,22,64,0.30) 60%,transparent);}}
.zpool{{position:absolute;left:150px;top:930px;width:860px;height:260px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,242,199,0.20) 0%,rgba(183,255,0,0.08) 38%,transparent 70%);mix-blend-mode:screen;}}
.zdust{{position:absolute;left:0;top:0;width:1080px;height:2900px;}}
.zd1{{background:{dots1};background-size:300px 300px;opacity:0.7;}}
.zd2{{background:{dots2};background-size:300px 300px;opacity:0.8;}}
.zorb{{position:absolute;border-radius:50%;opacity:0.9;box-shadow:0 18px 30px rgba(0,0,0,0.35);}}
.zbokeh{{position:absolute;border-radius:50%;background:radial-gradient(circle,var(--c) 0%,var(--c) 35%,transparent 70%);}}
.zvig{{position:absolute;inset:0;background:radial-gradient(ellipse 75% 62% at 50% 44%,transparent 55%,rgba(6,3,8,0.55) 100%);}}
.zhl{{color:{acc};display:inline-block;}}
.zhead{{position:absolute;left:100px;width:830px;top:288px;font-family:'FN {display}';font-weight:700;font-size:78px;line-height:1.04;color:{text};text-align:center;text-shadow:0 7px 0 #4B1640,0 14px 30px rgba(0,0,0,0.5);}}
.zh2{{position:absolute;left:100px;width:830px;top:300px;font-family:'FN {display}';font-weight:700;font-size:72px;line-height:1.05;color:{text};text-align:center;text-shadow:0 6px 0 #4B1640,0 14px 30px rgba(0,0,0,0.45);}}
.zpl{{position:absolute;transform-origin:50% 92%;}}
.zpl svg{{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;}}
.zpb{{position:absolute;inset:0;opacity:0;}}
.zsign{{position:absolute;left:{DOOR_X - 30}px;width:360px;top:470px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:42px;color:{bg};background:{acc};border-radius:16px;padding:8px 0;box-shadow:0 8px 0 #5d8a00,0 0 40px rgba(183,255,0,0.35);}}
.zdoor{{position:absolute;left:{DOOR_X}px;width:300px;top:560px;height:500px;border:16px solid #B04A92;border-bottom:none;border-radius:150px 150px 0 0;background:linear-gradient(#0b0810,#1d1324);box-shadow:inset 0 0 60px rgba(0,0,0,0.8),0 0 0 rgba(255,67,192,0);}}
.zdoor::after{{content:"";position:absolute;left:-60px;right:-60px;bottom:-34px;height:60px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,0.55),transparent 70%);}}
.zdoor-in{{position:absolute;left:30px;right:30px;top:40px;bottom:0;border-radius:120px 120px 0 0;background:repeating-linear-gradient(90deg,#140e19 0 18px,#191120 18px 36px);}}
.zlamp{{position:absolute;left:50%;top:-4px;width:40px;height:40px;margin-left:-20px;border-radius:50%;background:#3a2a36;border:5px solid #101010;}}
.zbeam{{position:absolute;left:{DOOR_X - 20}px;width:340px;top:580px;height:46px;opacity:0;border-radius:23px;background:linear-gradient(transparent,color-mix(in srgb,{acc} 70%,transparent),transparent);}}
.zitem{{position:absolute;left:{DOOR_X + 40}px;top:810px;width:220px;height:240px;}}
.zstamp{{position:absolute;left:{DOOR_X - 50}px;width:380px;top:700px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:64px;line-height:1;padding:16px 0;border-radius:20px;border:9px solid;opacity:0;}}
.zreject{{color:{pop};border-color:{pop};background:rgba(16,16,16,0.85);}}
.zaccept{{color:{REACHED};border-color:{REACHED};background:rgba(16,16,16,0.85);}}
.zcounter{{position:absolute;left:100px;top:330px;width:830px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:70px;color:{text};text-shadow:0 6px 0 #4B1640;opacity:0;}}
.zcounter .zcn{{position:relative;display:inline-block;width:54px;height:76px;color:{acc};vertical-align:top;}}
.zcn b{{position:absolute;left:0;top:0;font-weight:700;}}
.zdisplay{{position:absolute;left:{DOOR_X - 250}px;width:580px;top:350px;text-align:center;white-space:nowrap;font-family:'FN {display}';font-weight:700;font-size:40px;color:#101010;background:{OPEN};border-radius:18px;padding:14px 10px;border:5px solid #101010;opacity:0;}}
.zmerke{{position:absolute;left:100px;width:830px;top:284px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:54px;line-height:1.08;color:{text};text-shadow:0 6px 0 #4B1640;opacity:0;}}
.zmk{{display:block;margin:0 auto 10px;width:200px;font-size:32px;color:#101010;background:{pop};border-radius:999px;padding:4px 0;text-shadow:none;}}
.zplumps{{position:absolute;left:180px;top:760px;font-family:'FN {display}';font-weight:700;font-size:96px;color:{pop};text-shadow:0 7px 0 #4B1640;opacity:0;}}
.zword{{position:absolute;left:60px;width:870px;top:400px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:160px;line-height:1;color:{text};text-shadow:0 10px 0 #4B1640,0 24px 40px rgba(0,0,0,0.5);opacity:0;}}
.zwb{{position:relative;display:inline-block;color:{pop};}}
.zstrike{{position:absolute;left:-10px;right:-10px;top:52%;height:18px;background:{acc};border-radius:9px;transform-origin:left center;transform:scaleX(0) rotate(-4deg);}}
.zchip{{position:absolute;left:420px;width:500px;box-sizing:border-box;font-family:'FN {display}';font-weight:700;font-size:40px;line-height:1.1;border-radius:22px;padding:18px 24px;opacity:0;box-shadow:0 7px 0 #4B1640;}}
.zchip-c{{top:660px;background:{PC['sticker']};color:#101010;}}
.zchip-m{{top:800px;background:{pop};color:#101010;}}
.zchip-m .zhl,.zchip-c .zhl{{color:#101010;text-decoration:underline;}}
.zwitem{{position:absolute;left:700px;top:925px;width:190px;}}
.zxs{{position:absolute;left:230px;top:420px;filter:drop-shadow(0 22px 30px rgba(0,0,0,0.5));}}
.zlabel{{position:absolute;max-width:470px;font-family:'FN {display}';font-weight:700;font-size:42px;line-height:1.1;color:#101010;background:{text};border-radius:20px;padding:14px 22px;box-shadow:0 7px 0 #4B1640,0 16px 30px rgba(0,0,0,0.35);opacity:0;}}
.zlabel .zhl{{color:#7A1F5E;}}
.zbig{{position:absolute;left:160px;top:400px;width:580px;filter:drop-shadow(0 26px 30px rgba(0,0,0,0.5));}}
.zmag{{position:absolute;left:550px;top:390px;width:350px;height:350px;}}
.zmag-in{{position:absolute;inset:0;border-radius:50%;overflow:hidden;border:16px solid {text};box-shadow:0 14px 40px rgba(0,0,0,0.6);background:#E5163F;}}
.zmag-in svg{{position:absolute;left:0;top:0;}}
.zmag-h{{position:absolute;left:265px;top:275px;width:46px;height:170px;border-radius:23px;background:#B04A92;transform:rotate(-40deg);transform-origin:50% 0;}}
.zterm{{position:absolute;left:110px;width:620px;top:800px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:62px;color:#101010;background:{acc};border-radius:24px;padding:16px 0;box-shadow:0 9px 0 #5d8a00;opacity:0;}}
.zcta{{position:absolute;left:120px;width:790px;box-sizing:border-box;top:300px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:64px;line-height:1.08;color:#101010;background:{acc};border-radius:28px;padding:22px 20px;box-shadow:0 9px 0 #5d8a00;opacity:0;}}
.zcta .zhl{{color:#7A1F5E;}}
.zbar{{position:absolute;border-radius:22px 22px 6px 6px;box-shadow:0 9px 0 #4B1640,0 20px 40px rgba(0,0,0,0.4);display:flex;align-items:flex-start;justify-content:center;overflow:hidden;}}
.zbv{{margin-top:14px;font-family:'FN {display}';font-weight:700;font-size:38px;line-height:1.05;color:#101010;background:{text};border-radius:14px;padding:6px 12px;text-align:center;opacity:0;}}
.zcp{{position:absolute;filter:drop-shadow(0 12px 16px rgba(0,0,0,0.45));}}
.zbl{{position:absolute;text-align:center;font-family:'FN {display}';font-weight:700;font-size:32px;line-height:1.05;color:{text};text-shadow:0 4px 0 #4B1640;opacity:0;}}
.zcst{{top:462px;left:200px;width:600px;}}
html body #status{{background:linear-gradient(180deg,rgba(58,28,70,0.94),rgba(28,14,36,0.94));border:3px solid rgba(183,255,0,0.6);border-radius:42px;
  box-shadow:0 7px 0 #4B1640,0 18px 40px rgba(0,0,0,0.45);font-family:'FN {display}';font-weight:600;font-size:32px;}}
html body #status .st-file{{font-family:'FN {display}';font-weight:700;color:{text};}}
html body #status .st-icon{{display:inline-block;width:30px;height:38px;font-size:0;background:url("{door}") center/contain no-repeat;}}
html body #status .st{{font-weight:700;}}
.st-pop{{color:{pop};}}
.st-lime{{color:{acc};}}
.st-mint{{color:{REACHED};}}
"""
