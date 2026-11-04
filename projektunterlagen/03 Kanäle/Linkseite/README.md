# Linkseiten mit Impressum (alle Marken)

Stand: 04.11.2026 (Wien), Entwurf von Claude, **nicht veröffentlicht**.

## Was hier liegt

- `<marke>.html` (neun Seiten): Markenname, Kurzbeschreibung DE und EN (Instagram-Bio aus dem Profilpaket), Knöpfe zu TikTok, Instagram und YouTube, Sprung zum Impressum, Impressum und Offenlegung auf derselben Seite (ein Klick vom Profil-Link, die Vorgabe „höchstens zwei Klicks“ ist damit erfüllt). Tintora zusätzlich mit dem Hinweis zur Familienserie. Farben aus `brands\<id>\brand.yaml`. Keine Schriften oder Skripte von fremden Servern, keine Cookies, kein Tracking.
- `index.html`: Vorschau-Liste aller Seiten.
- `impressum.json`: die Impressum-Angaben für alle Seiten an einer Stelle.
- `build_linkseiten.py`: baut alle Seiten neu (`python build_linkseiten.py`), nach jeder Änderung an `impressum.json` oder an einem Profilpaket.

## Bevor das online geht (Stefan)

1. **Impressum ergänzen:** Gewerbeberechtigung und Behörde (GISA), Kammer und Fachgruppe, Umsatzsteuer-Nummer oder Kleinunternehmer-Hinweis. Diese drei Zeilen stehen auf den Seiten noch als Platzhalter in eckigen Klammern. Das gleiche ist im Scutoria-Impressum offen. Ob für die Videokanäle ein eigenes Gewerbe nötig ist, ist offen (Faktencheck: für Werbung und Kooperationen in der Regel Gewerbe „Werbeagentur“, WKO, Stand 20.03.2026). Keine Rechtsberatung.
2. **Anschrift prüfen:** übernommen aus dem Scutoria-Impressum; dort steht „Hausnummer aus dem Stripe-Konto, Stand prüfen“.
3. **Unternehmensgegenstand und grundlegende Richtung** sind Vorschläge von Claude; bitte bestätigen oder ändern.
4. **Ort der Veröffentlichung** wählen (unten).

## Wo veröffentlichen

| Weg | Adresse je Marke | Für | Gegen |
|---|---|---|---|
| **Empfohlen:** Unterseiten auf scutoria.com (Lovable) | `scutoria.com/links/<marke>` | eigene Domain, kein neuer Dienst, keine Kosten | Veröffentlichen bei Lovable nur auf Stefans Wort (Scutoria-Regeln); zeigt die Verbindung aller Marken zu Scutoria |
| Eigene Domain je Marke | z. B. `tintora.tv` | sauber getrennte Marken | Domainkosten je Marke, mehr Pflege |
| Linkdienst (z. B. Linktree) | `linktr.ee/<marke>` | schnell | Impressum dort nur eingeschränkt, fremder Dienst |

Die Verbindung zu Scutoria ist ohnehin im Impressum sichtbar (gleicher Medieninhaber, gleiche Anschrift).
