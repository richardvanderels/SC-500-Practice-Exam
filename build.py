"""Validate all questions and write docs/index.html (self-contained, GitHub Pages ready)."""
import json
import os
import sys

from objectives import DOMAINS, EXAM, EXAM_TITLE, GROUPS, TOTAL, objectives
from validate import check, load, load_cases

partial = "--partial" in sys.argv  # preview with whatever groups exist so far
qs = load(list(GROUPS))
err = [] if partial else check(qs, list(GROUPS))
if not partial and (err or len(qs) != TOTAL):
    sys.exit(f"not building: {len(err)} validation errors, {len(qs)} questions (run validate.py)")

data = {
    "exam": {"id": EXAM, "title": EXAM_TITLE},
    "domains": {k: {"title": t, "weight": w} for k, (t, w) in DOMAINS.items()},
    "objectives": {k: t for k, (t, _) in objectives().items()},
    "questions": qs,
    "cases": {c["id"]: c for c in load_cases()},
}
# "</" would close the <script> tag early.
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
with open("template.html", encoding="utf-8") as f:
    html = f.read().replace("/*__DATA__*/", blob).replace("__EXAM_TITLE__", EXAM_TITLE).replace("__EXAM__", EXAM)
os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"docs/index.html: {len(qs)} questions, {len(html) // 1024} KB")
