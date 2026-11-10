# SC-500 Practice Exam

500 practice questions for Microsoft exam **SC-500: Implementing End-to-End
Security Controls for Cloud and AI Workloads**, spread over all 87 objectives in the official
[study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-500),
weighted by domain, at three difficulty levels. Original questions, not exam dumps.
Unofficial: not affiliated with or endorsed by Microsoft.

Open `docs/index.html` in a browser, or host it on GitHub Pages:

1. Push this folder to a GitHub repository.
2. Repository **Settings** -> **Pages** -> Source: *Deploy from a branch*,
   branch `main`, folder `/docs`.
3. Open `https://<your-user>.github.io/<repo>/`.

Progress is stored in your browser (localStorage), per device.

Question types, as on the real exam: single and multiple choice, build list
(ordering, mostly real `az`/`azd`/SDK command sequences), drag and drop,
code completion with drop-down lists, yes/no statements, problem-solution
series (no going back) and case studies. Every choice, value and option has an
explanation of what it does and when it would be right.

Modes: practice (feedback per question), exam (feedback at the end), and exam
simulation: 50 questions weighted by domain, 100 minutes, no hints, mark for
review, review screen, and series and case study sections you cannot return
to. Multi-part questions earn partial credit. Labs are not simulated.

## Known gaps

These questions are original and were checked against Microsoft Learn, but
not every fact was verified. Review them before you rely on them:

- **3.1.5 (blast radius):** four questions assume an Entra agent identity can be
  chosen as a node in the blast-radius graph. Learn does not confirm this.
- **3.3.8-03:** `MatchRule` appears as a wrong option; it was not seen on Learn.
- **2.3.6-07:** the zone `privatelink.vaultcore.azure.net` was not seen on Learn.
- **Command syntax:** a few Azure CLI commands in order questions were not
  confirmed (2.1.2-07, 2.1.4-07, 3.2.1-04, 1.3.5-05). Several 2.3 and 4.3 order
  questions use worded steps, not commands.
- **Preview features:** many questions cover preview features (agent guardrails,
  egress controls, Copilot Studio real-time protection, agent risk).
- **Difficulty:** group 1.3 has 18 easy, 18 medium and 9 hard questions.
- **Passes not run:** no separate conversion or verification pass (`CONVERT.md`,
  `VERIFY.md`) was done, and the explanation length rule was not checked everywhere.

## A base for other exams

This project is meant as a starting point for colleagues who want to build
the same kind of practice exam for another Microsoft certification (AB-700,
AZ-104, AI-102, PL-200, ...). The app, the validator, the briefs and the
skills are exam-neutral. Everything exam-specific sits in `objectives.py`:

| Setting | SC-500 value | What it sets |
|---|---|---|
| `EXAM` | `"SC-500"` | page title, header, browser storage prefix (`sc500.`) |
| `EXAM_TITLE` | `"Implementing End-to-End Security Controls for Cloud and AI Workloads"` | subtitle on the page |
| `STUDY_GUIDE` | Learn study guide URL | source for the objectives |
| `DOMAINS`, `GROUPS`, `OVERRIDE` | 4 domains, 87 objectives | domains, weights, questions per objective |
| `TOTAL` | `500` | bank size the validator and build check |

Example: a practice exam for AB-700.

1. Fork or copy this repository.
2. Open it in Claude Code and ask: *"Set objectives.py up for AB-700 from the
   live study guide: EXAM, EXAM_TITLE, STUDY_GUIDE, DOMAINS and GROUPS,
   TOTAL = 500, weighted by domain."* The skills fetch the study guide through
   the Microsoft Learn MCP server. `python objectives.py` checks that the
   counts add up to `TOTAL`.
3. Rewrite the audience paragraph at the top of `BRIEF.md` from the study
   guide's audience profile. The writing rules below it stay.
4. Empty `data/` and let Claude Code write questions per objective group,
   following `BRIEF.md` and `DISTRACTORS.md`. Then run the conversion pass
   (`CONVERT.md`) and an independent verification pass (`VERIFY.md`).
5. `python validate.py` until 0 errors, then `python build.py`, and publish
   `docs/` with GitHub Pages.
6. Practice in exam simulation mode until you score clearly above 70% several
   times. The real exam passes at 700 on a scale of 1 to 1000; that scaled
   score is not exactly 70% correct, so keep a margin.

Several exams on one site? Each one gets its own storage prefix from `EXAM`,
so progress never mixes. The simulation (50 questions, 100 minutes) matches
role-based exams; adjust it in `template.html` if your exam differs.

`/cert-quiz exam=AB-700 count=5` works for any exam without changes.

## Claude Code skills

Open this folder in Claude Code and the project skills load automatically:

- `ms-cert-item-creator`: writes exam-realistic questions for any Microsoft
  exam, following the WWL style guide.
- `/cert-quiz exam=SC-500 count=5`: slash command wrapper around the item
  creator.

The skills read the live study guide through the Microsoft Learn MCP server,
configured in `.mcp.json` (no key needed; approve it when Claude Code asks).

## Editing questions

Questions live in `data/<group>.json`, case studies in `data/cases_*.json`.
Format examples for each type: `examples/`. Writing briefs: `BRIEF.md`,
`DISTRACTORS.md`, `CONVERT.md`, `VERIFY.md`. After a change:

```
python validate.py   # coverage, counts, style checks
python similar.py    # look-alike questions across objectives
python build.py      # regenerates docs/index.html
```
