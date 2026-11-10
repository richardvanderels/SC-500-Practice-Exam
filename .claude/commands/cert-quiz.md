---
description: Generate exam-realistic practice questions for any Microsoft Certification exam.
argument-hint: exam=AI-200 count=5 domain=<optional> difficulty=<easy|medium|hard> mode=<batch|interactive>
---

Generate Microsoft Certification practice questions using the **ms-cert-item-creator** skill.

Parse these from the user input (`$ARGUMENTS`); apply the skill defaults for anything omitted:

- **exam** (required) -- the exam ID, for example AI-200, AI-102, AB-731, PL-200. If missing, ask which exam before generating.
- **count** -- number of items (default 5).
- **domain** -- restrict to one skills-measured functional group (default: spread across all, weighted).
- **difficulty** -- easy | medium | hard (default: spread).
- **mode** -- batch (all questions up front, then grade) or interactive (one at a time). Default batch.

Follow the skill exactly: resolve the exam's live skills-measured from the Microsoft Learn MCP first, calibrate difficulty to the audience profile, ground every item, randomize the correct letter with the batch balance rule, and use WWL style throughout.
