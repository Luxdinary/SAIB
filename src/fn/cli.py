"""Command line: python -m fn.cli <command>

  status                      state counts, free space, queue
  calendar init <brand> [--start YYYY-MM-DD] [--days 30]
  calendar check <file>
  script check <file>
  produce <script.md> [--tts mock|gemini|edge] [--quality draft|looks] [--no-gpu]
  validate <video_id>         re-run the report on an existing folder
  publish --dry-run [--publisher mock|upload-post] [--video <id>]
  costs [<video_id>]
  demos                       render the nine 10-second demos (scripts/render_demos.py)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from . import calendar as cal
from . import queue, scripting
from .config import DATA_DIR, ensure_dirs
from .costs import CostLogger
from .disk import check_free_space
from .publishing import build_request, get_publisher
from .state import StateDB


def cmd_status(_: argparse.Namespace) -> int:
    ensure_dirs()
    db = StateDB()
    print(check_free_space().message)
    print("states:", json.dumps(db.counts()))
    for s in queue.STAGES:
        print(f"queue/{s}: {queue.list_stage(s)}")
    return 0


def cmd_calendar(a: argparse.Namespace) -> int:
    if a.action == "init":
        start = date.fromisoformat(a.start) if a.start else date.today()
        rows = cal.build_grid(a.brand, start, a.days)
        path = cal.calendar_path(a.brand, start)
        if path.exists() and not a.force:
            print(f"exists: {path} (use --force)")
            return 1
        cal.save(rows, path)
        print(f"wrote {len(rows)} slots to {path}")
        return 0
    rows = cal.load(Path(a.file))
    problems = cal.validate(rows)
    print("\n".join(problems) if problems else f"ok: {len(rows)} rows")
    return 1 if problems else 0


def cmd_script(a: argparse.Namespace) -> int:
    s = scripting.load(Path(a.file))
    problems = scripting.check(s)
    print(f"{s.topic_id} {s.language}: {s.word_count} words, {len(s.scenes)} scenes, {len(s.sources)} sources")
    print("\n".join(problems) if problems else "ok")
    return 1 if problems else 0


def cmd_produce(a: argparse.Namespace) -> int:
    from .pipeline import produce
    res = produce(Path(a.script), tts_provider=a.tts, quality=a.quality, gpu=not a.no_gpu, workers=a.workers,
                  force_mock_words=a.mock_words)
    print(json.dumps({"video_id": res.video_id, "state": res.state, "folder": str(res.folder), "message": res.message,
                      "cost": res.cost, "failures": [f for f in res.report.get("findings", []) if not f["ok"]]}, indent=2, ensure_ascii=False))
    return 0 if res.state in ("APPROVED", "HUMAN_REVIEW") else 1


def cmd_publish(a: argparse.Namespace) -> int:
    db = StateDB()
    pub = get_publisher(a.publisher, dry_run=not a.live)
    if a.live and a.publisher == "upload-post":
        print("refusing: live upload needs Stefan's explicit go in Phase 2 (and an API key)")
        return 2
    ids = [a.video] if a.video else [v["video_id"] for v in db.list(state="APPROVED")]
    for vid in ids:
        found = queue.find(vid)
        if not found:
            print(f"{vid}: not in queue")
            continue
        stage, folder = found
        post = json.loads((folder / "post.json").read_text(encoding="utf-8"))
        v = db.get(vid) or {}
        if v.get("state") != "APPROVED":
            print(f"{vid}: state {v.get('state')} is not APPROVED, skipped")
            continue
        when = v.get("publish_at") or a.scheduled or "2026-12-01T12:00:00+01:00"
        for platform in ("tiktok", "instagram", "youtube"):
            prior = db.publish_request(vid, platform)
            if prior and prior["status"] in ("scheduled", "published"):
                print(f"{vid}/{platform}: already {prior['status']} ({prior['request_id']})")
                continue
            req = build_request(vid, platform, f"{post['brand_id']}", str(folder / "video.mp4"), post, when)
            resp = pub.schedule(req)
            print(f"{vid}/{platform}: {resp.status} {resp.message}")
            if resp.status in ("scheduled", "duplicate"):
                db.record_publish_request(vid, platform, req.external_id, "scheduled", resp.request_id, resp.raw)
        if not pub.dry_run and all((db.publish_request(vid, p) or {}).get("status") == "scheduled" for p in ("tiktok", "instagram", "youtube")):
            db.transition(vid, "SCHEDULED", "social_publisher", f"via {pub.name}")
    return 0


def cmd_costs(a: argparse.Namespace) -> int:
    c = CostLogger()
    if a.video_id:
        print(json.dumps(c.summary(a.video_id), indent=2))
    else:
        ids = sorted({e["video_id"] for e in c.entries()})
        for vid in ids:
            s = c.summary(vid)
            print(f"{vid}: {s['usd_variable']:.4f} USD variable, render {s['render_seconds']:.0f} s")
    return 0


def cmd_validate(a: argparse.Namespace) -> int:
    found = queue.find(a.video_id)
    if not found:
        print("not found")
        return 1
    _, folder = found
    rep = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep.get("passed") else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fn")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    c = sub.add_parser("calendar")
    c.add_argument("action", choices=["init", "check"])
    c.add_argument("brand", nargs="?")
    c.add_argument("--file")
    c.add_argument("--start")
    c.add_argument("--days", type=int, default=30)
    c.add_argument("--force", action="store_true")
    c.set_defaults(fn=lambda a: cmd_calendar(a) if a.action == "init" else cmd_calendar(argparse.Namespace(action="check", file=a.file or a.brand)))
    s = sub.add_parser("script")
    s.add_argument("action", choices=["check"])
    s.add_argument("file")
    s.set_defaults(fn=cmd_script)
    pr = sub.add_parser("produce")
    pr.add_argument("script")
    pr.add_argument("--tts", default=None)
    pr.add_argument("--quality", default="looks")
    pr.add_argument("--workers", default="4")
    pr.add_argument("--no-gpu", action="store_true")
    pr.add_argument("--mock-words", action="store_true")
    pr.set_defaults(fn=cmd_produce)
    pb = sub.add_parser("publish")
    pb.add_argument("--publisher", default="mock")
    pb.add_argument("--dry-run", action="store_true", default=True)
    pb.add_argument("--live", action="store_true")
    pb.add_argument("--video")
    pb.add_argument("--scheduled")
    pb.set_defaults(fn=cmd_publish)
    co = sub.add_parser("costs")
    co.add_argument("video_id", nargs="?")
    co.set_defaults(fn=cmd_costs)
    va = sub.add_parser("validate")
    va.add_argument("video_id")
    va.set_defaults(fn=cmd_validate)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
