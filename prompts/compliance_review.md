# Compliance review (for HUMAN_REVIEW cases and spot checks)

Read `script.md`, `manifest.json` and `report.json` of the video folder. Answer in German, short:

1. Technical: duration, aspect, audio, captions, black frames (from the report). Anything failed?
2. Sources: does every factual sentence have a marker, does every marker point to a source with URL and date,
   does the source actually say that (open it)?
3. Licences: fonts, music, images, clips each with proof?
4. AI labelling: all three labels true; Art. 50 disclosure where realistic scenes of real events could be read into it?
5. Brand rules and platform policies: anything from the forbidden list (`brands/<id>/script_prompt.md`,
   `config/policies.yaml`), medical or product promises, military tactics, service-related content, uniform?
6. Risk level correct? Recommendation: approve (Stefan decides), reject with reason, or send back to research.

Never set `APPROVED` yourself. Write the recommendation to the video folder as `review.md`.
