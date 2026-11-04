# Dewlane - Script prompt (template 0.9)

Used by Claude Code together with `prompts/script_writer.md` and the direction system (`docs/direction-system.md`).
Template and checklist: `C:\Users\Stefa\OneDrive\Business\02 Marke\Dewlane\Vorlage Dewlane.md`. Example plan:
`data/direction/beauty-20261105-1-de.json`.

## Brand

- Name: Dewlane (`beauty`), niche: knowledge about ingredients, skin types, routines and labelling.
- Audience: people who want to understand skincare without being sold to. Address: "du".
- Tone: knowledgeable, gentle, honest about uncertainty. Risk level high: every video ends in HUMAN_REVIEW.

## Binding rules

- Knowledge only: what an ingredient is, how it is labelled, what a rule says. No product recommendation, no brand name
  as recommendation, no efficacy or healing claims ("wirkt", "hilft gegen", "repariert"), no before/after, no invented tests,
  no AI faces or artificial skin as proof, no medical advice; when health is touched, say what a source says and stop.
- Every factual sentence has a source id: EU Cosmetics Regulation 1223/2009 and amendments, CosIng, Commission texts,
  dermatology societies (e.g. AAD), reviews in PubMed (with DOI). Unsourced statements go to `unverified`.
- Numbers only with their population or condition (e.g. "among patch-tested dermatitis patients"), never as general rates.

## Hooks that fit

What a label line means; a labelling rule most people do not know; what a list does NOT tell you. Five candidates, one per
type, truth at least 4.

## Structure (65-90 s, about 160-175 words in German)

Hook -> problem -> explanation -> demonstration -> insight -> benefit -> close inside the story (`file_close`),
spoken CTA "Beauty-Wissen klar erklärt: Folge Dewlane."; claim "Wissen statt Versprechen.", disclaimer
"Keine medizinische Beratung." on screen.
