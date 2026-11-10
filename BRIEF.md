# Question-writing brief

Project folder: the folder that contains this file. Exam and objective map:
`EXAM`, `EXAM_TITLE`, `STUDY_GUIDE` and `GROUPS` in `objectives.py` (source of
truth: the official study guide at `STUDY_GUIDE`).

For another exam, rewrite the audience paragraph below from the study guide's
audience profile; the writing rules after it apply to every exam.

Audience (SC-500, associate level): security engineer who protects cloud and hybrid
workloads and the AI workloads on them: secures identity with Microsoft Entra ID and
Key Vault, enforces governance with Azure Policy and Defender for Cloud, secures
storage, databases, networks, servers, containers and app platforms, runs Microsoft
Sentinel and Security Copilot, and knows Microsoft Foundry agents and Entra Agent ID.
Comfortable with the Azure portal, Azure CLI, Az PowerShell, Bicep and KQL.

## Your job

Write the questions for ONE objective group, save them as `data/<group>.json`
(for example `data/2.3.json`), and run `python validate.py <group>` until it
prints `0 errors`.

For every objective in your group write EXACTLY the target count from
`objectives.py` (`python objectives.py` prints it). Split difficulty as evenly
as possible: easy / medium / hard about one third each.

## Scope rule: no more, no less

- Each question tests the objective it is tagged with, and only that objective.
- Cover every named sub-topic in the objective's wording across its questions.
  Example: 2.4.1 names hub-and-spoke, sequential, parallel, peer-to-peer and
  orchestrator-subagent -> each one appears in at least one question.
- Do not drift into topics that belong to another objective or group. Do not
  test anything that is not in the study guide.

## Grounding (mandatory)

Load the Microsoft Learn tools with ToolSearch
(`select:mcp__microsoft-learn__microsoft_docs_search,mcp__microsoft-learn__microsoft_docs_fetch,mcp__microsoft-learn__microsoft_code_sample_search`)
and verify the correct answer of every question against Microsoft Learn before
writing it. The `ref` field must be a learn.microsoft.com URL that you actually
saw in a tool result; never invent one. If a fact (parameter name, API, limit,
role name) cannot be verified on Learn, do not test it. Prefer concepts and
design decisions that are stable over exact SDK signatures. Code snippets are
allowed only when the syntax is verified by `microsoft_code_sample_search` or a
fetched page. For open-source frameworks (LangGraph, LangChain, A2A, MCP, Hugging
Face) test well-established concepts only, and use the closest Learn page as ref.

Use current product names: Microsoft Foundry (not Azure AI Foundry / AI Studio),
Microsoft Entra ID (not Azure AD), Foundry Agent Service, Microsoft Agent
Framework, Azure AI Search, Azure AI Content Safety, Azure API Management.

## Style (Microsoft WWL exam style, short version)

Full rules: `~/.claude/skills/ms-cert-item-creator/SKILL.md` (read it once).

- Scenario first, then one question sentence: starts with **What** or **Which**,
  uses **should**: "Which service should you use?", "What should you do?",
  "Which two actions should you perform?".
- Multi-select: say the count and add "Each correct answer presents a complete
  solution." or "Each correct answer presents part of the solution."
- Fictional companies only from the WWL list, full name every time (Litware,
  Inc.; Fabrikam, Inc.; Woodgrove Bank; Tailspin Toys; Relecloud; ...). Vary them.
  People: "the user" or User1, User2. Resources: Agent1, App1, Server1.
- No contractions, no "all/none of the above", no True/False, no trick wording,
  no "always/never/all/only" in choices. Plain ASCII in stem and choices
  (use -- and ->, straight quotes).
- Choices are parallel, mutually exclusive, all real Microsoft or framework
  features. **Same-family rule**: all choices come from one category, and each
  wrong choice is the right answer to a plausible neighbouring scenario. A wrong
  choice must be eliminated by a constraint in the stem, not by being off-topic.
- Never copy or paraphrase real exam questions or braindumps.

## Difficulty

- **easy**: one constraint; recognise the right pattern, component or concept.
- **medium**: realistic scenario with two constraints; apply the concept.
- **hard**: two or three buried constraints, trade-off reasoning, failure
  diagnosis, code-completion, ordering, or multi-select. About 1 in 3 hard
  questions is `multi`.

Format mix across the group: mostly scenario single-answer; include some
code/config completion (put code in a fenced block in the stem), some ordering
("Which sequence of actions should you perform?" with four sequences as
choices), and some multi-select.

## Language

- Everything is English (the real exam is English): `stem`, `choices`,
  `explanation` and `rationale`.

## JSON format

A single JSON array. Each item:

```json
{
  "id": "2.3.1-01",
  "obj": "2.3.1",
  "difficulty": "medium",
  "type": "single",
  "stem": "Fabrikam, Inc. ... \n\nWhich tool type should you configure?",
  "choices": ["choice A", "choice B", "choice C", "choice D"],
  "answer": [2],
  "explanation": "2-3 sentences, why the answer is right and the key constraint.",
  "rationale": ["1-2 sentences for choice A", "... B", "... C", "... D"],
  "ref": "https://learn.microsoft.com/..."
}
```

- `type`: `single` (exactly 4 choices, 1 answer) or `multi` (5 choices, 2 or 3
  answers).
- `answer`: zero-based indexes into `choices`. The app shuffles choices, so do
  not write "A/B" references in the stem, choices or rationale.
- `rationale`: one entry per choice, same order as `choices`.
- `id`: `<obj>-<two-digit sequence>`.

Write UTF-8 JSON. Then run `python validate.py <group>` and fix every error.
Finally re-read your file once as a strict reviewer: is every answer correct per
Learn, is exactly one answer defensible, is every sub-topic covered? Fix, re-run
the validator, and report the per-objective sub-topic coverage in 1 line each.
