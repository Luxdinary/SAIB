"""Hook engine: at least five hook candidates per video, one per hook type, scored on five criteria.

The strongest *defensible* hook wins, not the most dramatic one: a candidate whose `truth` score is
below TRUTH_GATE is ineligible regardless of its other scores. Scores are integers 1-5 given by the
script writer (Claude) with a one-line justification each; the engine only ranks and validates.
"""
from __future__ import annotations

from dataclasses import dataclass, field

HOOK_TYPES: dict[str, str] = {
    "question": "provokante, sachlich vertretbare Frage",
    "misconception": "haeufiger Denkfehler",
    "surprising_fact": "ueberraschender, belegbarer Sachverhalt",
    "concrete_risk": "konkretes Risiko aus dem Alltag der Zielgruppe",
    "demonstration": "sichtbare Demonstration",
}
CRITERIA: dict[str, float] = {        # weights
    "clarity": 1.0,
    "relevance": 1.2,
    "curiosity": 1.2,
    "truth": 1.5,
    "visual": 1.0,
}
TRUTH_GATE = 4
MAX_CHARS = 90          # spoken hook, one sentence
MAX_ON_SCREEN = 64      # on-screen question/claim (3 lines at 84 px)


@dataclass
class HookCandidate:
    id: str
    type: str
    spoken: str                      # the sentence the voice says
    on_screen: str                   # the big text in the Cinematic Hook scene
    scores: dict[str, int]
    source_ids: list[str] = field(default_factory=list)
    visual: str = ""                 # one line: what moves on screen
    why: dict[str, str] = field(default_factory=dict)   # justification per criterion

    @property
    def eligible(self) -> bool:
        return not self.problems()

    def problems(self) -> list[str]:
        p = []
        if self.type not in HOOK_TYPES:
            p.append(f"{self.id}: unknown hook type {self.type!r}")
        for c in CRITERIA:
            v = self.scores.get(c)
            if not isinstance(v, int) or not 1 <= v <= 5:
                p.append(f"{self.id}: score {c} must be an integer 1-5")
        if self.scores.get("truth", 0) < TRUTH_GATE:
            p.append(f"{self.id}: truth {self.scores.get('truth')} below gate {TRUTH_GATE} (not defensible)")
        if len(self.spoken) > MAX_CHARS:
            p.append(f"{self.id}: spoken hook longer than {MAX_CHARS} chars")
        if len(self.on_screen) > MAX_ON_SCREEN:
            p.append(f"{self.id}: on-screen text longer than {MAX_ON_SCREEN} chars")
        if self.type in ("surprising_fact", "misconception", "concrete_risk") and not self.source_ids:
            p.append(f"{self.id}: a {self.type} hook needs at least one source id")
        return p

    @property
    def score(self) -> float:
        """Weighted score normalised to 0..100. Ineligible candidates score 0."""
        if not self.eligible:
            return 0.0
        total = sum(self.scores[c] * w for c, w in CRITERIA.items())
        return round(100.0 * total / (5 * sum(CRITERIA.values())), 1)

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.type, "spoken": self.spoken, "on_screen": self.on_screen,
                "scores": self.scores, "score": self.score, "eligible": self.eligible,
                "problems": self.problems(), "source_ids": self.source_ids, "visual": self.visual, "why": self.why}


def from_dict(d: dict) -> HookCandidate:
    return HookCandidate(id=d["id"], type=d["type"], spoken=d["spoken"], on_screen=d.get("on_screen", d["spoken"]),
                         scores={k: int(v) for k, v in d.get("scores", {}).items()},
                         source_ids=list(d.get("source_ids", [])), visual=d.get("visual", ""), why=dict(d.get("why", {})))


def validate_set(cands: list[HookCandidate]) -> list[str]:
    """A complete hook set has >= 5 candidates covering all five hook types."""
    p: list[str] = []
    if len(cands) < 5:
        p.append(f"only {len(cands)} hook candidates, need at least 5")
    missing = [t for t in HOOK_TYPES if not any(c.type == t for c in cands)]
    if missing:
        p.append(f"hook types not covered: {missing}")
    ids = [c.id for c in cands]
    if len(set(ids)) != len(ids):
        p.append("duplicate hook ids")
    return p


def rank(cands: list[HookCandidate]) -> list[HookCandidate]:
    """Eligible candidates first, by score; ties broken by truth, then clarity."""
    return sorted(cands, key=lambda c: (c.eligible, c.score, c.scores.get("truth", 0), c.scores.get("clarity", 0)), reverse=True)


def winner(cands: list[HookCandidate]) -> HookCandidate | None:
    ranked = rank(cands)
    return ranked[0] if ranked and ranked[0].eligible else None
