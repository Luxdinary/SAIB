# Faceless Network – Betriebsregeln für Claude

Angelegt 30.10.2026. Dieses Repository ist die Produktionsmaschine für Stefans KI-Kurzvideo-Netzwerk (TikTok, Instagram Reels, YouTube Shorts; Deutsch und Englisch). Planung, Konzept, Ablaufplan und Faktencheck liegen nicht hier, sondern in `C:\Users\Stefa\OneDrive\Business\01 Idee und Strategie` (dort `Konzept.md`, `Ablaufplan.md`, `Fragenkatalog.md`, `Recherche\Faktencheck 2026-10-29.md`). Der gültige Stand des Vorhabens steht in Google Drive › Claude-Gedächtnis › Übersichten › `Übersicht — Business (Video und Social Media).md`. Lies zu Beginn einer Sitzung Konzept und Ablaufplan.

Antworte auf Deutsch. Code, Bezeichner und Commit-Nachrichten auf Englisch.

## Verbindliche Regeln

- Keine Veröffentlichung ohne Status `APPROVED`. Die automatische Freigabe (Stefans Entscheidung vom 29.10.2026) setzt `APPROVED` nur, wenn alle Prüfungen bestanden sind und `risk_level` nicht `high` ist. `high` wartet auf Stefan. Claude setzt `APPROVED` nie von Hand.
- Keine erfundenen Fakten, Studien, Zitate, Zahlen. Jede Tatsachenbehauptung im Skript hat eine Quelle mit URL und Abrufdatum im Manifest; ohne Quelle Status `NEEDS_RESEARCH`, nie Produktion.
- Keine erfundenen API-Endpunkte oder Parameter. Nur dokumentierte Schnittstellen; Undokumentiertes heißt `NOT_VERIFIED`.
- Keine Zugangsdaten im Repository, in Logs oder in Ausgaben. Schlüssel nur über `.env` (siehe `.env.example`). Nie einen Schlüsselwert ausgeben, auch nicht gekürzt.
- Keine Kontoerstellung, kein Login, keine Eingabe von Passwörtern durch Claude. Konten legt Stefan an; OAuth-Verbindungen zu Upload-Post stellt Stefan her.
- Keine kostenpflichtigen Dienste aktivieren oder Tarife ändern ohne Stefans Zustimmung. Jeder Aufruf eines bezahlten Dienstes wird im Kostenlogger erfasst.
- Keine Umgehung von Plattformlimits, kein VPN, kein fremder Wohnsitz, keine Engagement-Manipulation.
- Jedes Video wird als KI-Inhalt gekennzeichnet (TikTok `is_aigc`, Instagram `is_ai_generated`, YouTube `containsSyntheticMedia`), unabhängig davon, ob die Plattform es verlangt. Realistische Szenen realer Personen, Orte oder Ereignisse zusätzlich mit Offenlegung am Videoanfang (EU AI Act Art. 50).
- Nur lizenzierte Musik, Bilder, Schriften und Clips; Nachweis im Manifest. Kein automatischer Chartsong.
- Keine Duplikate und keine nur kosmetisch veränderten Kopien; jedes Video hat einen eigenen redaktionellen Blickwinkel.
- Keine Heilversprechen, keine Produktversprechen, keine operativen Gewalt- oder Waffenanleitungen, nichts aus Stefans Dienst, keine Uniform.
- Claude löscht nichts. Zu Entfernendes nach `C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`.
- Wird eine Aktion vom System abgelehnt, nicht anders erzwingen, sondern melden.

## Produktionsziel

- 9:16, 1080 × 1920, H.264 (NVENC), AAC; Länge 65–90 s (nie unter 61 s).
- Je Thema eine deutsche und eine englische Fassung (lokalisiert, nicht wörtlich übersetzt), gleiches Layout.
- Je Video: `video.mp4`, `cover.jpg`, `post.json` (Titel, Beschreibung, Hashtags je Plattform, Labels), `script.md`, `manifest.json` (Quellen, Lizenzen, Modelle, Kosten, Prüfbericht).
- Slots je Marke: 12:00, 14:00, 18:00 Europe/Vienna; je Slot eine Sprachfassung (Annahme, bis Stefan anderes sagt).

## Zustände

`PLANNED → RESEARCHED → SCRIPTED → RENDERED → VALIDATED → APPROVED → SCHEDULED → PUBLISHED → VERIFIED`, daneben `NEEDS_RESEARCH`, `BLOCKED` (Rechte), `HUMAN_REVIEW` (Risiko hoch), `REJECTED`, `FAILED`. Übergänge nur durch die zuständigen Module, idempotent, mit Zeitstempel in der Datenbank.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `config/brands.yaml` | alle Marken mit `enabled`, Sprachen, Slots, Risiko-Regeln |
| `config/platforms.yaml`, `config/policies.yaml`, `config/voices.yaml` | Plattformregeln, Richtlinien-Checks, TTS-Stimmen |
| `brands/<brand_id>/` | Designsystem je Marke: `brand.yaml`, `visual_style.md`, `script_prompt.md`, `image_prompt.md`, `subtitle_style.json`, `intro_config.json`, `outro_config.json`, `audio_style.yaml`, `assets/`, `references/` |
| `prompts/` | Prompts für Recherche, Kalender, Skript, Lokalisierung, Faktenprüfung, Compliance |
| `src/` | Module: scheduler, research, generation (TTS, Bilder), rendering (HyperFrames, FFmpeg, Whisper), compliance, publishing (Upload-Post-Adapter, Mock), analytics |
| `data/` | Kalender, Skripte, Manifeste, Statistik; SQLite-Datenbank `data/state.db` |
| `storage/` | `drafts/ → approved/ → published/`, `failed/`; wird nach `OneDrive\Business\05 Produktion` gespiegelt |
| `.claude/skills/` | Skills: calendar-planner, research-factcheck, script-writer, localizer, voice-generator, video-producer, video-editor, compliance-check, social-publisher, analytics-review |
| `automation/` | Windows-Aufgabenplanung (XML und PowerShell), Vorlagen für geplante Aufgaben |
| `tests/` | Tests je Modul; Publisher immer zuerst im Dry-Run |

## Werkzeuge (installiert, geprüft 29.10.2026)

Git 2.53 · Node 24 · Python 3.13 · FFmpeg mit h264_nvenc/hevc_nvenc/av1_nvenc · Claude Code 2.1 · VS Code · NVIDIA RTX 5080 Laptop 16 GB (Treiber 610.74). Noch einzurichten: Python-venv `.venv` (faster-whisper mit CUDA 12/cuDNN 9, google-genai, pyyaml), HyperFrames über `npx hyperframes` (Node ≥ 22), Upload-Post MCP-Server (`claude mcp add --transport http upload-post https://mcp.upload-post.com/mcp --header "Authorization: ApiKey <aus .env>"`).

## Arbeitsweise

Kleine, testbare Schritte; nach jedem Schritt Tests ausführen und sagen, was funktioniert und was fehlt. Mock-Dienste zuerst, echte Dienste erst nach Stefans Zustimmung. Kosten je Video messen (TTS-Token, Clips, Claude-Aufrufe, Renderzeit). Freien Platz auf C: vor jedem Produktionslauf prüfen; unter 30 GB warnen und keine neuen Renders starten.
