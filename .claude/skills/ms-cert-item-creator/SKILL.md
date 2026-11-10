---
name: ms-cert-item-creator
description: Generate exam-realistic practice questions for ANY Microsoft Certification exam (for example AI-900, AI-102, AI-200, AB-731, PL-200, AZ-204) without copying the real exam. Takes an exam ID, fetches that exam's live skills-measured from the Microsoft Learn MCP server, calibrates difficulty to the audience profile, and follows the Microsoft Worldwide Learning Exam Writing Style Guide (WWL). Use when the user asks for practice questions, quiz items, or exam prep for a Microsoft certification.
---

# Skill: microsoft.cert.practice_questions.exam_realistic

**Description:** Generate practice questions for any Microsoft Certification exam that feel like the real exam without copying it. Every item is grounded in the current Microsoft Learn study guide for that exam, uses modern Microsoft product names, and follows Microsoft-style exam item rules: scenario-first stems, plausible distractors, parallel choices, no trick wording.

## Inputs

- **exam** (required) -- the exam ID, for example `AI-200`, `AI-102`, `AB-731`, `PL-200`. Normalize casing to the canonical form (uppercase letters, hyphen, digits).
- **count** (optional, default 5) -- number of items.
- **domain** (optional) -- restrict to one skills-measured functional group. Blank = spread across all domains weighted by their exam percentages.
- **difficulty** (optional) -- `easy | medium | hard`. Blank = spread.
- **mode** (optional) -- `batch` (all questions up front, then grade, default) or `interactive` (one at a time, Phase 1 / Phase 2 per item).

## Step 1 -- Resolve the exam (do this first, every time)

Never hardcode exam facts. Fetch them live:

1. Call `microsoft_docs_search` with a query like `<exam ID> certification exam skills measured study guide` to locate the study guide at `https://learn.microsoft.com/credentials/certifications/resources/study-guides/<exam-id-lowercase>`.
2. If the search snippets do not contain the full skills-measured list, call `microsoft_docs_fetch` on that study-guide URL for the complete functional groups, sub-objectives, and weightings.
3. Extract and hold for the whole batch:
   - Exam ID and full title.
   - Pass score (Microsoft exams pass at **700** unless the guide states otherwise).
   - The **audience profile** (drives difficulty calibration -- see below).
   - Every functional group with its percentage weight.
   - The sub-objective bullets under each group.
4. Check the study guide for a **retirement warning** (for example "This exam was retired on ..."). If present, tell the user the exam is retired and no longer bookable before delivering questions; still generate if they want practice.
5. If the exam ID cannot be resolved on Microsoft Learn, stop and tell the user the exam ID was not found; do not invent objectives.

## Difficulty calibration (from the audience profile)

Read the audience profile from the study guide and calibrate depth, not just wording:

| Exam tier (from title / profile) | Calibration |
| --- | --- |
| Fundamentals (`-900`, `AB-730`) | Conceptual. "Which service fits this need." No SDK internals. Beginning of career. |
| Associate (`-102`, `-204`, `AI-200`) | Developer / implementer depth. SDK calls, config choices, architecture trade-offs, troubleshooting. |
| Expert / Specialty (`AB-731`, `AB-100`) | Strategy, design, and adoption decisions. Cross-service reasoning, governance, ALM. |

When the profile lists prerequisite proficiencies (for example "Python programming", "vector databases"), you may assume that knowledge in stems. Do not exceed the profile's depth.

## Grounding

**Required sources, queried in this order before writing any item:**

- `microsoft_docs_search` -- first pass, breadth and objective discovery.
- `microsoft_docs_fetch` -- full page when a stem needs precise wording or a complete behavior description.
- `microsoft_code_sample_search` -- SDK / config accuracy for developer-tier exams (associate and above).

Grounding-first rule: query the Microsoft Learn MCP before any other source. Never substitute generic web search. Never invent a Microsoft Learn URL; if a URL cannot be verified through the MCP, omit it.

## Style precedence

The **Microsoft Worldwide Learning Exam Writing Style Guide** (WWL) is authoritative for every item. The **Microsoft Writing Style Guide** (MWSG) governs prose voice where WWL is silent. When they conflict, **WWL wins**.

Two MWSG conventions overridden by WWL for exam items:

- **No contractions** anywhere in an item.
- **All uppercase** for key names: TAB, ENTER, CTRL+ALT+DELETE.

## Style and word usage (WWL, mandatory)

### Question sentence

- Begin with **What** (stand-alone interrogative pronoun) or **Which** (followed by a noun).
- The auxiliary is **should**. Do not use *can, must, might, do, would, may* in question sentences.
- Approved stems: *What should you do?* / *What should you recommend?* / *Which service should you use?* / *Which two actions should you perform?* / *What are two possible ways to achieve this goal?*
- For Choose-N items, embed the count and use a plural noun: *Which two actions should you perform? Each correct answer presents part of the solution.*
- Avoid negatives. If unavoidable, **CAP** and **bold** it (for example, **NOT**).
- Goal statements use *You need to ...* or *You need to ensure that ...*.
- True/False stems are not allowed.

### Word usage

- **named**, not *called*. **report**, not *complain*.
- Avoid **determine** (use *verify, clarify, identify, set, discover, establish, calculate, decide*).
- Avoid **may** (use *can* or *might*). Avoid **would** in questions (use *should*).
- Avoid **using** alone (use *by using*). Avoid **with** in place of *by using*.
- Avoid specific determiners: *all, none, only, always, never*.
- Avoid indefinite qualifiers: *few, many, multiple, several, some, usually, a number of*.
- *site* is logical; *location* is physical -- never interchange.
- Use **plural**; do not use *(s)*. Present tense throughout.

### People (WWL legal rule)

- Never use a personal name. Use **the user**. For multiple people, use **User1, User2, User3** (no spaces).

### Approved fictional companies (WWL Fictitious Names List)

Use only these. Always use the **entire** company name on every mention (write *Litware, Inc.*, not *Litware*). Randomize across the full list -- do not default to Contoso, Ltd.

A. Datum Corporation; Adventure Works Cycles; Alpine Ski House; Bellows College; Best For You Organics Company; Blue Yonder Airlines; City Power & Light; Coho Vineyard; Coho Winery; Consolidated Messenger; Contoso, Ltd.; Contoso Pharmaceuticals; Contoso Suites; Fabrikam, Inc.; Fabrikam Residences; First Up Consultants; Fourth Coffee; Graphic Design Institute; Humongous Insurance; Lamna Healthcare Company; Litware, Inc.; Lucerne Publishing; Margie's Travel; Nod Publishers; Northwind Traders; Proseware, Inc.; Relecloud; Southridge Video; Tailspin Toys; The Phone Company; Trey Research; VanArsdel, Ltd.; Wide World Importers; Wingtip Toys; Woodgrove Bank.

### Approved cities (WWL city list)

Use without state, province, or country: Atlanta, Boston, Chicago, Dallas, Denver, Detroit, Los Angeles, Mexico City, Montreal, New York, Ottawa, San Diego, San Francisco, Seattle, Toronto, Vancouver; Amsterdam, Athens, Barcelona, Berlin, Brussels, Copenhagen, Dublin, Frankfurt, Geneva, Helsinki, Lisbon, London, Madrid, Oslo, Paris, Prague, Rome, Stockholm, Vienna, Warsaw; Beijing, Hong Kong, Seoul, Shanghai, Singapore, Sydney, Tokyo; Buenos Aires, Cairo, Cape Town, Johannesburg, Nairobi, Rio de Janeiro, Sao Paulo.

### Resource names (WWL conventions)

- **Servers:** Server1, Server2; SQL1, SQL2; DC1, DC2 (no space between noun and digit).
- **Computers:** Computer1. **Applications:** App1. **Subnets:** Subnet1. **Sites:** Site1.
- **Offices:** *main office*, *branch office*, *satellite office* (lowercase).
- Define each name on first mention.

### Answer choices (WWL)

- Default 4 choices (A-D): 1 correct + 3 distractors. Choose-N items: N correct + at least 2 distractors.
- Choices are **mutually exclusive** and **parallel** in form, length, detail, and grammar.
- All choices are sentence fragments (lowercase initial, no end punctuation) **OR** all complete sentences. Do not mix.
- No *all of the above*, *none of the above*, *both A and B*.
- Move redundant lead-in wording from choices into the stem.
- Distractors must reference **real** Microsoft services, features, or resource kinds. Never invent fake names, models, or capabilities. Distractor realism is governed by the same-family rule below -- "relevant to the topic" is not enough.
- No explanations inside choices. Order choices logically (numerical, shortest to longest, related pairs together).

### Distractor realism (same-family rule, non-negotiable)

This is the difference between an exam-realistic item and an obvious one. A candidate must eliminate a distractor by catching the constraint in the stem, NOT by recognizing the distractor is off-topic.

- **Same family or same axis.** All four choices come from one set: the same service category (for example all four are container hosts: Container Apps, Azure Kubernetes Service, App Service, Container Instances), the same feature of one service (input binding, output binding, trigger, direct SDK call), or the same ordered axis (the five Cosmos DB consistency levels). Do not mix a database knob, a messaging service, and a secrets store into one item.
- **Each distractor is right for a different requirement.** Every wrong answer must be the correct answer to a plausibly adjacent scenario. If you cannot write the one-line requirement that would make a distractor correct, it is filler -- replace it.
- **Wrong only because of the stem's constraint.** The stem carries exactly one discriminator (least code, already instrumented, tolerates stale reads, must fan out to independent consumers) that makes one choice correct and the near-neighbors wrong.
- **Banned distractor pattern:** a service from an unrelated exam domain used as filler (RUs on a Kubernetes question, Key Vault on a caching question, Event Grid on a monitoring question). A choice dismissible without reading the stem fails the item.
- **Sourcing shortcut:** for "which service" items, pull the distractors from the Microsoft Learn "choose a service" / comparison page for that category. Those are the real near-neighbors Microsoft tests against.

### Formatting

- **Bold** for UI element names and cmdlets. **All uppercase** for key names.
- File names labelled with *file*: *the deploy.bicep file*, not *deploy.bicep* alone.
- Sentence-style capitalization except product names and proper nouns. Oxford comma in lists of three or more.
- Plain ASCII only -- no curly quotes, en or em dashes. Use `--` and `->`.
- Spell out zero through nine; numerals for 10 and above.
- **should** = recommendation; **must** = requirement.
- Acronyms: spell out + acronym in parens on first mention, acronym only after.

### Globalization

- Sentences 15-20 words. Active voice. Simple tenses. No `/` or `-` as punctuation. No possessives on product names. No idioms, slang, or US-only references.

## Terminology rename table (non-negotiable)

Always use current Microsoft product names. Never use a retired name, even if the user does. If Microsoft Learn shows a different current name, prefer the Learn name.

| Retired / legacy name | Current name |
| --- | --- |
| Azure Active Directory (Azure AD) | Microsoft Entra ID |
| Azure Cognitive Services (umbrella) | Azure AI services |
| Cognitive Services for Language | Azure AI Language |
| Cognitive Services for Speech | Azure AI Speech |
| Computer Vision | Azure AI Vision |
| Form Recognizer | Azure AI Document Intelligence |
| QnA Maker | Azure AI Language question answering |
| LUIS | Azure AI Language conversational language understanding |
| Azure AI Studio | Microsoft Foundry |
| Azure AI Foundry | Microsoft Foundry |
| Azure AI Foundry portal | Microsoft Foundry portal |
| Azure AI Foundry SDK | Microsoft Foundry SDK |
| Azure AI Foundry Agent Service | Microsoft Foundry agents |

Confirm current naming through the Microsoft Learn MCP for any product not in this table.

## Answer choice randomization (non-negotiable)

Randomize which letter (A, B, C, D) is correct for each item. Never default to a position.

**Batch balance rule:**

- 4 to 7 items: every letter A/B/C/D is correct at least once.
- 8 to 11 items: every letter appears at least twice.
- 12 or more items: target 25 percent per letter, drift +/- 1.

**Before delivery:** count correct letters, rewrite any item on an over-represented letter to move its answer to an under-represented one, re-count until balanced, then state the final distribution in the batch summary. Position must carry no signal. Disable randomization only when choices are numerical (order them numerically instead).

## Guardrails

- **Exam integrity:** Do not recreate or paraphrase real exam questions or braindumps. Original scenarios and stems every time.
- **Item quality:** One skill measured per item. No trivia, no hidden requirements. One problem, one decision.
- **Audience fit:** Match the difficulty calibration table -- do not exceed the audience profile's depth.
- **Real features only:** Confine items to features in the exam's study guide, validated through the Microsoft Learn MCP.

## Workflow

1. Resolve the exam (Step 1) and hold the skills-measured, weights, and audience profile.
2. Calibrate difficulty to the audience profile.
3. Pick the target objective (respect the `domain` input, else weight by exam percentages).
4. Ground the intended correct behavior via `microsoft_docs_search`, then `microsoft_docs_fetch` for detail; use `microsoft_code_sample_search` for SDK/config specifics on associate+ exams.
5. Pick a random WWL-approved company. Draft a scenario stem that forces one real candidate decision.
6. Randomly assign the correct letter. Write 1 correct + 3 distractors that pass the same-family rule (same service category, feature set, or decision axis; each correct for a different requirement). For "which service" items, source distractors from the Learn comparison page for that category. Apply the batch balance rule.
7. Run the WWL style sweep, terminology check, mutual-exclusivity check, and single-skill clarity check.
8. Choose the item format (see Item formats). Single-best-answer by default; mix in code-completion, yes/no series, build-list, or a case study for associate+ exams or when the user asks for a realistic mock.
9. Prepare rationale internally; deliver per the mode rules.

## Item formats

Default to single-best-answer (four choices A-D). For associate+ exams, and whenever the user asks for a realistic mock, mix in the formats below -- real Microsoft exams are not all single-select. Every format still obeys the same-family distractor rule and WWL style.

- **Single best answer** -- four choices, one correct. The default.
- **Code-completion** -- show a short, real code, manifest, YAML, or KQL snippet with one blank (or an error), and ask which option completes or fixes it. Choices are same-family (for example four SDK methods, four KQL operators). Use for SDK, binding, manifest, and query objectives on developer-tier exams. Ground the syntax with `microsoft_code_sample_search`.
- **Yes/No series** -- a shared stem plus 3 to 5 independent statements, each answered Yes or No. State that statements are scored independently and do not depend on each other. Balance the answer key (do not make them all Yes).
- **Build-list / ordering** -- give a scrambled set of steps and ask for the correct order. Use for deploy, provision, or pipeline sequences.
- **Case study** -- one multi-requirement scenario followed by 3 to 5 questions, each tied to a specific numbered requirement in the scenario. Each question is still single-best-answer with same-family distractors. Use to test whether the candidate can hold several constraints at once.

When mixing formats in one set, label each item with its format so the candidate learns the shape. Difficulty on associate+ exams should bury two or three constraints in the stem, not one.

## Delivery rules

**Batch mode (default):** Show all items (metadata + stem + choices A-D), then wait for the user's answers. On reply, grade every item with the evaluation format below. End with a score summary and any weak domains.

**Interactive mode:** Per item, Phase 1 = stem + choices only, then stop and wait. Phase 2 (after the user answers) = result + rationale + references. Repeat sequentially.

**Invalid answer handling (interactive):** `hint` -> eliminate one distractor and re-present. `skip` / `I do not know` -> reveal answer and rationale. Unrecognized -> prompt for **A**, **B**, **C**, **D**, `hint`, or `skip`.

## Output format

**Question (Phase 1):**

- **metadata:** exam, domain, objective, bloom (`Remember | Understand | Apply | Analyze | Evaluate`), difficulty.
- **question:** scenario stem (tight, one decision) then the question sentence.
- **choices:** A / B / C / D.

*(Batch mode: repeat for each item, then stop. Interactive mode: stop after one.)*

**Evaluation (Phase 2):**

- **result:** *Correct! / Incorrect.* The correct answer is `<A|B|C|D>`.
- **rationale:** one entry per choice, exactly 2 sentences (Sentence 1: correct/incorrect and why; Sentence 2: candidate context, the misconception it tests, or how it differs from the correct answer).
- **references:** verified Microsoft Learn URLs only.

**Quality checklist (run before delivering):** stem starts with What/Which + should; no banned auxiliaries; no specific determiners or indefinite qualifiers; scenario fits the audience profile; exactly one skill measured; correct answer unambiguous per Learn; distractors real and unambiguously wrong; distractors pass the same-family rule (same category/feature/axis, each eliminable only by the stem's constraint, none dismissible as off-topic); no contractions; choices parallel and all-fragments-or-all-sentences; at least one Learn reference; current product names; each rationale exactly 2 sentences; correct letter randomized; batch balance satisfied; company from the WWL list with its full name; resource names follow the Server1/App1 pattern; people are *the user* or User1/User2.
