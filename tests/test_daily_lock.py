"""Daily runner: one run at a time (lock file without deleting anything)."""
from __future__ import annotations

import os
import time

from fn.daily.records import RunLock


def test_second_run_is_refused_until_the_first_released(tmp_path):
    p = tmp_path / "runner.lock"
    a, b = RunLock(p), RunLock(p)
    assert a.acquire() is True
    assert b.acquire() is False                         # a is running
    a.release()
    assert p.exists() and p.read_text(encoding="utf-8").startswith("released")   # marked, not deleted
    assert b.acquire() is True


def test_stale_lock_of_a_crashed_run_is_taken_over(tmp_path):
    p = tmp_path / "runner.lock"
    p.write_text("held pid 999999 since 2026-11-03T06:30:00\n", encoding="utf-8")
    old = time.time() - RunLock.STALE_S - 60
    os.utime(p, (old, old))
    assert RunLock(p).acquire() is True


def test_heartbeat_keeps_a_lock_fresh(tmp_path):
    p = tmp_path / "runner.lock"
    a = RunLock(p)
    assert a.acquire()
    old = time.time() - RunLock.STALE_S - 60
    os.utime(p, (old, old))
    RunLock.heartbeat(p)
    assert RunLock(p).acquire() is False


def test_lock_of_a_process_that_is_gone_is_taken_over_at_once(tmp_path):
    p = tmp_path / "runner.lock"
    p.write_text("held pid 2147483000 since 2026-11-03T06:30:00\n", encoding="utf-8")     # no such process, but a fresh file
    assert RunLock(p).acquire() is True
    assert f"pid {os.getpid()} " in p.read_text(encoding="utf-8")


def test_pid_alive_knows_this_process_and_a_missing_one():
    from fn.daily.records import pid_alive
    assert pid_alive(os.getpid()) is True
    assert pid_alive(2147483000) is False
    assert pid_alive(0) is False
