# Musik (gemeinsamer Renderer)

Stand 03.11.2026. Dieser Ordner ist der Haken für **lizenzierte** Musikbetten. Solange er leer ist, erzeugt die
Tonebene (`src/fn/render/sound.py`) je Video ein prozedurales Bett (additive Synthese, `src/fn/render/sound_synth.py`,
Stimmung `calm | tech | warm | dark | bright`), gekennzeichnet im Manifest als `sound.music.source = "procedural"`.
Entscheidung Stefan, 03.11.2026: „Vorerst selbst erzeugt.“

## Lizenzmusik einhängen

1. Datei als WAV (48 kHz, stereo) hier ablegen (`assets\music\<name>.wav`) oder markenlokal unter
   `brands\<id>\assets\music\<name>.wav`.
2. Nachweis eintragen: entweder eine Zeile `<name>.wav: <Lizenztext>` in einer `LICENSE.md` neben der Datei
   oder eine Tabellenzeile mit dem Dateinamen in
   `OneDrive\Business\08 Recht und Verwaltung\Lizenzen\Lizenzübersicht.md`. Ohne Nachweis bleibt das Bett prozedural,
   und der Prüfbericht setzt `music_license` (review).
3. Einschalten in `brands\<id>\brand.yaml`:

   ```yaml
   sound:
     music: <name>.wav
   ```

   oder im Plan unter `layout.sound.music`. Pegel wie beim prozeduralen Bett (`levels.music_db`, `levels.duck_db`).

Keine Downloads von Musikseiten ohne dokumentierte Lizenz. Higgsfield-Audio (`generate_audio`) ist nicht freigegeben,
solange der Lizenzbefund fehlt (siehe `docs/direction-system.md`, Abschnitt 6i).
