"""Bookkeeping of the daily runner: video ids, state file, Redaktionsplan.csv rows, Konzeptplan markers."""
from __future__ import annotations

import csv
import io
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from ..config import DATA_DIR, STORAGE_DIR
from .settings import LOCK_FILE, REDAKTIONSPLAN, STATE_FILE
from .topics import Topic

PLATFORMS = "TikTok, Instagram Reels, YouTube Shorts"


def csv_done_stems(brand_id: str, path: Path = REDAKTIONSPLAN) -> set[str]:
    """Calendar stems (<brand>-<date>-<n>) of Redaktionsplan rows with status fertig/geplant/veröffentlicht."""
    out: set[str] = set()
    if not path.exists():
        return out
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            if row.get("Status") not in ("fertig", "geplant", "veröffentlicht"):
                continue
            m = re.match(rf"^({re.escape(brand_id)}-\d{{8}}-\d+)", row.get("ID", ""))
            if m:
                out.add(m.group(1))
    return out


def csv_done_titles(brand_id: str, path: Path = REDAKTIONSPLAN) -> list[str]:
    """Normalised titles of the brand's Redaktionsplan rows with status fertig/geplant/veröffentlicht (DE/EN suffix removed), so a topic whose
    video exists under another id (test videos, Tagesläufer ids with -d<n>-) is not produced twice. Never raises."""
    from .topics import _norm
    out: list[str] = []
    try:
        if not path.exists():
            return out
        with path.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh, delimiter=";"):
                if row.get("Status") not in ("fertig", "geplant", "veröffentlicht") or not str(row.get("ID", "")).startswith(brand_id + "-"):
                    continue
                title = re.sub(r"\((?:[^()]*,\s*)?(?:DE|EN)\)\s*$", "", str(row.get("Thema", "")), flags=re.I)
                n = _norm(title)
                if len(n) >= 12:
                    out.append(n)
    except Exception:  # noqa: BLE001
        return []
    return out


def next_slot(brand_id: str, yyyymmdd: str) -> int:
    """Next free topic number for <brand>-<date>-<n>-<lang> (plans and renders of that day count)."""
    used: set[int] = set()
    pat = re.compile(rf"^{re.escape(brand_id)}-{yyyymmdd}-d?(\d+)-(?:de|en)")
    for folder in (DATA_DIR / "direction", STORAGE_DIR / "direction"):
        if folder.exists():
            for p in folder.iterdir():
                m = pat.match(p.name)
                if m:
                    used.add(int(m.group(1)))
    n = 1
    while n in used:
        n += 1
    return n


def next_version(video_id: str, prefix: str) -> str:
    n = 1
    while (STORAGE_DIR / "direction" / f"{video_id}-{prefix}{n}").exists() or (DATA_DIR / "direction" / f"{video_id}.{prefix}{n}.json").exists():
        n += 1
    return f"{prefix}{n}"


class State:
    def __init__(self, path: Path = STATE_FILE):
        self.path = path
        self.data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"brands": {}, "tts": {}}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _brand(self, brand_id: str) -> dict:
        return self.data.setdefault("brands", {}).setdefault(brand_id, {"done": [], "started": []})

    def done_keys(self, brand_id: str) -> set[str]:
        return {d.get("key") for d in self._brand(brand_id).get("done", [])}

    def is_done(self, brand_id: str, topic: Topic) -> bool:
        return topic.key in self.done_keys(brand_id)

    def done_list(self, brand_id: str) -> list[dict]:
        return list(self._brand(brand_id).get("done", []))

    def last_done(self, brand_id: str) -> dict | None:
        done = self._brand(brand_id).get("done", [])
        return done[-1] if done else None

    def mark_done(self, brand_id: str, topic: Topic, date: str, video_ids: list[str], aufbau: str | None, status: dict) -> None:
        self._brand(brand_id).setdefault("done", []).append({
            "key": topic.key, "nr": topic.nr, "title": topic.title, "date": date, "video_ids": video_ids,
            "aufbau": aufbau, "status": status, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        self.save()

    def mark_started(self, brand_id: str, topic: Topic, date: str, video_ids: list[str]) -> None:
        self._brand(brand_id).setdefault("started", []).append({"key": topic.key, "date": date, "video_ids": video_ids})
        self.save()

    def tts_used(self, brand_id: str, date: str, kind: str = "flash") -> int:
        return int(self.data.setdefault("tts", {}).get(date, {}).get(brand_id, {}).get(kind, 0))

    def tts_add(self, brand_id: str, date: str, kind: str = "flash", n: int = 1) -> None:
        day = self.data.setdefault("tts", {}).setdefault(date, {})
        day.setdefault(brand_id, {})[kind] = day.get(brand_id, {}).get(kind, 0) + n
        self.save()


def csv_row(video_id: str, title: str, lang: str, duration_s: float | None, brand_name: str, folder_rel: str, note: str) -> str:
    fmt = f"Kurzvideo 9:16, {duration_s:.1f} s".replace(".", ",") if duration_s else "Kurzvideo 9:16"
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
    w.writerow([video_id, f"{title} ({lang.upper()})", fmt, f"{brand_name}: {PLATFORMS}", "fertig", "", "", folder_rel, "", note])
    return buf.getvalue()


def append_csv_row(row: str, path: Path = REDAKTIONSPLAN) -> None:
    """Append one row in append mode (other sessions write the same file; never rewrite the whole file). Keeps BOM and CRLF."""
    if not path.exists():
        path.write_bytes(b"\xef\xbb\xbf")
    with path.open("r+b") as fh:
        fh.seek(0, 2)
        size = fh.tell()
        if size:
            fh.seek(size - 1)
            last = fh.read(1)
            fh.seek(0, 2)
            if last != b"\n":
                fh.write(b"\r\n")
        fh.write(row.encode("utf-8"))


def mark_konzeptplan(path: Path, topic: Topic, marker: str) -> list[str]:
    """Append `marker` to the topic's proposal row and day-table row. The rows are found by their text as read when the
    run started (the brand sessions edit the same file, so line numbers from then may be stale); a row that changed since
    is not marked and reported. Every line keeps its own ending (CRLF, LF or mixed)."""
    text = path.read_bytes().decode("utf-8")
    parts = re.findall(r"[^\n]*\n|[^\n]+", text)
    done: list[str] = []

    def mark(original: str | None, cell_index: int | None, what: str) -> None:
        if not original:
            return
        for i, part in enumerate(parts):
            body = part.rstrip("\r\n")
            end = part[len(body):]
            if body != original:
                continue
            if marker in body:
                return
            inner = body.strip()
            cells = inner[1:-1].split("|") if inner.startswith("|") and inner.endswith("|") else None
            if cells is None:
                new_body = body.rstrip() + f" · {marker}"
            else:
                idx = cell_index if cell_index is not None and cell_index < len(cells) else len(cells) - 1
                cells[idx] = cells[idx].rstrip() + f" · {marker} "
                new_body = "|" + "|".join(cells) + "|"
            parts[i] = new_body + end
            done.append(f"{what} Zeile {i + 1}")
            return
        done.append(f"{what}: Zeile inzwischen geändert, nicht markiert")

    mark(topic.extra.get("row_text"), None, "Vorschlag")
    mark(topic.extra.get("day_text"), topic.extra.get("day_cell"), "Tagestabelle")
    if any("geändert" not in d for d in done):
        path.write_bytes("".join(parts).encode("utf-8"))
    return done


def flash_used_since_quota_reset(path: Path | None = None) -> int:
    """Gemini TTS requests of all sessions since the last quota reset (midnight Pacific), from data/costs/costs.jsonl.
    Pro requests count too (conservative); failed 429 attempts are not logged and therefore not counted."""
    from datetime import timedelta
    from zoneinfo import ZoneInfo
    path = path or (DATA_DIR / "costs" / "costs.jsonl")
    if not path.exists():
        return 0
    la = ZoneInfo("America/Los_Angeles")
    now = datetime.now(timezone.utc)
    reset = now.astimezone(la).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines()[-4000:]:
        if not line.strip():
            continue
        try:
            e = json.loads(line)
            at = datetime.fromisoformat(e["at"])
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
        if at >= reset and e.get("kind") == "tts" and e.get("provider") == "gemini":
            n += 1
    return n


def pid_alive(pid: int) -> bool:
    """True when a process with this id is running (Windows: OpenProcess; os.kill(pid, 0) would send Ctrl+C there)."""
    if pid <= 0:
        return False
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except OSError:
            return True
        return True
    import ctypes
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    handle = kernel32.OpenProcess(0x1000, False, pid)        # PROCESS_QUERY_LIMITED_INFORMATION
    if not handle:
        return ctypes.get_last_error() == 5                  # access denied: the process exists
    code = ctypes.c_ulong()
    ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
    kernel32.CloseHandle(handle)
    return bool(ok) and code.value == 259                    # STILL_ACTIVE


class RunLock:
    """One daily run at a time (a manual start while the scheduled task runs would produce every topic twice).
    The lock is a small file; a run refreshes its modification time with every log line. A lock counts as left behind by a
    crashed or stopped run when its process is gone or when it is older than `STALE_S` without a sign of life. Nothing is
    deleted: a finished run writes "released" into the file."""
    STALE_S = 3 * 3600

    def __init__(self, path: Path = LOCK_FILE):
        self.path = path

    def acquire(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            content = self.path.read_text(encoding="utf-8")
            held = not content.startswith("released")
            m = re.search(r"pid (\d+)", content)
            owner_gone = bool(m) and not pid_alive(int(m.group(1)))
            if held and not owner_gone and time.time() - self.path.stat().st_mtime < self.STALE_S:
                return False
        self.path.write_text(f"held pid {os.getpid()} since {datetime.now().isoformat(timespec='seconds')}\n", encoding="utf-8")
        return True

    def release(self) -> None:
        if self.path.exists() and f"pid {os.getpid()} " in self.path.read_text(encoding="utf-8"):
            self.path.write_text(f"released {datetime.now().isoformat(timespec='seconds')}\n", encoding="utf-8")

    @staticmethod
    def heartbeat(path: Path = LOCK_FILE) -> None:
        try:
            os.utime(path, None)
        except OSError:
            pass
