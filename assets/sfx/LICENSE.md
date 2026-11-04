# Lizenz der Soundeffekte (gemeinsamer Renderer)

Alle Dateien in diesem Ordner sind mit `src/fn/render/sound_synth.py` (Version 1.0) aus Rauschen und Sinuswellen synthetisiert (numpy, fester Zufallsstartwert je Klang, 48 kHz mono 16 bit, Spitze -3 dBFS). Keine Samples, keine Fremdaufnahmen, keine Downloads, keine Rechte Dritter.
Erzeugt am 2026-11-03 von Claude Code fuer Stefan Dallinger; frei verwendbar in allen Videos des Netzes.
Neu erzeugen (byte-identisch): `.venv\Scripts\python.exe -m fn.render.sound_synth sfx`

Eine Zeile je Datei (Format `<datei>: <lizenztext>`, wie fn.render.assets es liest):

whoosh.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_whoosh`, Seed 20261103, steigender Rauschsweep 260-2600-900 Hz, 0,85 s
whoosh2.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_whoosh2`, Seed 20261104, fallender Rauschsweep 2400-320 Hz, 0,8 s
swipe.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_swipe`, Seed 20261105, kurzer heller Sweep 900-4200 Hz, 0,42 s
swipe2.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_swipe2`, Seed 20261106, kurzer Sweep 3800-1100 Hz, 0,4 s
click.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_click`, Seed 20261107, Rauschimpuls 1,5 ms um 3 kHz plus gedaempfte Sinus 1900/3400 Hz, 0,09 s
tick.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_tick`, Seed 20261108, Rauschimpuls 1 ms um 4,5 kHz plus Sinus 4200 Hz, 0,045 s
stamp.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_stamp`, Seed 20261109, Schlag mit Tonhoehenfall 150-55 Hz plus 12 ms Rauschen 0,9-3,5 kHz, 0,4 s
paper.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_paper`, Seed 20261110, Rauschen mit Knistern, Band 1,2-2,6 kHz, zwei Schwellungen, 0,6 s
pop.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_pop`, Seed 20261111, Sinusfall 620-240 Hz, 45 ms Abklingen, 0,14 s
thud.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_thud`, Seed 20261112, Sinus 85-48 Hz, 130 ms Abklingen, wenig Tiefenrauschen, 0,33 s
chime.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_chime`, Seed 20261113, Sinus C6/G6/C7 mit Abklingen, 0,9 s
riser.wav: selbst erzeugt (fn.render.sound_synth, numpy-Synthese aus Rauschen und Sinuswellen), keine Samples, keine Rechte Dritter; Funktion `sfx_riser`, Seed 20261114, steigendes Rauschband 180-3200 Hz mit Crescendo plus Sinus 110-440 Hz, 1,3 s
