"""Topics from the Konzeptplan markdown of a brand: proposal tables, day tables, Bildaufbau tables, selection.

The Konzeptplan files (OneDrive\\Business\\04 Redaktionsplan\\Konzeptplan <Marke> (ab November 2026).md) differ per
brand; this module reads them generically: every markdown table is parsed with its header, the nearest heading and
its line numbers. Proposal tables have a `Nr` and a `Thema` column; day tables start with a `Tag` column; Bildaufbau
tables map a letter A-E to a description. Selection order: day table rows (all days, in order), then the
proposal table(s) in table order (optionally restricted to `then_nrs` / `feasible_nrs`), skipping topics that are
done (state file or a marker in the row) and topics without sources when `require_sources` is set.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from pathlib import Path

_DONE_WORDS = ("Tagesläufer: produziert", "Pilot produziert", "(Pilot fertig)", "✔", "produziert am")


@dataclass
class Table:
    heading: str
    header: list[str]
    rows: list[list[str]]
    header_line: int
    row_lines: list[int]

    @property
    def norm_header(self) -> list[str]:
        return [_norm(h) for h in self.header]

    def col(self, *names: str) -> int | None:
        nh = self.norm_header
        for n in names:
            n = _norm(n)
            for i, h in enumerate(nh):
                if h == n or h.startswith(n):
                    return i
        return None


@dataclass
class Topic:
    brand_id: str
    nr: str | None
    title: str
    reihe: str = ""
    bereich: str = ""
    hook_idea: str = ""
    source_state: str = ""
    risk: str = ""
    aufbau: str | None = None          # planned Bildaufbau letter (table or day table)
    aufbau_note: str = ""
    material_hint: str = ""
    new_image_hint: str = ""
    day: str | None = None
    slot: int | None = None
    row_line: int | None = None        # line of the proposal row (for the marker)
    day_line: int | None = None        # line of the day-table row
    calendar_id: str | None = None
    done_marker: bool = False
    reserved: bool = False             # row says "reserviert" (brand session builds it) or its day is in reserved_days
    unmatched: bool = False
    notes: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return f"nr:{self.nr}" if self.nr else f"title:{_norm(self.title)}"

    def describe(self) -> str:
        parts = [f"Nr. {self.nr}" if self.nr else "ohne Nr.", self.title]
        if self.reihe:
            parts.append(f"Reihe {self.reihe}")
        if self.aufbau:
            parts.append(f"Aufbau {self.aufbau}")
        if self.day:
            parts.append(f"Tag {self.day}")
        return " · ".join(parts)


def _norm(s: str) -> str:
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[*_`„“\"'’‘(),.:;!?]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _cells(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.replace("\x00", "|").strip() for c in inner.replace("\\|", "\x00").split("|")]


def parse_tables(text: str) -> list[Table]:
    lines = text.splitlines()
    tables: list[Table] = []
    heading = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            header = _cells(line)
            rows, row_lines = [], []
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(_cells(lines[j]))
                row_lines.append(j)
                j += 1
            tables.append(Table(heading, header, rows, i, row_lines))
            i = j
            continue
        i += 1
    return tables


def section_text(text: str, heading_part: str, level: str = "##") -> str:
    """Text of the first section whose heading contains `heading_part` (up to the next heading of the same level or higher)."""
    lines = text.splitlines()
    out: list[str] = []
    inside = False
    depth = 0
    for line in lines:
        if line.startswith("#"):
            d = len(line) - len(line.lstrip("#"))
            if inside and d <= depth:
                break
            if not inside and heading_part.lower() in line.lower():
                inside = True
                depth = d
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def aufbau_table(tables: list[Table]) -> dict[str, str]:
    """Letter -> description from the Bildaufbau table (first column 'Aufbau' or 'Kürzel', no 'Tag' column)."""
    out: dict[str, str] = {}
    for t in tables:
        h0 = t.norm_header[0] if t.header else ""
        if h0.startswith("tag") or not (h0.startswith("aufbau") or h0.startswith("kuerzel")):
            continue
        for r in t.rows:
            if not r:
                continue
            m = re.match(r"\W*([A-E])\b", r[0].replace("*", ""))
            if not m:
                continue
            if m.group(1) in out:
                continue
            out[m.group(1)] = " · ".join(f"{t.header[k]}: {c}" for k, c in enumerate(r) if k < len(t.header) and c)
    return out


def proposal_tables(tables: list[Table], headings: list[str] | None = None) -> list[Table]:
    out = []
    for t in tables:
        if t.col("nr") is None or t.col("thema") is None:
            continue
        if headings and not any(h.lower() in t.heading.lower() for h in headings):
            continue
        out.append(t)
    return out


def day_tables(tables: list[Table], marker: str | None = None) -> list[Table]:
    out = []
    for t in tables:
        if not t.header or not t.norm_header[0].startswith("tag"):
            continue
        if marker and _norm(marker.strip("| ")) not in _norm(" | ".join(t.header)):
            continue
        out.append(t)
    return out


def _is_done_row(cells: list[str], title_cell: str) -> bool:
    last = cells[-1] if cells else ""
    return any(w in title_cell for w in ("(Pilot produziert)", "(Pilot fertig)", "**Testvideo**", "(Testvideo)")) or \
        any(w in last for w in _DONE_WORDS) or any("Pilot-Export" in c for c in cells)


def topics_from_proposals(brand_id: str, tables: list[Table], exclude_format_words: list[str] | None = None) -> list[Topic]:
    out: list[Topic] = []
    for t in tables:
        c_nr, c_title = t.col("nr"), t.col("thema")
        c_reihe, c_hook = t.col("reihe"), t.col("hook")
        c_src, c_risk = t.col("quellenstand"), t.col("risiko")
        c_auf, c_bereich, c_fmt = t.col("bildaufbau"), t.col("bereich"), t.col("format")
        for cells, ln in zip(t.rows, t.row_lines):
            if c_title is None or c_title >= len(cells) or c_nr >= len(cells):
                continue
            nr = cells[c_nr].strip().strip("*")
            if not re.match(r"^\d+$", nr):
                continue
            fmt = cells[c_fmt] if c_fmt is not None and c_fmt < len(cells) else ""
            if exclude_format_words and any(w.lower() in fmt.lower() for w in exclude_format_words):
                continue
            title_cell = cells[c_title]
            title = re.sub(r"\s*\((Pilot produziert|Pilot fertig|Testvideo)\)\s*", " ", title_cell).replace("**", "").strip()
            src = cells[c_src] if c_src is not None and c_src < len(cells) else ""
            m = re.search(r"([a-z_]+-\d{8}-\d+-(?:de|en))", src)
            auf = None
            if c_auf is not None and c_auf < len(cells):
                mm = re.match(r"\W*([A-E])\b", cells[c_auf])
                auf = mm.group(1) if mm else None
            out.append(Topic(brand_id=brand_id, nr=nr, title=title, reserved="reserviert" in " ".join(cells).lower(),
                             reihe=cells[c_reihe] if c_reihe is not None and c_reihe < len(cells) else "",
                             bereich=cells[c_bereich] if c_bereich is not None and c_bereich < len(cells) else "",
                             hook_idea=cells[c_hook] if c_hook is not None and c_hook < len(cells) else "",
                             source_state=src, risk=cells[c_risk] if c_risk is not None and c_risk < len(cells) else "",
                             aufbau=auf, row_line=ln, calendar_id=m.group(1) if m else None,
                             done_marker=_is_done_row(cells, title_cell),
                             extra={"format": fmt, "heading": t.heading}))
    return out


_AUFBAU_TAIL = re.compile(r"\(([A-E])(?:[,;][^)]*)?\)\s*$")


def _parse_day_cell(text: str) -> tuple[str | None, str, str | None, str]:
    """(nr, title text, aufbau letter, aufbau note) from a day-table cell like
    'Nr. 47 „Was ein KI-Chat …“, A (Chatfenster statt Mail)', 'Hadrianswall (Nr. 24)', 'Stoffgewicht (B)'."""
    s = text.replace("**", "").strip()
    s = re.sub(r"\s*(?:·\s*)?(?:reserviert\b.*|✔.*|Tagesläufer:.*)$", "", s, flags=re.I).strip()   # markers after the topic
    nr = None
    m = re.search(r"Nr\.?\s*(\d+)", s)
    if m:
        nr = m.group(1)
    auf, note = None, ""
    m2 = _AUFBAU_TAIL.search(s)
    if m2:
        auf = m2.group(1)
        inner = s[m2.start():].strip("() ")
        note = inner[1:].strip(",; ") if len(inner) > 1 else ""
        s = s[:m2.start()].strip()
    else:
        m3 = re.search(r"[“\"”],\s*([A-E])\b\s*(\(([^)]*)\))?", s)
        if m3:
            auf = m3.group(1)
            note = m3.group(3) or ""
            s = s[:m3.start() + 1].strip()
    s = re.sub(r"\(Nr\.?\s*\d+\)", "", s).strip(" ,")
    s = re.sub(r"^Nr\.?\s*\d+\s*", "", s).strip(" ,")
    s = s.strip("„“\"”")
    return nr, s, auf, note


def topics_from_day_tables(brand_id: str, tables: list[Table]) -> list[Topic]:
    """Day rows in order; each row gives one or two topics (nr or title text, planned Aufbau, material hints)."""
    out: list[Topic] = []
    for t in tables:
        nh = t.norm_header
        c_nr = t.col("nr")
        c_thema = next((i for i, h in enumerate(nh) if h == "thema"), None)
        c_auf_single = next((i for i, h in enumerate(nh) if h == "aufbau"), None)
        c_mat = t.col("material")
        c_new = next((i for i, h in enumerate(nh) if h.startswith("neues bild")), None)
        c_stand = t.col("stand")
        thema_cols = [i for i, h in enumerate(nh) if h.startswith("thema 1") or h.startswith("thema 2")]
        for cells, ln in zip(t.rows, t.row_lines):
            if not cells:
                continue
            day = cells[0].strip()
            if c_nr is not None and c_thema is not None:          # Dewlane: Tag | Nr. | Thema | Aufbau | Material | Neues Bild
                if c_nr >= len(cells):
                    continue
                nr = cells[c_nr].strip()
                if not re.match(r"^\d+$", nr):
                    continue
                auf = None
                if c_auf_single is not None and c_auf_single < len(cells):
                    mm = re.match(r"\W*([A-E])\b", cells[c_auf_single])
                    auf = mm.group(1) if mm else None
                out.append(Topic(brand_id=brand_id, nr=nr, title=cells[c_thema].strip(), aufbau=auf, day=day, slot=1,
                                 day_line=ln, reserved="reserviert" in " ".join(cells).lower(), extra={"day_cell": c_thema},
                                 material_hint=cells[c_mat] if c_mat is not None and c_mat < len(cells) else "",
                                 new_image_hint=cells[c_new] if c_new is not None and c_new < len(cells) else "",
                                 done_marker=any(w in " ".join(cells) for w in _DONE_WORDS)))
                continue
            for slot, ci in enumerate(thema_cols, 1):
                if ci >= len(cells) or not cells[ci].strip():
                    continue
                nr, title, auf, note = _parse_day_cell(cells[ci])
                # Frontlore: a separate 'Aufbau' column follows every 'Thema n' column
                if auf is None and ci + 1 < len(cells) and ci + 1 < len(nh) and nh[ci + 1] == "aufbau":
                    mm = re.match(r"\W*([A-E])\b", cells[ci + 1])
                    if mm:
                        auf = mm.group(1)
                        note = cells[ci + 1][mm.end():].strip(", ")
                stand = cells[c_stand] if c_stand is not None and c_stand < len(cells) else ""
                out.append(Topic(brand_id=brand_id, nr=nr, title=title, aufbau=auf, aufbau_note=note, day=day, slot=slot,
                                 day_line=ln, extra={"stand": stand, "day_cell": ci}, reserved="reserviert" in (cells[ci] + " " + stand).lower(),
                                 done_marker=any(w in cells[ci] for w in _DONE_WORDS) or "✔" in stand))
    return out


def match_topic(day_topic: Topic, proposals: list[Topic]) -> Topic | None:
    if day_topic.nr:
        return next((p for p in proposals if p.nr == day_topic.nr), None)
    raw_main = day_topic.title.split(",")[0] if "," in day_topic.title else day_topic.title
    want = _norm(day_topic.title)
    want_main = _norm(raw_main)
    best, best_score = None, 0.0
    for p in proposals:
        have = _norm(p.title)
        score = 0.0
        if want_main and (have.startswith(want_main) or want_main in have):
            score = 0.9 + min(0.1, len(want_main) / 100)
        else:
            tw = {w for w in want_main.split() if len(w) >= 4}
            th = {w for w in have.split() if len(w) >= 4}
            common = {w for w in tw if any(h.startswith(w[:6]) or w.startswith(h[:6]) for h in th)}
            jac = len(common) / len(tw) if tw else 0.0
            score = max(jac * 0.8, difflib.SequenceMatcher(None, want_main, have).ratio() * 0.8)
        if score > best_score:
            best, best_score = p, score
    return best if best_score >= 0.5 else None


@dataclass
class Konzeptplan:
    path: Path
    text: str
    tables: list[Table]
    proposals: list[Topic]
    day_topics: list[Topic]
    aufbauten: dict[str, str]

    @property
    def kurzkonzept(self) -> str:
        return section_text(self.text, "Kurzkonzept")

    @property
    def aufbau_section(self) -> str:
        for part in ("Bildaufbauten", "Neuausrichtung", "Neustart ab"):
            s = section_text(self.text, part)
            if s:
                return s
        return ""


def load_konzeptplan(brand_id: str, path: Path, source_cfg: dict) -> Konzeptplan:
    text = path.read_text(encoding="utf-8")
    tables = parse_tables(text)
    props = topics_from_proposals(brand_id, proposal_tables(tables, source_cfg.get("tables")),
                                  exclude_format_words=source_cfg.get("exclude_format_words"))
    days = topics_from_day_tables(brand_id, day_tables(tables, source_cfg.get("day_table_marker"))) \
        if source_cfg.get("kind") == "day_table" else []
    lines = text.splitlines()
    for p in props:                                    # raw rows as read now: the markers are placed by content, not by line number
        if p.row_line is not None and p.row_line < len(lines):
            p.extra["row_text"] = lines[p.row_line]
    for d in days:
        if d.day_line is not None and d.day_line < len(lines):
            d.extra["day_text"] = lines[d.day_line]
    return Konzeptplan(path, text, tables, props, days, aufbau_table(tables))


def limited_allowed(history: list[bool], every: int) -> bool:
    """At most one limited topic in any `every` consecutive topics: another one may follow only when none of the last
    every-1 topics was limited (Revlore: Motor topics at most every third topic, Hauptsitzung 03.11.2026)."""
    if every <= 1:
        return True
    return not any(history[-(every - 1):])


def ordered_candidates(kp: Konzeptplan, source_cfg: dict) -> list[Topic]:
    """Day-table topics first (merged with their proposal row), then the proposal order."""
    out: list[Topic] = []
    seen: set[str] = set()
    for d in kp.day_topics:
        p = match_topic(d, kp.proposals)
        if p is not None:
            merged = Topic(**{**p.__dict__})
            merged.aufbau = d.aufbau or p.aufbau
            merged.aufbau_note, merged.day, merged.slot, merged.day_line = d.aufbau_note, d.day, d.slot, d.day_line
            merged.material_hint, merged.new_image_hint = d.material_hint, d.new_image_hint
            merged.done_marker = p.done_marker or d.done_marker
            merged.reserved = p.reserved or d.reserved
            merged.extra = {**p.extra, **d.extra}
        else:
            merged = d
            merged.unmatched = True
            merged.notes.append("Tagesthema ohne passende Zeile in der Vorschlagstabelle (Titel nur aus der Tagestabelle)")
        if merged.key in seen:
            continue
        seen.add(merged.key)
        out.append(merged)
    feasible = source_cfg.get("feasible_nrs")
    then = source_cfg.get("then_nrs")
    ordered = kp.proposals
    if then:
        by_nr = {p.nr: p for p in kp.proposals}
        ordered = [by_nr[str(n)] for n in then if str(n) in by_nr] + [p for p in kp.proposals if p.nr not in {str(n) for n in then}]
    for p in ordered:
        if feasible is not None and (p.nr is None or int(p.nr) not in set(int(x) for x in feasible)):
            continue
        if p.key in seen:
            continue
        seen.add(p.key)
        out.append(p)
    return out
