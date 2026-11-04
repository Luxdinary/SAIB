from fn.render.compose import Word
from fn.transcribe import align_to_script, mock_words


def test_mock_words_cover_duration():
    ws = mock_words("Ein kurzer Satz. Noch einer.", 10.0, start=2.0)
    assert ws[0].start == 2.0 and ws[-1].end <= 12.0 and len(ws) == 5
    assert all(b.start >= a.end for a, b in zip(ws, ws[1:]))


def test_align_keeps_script_words_and_interpolates_gaps():
    script = "Dein Mitarbeiter tippt die Kundenliste ein. Wo landet sie?"
    whisper = [Word("Dein", 0.0, 0.3), Word("Mitarbeiter", 0.3, 0.7), Word("tippt", 0.7, 1.0),
               # "die Kundenliste" missed, "ein." garbled as "einen"
               Word("einen", 1.6, 1.9), Word("Wo", 2.2, 2.4), Word("landet", 2.4, 2.7), Word("sie", 2.7, 2.9)]
    out = align_to_script(whisper, script)
    assert [w.text for w in out] == script.split()
    assert all(w.end > w.start for w in out)
    assert all(b.start >= a.start for a, b in zip(out, out[1:]))
    assert out[0].start == 0.0 and out[-1].end == 2.9
    # interpolated words sit between their neighbours
    assert 1.0 <= out[3].start < out[5].start <= 2.2


def test_align_umlauts_and_punctuation_match():
    script = "Privatsphäre-Einstellungen prüfen, heute!"
    whisper = [Word("privatsphäre-einstellungen", 0.0, 1.0), Word("prüfen", 1.0, 1.5), Word("heute", 1.6, 2.0)]
    out = align_to_script(whisper, script)
    assert [w.start for w in out] == [0.0, 1.0, 1.6]
