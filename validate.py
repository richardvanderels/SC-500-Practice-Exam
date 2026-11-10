"""Validate data/*.json against the objective map in objectives.py. Exit 1 on any error.

Usage: python validate.py [group ...]   (no args = all groups, plus exact-TOTAL check)
"""
import glob
import json
import re
import sys
from collections import Counter

from objectives import GROUPS, TOTAL, objectives

OBJ = objectives()
DIFF = ("easy", "medium", "hard")
TYPES = ("single", "multi", "yesno", "order", "dragdrop", "dropdown")
YN_STEM = "For each of the following statements, select Yes if the statement is true. Otherwise, select No."
# ponytail: stopword heuristic, catches untranslated Dutch; not a language detector.
DUTCH = re.compile(r"\b(het|een|niet|wordt|worden|zijn|moet|omdat|alleen|zodat|maar|ook|deze|bij|naar|voor de|van de|is fout|juist)\b")
BANNED = ["all of the above", "none of the above", "both a and b", "n't "]
MIN_WHY = 60  # a wrong-answer explanation must teach something, not just say "wrong"


def load(groups):
    qs = []
    for g in groups:
        for f in sorted(glob.glob(f"data/{g}.json")):
            with open(f, encoding="utf-8") as fh:
                qs += json.load(fh)
    return qs


def load_cases():
    cases = []
    for f in sorted(glob.glob("data/cases_*.json")):
        with open(f, encoding="utf-8") as fh:
            cases += json.load(fh)
    return cases


def check_type(q):
    """Format rules per question type. Returns error strings (without the id)."""
    e = []
    t, ch, ans, rat, st = q.get("type"), q.get("choices", []), q.get("answer", []), q.get("rationale", []), q.get("stem", "")
    n = len(ch)
    if t not in TYPES:
        return ["bad type"]
    if t == "dropdown":
        tg = q.get("targets", [])
        if not 2 <= len(tg) <= 6 or len(ans) != len(tg):
            return ["dropdown needs 2-6 targets and one answer per target"]
        for i, x in enumerate(tg):
            ops, wy = x.get("options", []), x.get("why", [])
            if not x.get("label") or not 2 <= len(ops) <= 5 or len(set(ops)) != len(ops):
                e.append(f"dropdown target {i + 1} needs a label and 2-5 distinct options")
            elif not isinstance(ans[i], int) or not 0 <= ans[i] < len(ops):
                e.append(f"dropdown target {i + 1} answer out of range")
            elif len(wy) != len(ops) or any(w.lower().startswith("correct") != (k == ans[i]) for k, w in enumerate(wy)):
                e.append(f"dropdown target {i + 1} needs one 'why' per option, 'Correct...' only on the key")
        if "[[1]]" in st and any(f"[[{i + 1}]]" not in st for i in range(len(tg))):
            e.append("dropdown stem uses [[n]] markers but not one per target")
        return e
    if t == "dragdrop":
        tg = q.get("targets", [])
        if not 2 <= len(tg) <= 6 or len(ans) != len(tg):
            return ["dragdrop needs 2-6 targets and one answer per target"]
        if any(not isinstance(a, int) or not 0 <= a < n for a in ans):
            return ["dragdrop answer out of range"]
        if n < len(set(ans)) + 1:
            e.append("dragdrop needs at least one value that is not used")
        if len(rat) != len(tg):
            e.append("dragdrop needs one rationale per target")
        if len(q.get("notes", [])) != n:
            e.append("dragdrop needs one note per value (what it is, when to use it)")
        return e
    if any(not isinstance(a, int) or not 0 <= a < n for a in ans) or len(set(ans)) != len(ans):
        return ["answer index out of range"]
    if len(rat) != n:
        return [f"rationale count {len(rat)} != choices {n}"]
    if q.get("series"):
        if t != "single" or ch != ["Yes", "No"]:
            e.append("series item must be single with choices ['Yes', 'No']")
        if "Solution:" not in st or not st.rstrip().endswith("Does this meet the goal?"):
            e.append("series stem needs 'Solution:' and must end with 'Does this meet the goal?'")
    elif t == "single" and not (n == 4 and len(ans) == 1):
        e.append("single needs 4 choices and 1 answer")
    elif t == "multi" and not (n >= 5 and len(ans) >= 2 and n - len(ans) >= 2):
        e.append("multi needs >=5 choices, >=2 answers, >=2 distractors")
    elif t == "yesno":
        if not 3 <= n <= 4 or YN_STEM not in st:
            e.append(f"yesno needs 3-4 statements and the sentence '{YN_STEM}'")
        if any(r.startswith("Yes:") != (k in ans) or not r.startswith(("Yes:", "No:")) for k, r in enumerate(rat)):
            e.append("yesno rationale must start 'Yes:' for keyed statements and 'No:' for the others")
    elif t == "order":
        if not (3 <= len(ans) <= 6 and n - len(ans) >= 2 and n <= 8):
            e.append("order needs 3-6 steps, >=2 extra actions, <=8 actions")
        if "in sequence" not in st or "arrange them in the correct order" not in st:
            e.append("order stem must say 'in sequence' and '... arrange them in the correct order'")
        steps = {k: p + 1 for p, k in enumerate(ans)}
        if any(not r.startswith(f"Step {steps[k]}:") if k in steps else not r.startswith("Incorrect:") for k, r in enumerate(rat)):
            e.append("order rationale must start 'Step N:' for steps and 'Incorrect:' for extra actions")
    if t in ("single", "multi") and any(r.lower().startswith("correct") != (k in ans) for k, r in enumerate(rat)):
        e.append("answer key disagrees with rationale ('Correct...')")
    return e


def check(qs, groups):
    err = []
    ids = Counter(q.get("id") for q in qs)
    err += [f"duplicate id {i}" for i, c in ids.items() if c > 1]
    stems = Counter(re.sub(r"\W+", " ", q.get("stem", "")).lower().strip() for q in qs)
    err += [f"duplicate stem: {s[:60]}" for s, c in stems.items() if c > 1]
    cases = {c["id"]: c for c in load_cases()}

    for q in qs:
        i = q.get("id", "?")
        if q.get("obj") not in OBJ:
            err.append(f"{i}: unknown objective {q.get('obj')}")
            continue
        if q.get("difficulty") not in DIFF:
            err.append(f"{i}: bad difficulty")
        err += [f"{i}: {m}" for m in check_type(q)]
        t, ch, st = q.get("type"), q.get("choices", []), q.get("stem", "")
        tg = q.get("targets", [])
        boxes = [x["label"] + " " + " ".join(x.get("options", [])) if isinstance(x, dict) else x for x in tg]
        if len(set(c.strip().lower() for c in ch)) != len(ch):
            err.append(f"{i}: duplicate choices")
        if not str(q.get("ref", "")).startswith("https://learn.microsoft.com/"):
            err.append(f"{i}: ref must be a learn.microsoft.com URL")
        if not q.get("explanation"):
            err.append(f"{i}: missing explanation")
        if q.get("case") and q["case"] not in cases:
            err.append(f"{i}: unknown case {q['case']}")
        exam_text = " ".join([st] + ch + boxes)
        low = exam_text.lower()
        err += [f"{i}: banned phrase '{b.strip()}'" for b in BANNED if b in low]
        if not q.get("series") and t != "yesno" and not re.search(r"\b(What|Which|How)\b[^?]*\bshould\b[^?]*\?", st):
            err.append(f"{i}: question sentence must be What/Which/How ... should ...?")
        whys = q.get("rationale", []) + q.get("notes", []) + [w for x in tg if isinstance(x, dict) for w in x.get("why", [])]
        short = [w for w in whys if len(w) < MIN_WHY]
        if short:
            err.append(f"{i}: {len(short)} explanation(s) under {MIN_WHY} chars, e.g. '{short[0]}'")
        prose = " ".join([q.get("explanation", "")] + whys).lower()
        dutch = DUTCH.findall(prose)
        if len(dutch) >= 2:
            err.append(f"{i}: explanation/rationale must be English (found: {', '.join(sorted(set(dutch))[:5])})")
        # the study guide names Python only
        text = exam_text + " " + " ".join([q.get("explanation", "")] + whys)
        # case-sensitive .NET so domains such as vault.azure.net pass
        if re.search(r"```(csharp|cs|c#|dotnet)\b", text, re.I) or re.search(r"\bC#|\.NET\b", text):
            err.append(f"{i}: use Python, not C#/.NET")
        if t == "multi" and "Each correct answer" not in st:
            err.append(f"{i}: multi stem must say 'Each correct answer ...'")
        if re.search(r"[^\x00-\x7f]", exam_text):
            err.append(f"{i}: non-ASCII in stem or choices")

    # case studies and problem-solution series must be real groups
    for key, lo, hi in (("case", 4, 6), ("series", 3, 4)):
        for g, c in Counter(q[key] for q in qs if q.get(key)).items():
            if not lo <= c <= hi:
                err.append(f"{key} {g}: {c} questions, need {lo}-{hi}")
    for c in cases.values():
        secs = c.get("sections", [])
        if not c.get("title") or len(secs) < 3 or any(len(s) != 2 or not s[1].strip() for s in secs):
            err.append(f"case {c.get('id')}: needs a title and >=3 [heading, text] sections")
        if re.search(r"[^\x00-\x7f]", json.dumps(c, ensure_ascii=False)):
            err.append(f"case {c.get('id')}: non-ASCII text")

    # giveaway: correct choice clearly longest (random baseline ~25% for 4 choices)
    single = [q for q in qs if q.get("type") == "single" and len(q.get("choices", [])) == 4]
    longest = [q["id"] for q in single
               if len(q["choices"][q["answer"][0]]) > 1.25 * max(len(c) for i, c in enumerate(q["choices"]) if i != q["answer"][0])]
    if single and len(longest) / len(single) > 0.15:
        err.append(f"{len(longest)}/{len(single)} single items have a clearly longest correct choice "
                   f"(max 15%): {', '.join(longest)}")

    # coverage: exact count per objective and a spread of difficulties
    per = Counter(q.get("obj") for q in qs)
    for oid, (_, n) in OBJ.items():
        if oid.rsplit(".", 1)[0] not in groups:
            continue
        if per[oid] != n:
            err.append(f"objective {oid}: {per[oid]} questions, target {n}")
        d = Counter(q.get("difficulty") for q in qs if q.get("obj") == oid)
        if any(abs(d[x] - n / 3) > 1.5 for x in DIFF):
            err.append(f"objective {oid}: difficulty spread {dict(d)} not ~{n/3:.0f} each")
    return err


def kind(q):
    return "case" if q.get("case") else "series" if q.get("series") else q.get("type")


if __name__ == "__main__":
    groups = sys.argv[1:] or list(GROUPS)
    qs = load(groups)
    err = check(qs, groups)
    for e in err:
        print("ERROR", e)
    print(f"{len(qs)} questions, {len(err)} errors,",
          dict(Counter(q.get("difficulty") for q in qs)), dict(Counter(kind(q) for q in qs)))
    if not sys.argv[1:] and len(qs) != TOTAL:
        print("ERROR total is", len(qs), "not", TOTAL)
        sys.exit(1)
    sys.exit(1 if err else 0)
