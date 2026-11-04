"""One-off patch (2026-10-30): switch director/templates to brand tokens (Scutoria). Kept for traceability; safe to delete."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path, pairs):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        assert old in s, f"{path}: anchor not found: {old[:80]!r}"
        s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8", newline="\n")
    print("patched", path)


# ---------------- templates.py ----------------
patch("src/fn/render/templates.py", [
    ("    enter: float = 0.25\n    lang: str = \"de\"\n",
     "    enter: float = 0.25\n    lang: str = \"de\"\n    flat: bool = False          # brand rule: no glow, no gradients, calm camera, one-time motion\n"),
    ("def _camera(c: SceneCtx, *, scale_to: float = 1.05, y_to: int = -12) -> str:\n    return",
     "def _camera(c: SceneCtx, *, scale_to: float = 1.05, y_to: int = -12) -> str:\n    if c.flat:\n        scale_to, y_to = min(scale_to, 1.02), max(y_to, -6)\n    return"),
    ("        out.tl.append(f'tl.fromTo(\"#{s} .glow\",{{opacity:0.25,scale:0.9}},{{opacity:0.55,scale:1.12,duration:{c.duration:.2f},ease:\"sine.inOut\"}},{c.start:.3f});')\n        out.tl.append(f'tl.fromTo(\"#{s} .chat\",{{y:40,opacity:0}}",
     "        if not c.flat:\n            out.tl.append(f'tl.fromTo(\"#{s} .glow\",{{opacity:0.25,scale:0.9}},{{opacity:0.55,scale:1.12,duration:{c.duration:.2f},ease:\"sine.inOut\"}},{c.start:.3f});')\n        out.tl.append(f'tl.fromTo(\"#{s} .chat\",{{y:40,opacity:0}}"),
    ("    out.tl.append(f'tl.fromTo(\"#{s} .glow\",{{opacity:0.25,scale:0.9}},{{opacity:0.6,scale:1.15,duration:{c.duration:.2f},ease:\"sine.inOut\"}},{c.start:.3f});')",
     "    if not c.flat:\n        out.tl.append(f'tl.fromTo(\"#{s} .glow\",{{opacity:0.25,scale:0.9}},{{opacity:0.6,scale:1.15,duration:{c.duration:.2f},ease:\"sine.inOut\"}},{c.start:.3f});')"),
    ("    out.tl.append(f'tl.to(\"#{s} .badge\",{{scale:1.08,duration:0.5,ease:\"sine.inOut\"}},{t(q_at + 0.55):.3f});')",
     "    if not c.flat:\n        out.tl.append(f'tl.to(\"#{s} .badge\",{{scale:1.08,duration:0.5,ease:\"sine.inOut\"}},{t(q_at + 0.55):.3f});')"),
    ("        out.tl.append(f'tl.fromTo(\"#{s}-n{idx}\",{{boxShadow:\"0 0 0px rgba(0,212,255,0)\"}},{{boxShadow:\"0 0 46px rgba(0,212,255,0.55)\",duration:0.4}},{t(hl_at):.3f});')",
     "        if c.flat:\n            out.tl.append(f'tl.to(\"#{s}-n{idx}\",{{borderColor:\"{c.pal[\"accent\"]}\",duration:0.4}},{t(hl_at):.3f});')\n        else:\n            out.tl.append(f'tl.fromTo(\"#{s}-n{idx}\",{{boxShadow:\"0 0 0px rgba(0,212,255,0)\"}},{{boxShadow:\"0 0 46px rgba(0,212,255,0.55)\",duration:0.4}},{t(hl_at):.3f});')"),
    ("                mark = \"&#10003;\" if ok is True else (\"&#10007;\" if ok is False else (\"?\" if ok == \"open\" else \"&#8226;\"))\n                cls = \"ok\" if ok is True else (\"bad\" if ok is False else (\"open\" if ok == \"open\" else \"neutral\"))",
     "                cls = \"ok\" if ok is True else (\"bad\" if ok is False else (\"open\" if ok == \"open\" else \"neutral\"))\n                if c.flat:   # brand markers: Fakt = filled square, Unsicher = half circle, Luecke = dashed circle, Geregelt = green square\n                    mark = {\"ok\": '<i class=\"mk mk-ok\"></i>', \"bad\": '<i class=\"mk mk-gap\"></i>', \"open\": '<i class=\"mk mk-unc\"></i>', \"neutral\": '<i class=\"mk mk-fact\"></i>'}[cls]\n                else:\n                    mark = \"&#10003;\" if ok is True else (\"&#10007;\" if ok is False else (\"?\" if ok == \"open\" else \"&#8226;\"))"),
    ("        if open_rows:\n            pulse_at",
     "        if open_rows and not c.flat:\n            pulse_at"),
    ("def scene_css(pal: dict, display: str, display_w: int, body: str, mono: str, zone_top: int, zone_h: int) -> str:\n    \"\"\"CSS for all five templates (one shared identity, five distinguishable layouts).\"\"\"\n    acc, text, surf, muted, bg = pal[\"accent\"], pal[\"text\"], pal[\"surface\"], pal[\"muted\"], pal[\"bg\"]",
     "def scene_css(pal: dict, display: str, display_w: int, body: str, mono: str, zone_top: int, zone_h: int, flat: bool = False) -> str:\n    \"\"\"CSS for all five templates (one shared identity, five distinguishable layouts).\"\"\"\n    acc, text, surf, muted, bg = pal[\"accent\"], pal[\"text\"], pal[\"surface\"], pal[\"muted\"], pal[\"bg\"]\n    amber, on_amber, red = pal.get(\"signal_amber\", \"#F5B342\"), pal.get(\"on_signal\", \"#1a1200\"), pal.get(\"signal_red\", \"#FF6B6B\")\n    hair = pal.get(\"hairline\", f\"color-mix(in srgb,{acc} 35%,transparent)\")\n    card_border = hair if flat else f\"color-mix(in srgb,{acc} 35%,transparent)\"\n    rad = 20 if flat else 26\n    paper, paper_ink = pal.get(\"paper\", text), pal.get(\"paper_ink\", bg)\n    shadow_card = \"0 1px 2px rgba(0,0,0,0.3), 0 20px 50px rgba(0,0,0,0.35)\" if flat else \"0 40px 90px rgba(0,0,0,0.45)\"\n    shadow_paper = \"0 1px 1px rgba(0,0,0,0.22), 0 6px 14px rgba(0,0,0,0.24), 0 24px 48px rgba(0,0,0,0.36)\" if flat else \"0 30px 70px rgba(0,0,0,0.5)\"\n    glow_css = \"display:none;\" if flat else \"\"\n    tshadow = \"none\" if flat else \"0 10px 40px rgba(0,0,0,0.5)\"\n    green = pal.get(\"signal_green\", \"#2ec4b6\")"),
])
p = ROOT / "src/fn/render/templates.py"
s = p.read_text(encoding="utf-8")
i = s.index("def scene_css(")
head, body = s[:i], s[i:]
body = body.replace("#F5B342", "{amber}").replace("#1a1200", "{on_amber}").replace("#FF6B6B", "{red}")
body = body.replace("box-shadow:0 0 30px rgba(245,179,66,0.6);", "{'' if flat else 'box-shadow:0 0 30px rgba(245,179,66,0.6);'}")
body = body.replace("box-shadow:0 0 30px {acc};", "{'' if flat else 'box-shadow:0 0 30px ' + acc + ';'}")
body = body.replace(".card.right{{border-color:{acc};box-shadow:0 0 50px color-mix(in srgb,{acc} 25%,transparent);}}",
                    ".card.right{{border-color:{acc};{'' if flat else 'box-shadow:0 0 50px color-mix(in srgb,' + acc + ' 25%,transparent);'}}}")
body = body.replace(".glow{{position:absolute;", ".glow{{{glow_css}position:absolute;")
body = body.replace("text-shadow:0 10px 40px rgba(0,0,0,0.5);}}", "text-shadow:{tshadow};}}")
body = body.replace("text-shadow:0 10px 40px rgba(0,0,0,0.6);}}", "text-shadow:{tshadow};}}")
body = body.replace(".chat{{position:absolute;left:52px;top:80px;width:760px;height:560px;background:{surf};border:2px solid color-mix(in srgb,{acc} 40%,transparent);border-radius:30px;box-shadow:0 40px 90px rgba(0,0,0,0.45);",
                    ".chat{{position:absolute;left:52px;top:80px;width:760px;height:560px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;box-shadow:{shadow_card};")
body = body.replace(".doc{{position:absolute;left:300px;top:150px;width:260px;height:300px;background:{text};color:{bg};border-radius:18px;",
                    ".doc{{position:absolute;left:300px;top:150px;width:260px;height:300px;background:{paper};color:{paper_ink};border-radius:{4 if flat else 18}px;")
body = body.replace("box-shadow:0 30px 70px rgba(0,0,0,0.5);}}\n.doc-icon{{font-size:96px;line-height:1;color:{bg};}}\n.doc-label{{font-family:'FN {mono}';font-size:30px;color:{bg};}}",
                    "box-shadow:{shadow_paper};}}\n.doc-icon{{font-size:96px;line-height:1;color:{paper_ink};}}\n.doc-label{{font-family:'FN {mono}';font-size:30px;color:{paper_ink};}}")
body = body.replace(".node{{position:absolute;left:92px;width:680px;height:140px;background:{surf};border:2px solid color-mix(in srgb,{acc} 35%,transparent);border-radius:26px;",
                    ".node{{position:absolute;left:92px;width:680px;height:140px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;")
body = body.replace(".frame{{position:relative;flex:0 0 auto;background:{surf};border-radius:28px;border:2px solid color-mix(in srgb,{acc} 35%,transparent);box-shadow:0 40px 90px rgba(0,0,0,0.5);",
                    ".frame{{position:relative;flex:0 0 auto;background:{surf};border-radius:{rad}px;border:2px solid {card_border};box-shadow:{shadow_card};")
body = body.replace(".card{{background:{surf};border-radius:28px;border:2px solid color-mix(in srgb,{acc} 30%,transparent);",
                    ".card{{background:{surf};border-radius:{rad}px;border:2px solid {card_border};")
body = body.replace(".kcard{{display:flex;align-items:center;gap:30px;background:{surf};border-radius:28px;border:2px solid color-mix(in srgb,{acc} 30%,transparent);",
                    ".kcard{{display:flex;align-items:center;gap:30px;background:{surf};border-radius:{rad}px;border:2px solid {card_border};")
body = body.replace(".knum.q{{background:{amber};color:{on_amber};}}",
                    ".knum.q{{background:{amber};color:{on_amber};}}\n"
                    ".mk{{display:inline-block;width:22px;height:22px;vertical-align:middle;}}\n"
                    ".mk-fact{{background:{acc};border-radius:2px;}}\n"
                    ".mk-ok{{background:{green};border-radius:2px;}}\n"
                    ".mk-unc{{border:3px solid {amber};border-radius:50%;background:linear-gradient(90deg,{amber} 50%,transparent 50%);}}\n"
                    ".mk-gap{{border:3px dashed {red};border-radius:50%;}}\n"
                    ".crow .cmark .mk{{margin-top:12px;}}")
p.write_text(head + body, encoding="utf-8", newline="\n")
print("templates css patched")

# ---------------- templates_file.py ----------------
patch("src/fn/render/templates_file.py", [
    ("def _file_card(label: str, cls: str = \"\") -> str:\n    return (f'<div class=\"fcard {cls}\"><div class=\"fcard-icon\">&#9638;</div><div class=\"fcard-label\">{_e(label)}</div>'\n            f'<div class=\"fcard-q\">?</div></div>')",
     "def _qmark(c, cls: str) -> str:\n    \"\"\"Open-question marker: brand chip (half circle + word) when flat, amber question badge otherwise.\"\"\"\n    if c is not None and c.flat:\n        word = \"Unsicher\" if c.lang == \"de\" else \"Open\"\n        return f'<span class=\"qchip {cls}\"><i class=\"mk mk-unc\"></i>{word}</span>'\n    return f'<div class=\"{cls}\">?</div>'\n\n\ndef _file_card(label: str, cls: str = \"\", c=None) -> str:\n    return (f'<div class=\"fcard {cls}\"><div class=\"fcard-icon\">&#9638;</div><div class=\"fcard-label\">{_e(label)}</div>{_qmark(c, \"fcard-q\")}</div>')"),
    ("        f'<div class=\"route-sub\">{_e(r.get(\"sub\", \"\"))}</div><div class=\"route-q\">?</div></div>' for i, r in enumerate(routes))",
     "        f'<div class=\"route-sub\">{_e(r.get(\"sub\", \"\"))}</div>{_qmark(c, \"route-q\")}</div>' for i, r in enumerate(routes))"),
    ("    {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'fork-file')}",
     "    {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'fork-file', c)}"),
    ("    {f'<div class=\"approval\" id=\"{s}-ap\"><span class=\"approval-q\">?</span>{_e(approval)}</div>' if approval else ''}",
     "    {f'<div class=\"approval\" id=\"{s}-ap\">{_qmark(c, \"approval-q\")}{_e(approval)}</div>' if approval else ''}"),
    ("        kind = r.get(\"ok\")\n        mark = \"?\" if kind == \"open\" else \"&#8226;\"\n        cls = \"open\" if kind == \"open\" else \"neutral\"",
     "        kind = r.get(\"ok\")\n        cls = \"open\" if kind == \"open\" else \"neutral\"\n        if c.flat:\n            mark = '<i class=\"mk mk-unc\"></i>' if kind == \"open\" else '<i class=\"mk mk-fact\"></i>'\n        else:\n            mark = \"?\" if kind == \"open\" else \"&#8226;\""),
    ("      {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'beside-file')}",
     "      {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'beside-file', c)}"),
    ("      {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'close-file')}",
     "      {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'close-file', c)}"),
    ("    <div class=\"domain\">{_e(d.get('domain', 'scutoria.com'))}</div>\n  </div>\n</div>\"\"\")",
     "    <div class=\"domain\">{_e(d.get('domain', 'scutoria.com'))}</div>\n    {f'<div class=\"claim\">{_e(d[\"claim\"])}</div>' if d.get('claim') else ''}\n    {f'<div class=\"disclaimer\">{_e(d[\"disclaimer\"])}</div>' if d.get('disclaimer') else ''}\n  </div>\n</div>\"\"\")"),
    ("    out.tl.append(f'tl.fromTo(\"#{s} .domain\",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:\"power3.out\"}},{t(domain_at):.3f});')",
     "    out.tl.append(f'tl.fromTo(\"#{s} .domain\",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:\"power3.out\"}},{t(domain_at):.3f});')\n    if d.get('claim'):\n        out.tl.append(f'tl.fromTo(\"#{s} .claim\",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.4}},{t(domain_at + 0.3):.3f});')\n    if d.get('disclaimer'):\n        out.tl.append(f'tl.fromTo(\"#{s} .disclaimer\",{{opacity:0}},{{opacity:1,duration:0.4}},{t(domain_at + 0.5):.3f});')"),
    ("def file_css(pal: dict, display: str, display_w: int, mono: str) -> str:\n    acc, text, surf, muted, bg = pal[\"accent\"], pal[\"text\"], pal[\"surface\"], pal[\"muted\"], pal[\"bg\"]\n    return f\"\"\"",
     "def file_css(pal: dict, display: str, display_w: int, mono: str, flat: bool = False) -> str:\n    acc, text, surf, muted, bg = pal[\"accent\"], pal[\"text\"], pal[\"surface\"], pal[\"muted\"], pal[\"bg\"]\n    amber, on_amber, red = pal.get(\"signal_amber\", AMBER), pal.get(\"on_signal\", \"#1a1200\"), pal.get(\"signal_red\", RED)\n    paper, paper_ink = pal.get(\"paper\", text), pal.get(\"paper_ink\", bg)\n    card_border = pal.get(\"hairline\", f\"color-mix(in srgb,{acc} 35%,transparent)\") if flat else f\"color-mix(in srgb,{acc} 35%,transparent)\"\n    rad = 20 if flat else 26\n    shadow_paper = \"0 1px 1px rgba(0,0,0,0.22), 0 6px 14px rgba(0,0,0,0.24), 0 24px 48px rgba(0,0,0,0.36)\" if flat else \"0 30px 70px rgba(0,0,0,0.5)\"\n    tshadow = \"none\" if flat else \"0 10px 40px rgba(0,0,0,0.6)\"\n    return f\"\"\"\n.qchip{{position:absolute;right:-16px;top:-24px;display:inline-flex;align-items:center;gap:8px;background:{amber};color:{on_amber};border-radius:6px;padding:6px 14px;font-size:26px;font-weight:700;white-space:nowrap;}}\n.qchip .mk-unc{{border-color:{on_amber};background:linear-gradient(90deg,{on_amber} 50%,transparent 50%);width:18px;height:18px;}}\n.approval .qchip{{position:static;margin-right:18px;}}\n.claim{{font-family:'FN {display}';font-weight:700;font-size:36px;color:{text};margin-top:-18px;}}\n.disclaimer{{font-size:28px;color:{muted};margin-top:-26px;}}"),
])
p = ROOT / "src/fn/render/templates_file.py"
s = p.read_text(encoding="utf-8")
i = s.index("def file_css(")
head, body = s[:i], s[i:]
body = body.replace("{AMBER}", "{amber}").replace("{RED}", "{red}").replace("#1a1200", "{on_amber}")
body = body.replace(".fcard{{position:relative;width:290px;height:290px;background:{text};color:{bg};border-radius:20px;",
                    ".fcard{{position:relative;width:290px;height:290px;background:{paper};color:{paper_ink};border-radius:{4 if flat else 20}px;")
body = body.replace("box-shadow:0 30px 70px rgba(0,0,0,0.5);flex:0 0 auto;}}", "box-shadow:{shadow_paper};flex:0 0 auto;}}")
body = body.replace(".route{{position:relative;width:412px;background:{surf};border:2px solid color-mix(in srgb,{acc} 35%,transparent);border-radius:26px;",
                    ".route{{position:relative;width:412px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;")
body = body.replace(".bcard{{flex:1 1 auto;background:{surf};border:2px solid color-mix(in srgb,{acc} 35%,transparent);border-radius:26px;",
                    ".bcard{{flex:1 1 auto;background:{surf};border:2px solid {card_border};border-radius:{rad}px;")
body = body.replace(".upload-box{{width:760px;background:{surf};border:2px solid color-mix(in srgb,{acc} 35%,transparent);border-radius:30px;",
                    ".upload-box{{width:760px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;")
body = body.replace(".upload-btn{{width:420px;padding:18px 0;border-radius:16px;background:{acc};color:{bg};",
                    ".upload-btn{{width:420px;padding:18px 0;border-radius:999px;background:{pal.get('button', acc)};color:{pal.get('on_accent', bg)};")
body = body.replace("text-shadow:0 10px 40px rgba(0,0,0,0.6);}}", "text-shadow:{tshadow};}}")
body = body.replace(".bmark{{width:44px;flex:0 0 44px;text-align:center;font-weight:800;color:{muted};}}",
                    ".bmark{{width:44px;flex:0 0 44px;text-align:center;font-weight:800;color:{muted};padding-top:8px;}}")
p.write_text(head + body, encoding="utf-8", newline="\n")
print("templates_file css patched")

# ---------------- director.py ----------------
patch("src/fn/render/director.py", [
    ("from .templates_file import file_css, AMBER, RED\n", "from .templates_file import file_css, AMBER, RED\nfrom ..config import ROOT\n"),
    ("    used_fonts = {display, body, mono, cap_font}\n    for fam in used_fonts:\n        folder, fname = FONT_FILES[fam]\n        src, dst = ASSETS_DIR / \"fonts\" / folder, assets / \"fonts\" / folder\n        dst.mkdir(exist_ok=True)\n        for f in (fname, \"OFL.txt\"):\n            if (src / f).exists() and not (dst / f).exists():\n                shutil.copy2(src / f, dst / f)\n",
     "    used_fonts = {display, body, mono, cap_font}\n    font_css = _brand_font_css(b, used_fonts, assets)\n    flat = bool(b.design.get(\"flat\"))\n    logo_cfg = b.design.get(\"logo\") or {}\n    logo_src = \"\"\n    if logo_cfg.get(\"file\") and (ROOT / logo_cfg[\"file\"]).exists():\n        (assets / \"logo\").mkdir(exist_ok=True)\n        shutil.copy2(ROOT / logo_cfg[\"file\"], assets / \"logo\" / Path(logo_cfg[\"file\"]).name)\n        logo_src = f\"assets/logo/{Path(logo_cfg['file']).name}\"\n"),
    ("    parts.append(f'<div id=\"logo\" class=\"clip\" data-start=\"0\" data-duration=\"{total:.3f}\" data-track-index=\"4\">'\n                 f'<div class=\"logo-inner\"><span class=\"mark\"></span><span class=\"wordmark\">{html.escape(b.name)}</span></div></div>')",
     "    wordmark = logo_cfg.get(\"wordmark_text\", b.name) if logo_src else b.name\n    mark_html = f'<img class=\"logo-img\" src=\"{logo_src}\" alt=\"\">' if logo_src else '<span class=\"mark\"></span>'\n    parts.append(f'<div id=\"logo\" class=\"clip\" data-start=\"0\" data-duration=\"{total:.3f}\" data-track-index=\"4\">'\n                 f'<div class=\"logo-inner{\" brandmark\" if logo_src else \"\"}\">{mark_html}<span class=\"wordmark\">{html.escape(wordmark)}</span></div></div>')"),
    ("    tl.append(f'tl.fromTo(\"#bg\",{{x:-40,y:-30}},{{x:40,y:30,duration:{total:.3f},ease:\"none\"}},0);')\n    tl.append(f'tl.fromTo(\"#light\",{{x:-300,y:-500,opacity:0.5}},{{x:300,y:500,opacity:0.5,duration:{total:.3f},ease:\"sine.inOut\"}},0);')",
     "    tl.append(f'tl.fromTo(\"#bg\",{{x:-40,y:-30}},{{x:40,y:30,duration:{total:.3f},ease:\"none\"}},0);')\n    if not flat:\n        tl.append(f'tl.fromTo(\"#light\",{{x:-300,y:-500,opacity:0.5}},{{x:300,y:500,opacity:0.5,duration:{total:.3f},ease:\"sine.inOut\"}},0);')"),
    ("    parts: list[str] = ['<div id=\"bg\"></div>', '<div id=\"light\"></div>']",
     "    parts: list[str] = ['<div id=\"bg\"></div>'] + ([] if bool(b.design.get(\"flat\")) else ['<div id=\"light\"></div>'])"),
    ("                       mono_font=mono, zone_top=zone_top, zone_h=zone_h, enter=enter, lang=lang)",
     "                       mono_font=mono, zone_top=zone_top, zone_h=zone_h, enter=enter, lang=lang, flat=flat)"),
    ("            tl.append(f'tl.fromTo(\"#{cid}w{g.highlight}\",{{scale:0.92}},{{scale:1.06,duration:0.15,ease:\"back.out(1.6)\"}},{max(g.start, g.words[g.highlight].start):.3f});')",
     "            tl.append(f'tl.fromTo(\"#{cid}w{g.highlight}\",{{scale:0.94}},{{scale:{1.03 if flat else 1.06},duration:0.15,ease:\"power2.out\"}},{max(g.start, g.words[g.highlight].start):.3f});')"),
    ("{_font_face_css(used_fonts)}\n:root{{--bg:{pal['bg']};", "{font_css}\n:root{{--bg:{pal['bg']};"),
    ("#bg{{position:absolute;inset:-60px;z-index:0;{_bg_pattern_css(b.design.get('bg_pattern', ''), pal)}}}",
     "#bg{{position:absolute;inset:-60px;z-index:0;{_bg_css(b.design.get('bg_pattern', ''), pal)}}}"),
    (".logo-inner{{position:absolute;left:72px;top:116px;font-size:{int(layout['logo_px'])}px;line-height:56px;display:flex;align-items:center;gap:12px;color:var(--text);opacity:0.92;}}",
     ".logo-inner{{position:absolute;left:72px;top:116px;font-size:{int(layout['logo_px'])}px;line-height:56px;display:flex;align-items:center;gap:12px;color:var(--text);opacity:0.92;}}\n.logo-inner.brandmark{{gap:{int(logo_cfg.get('logo_height_px', 44))}px;}}\n.logo-img{{width:{int(logo_cfg.get('logo_height_px', 44))}px;height:{int(logo_cfg.get('logo_height_px', 44))}px;display:block;}}\n.logo-inner.brandmark .wordmark{{font-weight:700;font-size:28px;letter-spacing:0.18em;text-transform:uppercase;}}"),
    ("{scene_css(pal, display, display_w, body, mono, zone_top, zone_h)}\n{file_css(pal, display, display_w, mono)}",
     "{scene_css(pal, display, display_w, body, mono, zone_top, zone_h, flat)}\n{file_css(pal, display, display_w, mono, flat)}"),
    (".st-amber{{color:{AMBER};}}\n.st-red{{color:{RED};}}",
     ".st-amber{{color:{pal.get('signal_amber', AMBER)};}}\n.st-red{{color:{pal.get('signal_red', RED)};}}"),
])
p = ROOT / "src/fn/render/director.py"
s = p.read_text(encoding="utf-8")
s += '''

def _font_face(family: str, rel: str, weight: str = "100 900") -> str:
    fmt = "woff2" if rel.endswith(".woff2") else "truetype"
    return (f"@font-face{{font-family:'FN {family}';src:url('{rel}') format('{fmt}');"
            f"font-weight:{weight};font-style:normal;font-display:block;}}")


def _brand_font_css(brand: Brand, families: set[str], assets: Path) -> str:
    """@font-face for every used family: brand-specific files (brand.yaml fonts.*.file) first, shared fonts otherwise."""
    css: list[str] = []
    done: set[str] = set()
    for role in ("display", "body", "mono", "caption"):
        f = (brand.fonts.get(role) or {})
        fam, file = f.get("family"), f.get("file")
        if not fam or fam in done or fam not in families or not file:
            continue
        files = [file] + list(f.get("extra_files") or [])
        slug = fam.lower().replace(" ", "")
        (assets / "fonts" / slug).mkdir(parents=True, exist_ok=True)
        for fp in files:
            src = ROOT / fp
            if src.exists():
                dst = assets / "fonts" / slug / src.name
                if not dst.exists():
                    shutil.copy2(src, dst)
                weight = "100 900" if ("wght" in src.name or src.suffix == ".woff2") else str(f.get("weight", 400))
                css.append(_font_face(fam, f"assets/fonts/{slug}/{src.name}", weight))
        lic = f.get("license_file")
        if lic and (ROOT / lic).exists():
            dst = assets / "fonts" / slug / Path(lic).name
            if not dst.exists():
                shutil.copy2(ROOT / lic, dst)
        done.add(fam)
    for fam in sorted(families - done):
        if fam in FONT_FILES:
            folder, fname = FONT_FILES[fam]
            src, dst = ASSETS_DIR / "fonts" / folder, assets / "fonts" / folder
            dst.mkdir(parents=True, exist_ok=True)
            for fn in (fname, "OFL.txt"):
                if (src / fn).exists() and not (dst / fn).exists():
                    shutil.copy2(src / fn, dst / fn)
            css.append(_font_face(fam, f"assets/fonts/{folder}/{fname}"))
    return "\\n".join(css)


def _bg_css(pattern: str, pal: dict) -> str:
    if pattern == "hairline-grid":          # brand: flat ground, grid at most as hairlines
        hair = pal.get("hairline", "rgba(226,232,246,0.12)")
        return (f"background-color:{pal['bg']};background-image:linear-gradient({hair} 1px,transparent 1px),"
                f"linear-gradient(90deg,{hair} 1px,transparent 1px);background-size:96px 96px;")
    return _bg_pattern_css(pattern, pal)
'''
p.write_text(s, encoding="utf-8", newline="\n")
print("director patched")
