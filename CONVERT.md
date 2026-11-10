# Conversion and explanation brief (pass 2)

Goal: make this practice exam as close to the real exam (`EXAM` in objectives.py) as possible.
The learner studies by trial and error, so **the explanation of every wrong
answer is the most important text in the file.**

Read first: `BRIEF.md` (writing rules), `DISTRACTORS.md` (plausible
distractors), `validate.py` (the exact format rules), and the format examples
`examples/examples.json` and `examples/cases_example.json` (one of each new
type; format only, do not copy their content).

Load Microsoft Learn tools once:
ToolSearch `select:mcp__microsoft-learn__microsoft_docs_search,mcp__microsoft-learn__microsoft_docs_fetch,mcp__microsoft-learn__microsoft_code_sample_search`

## Task A: convert questions to real exam formats

In your assigned files, convert existing questions to the new types, with the
counts given in your assignment. A converted question keeps its `id`, `obj`
and `difficulty` and must still test the same objective; the content may be
rewritten so it fits the format. Spread conversions over different objectives.
Prefer questions whose content suits the format (existing "which sequence"
questions -> `order`, code snippets -> `dropdown`, multi-select -> `yesno` or
`dragdrop`). Never convert a question twice.

- **order (build list)**: 3-6 steps plus at least 2 extra actions that do not
  belong. At least two thirds of your order questions must be **command or
  code sequences to provision, deploy, or configure resources**: real `az`,
  Az PowerShell, or Bicep steps, written in backticks inside each choice, for
  example `` `az keyvault create --name ... --enable-rbac-authorization true` ``.
  The learner struggled most with exactly this on a previous exam.
  Extra actions must be real commands that are wrong here (wrong order
  dependency, wrong command group, a step for a different hosting option, a
  step that is not needed). Every command and parameter must be verified on
  Learn (`microsoft_code_sample_search` / fetched pages); if you cannot verify
  exact syntax, describe the action in words instead of inventing flags.
  The order must be forced by real dependencies (a resource must exist before
  a role assignment on it, a package before an import), so exactly one order
  is defensible.
- **dropdown (hot area / code completion)**: Azure CLI, PowerShell, Bicep, KQL or JSON in a
  fenced block with `[[1]]`, `[[2]]` markers; each target has 2-4 options that
  are all real and type-correct, and a `why` per option.
- **dragdrop**: values to targets; at least one value unused; `notes` explain
  every value (what it is, when to use it).
- **yesno**: 3 statements about one scenario or code snippet; mix Yes and No.
- **series (problem-solution)**: 3 items that share one identical problem
  statement and goal, each with a different `Solution:`; same objective; give
  them one `series` id `S-<tag>`; mix Yes and No answers. They replace 3
  existing questions of that objective (keep each one's difficulty).
- **case study**: write one case study `C-<tag>` in `data/cases_<tag>.json`
  (title = an approved fictional company; 4-6 sections such as Overview,
  Existing environment, Business requirements, Technical requirements,
  Constraints; 500-900 words; realistic details the questions depend on, plus
  some details that are irrelevant). Attach 5 questions from different
  objectives in your files to it (`"case": "C-<tag>"`), of mixed types
  (single, multi, yesno, dropdown). Each question must need the case details
  to be answered; the stem states only the specific task.

## Task B: explanations for every question in your files

For EVERY question (converted or not), rewrite the per-choice explanations so
that each one teaches:

- **Wrong choice** (`Incorrect:` / `No:` / extra action): what this option
  actually is or does, which constraint in the stem rules it out, and when it
  WOULD be the right answer. Example: "Incorrect: SlidingWindowStrategy keeps
  only the last N turns, so the early contract details would be dropped. Use it
  when only recent turns matter and you want no extra model calls."
- **Correct choice** (`Correct:` / `Yes:` / `Step N:`): why it satisfies each
  constraint in the stem.
- Aim for 150-350 characters each; the validator rejects under 60.
- `explanation`: 2-4 sentences on the underlying concept, so the learner can
  answer a different question on the same topic.
- If a wrong choice is nonsense (no real feature, obviously absurd), replace it
  first (DISTRACTORS.md rules), then explain it.

## Rules

- Verify every fact you add against Microsoft Learn; the `ref` must be a page
  you actually saw. Do not invent parameters, commands, or limits.
- Never create a second defensible answer. Keep the answer key consistent with
  the explanations.
- English, plain ASCII in stem/choices/targets/case text. Code is Azure CLI,
  Az PowerShell, Bicep, KQL or JSON, never Python.
- Work file by file and save often (a small Python script that loads, edits,
  and dumps the JSON with `indent=1, ensure_ascii=False` is fine).
- Validate ALL your assigned groups together, because your case study spans
  them: `python validate.py <group1> <group2>`, until 0 errors.
- Edit only your assigned files plus your own `data/cases_<tag>.json`.

Final report (short): per type, the ids converted; the case study id and its
question ids; number of explanations rewritten; any fact you could not verify.
