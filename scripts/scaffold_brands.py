"""Generate the per-brand design system folders from config/brands.yaml.

Run:  .venv\\Scripts\\python.exe scripts\\scaffold_brands.py [--force]

Writes brands/<id>/{brand.yaml, visual_style.md, script_prompt.md, image_prompt.md,
subtitle_style.json, intro_config.json, outro_config.json, audio_style.yaml}.
Existing files are kept unless --force is given, so hand edits survive.
Style decisions below are Claude's proposals (2026-10-30) for Stefan to review.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BRANDS_YAML = ROOT / "config" / "brands.yaml"
OUT = ROOT / "brands"

# Fonts available under assets/fonts (all SIL Open Font License, licence file next to each font).
FONTS = {
    "Inter": "assets/fonts/inter/Inter[opsz,wght].ttf",
    "Montserrat": "assets/fonts/montserrat/Montserrat[wght].ttf",
    "JetBrains Mono": "assets/fonts/jetbrainsmono/JetBrainsMono[wght].ttf",
    "Playfair Display": "assets/fonts/playfairdisplay/PlayfairDisplay[wght].ttf",
    "Oswald": "assets/fonts/oswald/Oswald[wght].ttf",
}

# Per-brand style proposals. Keys are brand ids from config/brands.yaml.
STYLES: dict[str, dict] = {
    "claude_workflows": dict(
        display="Inter", display_weight=800, body="Inter", mono="JetBrains Mono",
        motif="code-window", tempo="snappy", bg_pattern="dot-grid",
        subtitle=dict(font="Inter", weight=700, size=64, transform="none", group_words=3, style="highlight-word"),
        intro=dict(kind="typing-cursor", seconds=1.6),
        cta=dict(de="Folgen für den nächsten Workflow", en="Follow for the next workflow"),
        voices=dict(de="Kore", en="Puck"), speaking_rate=1.05,
        music="minimal electronic, soft keys, 90-100 bpm, no vocals",
        visual_words="clean SaaS interface, dark slate background, violet accent glow, rounded code panels, monospaced snippets, soft shadows, lots of air",
        hook_styles=["a concrete result in one sentence", "a mistake everyone makes with Claude", "before/after of a prompt"],
        audience="people who use Claude or Claude Code for real work and want workflows that provably work",
        tone="precise, friendly, zero hype; show the steps, name the Claude version",
        forbidden="no invented features, no screenshots with private data, no promises about model behaviour that was not tested",
    ),
    "ai_security": dict(
        display="Montserrat", display_weight=800, body="Inter", mono="JetBrains Mono",
        motif="shield-lines", tempo="medium", bg_pattern="hex-grid",
        subtitle=dict(font="Montserrat", weight=700, size=58, transform="uppercase", group_words=3, style="highlight-word"),
        intro=dict(kind="line-draw-shield", seconds=1.8),
        cta=dict(de="Mehr Schutz für kleine Betriebe: folgen", en="More protection for small businesses: follow"),
        voices=dict(de="Charon", en="Charon"), speaking_rate=1.0,
        music="calm cinematic pulse, low synth, 80 bpm, no vocals",
        visual_words="editorial tech look, deep navy, thin cyan lines, faint hexagonal grid, shield outline, data-card panels, no stock hacker imagery",
        hook_styles=["a plain-language risk a small business actually has", "a checklist item most owners skip", "what a real policy or standard says"],
        audience="owners and office staff of small businesses in DACH and the English-speaking world who use AI tools without a security team",
        tone="calm, concrete, no fear-mongering; always end with one thing to do today",
        forbidden="no exploit steps, no invented incidents or statistics, no naming of victims, Scutoria products only with paid-partnership flags",
    ),
    "engines": dict(
        display="Oswald", display_weight=600, body="Inter", mono="JetBrains Mono",
        motif="blueprint", tempo="precise", bg_pattern="blueprint-grid",
        subtitle=dict(font="Oswald", weight=600, size=62, transform="uppercase", group_words=3, style="highlight-word"),
        intro=dict(kind="gear-ring", seconds=1.8),
        cta=dict(de="Nächster Motor: folgen", en="Next engine: follow"),
        voices=dict(de="Fenrir", en="Orus"), speaking_rate=1.0,
        music="industrial ambient, low drone with mechanical ticks, 95 bpm",
        visual_words="precision engineering, dark graphite background, silver accents, blue technical text, blueprint grid, exploded-view diagrams, measurement ticks and dimension lines",
        hook_styles=["a number that sounds wrong but is right (with source)", "why a design choice exists", "what happens inside the engine in one second"],
        audience="car and motorcycle enthusiasts who want to understand how engines work, not buy parts",
        tone="exact, sober, engineering language explained; every number has a source",
        forbidden="no maintenance advice that can damage an engine, no tuning instructions, no brand bashing",
    ),
    "megaconstruction": dict(
        display="Oswald", display_weight=700, body="Inter", mono=None,
        motif="scale-bars", tempo="epic", bg_pattern="isometric-blocks",
        subtitle=dict(font="Oswald", weight=700, size=66, transform="uppercase", group_words=2, style="highlight-word"),
        intro=dict(kind="crane-build", seconds=2.0),
        cta=dict(de="Nächstes Bauwerk: folgen", en="Next megastructure: follow"),
        voices=dict(de="Charon", en="Fenrir"), speaking_rate=0.98,
        music="epic orchestral hybrid, slow build, 70 bpm",
        visual_words="engineering epic, dark steel blue, construction orange stripes, isometric blocks, scale comparison silhouettes, large numerals",
        hook_styles=["a scale comparison computed from sources", "a construction problem and how it was solved", "a date and what it took"],
        audience="viewers fascinated by huge structures and the engineering behind them",
        tone="awe without exaggeration; scale comparisons are computed, never guessed",
        forbidden="no estimated dimensions, no unsourced costs, no claims about ongoing projects without a dated primary source",
    ),
    "menswear": dict(
        display="Playfair Display", display_weight=600, body="Inter", mono=None,
        motif="gold-hairlines", tempo="slow", bg_pattern="fabric-gradient",
        subtitle=dict(font="Inter", weight=500, size=56, transform="none", group_words=4, style="italic-emphasis"),
        intro=dict(kind="monogram-line", seconds=2.0),
        cta=dict(de="Für den nächsten Stilhinweis folgen", en="Follow for the next style note"),
        voices=dict(de="Orus", en="Algenib"), speaking_rate=0.95,
        music="quiet jazz piano or soft strings, 60-70 bpm",
        visual_words="quiet luxury, midnight navy, champagne gold hairlines, fabric texture gradients, serif headlines, generous whitespace, product shown as a silhouette or abstract swatch",
        hook_styles=["one rule and the exception", "what a detail says about a suit", "a mistake that is easy to fix"],
        audience="men who want to dress well without following trends; international and DACH",
        tone="composed, knowledgeable, never snobbish; short sentences",
        forbidden="no affiliate link without product knowledge and disclosure, no body shaming, no brand ranking without criteria",
    ),
    "motivation": dict(
        display="Montserrat", display_weight=900, body="Inter", mono=None,
        motif="film-grain", tempo="punchy", bg_pattern="vignette",
        subtitle=dict(font="Montserrat", weight=800, size=70, transform="uppercase", group_words=2, style="word-by-word"),
        intro=dict(kind="flash-cut", seconds=1.2),
        cta=dict(de="Jeden Tag ein Schritt: folgen", en="One step every day: follow"),
        voices=dict(de="Fenrir", en="Enceladus"), speaking_rate=1.0,
        music="cinematic piano and low strings, 75 bpm, builds to the last line",
        visual_words="cinematic human, near-black background, warm gold light, film grain, vignette, single bold line of text, silhouettes rather than faces",
        hook_styles=["a named method and where it comes from", "a question the viewer cannot answer quickly", "a small action for today"],
        audience="people who want practical self-development, not slogans",
        tone="warm, direct, grounded; methods are attributed to their sources",
        forbidden="no psychological or medical claims, no guru quotes without source, no promises of outcomes",
    ),
    "military_history": dict(
        display="Oswald", display_weight=500, body="Inter", mono="JetBrains Mono",
        motif="archive-stamp", tempo="measured", bg_pattern="map-contours",
        subtitle=dict(font="Inter", weight=600, size=58, transform="none", group_words=4, style="highlight-word"),
        intro=dict(kind="archive-stamp", seconds=2.0),
        cta=dict(de="Nächstes Kapitel: folgen", en="Next chapter: follow"),
        voices=dict(de="Charon", en="Charon"), speaking_rate=0.97,
        music="restrained documentary score, sparse percussion, 65 bpm",
        visual_words="documentary tech, olive green, paper grain, contour map lines, archive labels with dates in monospace, stylized diagrams, never photorealistic battle scenes",
        hook_styles=["a documented technical decision and its consequence", "a date and a number from an archive", "why a design looked the way it did"],
        audience="history and technology viewers; strictly historical and publicly documented",
        tone="measured, factual, respectful; no glorification",
        forbidden="no tactics, no weapon handling or construction, no current conflicts, nothing from Stefan's service, no uniform, no graphic violence; realistic AI scenes of real events need the Art. 50 disclosure at the start, so prefer stylized visuals",
    ),
    "beauty": dict(
        display="Playfair Display", display_weight=500, body="Inter", mono=None,
        motif="soft-bloom", tempo="gentle", bg_pattern="petal-gradient",
        subtitle=dict(font="Inter", weight=500, size=56, transform="none", group_words=4, style="highlight-word"),
        intro=dict(kind="soft-bloom", seconds=1.8),
        cta=dict(de="Mehr Wissen zu Inhaltsstoffen: folgen", en="More ingredient knowledge: follow"),
        voices=dict(de="Leda", en="Aoede"), speaking_rate=0.97,
        music="light acoustic, soft pads, 80 bpm",
        visual_words="luxury editorial, warm ivory background, dusty rose accents, mauve text, soft gradients, petal shapes, serif italics, abstract ingredient illustrations, no faces, no before/after",
        hook_styles=["what an ingredient actually does (with source)", "how to read a label", "a routine myth and what the evidence says"],
        audience="people who want to understand skincare ingredients and routines without being sold to",
        tone="knowledgeable, gentle, honest about uncertainty",
        forbidden="no efficacy claims, no before/after, no fake tests, no medical advice, no paid content before a media kit exists",
    ),
    "brainrot": dict(
        display="Montserrat", display_weight=900, body="Montserrat", mono=None,
        motif="neon-wobble", tempo="chaotic", bg_pattern="checkerboard",
        subtitle=dict(font="Montserrat", weight=900, size=74, transform="uppercase", group_words=2, style="pop-rotate"),
        intro=dict(kind="character-bounce", seconds=1.2),
        cta=dict(de="Mehr Zonk: folgen", en="More Zonk: follow"),
        voices=dict(de="Puck", en="Zephyr"), speaking_rate=1.12,
        music="licensed hyperpop or chiptune, 140-160 bpm; licence proof required before use",
        visual_words="surreal 3D comedy, black background, acid lime accents, hot pink text, wobbling shapes, checkerboard floors, neon outlines, glitch cuts, the original Zonkfruit character (character sheet pending)",
        hook_styles=["the character in an impossible situation", "a deadpan rule of the Zonk world", "a visual gag in the first frame"],
        audience="viewers who like absurd, fast, harmless comedy",
        tone="deadpan absurd, fast, never mean",
        forbidden="no copied characters or memes with rights holders, no licensed music without proof, no shock content",
    ),
}

AI_LABEL = {"de": "KI-generiert", "en": "AI-generated"}


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def luminance(h: str) -> float:
    r, g, b = (c / 255 for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mix(a: str, b: str, t: float) -> str:
    ra, ga, ba = hex_to_rgb(a)
    rb, gb, bb = hex_to_rgb(b)
    return "#%02X%02X%02X" % (round(ra + (rb - ra) * t), round(ga + (gb - ga) * t), round(ba + (bb - ba) * t))


def write(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def build_brand(brand: dict, defaults: dict, force: bool) -> list[str]:
    bid = brand["id"]
    st = STYLES[bid]
    pal = brand["palette"]
    dark = luminance(pal["bg"]) < 0.5
    surface = mix(pal["bg"], "#FFFFFF" if dark else "#000000", 0.07)
    muted = mix(pal["text"], pal["bg"], 0.45)
    out = OUT / bid
    written = []

    brand_yaml = {
        "id": bid,
        "name": brand["name"],
        "niche": brand["niche"],
        "style": brand["style"],
        "phase": brand["phase"],
        "enabled": brand["enabled"],
        "languages": defaults["languages"],
        "primary_language": defaults["primary_language"],
        "risk_default": brand["risk_default"],
        "rules": brand["rules"],
        "palette": {
            "bg": pal["bg"], "accent": pal["accent"], "text": pal["text"],
            "surface": surface, "muted": muted, "scheme": "dark" if dark else "light",
        },
        "fonts": {
            "display": {"family": st["display"], "weight": st["display_weight"], "file": FONTS[st["display"]], "license": "OFL-1.1"},
            "body": {"family": st["body"], "weight": 400, "file": FONTS[st["body"]], "license": "OFL-1.1"},
            "mono": ({"family": st["mono"], "weight": 500, "file": FONTS[st["mono"]], "license": "OFL-1.1"} if st["mono"] else None),
        },
        "motif": st["motif"],
        "tempo": st["tempo"],
        "bg_pattern": st["bg_pattern"],
        "layout": "shared 9:16 layout, see docs/design-system.md",
        "audience": st["audience"],
        "tone": st["tone"],
        "ai_label": AI_LABEL,
    }
    if write(out / "brand.yaml", yaml.safe_dump(brand_yaml, sort_keys=False, allow_unicode=True), force):
        written.append("brand.yaml")

    mono_line = (f"- Mono: **{st['mono']}** (code, dates, measurements)." if st["mono"] else "- No monospace face.")
    visual = f"""# {brand['name']} - Visual style ({brand['style']})

Proposal by Claude, 2026-10-30. Shared 9:16 layout (1080 x 1920) from `docs/design-system.md`; this file holds only what is brand-specific.

## Look in one line

{st['visual_words']}.

## Palette

| Role | Hex | Use |
|---|---|---|
| bg | `{pal['bg']}` | full-frame background |
| surface | `{surface}` | cards, code panels, caption scrim |
| accent | `{pal['accent']}` | highlight word in captions, progress bar, logo mark, lines |
| text | `{pal['text']}` | headlines and body |
| muted | `{muted}` | counters, dates, secondary labels |

Scheme: {'dark' if dark else 'light'}. Contrast of text on bg must stay above 4.5:1 (checked by `npx hyperframes check`).

## Type

- Display: **{st['display']}** {st['display_weight']} (headlines, hook card, outro).
- Body: **{st['body']}** 400-600 (facts, labels).
{mono_line}
- All fonts under SIL OFL 1.1, files and licences in `assets/fonts/`.

## Motion

Tempo: **{st['tempo']}**. Motif: **{st['motif']}**. Background pattern: **{st['bg_pattern']}**.

- Intro: {st['intro']['kind']} ({st['intro']['seconds']} s), wordmark lands top-left.
- Scenes: one idea per scene, 6-12 s each, hard cuts or 0.25 s crossfades, no transition zoo.
- Captions: {st['subtitle']['font']} {st['subtitle']['weight']}, {st['subtitle']['transform']}, {st['subtitle']['group_words']} words per group, style `{st['subtitle']['style']}`.
- Outro: logo centered, CTA, AI label, 4 s.

## Imagery

{st['visual_words']}. Generated images follow `image_prompt.md`; placeholders in Phase 1 are shapes and gradients in the palette.

## Never

{st['forbidden']}.
"""
    if write(out / "visual_style.md", visual, force):
        written.append("visual_style.md")

    rules_md = "\n".join(f"- {r}" for r in brand["rules"])
    hooks_md = "\n".join("- " + h for h in st["hook_styles"])
    script_prompt = f"""# {brand['name']} - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: {brand['name']} (`{bid}`), niche: {brand['niche']}.
- Audience: {st['audience']}.
- Tone: {st['tone']}.
- Default risk level: {brand['risk_default']}.

## Brand rules (binding)

{rules_md}
- {st['forbidden']}.

## Hook styles that fit this brand

{hooks_md}

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
"""
    if write(out / "script_prompt.md", script_prompt, force):
        written.append("script_prompt.md")

    image_prompt = f"""# {brand['name']} - Image prompt template

For AI-generated stills (Phase 2+) and for the placeholder generator (Phase 1). Every generated image is logged in the manifest with model, prompt and licence.

## Base prompt (English, prepend to every scene prompt)

```
{st['visual_words']}. Vertical 9:16 composition, subject centered in the upper two thirds, lower third kept calm for captions. Colours: background {pal['bg']}, accent {pal['accent']}, text {pal['text']}. No text, no logos, no watermarks, no faces of real people.
```

## Negative prompt

```
text, watermark, logo, real person, celebrity, uniform, blood, weapon handling, low quality, blurry, stock photo look
```

## Scene prompt pattern

`<what is shown>, <camera or diagram type>, <mood word from tone>` - one subject per image, no collages.

## Rules

- No realistic depictions of real people, places or events (EU AI Act Art. 50 disclosure would otherwise be required). Prefer stylized, diagrammatic or abstract imagery.
- {st['forbidden']}.
"""
    if write(out / "image_prompt.md", image_prompt, force):
        written.append("image_prompt.md")

    sub = st["subtitle"]
    subtitle_style = {
        "font_family": sub["font"],
        "font_weight": sub["weight"],
        "font_size_px": sub["size"],
        "min_font_size_px": 42,
        "text_transform": sub["transform"],
        "group_words": sub["group_words"],
        "style": sub["style"],
        "color": pal["text"],
        "highlight_color": pal["accent"],
        "scrim": {"color": surface, "opacity": 0.0 if dark else 0.85, "padding_px": 18, "radius_px": 16},
        "position": {"anchor": "bottom", "bottom_px": 640, "max_width_px": 900, "align": "center"},
        "line_height": 1.15,
        "letter_spacing_em": 0.01 if sub["transform"] == "uppercase" else 0.0,
        "shadow": "0 4px 24px rgba(0,0,0,0.45)" if dark else "none",
        "enter": {"kind": "fade-up", "seconds": 0.12},
        "exit": {"kind": "fade", "seconds": 0.12},
    }
    if write(out / "subtitle_style.json", json.dumps(subtitle_style, indent=2, ensure_ascii=False) + "\n", force):
        written.append("subtitle_style.json")

    intro_config = {
        "kind": st["intro"]["kind"],
        "seconds": st["intro"]["seconds"],
        "wordmark": brand["name"],
        "wordmark_font": st["display"],
        "wordmark_weight": st["display_weight"],
        "logo_file": None,
        "logo_position": {"x": 72, "y": 120, "height": 56},
        "show_counter": True,
        "art50_disclosure": {
            "enabled": bid == "military_history",
            "seconds": 2.5,
            "text": {"de": "Hinweis: Szenen in diesem Video sind KI-generiert.", "en": "Notice: scenes in this video are AI-generated."},
        },
    }
    if write(out / "intro_config.json", json.dumps(intro_config, indent=2, ensure_ascii=False) + "\n", force):
        written.append("intro_config.json")

    outro_config = {
        "seconds": 4.0,
        "cta": st["cta"],
        "wordmark": brand["name"],
        "handle": None,
        "ai_label": AI_LABEL,
        "ai_label_always_visible": True,
        "ai_label_position": {"anchor": "bottom", "bottom_px": 150, "font_size_px": 26},
    }
    if write(out / "outro_config.json", json.dumps(outro_config, indent=2, ensure_ascii=False) + "\n", force):
        written.append("outro_config.json")

    audio_style = {
        "tts": {
            "provider": "gemini",
            "model": "gemini-2.5-flash-preview-tts",
            "voices": st["voices"],
            "speaking_rate": st["speaking_rate"],
            "style_instruction": {
                "de": f"Sprich ruhig und klar auf Deutsch, {st['tone'].split(';')[0]}.",
                "en": f"Speak clearly in English, {st['tone'].split(';')[0]}.",
            },
        },
        "music": {"mood": st["music"], "file": None, "license_proof": None, "gain_db": -18, "duck_db": -10},
        "loudness": {"target_lufs": -16, "true_peak_dbtp": -1.5},
        "sfx": {"enabled": False},
    }
    if write(out / "audio_style.yaml", yaml.safe_dump(audio_style, sort_keys=False, allow_unicode=True), force):
        written.append("audio_style.yaml")

    (out / "assets").mkdir(exist_ok=True)
    (out / "references").mkdir(exist_ok=True)
    return written


def main() -> int:
    force = "--force" in sys.argv
    cfg = yaml.safe_load(BRANDS_YAML.read_text(encoding="utf-8"))
    for brand in cfg["brands"]:
        written = build_brand(brand, cfg["defaults"], force)
        print(f"{brand['id']:18s} {brand['name']:12s} wrote {len(written)} files" + (f": {', '.join(written)}" if written else " (all present)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
