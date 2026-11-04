"""Topic proposals for the gaps of a month plan: `claude -p` (Sonnet, effort low), only on request.

The Konzeptplan of a brand rarely has enough topics with a verified source and a built Bildaufbau for a whole month. The proposals
fill the *list of ideas*, never the plan: every proposal is marked "Vorschlag, Quelle prüfen", carries the sources the model
names (the model may not know a URL, then it names the institution and a search hint), gets an HTTP reachability check of its URLs
and stays out of the plan until a brand session (or Stefan) has checked the source and moved the topic into the Konzeptplan.
Output: `04 Redaktionsplan/Themenvorschläge <Marke> <YYYY-MM>.md`. Nothing here writes to a Konzeptplan, a calendar or the Redaktionsplan.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from ..config import brands_config
from .settings import brand_settings, load_aufbauten

SYSTEM = (
    "Du bist Themenplaner für eine Marke mit Kurzvideos (Reels, 9:16, 65 bis 90 Sekunden), die ohne Gesichter und ohne Sprecher vor der Kamera "
    "arbeitet. Du schlägst neue Themen vor, die zum Format und zur Stimme der Marke passen. Regeln: Jedes Thema braucht belegbare Aussagen; "
    "nenne zu jedem Thema ein bis drei Quellen (amtliche oder wissenschaftliche Seiten, Normen, Hersteller- oder Behördenseiten). "
    "Erfinde keine URLs und keine Zahlen. Kennst du die genaue URL nicht sicher, lasse `url` leer und nenne Institution, Titel und einen "
    "Suchhinweis. Schlage nur Themen vor, die nicht schon in der Liste der vorhandenen Titel stehen, und ordne sie einer Reihe der Marke zu. "
    "Bei gesundheitlichen, rechtlichen oder finanziellen Themen setze das Risiko auf hoch. Antworte nur mit einem JSON-Objekt."
)


def _read(path: Path | None, limit: int) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")[:limit]


def build_prompt(brand_id: str, n: int, existing_titles: list[str], sample_rows: list[str], series: list[str]) -> tuple[str, str]:
    s = brand_settings(brand_id)
    entry = next((b for b in brands_config()["brands"] if b["id"] == brand_id), {})
    bible = _read(s.business_path("format_bible"), 3500)
    built = [f"{a['kuerzel']} {a.get('name', '')}" for a in load_aufbauten(brand_id) if a.get("gebaut")]
    user = "\n".join([
        f"## Marke {s.name} ({brand_id})",
        f"Themenfeld: {entry.get('niche', '–')}. Standardrisiko: {entry.get('risk_default', '–')}.",
        "Regeln der Marke: " + "; ".join(entry.get("rules") or []),
        "",
        "## Format-Bibel (Auszug)",
        bible or "(keine)",
        "",
        "## Muster aus dem Konzeptplan (Nr | Thema | Reihe | Hook | Quellenstand | Risiko)",
        *sample_rows,
        "",
        "Reihen der Marke: " + ", ".join(series[:20]),
        "Gebaute Bildaufbauten: " + (", ".join(built) or "keine"),
        "",
        "## Vorhandene Titel (nicht wiederholen)",
        "; ".join(t[:70] for t in existing_titles[:160]),
        "",
        f"## Aufgabe: {n} neue Themenvorschläge",
        'Gib ein JSON-Objekt aus: {"vorschlaege": [{"titel": "", "reihe": "", "hook": "ein Satz", "bildaufbau": "Buchstabe eines gebauten Aufbaus",'
        ' "risiko": "niedrig|mittel|hoch", "quellen": [{"titel": "", "institution": "", "url": "", "suchhinweis": ""}], "hinweis": "was zu prüfen ist"}]}',
    ])
    return SYSTEM, user


def parse_proposals(text: str) -> list[dict]:
    """The proposals list from the model answer (JSON object, possibly inside a code fence)."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("keine JSON-Antwort")
    data = json.loads(m.group(0))
    items = data.get("vorschlaege") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError('Antwort ohne Liste "vorschlaege"')
    out = []
    for it in items:
        if isinstance(it, dict) and str(it.get("titel", "")).strip():
            qs = [q for q in (it.get("quellen") or []) if isinstance(q, dict)]
            out.append({"titel": str(it["titel"]).strip(), "reihe": str(it.get("reihe", "")).strip(), "hook": str(it.get("hook", "")).strip(),
                        "bildaufbau": str(it.get("bildaufbau", "")).strip()[:1], "risiko": str(it.get("risiko", "")).strip(),
                        "quellen": qs, "hinweis": str(it.get("hinweis", "")).strip()})
    return out


def check_urls(proposals: list[dict], timeout: float = 10.0) -> None:
    """Mark every URL of every source as reachable or not (HTTP HEAD, GET on 403/405). Names only a status; changes no text."""
    try:
        import requests
    except ImportError:
        return
    headers = {"User-Agent": "Mozilla/5.0 (faceless-network month planner; source check)"}
    for p in proposals:
        for q in p["quellen"]:
            url = str(q.get("url", "")).strip()
            if not re.match(r"^https?://\S+$", url):
                q["status"] = "keine URL" if not url else "ungültige URL"
                continue
            try:
                r = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
                if r.status_code in (403, 405) or r.status_code >= 500:
                    r = requests.get(url, headers=headers, timeout=timeout, stream=True)
                q["status"] = "erreichbar" if r.status_code < 400 else f"HTTP {r.status_code}"
            except Exception:  # noqa: BLE001
                q["status"] = "nicht erreichbar"


def propose(brand_id: str, n: int, existing_titles: list[str], sample_rows: list[str], series: list[str], provider, costs, cfg: dict,
            month: str, check: bool = True) -> list[dict]:
    from .llm import log_llm_cost
    system, user = build_prompt(brand_id, n, existing_titles, sample_rows, series)
    res = provider.complete(system, user, max_tokens=int(cfg.get("proposal_max_tokens", 12000)), temperature=0.5)
    log_llm_cost(costs, f"monthplan-{month}-{brand_id}", "topic proposals", res, cfg)
    items = parse_proposals(res.text)
    if check:
        check_urls(items)
    return items


def proposals_markdown(brand_name: str, brand_id: str, month: str, items: list[dict], created: str) -> str:
    L = [f"# Themenvorschläge {brand_name} {month}", "",
         f"Stand {created}. Erzeugt von `scripts/month_planner.py` mit `claude -p` (Sonnet, effort low). **Vorschlag, Quelle prüfen:** nichts davon ist "
         "eingeplant. Ein Thema wird erst einplanbar, wenn die Quelle geprüft ist und es im Konzeptplan der Marke steht (mit Quelle, Bildaufbau, Risiko). "
         "Die URLs hat das Modell genannt; der Spalte Status ist nur zu entnehmen, ob die Seite erreichbar war, nicht ob sie die Aussage belegt.", ""]
    if not items:
        L.append("Keine Vorschläge.")
        return "\n".join(L) + "\n"
    L += ["| Nr. | Titel | Reihe | Bildaufbau | Risiko | Hook | Quellen (Status) | Prüfhinweis |", "|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(items, 1):
        qs = "; ".join(f"{(q.get('institution') or q.get('titel') or '–')}: {(q.get('url') or q.get('suchhinweis') or '–')} ({q.get('status', 'ungeprüft')})"
                       for q in p["quellen"]) or "keine genannt"
        row = [f"V{i}", p["titel"], p["reihe"] or "–", p["bildaufbau"] or "–", p["risiko"] or "–", p["hook"] or "–", qs, p["hinweis"] or "–"]
        L.append("| " + " | ".join(c.replace("|", "/").replace("\n", " ") for c in row) + " |")
    L.append("")
    L.append("Status aller Vorschläge: **Vorschlag, Quelle prüfen**, nicht einplanbar bis geprüft.")
    return "\n".join(L) + "\n"
