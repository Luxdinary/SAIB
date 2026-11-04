"""Write the project skills in .claude/skills/<name>/SKILL.md (thin wrappers around prompts/ and the CLI)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"

COMMON = """
Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\\Users\\Stefa\\Documents\\_zum_loeschen\\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\\Scripts\\python.exe` with `PYTHONIOENCODING=utf-8`.
"""

SKILLS_DEF = {
    "calendar-planner": ("Plan the 30-day topic calendar of one brand (angles, sources, risk, slots).",
                         "Follow `prompts/calendar_planner.md`. Create the grid with `python -m fn.cli calendar init <brand_id> --start <date>`, fill the rows, then run `python -m fn.cli calendar check --file <file>` until it prints ok."),
    "research-factcheck": ("Verify every fact for one topic against primary sources before a script is written.",
                           "Follow `prompts/research_factcheck.md`. Output the YAML sources block. Decision `needs_research` means the topic stays out of production."),
    "script-writer": ("Write the German 65-90 s script for one topic in the brand voice, with source markers.",
                      "Read `brands/<brand_id>/script_prompt.md` first, then follow `prompts/script_writer.md`. Save to `data/scripts/<topic_id>-de.md` and run `python -m fn.cli script check <file>`."),
    "localizer": ("Localise a German script into English (same scenes, same sources).",
                  "Follow `prompts/localizer.md`. Save to `data/scripts/<topic_id>-en.md` and run the script check."),
    "voice-generator": ("Generate the voice track with the configured TTS adapter (mock until a key exists).",
                        "The pipeline calls `fn.tts.get_provider()`; Gemini is used only when GEMINI_API_KEY is in `.env` (paid, logged in the cost logger). For a standalone test: `python -c \"from fn.tts import get_provider; ...\"`. Never print key values."),
    "video-producer": ("Produce one video end to end from a script (TTS, timings, HyperFrames, NVENC, checks).",
                       "`python -m fn.cli produce data/scripts/<file>.md [--tts gemini] [--quality draft|looks]`. Check free space first (`fn status`). Result folder in `storage/<stage>/<video_id>/`; read `report.json`."),
    "video-editor": ("Adjust the look of a rendered video: scenes, captions, layout, brand files.",
                     "Edit `brands/<id>/*.json|yaml|md` or `src/fn/render/compose.py`, rebuild with `fn produce`, then `npx hyperframes snapshot --at <s>` on the project folder and look at the frames before re-rendering."),
    "compliance-check": ("Review a video folder for sources, licences, AI labels, brand and platform rules.",
                         "Follow `prompts/compliance_review.md`. Write `review.md` into the video folder. Only Stefan or the auto-approval module set APPROVED."),
    "social-publisher": ("Schedule APPROVED videos through the publisher adapter (mock in Phase 1, dry-run).",
                         "`python -m fn.cli publish --dry-run [--publisher mock|upload-post]`. Live uploads need Stefan's explicit go, an API key in `.env` and Phase 2 verification of the Upload-Post endpoints."),
    "analytics-review": ("Read platform statistics and propose topics for the next days (Phase 3).",
                         "Not implemented in Phase 1. Inputs will be the Upload-Post analytics per profile; outputs go to `07 Auswertung` in OneDrive and to the idea store."),
}


def main() -> int:
    for name, (desc, body) in SKILLS_DEF.items():
        d = SKILLS / name
        d.mkdir(parents=True, exist_ok=True)
        text = f"---\nname: {name}\ndescription: {desc}\n---\n\n# {name}\n\n{body}\n{COMMON}"
        (d / "SKILL.md").write_text(text, encoding="utf-8", newline="\n")
        print("wrote", d / "SKILL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
