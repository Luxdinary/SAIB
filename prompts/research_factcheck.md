# Research and fact check

For one calendar row: collect the facts the script will use and verify each one against a primary source.

Procedure:
1. Open every URL in `source_urls`. If a page is gone or does not say what the angle needs, find a replacement
   primary source or mark the fact `UNVERIFIED`.
2. For each fact write: claim (one sentence, with numbers and dates as in the source), source id (S1, S2 ...),
   URL, title, checked_at, and a short quote or the exact location (section, table) that supports it.
3. Numbers: copy them exactly; convert units only with the formula shown. Scale comparisons must be computed
   and the computation written down.
4. Raise `risk_level` if the facts touch health, legal claims about people, military operations, product efficacy.
5. Brand rules apply (`brands/<brand_id>/script_prompt.md`): some facts are allowed in principle but not for this brand.

Output (YAML block, pasted into the script front matter):

```yaml
sources:
  - id: S1
    url: https://...
    title: ...
    checked_at: 2026-10-30
    supports: "claim in one sentence"
    quote: "exact words or location"
facts_unverified:
  - "claim that could not be verified"   # the script may not use these
risk_level: low
decision: go | needs_research
```
