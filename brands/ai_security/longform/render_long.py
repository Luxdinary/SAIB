"""Render a Scutoria long-form video (16:9) chapter by chapter, or its reels (9:16), from a plan.

Run through the render queue (never take data/render.lock yourself):
  .venv\\Scripts\\python.exe scripts\\render_queue.py ai_security -- brands\\ai_security\\longform\\render_long.py <plan.json> [options]

Options:
  --chapters c0,c1      only these chapters (probe); default all
  --tts gemini|mock     voice per chapter; a paid recording is cached in <out>/voice and reused while the text is unchanged
  --no-render           build projects and checks only (dry run)
  --reels [r1,r2]       render reels (9:16) instead of the long video; needs the chapter voices from a long run
  --workers N           HyperFrames workers (default 4)
  --overlap             run scripts/overlap_check.mjs on every project (FN_OVERLAP_STEP=0.5)

Output: storage/longform/<video_id>/ (chapters/<cid>/video.mp4, video.mp4, chapters.txt, captions.srt, report.json,
reels/<rid>.mp4). Plan format: README.md in this folder.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE.parent))

from fn import transcribe  # noqa: E402
from fn.config import STORAGE_DIR  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.render import ffmpeg, hyperframes  # noqa: E402
from fn.render.compose import Word  # noqa: E402
from fn.render.director import group_phrases  # noqa: E402

from longform import compose, fmt as fmts  # noqa: E402

CARD = 2.4            # chapter card before the voice of a chapter
LEAD = 0.3            # silence after the card
TAIL = 0.9            # after the last word of a chapter
SCENE_LEAD = 0.15     # a scene starts this much before its first word
CHUNK_CHARS = 1400    # Gemini request size: at most about 85 s of speech (main session, 02.11.2026: keep requests under 90 s)
OPENING = {"de": "Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung",
           "en": "Synthetic voice · Sources on screen · Not legal advice"}
ENDCARD = {"de": ["Das ganze Video: Scutoria auf YouTube", "Belegt. Datiert. Vorzeigbar.", "Quellenbasiert. Keine Rechtsberatung."],
           "en": ["The full video: Scutoria on YouTube", "Sourced. Dated. Ready to show.", "Source-based. No legal advice."]}
STYLE = {"de": "Sprich ruhig, klar und sachlich auf Deutsch, mittleres Tempo, wie ein erfahrener Kollege, der etwas erklärt. Keine Dramatik.",
         "en": "Speak calmly, clearly and matter-of-factly, medium pace, like an experienced colleague explaining something. No drama."}


# --- plan --------------------------------------------------------------------------------------------

def load_plan(path: Path) -> dict:
    plan = json.loads(path.read_text(encoding="utf-8"))
    src = {s["id"]: s for s in plan.get("sources", [])}
    problems = []
    for ch in plan["chapters"]:
        for k, sc in enumerate(ch["scenes"]):
            sc.setdefault("id", f"{ch['id']}s{k}")
            for p in sc.get("say", []):
                if p.get("source") and p["source"] not in src:
                    problems.append(f"{sc['id']}: source {p['source']} not in plan.sources")
                if p.get("marker") in ("fakt", "unsicher") and not p.get("source"):
                    problems.append(f"{sc['id']}: marker {p['marker']} without source")
            if not sc.get("say"):
                problems.append(f"{sc['id']}: scene without spoken text")
    for s in plan.get("sources", []):
        if not s.get("checked") and not re.search(r"Abruf|abgerufen|retrieved|accessed|geprüft|checked", s.get("label", "")):
            problems.append(f"source {s['id']}: no retrieval date")
    plan["_src"] = src
    plan["_problems"] = problems
    return plan


def chapter_text(ch: dict) -> str:
    return "\n\n".join(p["text"].strip() for sc in ch["scenes"] for p in sc["say"])


def _tokens(text: str) -> int:
    return len(text.split())


# --- voice -------------------------------------------------------------------------------------------

def _chunks(paras: list[str]) -> list[str]:
    out, cur = [], ""
    for p in paras:
        if cur and len(cur) + len(p) + 2 > CHUNK_CHARS:
            out.append(cur)
            cur = p
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        out.append(cur)
    return out


def voice_for(ch: dict, lang: str, vdir: Path, tts: str, costs: CostLogger, vid: str) -> tuple[Path, dict]:
    text = chapter_text(ch)
    h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    wav, side = vdir / f"{ch['id']}.wav", vdir / f"{ch['id']}.json"
    if wav.exists() and side.exists():
        info = json.loads(side.read_text(encoding="utf-8"))
        if info.get("hash") == h and (tts == "mock" or info.get("provider") == "gemini"):
            return wav, info
    vdir.mkdir(parents=True, exist_ok=True)
    paras = [p["text"].strip() for sc in ch["scenes"] for p in sc["say"]]
    if tts == "mock":
        secs = len(text) / (16.5 if lang == "de" else 15.7)
        ffmpeg.silent_wav(wav, secs)
        info = {"provider": "mock", "hash": h, "seconds": secs, "usd": 0.0}
    else:
        # quota rules of the main session (02.11.2026): no request unless allowed, at most LONGFORM_TTS_MAX requests per
        # counter file, never a retry after an error (failed requests may count), one model per video
        if os.environ.get("LONGFORM_NO_TTS"):
            raise RuntimeError(f"{ch['id']}: voice missing and LONGFORM_NO_TTS is set; Vertonung offen")
        from fn.tts.gemini import GeminiTTS
        g = GeminiTTS()
        others = [json.loads(p.read_text(encoding="utf-8")).get("model") for p in vdir.glob("c*.json") if not p.name.endswith("words.json")]
        others = {m for m in others if m and m != g.model}
        if others:
            raise RuntimeError(f"{ch['id']}: other chapters of this video use {others}, not {g.model}; one model per video")
        counter = STORAGE_DIR / "longform" / f"tts_requests_{datetime.now():%Y-%m-%d}.txt"
        limit = int(os.environ.get("LONGFORM_TTS_MAX", "0") or 0)
        parts, usd, toks = [], 0.0, 0
        for i, chunk in enumerate(_chunks(paras)):
            part = vdir / f"{ch['id']}.part{i}.wav"
            used = len(counter.read_text(encoding="utf-8").splitlines()) if counter.exists() else 0
            if limit and used >= limit:
                raise RuntimeError(f"TTS limit {limit} reached ({used} requests today); Vertonung offen")
            with counter.open("a", encoding="utf-8") as cf:
                cf.write(f"{datetime.now():%H:%M:%S} {vid} {ch['id']} part{i} {len(chunk)} chars {g.model}\n")
            try:
                r = g.synthesize(chunk, lang, "Charon", part, style=STYLE[lang])
            except Exception as ex:  # noqa: BLE001  no retry: stop and report
                print(f"  tts {ch['id']} part {i} failed, stopping: {str(ex)[:160]}")
                raise RuntimeError(f"Gemini TTS failed for {ch['id']} part {i}; Vertonung offen") from ex
            usd += r.usd
            toks += r.output_tokens
            costs.log_tts(f"{vid}-{ch['id']}", "gemini", r.input_chars, r.output_tokens, r.seconds)
            parts.append(part)
        _concat_wavs(parts, wav, gap=0.45)
        info = {"provider": "gemini", "model": g.model, "voice": "Charon", "hash": h, "seconds": ffmpeg.audio_duration(wav),
                "usd": round(usd, 5), "output_tokens": toks, "chunks": len(parts), "created": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    info["seconds"] = ffmpeg.audio_duration(wav)
    side.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    return wav, info


def _concat_wavs(parts: list[Path], dst: Path, gap: float) -> None:
    with wave.open(str(parts[0]), "rb") as w0:
        params = w0.getparams()
    silence = b"\x00\x00" * int(params.framerate * gap)
    with wave.open(str(dst), "wb") as out:
        out.setparams(params)
        for i, p in enumerate(parts):
            with wave.open(str(p), "rb") as w:
                out.writeframes(w.readframes(w.getnframes()))
            if i < len(parts) - 1:
                out.writeframes(silence)


def words_for(ch: dict, wav: Path, info: dict, lang: str, vdir: Path) -> list[Word]:
    text = chapter_text(ch)
    cache = vdir / f"{ch['id']}.words.json"
    if cache.exists():
        c = json.loads(cache.read_text(encoding="utf-8"))
        if c.get("hash") == info["hash"] and c.get("provider") == info["provider"]:
            return [Word(w[0], w[1], w[2]) for w in c["words"]]
    mock = info["provider"] == "mock"
    tr = transcribe.transcribe(wav, lang, script_text=text, model_size="large-v3", force_mock=mock)
    words = transcribe.align_to_script(tr.words, text)
    cache.write_text(json.dumps({"hash": info["hash"], "provider": info["provider"], "model": tr.model,
                                 "words": [[w.text, w.start, w.end] for w in words]}, ensure_ascii=False), encoding="utf-8")
    print(f"  words {ch['id']}: {len(words)} via {tr.model} ({tr.device}, {tr.elapsed:.0f} s)")
    return words


# --- timing ------------------------------------------------------------------------------------------

def time_chapter(ch: dict, words: list[Word], voice_s: float, plan: dict, first: bool, last: bool) -> dict:
    """Absolute timing inside the chapter's own timeline (0 = chapter start)."""
    card = 0.0 if first or ch.get("card") is False else CARD
    vstart = card + (LEAD if card else 0.4)
    shifted = [Word(w.text, round(w.start + vstart, 3), round(w.end + vstart, 3)) for w in words]
    end_extra = float(ch.get("end_seconds", 0.0))
    total = vstart + voice_s + TAIL + end_extra
    idx, scenes = 0, []
    for sc in ch["scenes"]:
        n = sum(_tokens(p["text"]) for p in sc["say"])
        sw = shifted[idx: idx + n]
        marks, j = [], idx
        for p in sc["say"]:
            pn = _tokens(p["text"])
            pw = shifted[j: j + pn]
            j += pn
            if pw and (p.get("marker") or p.get("source")):
                s = plan["_src"].get(p.get("source"), {})
                marks.append({"marker": p.get("marker"), "source": s.get("label", ""), "source_short": s.get("short", ""),
                              "start": pw[0].start - 0.1, "end": pw[-1].end + 0.5})
        scenes.append({"sid": sc["id"], "type": sc["type"], "data": sc.get("data", {}), "bg": sc.get("bg"), "scrim": sc.get("scrim"),
                       "words": sw, "marks": marks, "first_word": sw[0].start if sw else None})
        idx += n
    for i, s in enumerate(scenes):
        s["start"] = card if i == 0 else round((s["first_word"] or scenes[i - 1]["start"] + 1) - SCENE_LEAD, 3)
    for i, s in enumerate(scenes):
        s["end"] = round(total if i == len(scenes) - 1 else scenes[i + 1]["start"], 3)
        if s["end"] - s["start"] < 1.0:
            print(f"  warn {s['sid']}: only {s['end'] - s['start']:.2f} s")
    return {"card": card, "vstart": vstart, "total": round(total, 3), "scenes": scenes, "words": shifted}


def resolve_inserts(ch: dict, tm: dict) -> tuple[list[dict], list[str]]:
    """Insert times inside the chapter timeline: "at" is a phrase spoken in this chapter (first match), or "start"."""
    def norm(x: str) -> str:
        return re.sub(r"[^\w]", "", x.lower())
    words, out, problems = tm["words"], [], []
    for ins in ch.get("inserts", []):
        if "start" in ins and not ins.get("at"):
            out.append({**ins, "start": float(ins["start"])})
            continue
        toks = [norm(x) for x in ins["at"].split() if norm(x)]
        hit = None
        for i in range(len(words) - len(toks) + 1):
            if all(norm(words[i + k].text).startswith(toks[k]) for k in range(len(toks))):
                hit = words[i].start
                break
        if hit is None:
            problems.append(f"{ch['id']}: insert anchor '{ins['at']}' not found")
            continue
        start = max(0.0, hit - 0.2)
        out.append({**ins, "start": round(start, 3), "dur": min(float(ins["dur"]), tm["total"] - start - 0.3)})
    return out, problems


# --- render ------------------------------------------------------------------------------------------

def render_project(project: Path, out_mp4: Path, total: float, workers: int, audio: Path | None = None) -> float:
    raw = out_mp4.with_name("render_raw.mp4")
    t0 = time.perf_counter()
    hyperframes.render(project, raw, quality="looks", gpu=True, workers=workers, timeout=max(3600, int(total * 30)))
    if audio is not None:                       # sound layer: finished mix under the picture, static loudness gain
        ffmpeg.encode_nvenc(raw, out_mp4, audio=audio, loudness_lufs=-16.0, loudnorm="linear", timeout=max(1800, int(total * 4)))
    else:
        ffmpeg.encode_nvenc(raw, out_mp4, loudness_lufs=-16.0, timeout=max(1800, int(total * 4)))
    raw.unlink(missing_ok=True)
    return time.perf_counter() - t0


def overlap(project: Path) -> dict:
    env = dict(os.environ, FN_OVERLAP_STEP="0.5")
    p = subprocess.run(["node", str(ROOT / "scripts" / "overlap_check.mjs"), str(project)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, timeout=3600)
    return {"exit": p.returncode, "out": p.stdout[-3000:]}


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def yt_time(t: float) -> str:
    s = int(t)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--chapters", default="")
    ap.add_argument("--tts", default="gemini")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--reels", nargs="?", const="all", default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--overlap", action="store_true")
    ap.add_argument("--tag", default="", help="suffix for the output folder (probe runs)")
    ap.add_argument("--no-concat", action="store_true", help="render the chosen chapters only (one queue job per chapter)")
    ap.add_argument("--concat", action="store_true", help="join the rendered chapters, write chapters.txt, SRT, manifest (no render, no lock)")
    a = ap.parse_args()

    plan = load_plan(Path(a.plan))
    if plan["_problems"]:
        print("plan problems:", *plan["_problems"], sep="\n  ")
        return 2
    lang, vid = plan["lang"], plan["video_id"]
    out = STORAGE_DIR / "longform" / (vid + (f"-{a.tag}" if a.tag else ""))
    vdir = STORAGE_DIR / "longform" / vid / "voice"          # voices are shared by probe and full runs
    out.mkdir(parents=True, exist_ok=True)
    costs = CostLogger()
    chs = plan["chapters"]
    want = [c for c in a.chapters.split(",") if c]
    report: dict = {"video_id": vid, "lang": lang, "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "chapters": [], "problems": [], "reels": []}
    t_all = time.perf_counter()

    timed: dict[str, dict] = {}
    for i, ch in enumerate(chs):
        if want and ch["id"] not in want and a.reels is None:
            continue
        wav, info = voice_for(ch, lang, vdir, a.tts, costs, vid)
        words = words_for(ch, wav, info, lang, vdir)
        tm = time_chapter(ch, words, info["seconds"], plan, first=(i == 0), last=(i == len(chs) - 1))
        tm.update({"wav": wav, "info": info, "index": i})
        timed[ch["id"]] = tm
        print(f"chapter {ch['id']}: voice {info['seconds']:.1f} s ({info['provider']}, {info.get('usd', 0)} USD), total {tm['total']:.1f} s, {len(tm['scenes'])} scenes")

    if a.reels is not None:
        return render_reels(plan, timed, out, a, report)

    f = fmts.get("16x9")
    done = []
    for ch in chs:
        if ch["id"] not in timed:
            continue
        tm = timed[ch["id"]]
        i = tm["index"]
        seg = {"lang": lang, "title": f"{plan['title']} · {ch['title']}", "total": tm["total"], "scenes": tm["scenes"],
               "heads": [{"start": tm["card"], "end": tm["total"], "kicker": ch.get("kicker", ""), "title": ch.get("title", ""),
                          "title_seconds": 8.0}],
               "cards": [{"start": 0.0, "dur": tm["card"], "num": ch.get("num", ""), "title": ch.get("title", "")}] if tm["card"] else [],
               "opening": {"start": 0.0, "end": 7.0, "text": OPENING[lang]} if i == 0 else None,
               "voice": tm["wav"], "voice_start": tm["vstart"], "voice_seconds": tm["info"]["seconds"]}
        cdir = out / "chapters" / ch["id"]
        if a.concat:                                          # join only: take the chapter renders as they are
            if not (cdir / "video.mp4").exists():
                print(f"  missing render of {ch['id']}; run it first")
                return 4
            entry = json.loads((cdir / "entry.json").read_text(encoding="utf-8")) if (cdir / "entry.json").exists() else {"id": ch["id"]}
            report["chapters"].append(entry)
            done.append((ch, tm, cdir / "video.mp4"))
            continue
        res = compose.build(seg, f, cdir / "project")
        chk = hyperframes.check(cdir / "project")
        lint = chk.get("lint", {})
        entry = {"id": ch["id"], "title": ch["title"], "seconds": tm["total"], "voice": tm["info"], "problems": res["problems"],
                 "lint_errors": lint.get("errorCount"), "layout_errors": chk.get("layout", {}).get("errorCount")}
        gaps = [b - a2 for a2, b in zip(res["events"], res["events"][1:])]
        entry["longest_static_s"] = round(max(gaps), 2) if gaps else None
        for p in res["problems"]:
            print("  problem:", p)
        if lint.get("errorCount"):
            for it in lint.get("findings", [])[:8]:
                print("  lint:", it.get("code"), it.get("selector"), (it.get("message") or "")[:140])
            report["chapters"].append(entry)
            break
        if not a.no_render:
            secs = render_project(cdir / "project", cdir / "video.mp4", tm["total"], a.workers)
            entry["render_seconds"] = round(secs, 1)
            entry["render_factor"] = round(secs / tm["total"], 2)
            costs.log_render(f"{vid}-{ch['id']}", secs, "hyperframes looks + nvenc (longform 16:9)")
            print(f"  render {ch['id']}: {secs:.0f} s for {tm['total']:.0f} s video (x{secs / tm['total']:.2f})")
            done.append((ch, tm, cdir / "video.mp4"))
        if a.overlap:
            entry["overlap"] = overlap(cdir / "project")
            print(f"  overlap {ch['id']}: exit {entry['overlap']['exit']}")
        report["chapters"].append(entry)
        (cdir / "entry.json").write_text(json.dumps(entry, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    if done and not a.no_render and not a.no_concat:
        if a.concat and len(done) != len(chs):
            print("concat needs every chapter")
            return 4
        lst = out / "concat.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for _, _, p in done), encoding="utf-8")
        final = out / "video.mp4"
        ffmpeg.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", str(final)])
        # chapters and subtitles on the joined timeline
        t, marks, srt, n = 0.0, [], [], 1
        for ch, tm, p in done:
            marks.append(f"{yt_time(t)} {ch['title']}")
            for g in group_phrases(tm["words"], min_words=3, max_words=9):
                srt.append(f"{n}\n{srt_time(t + g.start)} --> {srt_time(t + g.end)}\n{g.text}\n")
                n += 1
            t += ffmpeg.audio_duration(p)
        (out / "chapters.txt").write_text("\n".join(marks) + "\n", encoding="utf-8")
        (out / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
        report["duration_s"] = round(t, 1)
        voices = {c.get("id"): (c.get("voice") or {}).get("provider") for c in report["chapters"]}
        report["tts_all_gemini"] = all(v == "gemini" for v in voices.values())
        manifest = {"video_id": vid, "brand_id": "ai_security", "language": lang, "title": plan["title"], "duration_s": round(t, 1),
                    "tts": {"provider": "gemini" if report["tts_all_gemini"] else "MIXED", "per_chapter": voices, "voice": "Charon"},
                    "ai_disclosure": {"in_picture": "KI-GENERIERT · SYNTHETISCHE STIMME (oben rechts), Einstiegszeile, gesprochener Hinweis im Schluss",
                                      "labels": {"is_ai_generated": True, "containsSyntheticMedia": True}},
                    "sources": plan["sources"], "chapters": [c.get("id") for c in report["chapters"]],
                    "overlap_ok": all((c.get("overlap") or {}).get("exit") == 0 for c in report["chapters"]),
                    "created": report["created"]}
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        if not report["tts_all_gemini"]:
            print("NOT all chapters voiced by Gemini:", voices)
        for k, at in enumerate([5, 60, 180, 400, 700, 1000]):
            if at < t - 1:
                ffmpeg.extract_frame(final, out / f"frame_{at:04d}s.jpg", float(at))
        print(f"video: {final} ({t:.1f} s)")
    report["seconds_total_run"] = round(time.perf_counter() - t_all, 1)
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    bad = any(c.get("problems") or c.get("lint_errors") for c in report["chapters"])
    print("report:", out / "report.json", "· problems" if bad else "· ok")
    return 1 if bad else 0


def render_reels(plan: dict, timed: dict, out: Path, a, report: dict) -> int:
    """Reels in 9:16 from scene ranges of the long video; the voice is cut from the chapter recording."""
    f = fmts.get("9x16")
    lang = plan["lang"]
    want = None if a.reels == "all" else set(a.reels.split(","))
    rc = 0
    for r in plan.get("reels", []):
        if want and r["id"] not in want:
            continue
        cid = r["chapter"]
        tm = timed[cid]
        ids = r["scenes"]
        scs = [s for s in tm["scenes"] if s["sid"] in ids]
        if not scs:
            print(f"reel {r['id']}: no scenes")
            rc = 1
            continue
        end_s = 3.2
        # length rule 65-95 s: extend by whole neighbouring scenes of the same chapter, forward first; never prepend
        # a scene before a reel that opens with a case (it would start with the end of the previous case)
        allsc = tm["scenes"]
        lo, hi = allsc.index(scs[0]), allsc.index(scs[-1])
        length = lambda a, b: allsc[b]["end"] - allsc[a]["first_word"] + 0.35 + end_s   # noqa: E731
        while length(lo, hi) < 65:
            if hi + 1 < len(allsc) and allsc[hi + 1]["type"] != "case" and length(lo, hi + 1) <= 95:
                hi += 1
            elif lo > 0 and allsc[lo]["type"] != "case" and length(lo - 1, hi) <= 95:
                lo -= 1
            else:
                break
        if [s["sid"] for s in allsc[lo:hi + 1]] != [s["sid"] for s in scs]:
            print(f"  reel {r['id']}: extended to {allsc[lo]['sid']}..{allsc[hi]['sid']} for the length rule")
            scs = allsc[lo:hi + 1]
        if length(lo, hi) < 65:
            msg = f"reel {r['id']}: only {length(lo, hi):.1f} s even with neighbouring scenes; not rendered"
            print("  " + msg)
            report["reels"].append({"id": r["id"], "problems": [msg]})
            rc = 1
            continue
        t0 = scs[0]["first_word"] - 0.35
        t1 = scs[-1]["end"]
        span = t1 - t0
        total = round(span + end_s, 3)
        shift = lambda x: round(x - t0, 3)   # noqa: E731
        scenes = []
        for k, s in enumerate(scs):
            s2 = dict(s)
            s2["start"] = 0.0 if k == 0 else shift(s["start"])
            s2["end"] = shift(s["end"]) if k < len(scs) - 1 else round(span, 3)
            s2["words"] = [Word(w.text, shift(w.start), shift(w.end)) for w in s["words"]]
            s2["marks"] = [{**m, "start": shift(m["start"]), "end": shift(m["end"])} for m in s["marks"]]
            scenes.append(s2)
        words = [w for s in scenes for w in s["words"] if w.start < span]
        rdir = out / "reels" / r["id"]
        rdir.mkdir(parents=True, exist_ok=True)
        clip = rdir / "voice.wav"
        a_from = t0 - tm["vstart"]
        ffmpeg.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{max(0.0, a_from):.3f}", "-t", f"{span - 0.1:.3f}", "-i", str(tm["wav"]),
                    "-af", f"afade=t=out:st={max(0.0, span - 0.6):.3f}:d=0.5", "-c:a", "pcm_s16le", str(clip)])
        seg = {"lang": lang, "title": r.get("title", ""), "total": total, "scenes": scenes,
               "heads": [{"start": 0.0, "end": span, "kicker": r.get("kicker", ""), "title": ""}],
               "captions": group_phrases(words, min_words=2, max_words=4),
               "endcard": {"start": round(span, 3), "dur": end_s, "lines": ENDCARD[lang]},
               "voice": clip, "voice_start": 0.0, "voice_seconds": ffmpeg.audio_duration(clip)}
        r_ins, r_probs = [], []                    # inserts of the reel: phrase of the chapter -> reel seconds
        for ins in r.get("inserts", []):
            found, pr = resolve_inserts({"id": cid, "inserts": [ins]}, tm)
            r_probs += pr
            for it in found:
                st = round(it["start"] - t0, 3)
                if st < 0.0 or st > span - 2.0:
                    r_probs.append(f"{r['id']}: insert '{ins['at']}' lies outside the reel ({st:.1f} s)")
                    continue
                r_ins.append({**it, "start": st, "dur": round(min(it["dur"], span - st - 0.3), 3)})
        seg["inserts"] = r_ins
        for p_ in r_probs:
            print("  reel", r["id"], "problem:", p_)
        res = compose.build(seg, f, rdir / "project")
        res["problems"] = list(res["problems"]) + r_probs
        for p in res["problems"]:
            print(f"  reel {r['id']} problem:", p)
        entry = {"id": r["id"], "seconds": total, "problems": res["problems"]}
        if not (65 <= total <= 95):
            entry["problems"].append(f"length {total:.1f} s outside 65-95 s")
            print(f"  reel {r['id']}: length {total:.1f} s outside 65-95 s")
        if not a.no_render:
            from longform import tonmix
            mixrep = tonmix.mix_reel(plan["video_id"], r["id"], clip, scenes, r_ins, span, total, rdir / "ton", brand_dir=HERE.parent)
            entry["sound"] = {k: mixrep[k] for k in ("cues", "measured", "problems")}
            secs = render_project(rdir / "project", rdir / "video.mp4", total, a.workers, audio=Path(mixrep["path"]))
            entry["render_seconds"] = round(secs, 1)
            ffmpeg.extract_frame(rdir / "video.mp4", rdir / "frame_03s.jpg", 3.0)
            print(f"  reel {r['id']}: {total:.1f} s, render {secs:.0f} s")
        if a.overlap:
            entry["overlap"] = overlap(rdir / "project")
            print(f"  overlap {r['id']}: exit {entry['overlap']['exit']}")
        report["reels"].append(entry)
    (out / "report_reels.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
