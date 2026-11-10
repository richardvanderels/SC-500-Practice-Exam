# Question review brief

You are an independent, skeptical technical reviewer (a subject-matter
expert). Another writer produced the questions; assume each one may be wrong.
Read BRIEF.md (writing rules) and objectives.py (official objective list) first.

For EVERY question in your assigned `data/<group>.json` files:

1. **Correctness.** Open the `ref` with `microsoft_docs_fetch` (load the
   Microsoft Learn tools via ToolSearch:
   `select:mcp__microsoft-learn__microsoft_docs_search,mcp__microsoft-learn__microsoft_docs_fetch,mcp__microsoft-learn__microsoft_code_sample_search`)
   and verify the keyed answer. Search Learn further when the ref does not
   settle it. Check that the ref page actually supports the answer.
2. **Exactly one defensible answer** (or exactly the keyed set for multi). If a
   distractor is also arguably right, rewrite the stem constraint or the
   distractor.
3. **Objective fit.** The question tests its tagged objective, and nothing
   outside the study guide. Retag or rewrite if it fits another objective of the
   SAME file better only when counts stay exact; otherwise rewrite the question.
4. **Currency.** No retired features or names (check Learn for retirement
   notices), no preview-only trivia, no invented parameters or role names.
5. **Difficulty label** plausible (easy = 1 constraint, medium = 2, hard = 2-3
   buried constraints or diagnosis/code/order/multi).
6. **Clarity.** No giveaways (longest choice is always right, keyword echo from
   stem only in the right answer), choices parallel, English explanation and
   rationale correct and consistent with the key.

The validator flags single-answer items whose correct choice is more than
25% longer than every distractor (max 15% of a file). Fix flagged items by
making the choices similar in length and detail (shorten the key, move detail
to the stem or rationale, or enrich distractors). Do not pad with filler.

Fix problems directly in the JSON file (keep `id`, `obj` and counts unchanged;
replace a broken question with a new one for the same objective and
difficulty). Run `python validate.py <group>` after editing until 0 errors.
Only edit your assigned files.

Final report (short): per file, number of questions checked, number changed,
and one line per changed question id with what was wrong.
