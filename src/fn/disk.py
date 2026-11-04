"""Free-space guard for C: (warn and refuse new renders under FN_MIN_FREE_GB)."""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .config import ROOT, min_free_gb


@dataclass(frozen=True)
class SpaceCheck:
    free_gb: float
    min_gb: float
    path: str

    @property
    def ok(self) -> bool:
        return self.free_gb >= self.min_gb

    @property
    def message(self) -> str:
        state = "ok" if self.ok else "WARNING: below minimum, no new renders"
        return f"free space on {self.path}: {self.free_gb:.1f} GB (minimum {self.min_gb:.0f} GB) - {state}"


def check_free_space(path: Path | None = None, minimum_gb: float | None = None) -> SpaceCheck:
    p = Path(path or ROOT)
    usage = shutil.disk_usage(str(p.anchor or p))
    return SpaceCheck(free_gb=usage.free / 1e9, min_gb=float(minimum_gb if minimum_gb is not None else min_free_gb()),
                      path=str(p.anchor or p))
