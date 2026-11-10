# Distractor hardening brief

Goal: a candidate must not be able to answer a question by common sense,
elimination of nonsense, or wording tells. Only real knowledge of the exam
material should get them to the key. Read BRIEF.md (writing rules) first.

For EVERY question in your assigned `data/<group>.json` files, check each
wrong choice and the question as a whole for these tells, and fix them:

1. **Nonsense / off-topic distractor**: a choice that is obviously wrong to
   someone who does not know the product (destructive, absurd, unrelated
   service, "do nothing", "disable security", manual workaround nobody would
   pick). Replace it with a real feature, setting, step or pattern from the
   SAME family as the key that would be the right answer to a neighbouring
   scenario, and is ruled out only by a specific constraint in the stem.
2. **Keyword echo**: a distinctive word or phrase from the stem appears only in
   the key. Reword the key, or put the term into distractors too.
3. **Virtue tell**: the key is the only "secure / least privilege / managed /
   recommended / best practice" sounding option. Make distractors sound
   equally reasonable (e.g. also managed, also secure, but wrong for a stated
   constraint).
4. **Hedge / absolute tell**: only the key is nuanced, or distractors contain
   extreme wording. Make choices parallel in tone.
5. **Length and detail**: the key must not be the most specific or detailed
   choice. Keep lengths similar (the validator fails single items whose key is
   >25% longer than every distractor, max 15%).
6. **Grammatical or format mismatch** with the stem that only the key avoids.
7. **Multi-select**: every wrong choice must be a plausible part of a
   solution, not filler.

Rules:
- Verify every NEW distractor is a real thing (Microsoft Learn tools:
  ToolSearch `select:mcp__microsoft-learn__microsoft_docs_search,mcp__microsoft-learn__microsoft_docs_fetch`)
  and that it is truly WRONG for this stem. Never create a second defensible
  answer; if a new distractor could also be right, add or sharpen a
  constraint in the stem instead.
- Keep the key, `id`, `obj`, `difficulty`, `type` and `ref` unchanged. You may
  sharpen the stem to rule out a stronger distractor. Keep the answer index
  pointing at the correct choice (reorder nothing unless you update `answer`).
- Update `rationale` for every choice you change (starts with "Correct:" for
  keyed choices, "Incorrect:" otherwise, and names the constraint that rules it
  out), and update `explanation` if needed. Everything in English.
- Python only, no C#/.NET. Plain ASCII in stem and choices.
- Leave good questions alone; do not rewrite for the sake of it.
- Run `python validate.py <group>` after editing until 0 errors. Edit only
  your assigned files.

Final report (short): per file, questions checked, questions changed, and the
three most common tells you fixed.
