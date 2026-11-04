from fn import scripting
from fn.pipeline import _post_json, plan_scenes
from fn.render.compose import Word
from fn.brands import load_brand


def test_plan_scenes_follows_word_timings(sample_script_text):
    s = scripting.parse(sample_script_text)
    counts = [len(sc.spoken.split()) for sc in s.scenes]
    words, t = [], 2.0
    for n in counts:
        for _ in range(n):
            words.append(Word("w", round(t, 3), round(t + 0.3, 3)))
            t += 0.35
    scenes = plan_scenes(s, words, intro_s=1.8, outro_start=t + 1.0, voice_start=2.0)
    assert len(scenes) == 3
    assert scenes[0].start == 1.8 and scenes[0].kind == "hook"
    assert abs(scenes[1].start - (words[counts[0]].start - 0.15)) < 1e-6
    assert abs(scenes[-1].end - (t + 1.0)) < 1e-3
    assert scenes[1].source_label.startswith("[S1] example.org")
    for a, b in zip(scenes, scenes[1:]):
        assert abs(a.end - b.start) < 1e-6


def test_post_json_sets_all_three_ai_labels(sample_script_text):
    s = scripting.parse(sample_script_text)
    post = _post_json(s, load_brand("ai_security"), "vid-1")
    assert post["labels"] == {"is_aigc": True, "is_ai_generated": True, "containsSyntheticMedia": True}
    assert set(post["platforms"]) == {"tiktok", "instagram", "youtube"}
    assert len(post["platforms"]["youtube"]["title"]) <= 100
    assert "KI-generiert" in post["description"]
