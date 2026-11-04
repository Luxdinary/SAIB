# Vorschlag: Ordnerstruktur für den Regelbetrieb

Stand: 30.10.2026, 22:40 (Wien). **Vorschlag, nicht umgesetzt.** Laut `CLAUDE.md` ändert Claude die Ordnerstruktur nur nach Stefans Freigabe.

## Warum

Im Regelbetrieb entstehen je Marke 3 Videos am Tag, bei 9 Marken also 27 Videos am Tag und rund 800 im Monat. Mit einem flachen Ordner `05 Produktion` mit einem Unterordner je Video wird das unübersichtlich. Der Ordner wächst außerdem schnell in OneDrive: Ein fertiges Video belegt mit Cover und Untertiteln etwa 20 bis 60 MB.

## Vorschlag

| Ordner | heute | Vorschlag |
|---|---|---|
| `05 Produktion` | ein Ordner je Video | `05 Produktion\<Marke>\<JJJJ-MM>\JJJJ-MM-TT Kurztitel`; `_Vorlage Video` bleibt oben |
| `05 Produktion\_Demos`, `_Test` | Vorschauen aller Fassungen, 620 MB | nach Freigabe der Testvideos nach `C:\Users\Stefa\Documents\_zum_loeschen\…` verschieben; künftig liegen Vorschauen nur im Code-Ordner |
| `04 Redaktionsplan` | eine CSV für alles, Themenpläne als Dateien | Themenpläne in `04 Redaktionsplan\<JJJJ-MM>\`; die CSV bleibt die eine Liste aller Veröffentlichungen |
| `07 Auswertung` | leer | `07 Auswertung\<JJJJ-MM>\` mit Exporten und Monatsauswertung |
| `03 Kanäle` | ein Ordner je Marke | bleibt so |

Für fertige Monate gilt: In OneDrive „Nur online verfügbar“ einstellen, damit C: nicht vollläuft.

## Was Stefan entscheidet

1. Gilt die Struktur „Marke, dann Monat“ für `05 Produktion`?
2. Dürfen `_Demos` und `_Test` nach der Freigabe der Testvideos in den Löschordner?
