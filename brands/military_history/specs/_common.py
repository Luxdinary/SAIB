"""Shared helpers for Frontlore topic specs (plan_builder.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plan_builder import C, E, L, PATH, PL, R, SIGHT  # noqa: E402,F401


def T(de, en):
    return {"de": de, "en": en}


def hooks(items):
    """items: (type, spoken_de, spoken_en, screen_de, screen_en, (clarity, relevance, curiosity, truth, visual), source_ids)"""
    out = []
    for i, (typ, de, en, ode, oen, sc, src) in enumerate(items):
        out.append({"id": f"H{i + 1}", "type": typ, "spoken": T(de, en), "on_screen": T(ode, oen),
                    "scores": dict(zip(("clarity", "relevance", "curiosity", "truth", "visual"), sc)), "source_ids": src,
                    "visual": "", "why": {"truth": "aus den geöffneten Quellen" if sc[3] >= 4 else "nicht belegt, nicht wählbar"}})
    return out


def hook_beat(spoken, question, em, title, meta, no, stamp, drawing, packet, stamp_at, packet_at, em_at, src):
    return {"id": "b1", "function": "hook", "scene_type": "cinematic_hook", "source_ids": src, "overlay": {"marker": "none"},
            "spoken": spoken,
            "data": {"question": question, "question_em": em, "card_title": title, "card_meta": meta, "card_no": no, "stamp": stamp,
                     "drawing": drawing, "packet_label": packet, "card_at": 0.05, "draw_at": 0.4, "question_at": 0.15,
                     "stamp_at": stamp_at, "packet_at": packet_at, "em_at": em_at}}


def map_beat(spoken, headline, a, b, road_at, route_label, route_label_at, wait_at, chip, chip_at, packet, packet_at,
             line_label, line_label_at, src, marker="fakt", example=False):
    """a: (label, code, at) seat/point top right; b: (label, code, at) region bottom left."""
    ov = {"marker": marker, "transition": {"type": "blende", "seconds": 0.7}}
    if example:
        ov["example"] = True
    return {"id": "b2", "function": "problem", "scene_type": "data_flow", "source_ids": src, "overlay": ov, "spoken": spoken,
            "data": {"mode": "map", "headline": headline,
                     "places": [{"label": a[0], "code": a[1], "x": 600, "y": 80, "at": a[2]},
                                {"label": b[0], "code": b[1], "x": 190, "y": 500, "rx": 170, "ry": 95, "at": b[2]}],
                     "route_at": road_at, "route_label": route_label, "route_label_at": route_label_at, "wait_at": wait_at,
                     "route_label_xy": [470, 330], "chip": chip, "chip_at": chip_at, "chip_xy": [350, 560],
                     "packet_label": packet, "packet_at": packet_at, "packet_xy": [594, 176], "masts": 0,
                     "line_label": line_label, "line_label_at": line_label_at}}


def sheet_beat(spoken, headline, drawing, sheet_title, callouts, zoom_at, back_at, dim_at, src, zoom_xy=(230, 300)):
    """callouts: (label, x, y, at) in drawing units; labels stacked on the right of the sheet."""
    cos = [{"label": lab, "x": x, "y": y, "lx": 500, "ly": 60 + 110 * i, "at": at} for i, (lab, x, y, at) in enumerate(callouts)]
    return {"id": "b3", "function": "explanation", "scene_type": "ui_demo", "source_ids": src,
            "overlay": {"marker": "fakt", "transition": {"type": "iris", "x": 300, "y": 900, "seconds": 0.7}, "vignette": True, "dim_at": dim_at},
            "spoken": spoken,
            "data": {"headline": headline, "drawing": drawing, "sheet_title": sheet_title, "draw_at": 0.1, "draw_seconds": 1.6,
                     "callouts": cos, "zoom": {"x": zoom_xy[0], "y": zoom_xy[1], "scale": 1.12, "at": zoom_at, "back_at": back_at, "grow": "up"}}}


def versus_beat(spoken, headline, left, right, verdict, verdict_at, src, dim_left_at=None, marker="fakt"):
    """left/right: {"tag", "title", "at", "rows": [text or {"text", "at"}]}"""
    d = {"mode": "versus_fl", "headline": headline, "left": left, "right": right, "verdict": verdict, "verdict_at": verdict_at}
    if dim_left_at:
        d["dim_left_at"] = dim_left_at
    return {"id": "b4", "function": "demonstration", "scene_type": "comparison", "source_ids": src,
            "overlay": {"marker": marker, "transition": {"type": "blende", "seconds": 0.7}}, "spoken": spoken, "data": d}


def route_beat(spoken, headline, nodes, edge_labels, packet, src, count=None, total=None, marker="fakt", example=False):
    """nodes: (label, code, at); edge_labels: one per gap."""
    d = {"headline": headline, "nodes": [{"label": a, "code": b, "at": c} for a, b, c in nodes],
         "edges": [{"label": e} for e in edge_labels], "packet_label": packet}
    if count:
        d["count"] = count
    if total:
        d["total"] = total
    ov = {"marker": marker}
    if example:
        ov["example"] = True
    return {"id": "b5", "function": "insight", "scene_type": "data_flow", "source_ids": src, "overlay": ov, "spoken": spoken, "data": d}


def timeline_beat(spoken, headline, items, src, end_at=None):
    """items: (year, title, sub, at, sub_at or None)"""
    its = []
    for y, ti, sub, at, sub_at in items:
        it = {"year": y, "title": ti, "sub": sub, "at": at}
        if sub_at:
            it["sub_at"] = sub_at
        its.append(it)
    d = {"mode": "timeline", "headline": headline, "items": its}
    if end_at:
        d["end_at"] = end_at
    return {"id": "b6", "function": "insight", "scene_type": "key_takeaway", "source_ids": src,
            "overlay": {"marker": "fakt", "transition": {"type": "iris", "x": 231, "y": 1000, "seconds": 0.7}}, "spoken": spoken, "data": d}


def close_beat(spoken, title, meta, no, stamp, drawing, statement, statement_at, stamp_at, note, note_at, src, sign=None, sign_at=None, ghost_at=None):
    d = {"mode": "closing", "card_title": title, "card_meta": meta, "card_no": no, "stamp": stamp, "drawing": drawing,
         "statement": statement, "statement_at": statement_at, "stamp_at": stamp_at, "note": note, "note_at": note_at,
         "chip": T("Folge Frontlore", "Follow Frontlore"), "chip_at": T("w:Folge", "w:follow")}
    if sign:
        d.update(sign=sign, sign_at=sign_at)
    if ghost_at:
        d["ghost_at"] = ghost_at
    return {"id": "b7", "function": "close", "scene_type": "key_takeaway", "source_ids": src,
            "overlay": {"marker": "fakt", "transition": {"type": "blende", "seconds": 0.7}}, "spoken": spoken, "data": d}
