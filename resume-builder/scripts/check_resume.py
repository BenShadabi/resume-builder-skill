#!/usr/bin/env python3
"""Check a resume.md (and its PDF) against the skill's rules.

Usage:
  check_resume.py resume.md [--type letter] [--profile profile.md] [--posting posting.txt] [--pdf resume.pdf]

Checks: one page (if --pdf), no em/en dashes, no banned words, every number appears in profile.md,
bullets start with different words, file name length, and keyword coverage against a posting.
Exit code 1 if a hard check fails. Standard library only.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

BANNED = ["spearheaded", "leveraged", "utilized", "synergy", "pivotal", "intricate", "realm", "showcasing",
          "delve", "robust", "seamless", "dynamic", "results-driven", "passionate", "proven track record",
          "detail-oriented", "fast-paced", "team player", "go-getter", "hard-working"]
AI_TOOLS = ["chatgpt", "claude", "copilot", "gemini", "codex", "midjourney", "perplexity", "cursor", "grammarly"]
STOP = set("a an the and or of to in for with on at by from as is are be your you we our will can must have has "
           "de la el los las un una y o en con para por del al que se su sus es son esta este requiere deseable le les des du et ou pour dans sur avec this that these those it its their they who what which about into over more other than such not apply teams team centre center health requires require required nice preferred applicants applicant must live work experience skills ability strong".split())


def fold(text):
    """Lowercase and strip accents so 'comunicación' matches 'comunicacion'."""
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))


def norm_num(n):
    s = n.replace(" ", "").rstrip(",.")
    if re.fullmatch(r"\$?\d{1,3}([.,]\d{3})+%?", s):  # 1.500 or 1,500 are both fifteen hundred
        s = re.sub(r"[.,]", "", s)
    return s


def numbers(text):
    found = re.findall(r"\$?\d+(?:[.,]\d{3})*(?:\.\d+)?(?: ?%)?", text)
    return {norm_num(n) for n in found}


def words(text):
    return [w.rstrip(".-") for w in re.findall(r"[a-z][a-z+#.\-]{1,}", fold(text))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume")
    ap.add_argument("--profile")
    ap.add_argument("--posting")
    ap.add_argument("--pdf")
    ap.add_argument("--type", choices=["resume", "letter"], default="resume")
    ap.add_argument("--lang", default="en", help="document language; the banned-word list is English only")
    ap.add_argument("--forbid", action="append", default=[], help="text that must NOT appear (repeatable)")
    ap.add_argument("--max-pages", type=int, default=1, help="pages allowed (default 1; use 2 only if the person chose it and the content fills it)")
    a = ap.parse_args()
    md = Path(a.resume).read_text(encoding="utf-8")
    low = md.lower()
    fails = 0

    def report(ok, msg, hard=True):
        nonlocal fails
        print(("PASS " if ok else ("FAIL " if hard else "WARN ")) + msg)
        if not ok and hard:
            fails += 1

    if a.pdf:
        data = Path(a.pdf).read_bytes()
        pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
        report(1 <= pages <= a.max_pages, f"document is within {a.max_pages} page(s) ({pages} found)")
        report(len(Path(a.pdf).name) <= 50, f"file name {len(Path(a.pdf).name)} characters (max 50)")

    report("—" not in md and "–" not in md, "no em or en dashes")
    hits = [w for w in BANNED if w in low]
    report(not hits, "no banned words" + (f": {hits}" if hits else ""))
    if a.lang != "en":
        report(False, "banned-word list is English only; read this document yourself for empty buzzwords", hard=False)

    # rejected or private claims: --forbid, plus the profile's "Never write" list
    forbid = list(a.forbid)
    if a.profile:
        sec = re.search(r"## Never write[^\n]*\n(.*?)(\n## |\Z)", Path(a.profile).read_text(encoding="utf-8"), re.S)
        if sec:
            forbid += [l.lstrip("-* ").strip() for l in sec.group(1).splitlines() if l.strip().startswith(("-", "*"))]
    forbid = [f for f in forbid if len(f) > 2 and not f.startswith("(")]
    leaked = [f for f in forbid if fold(f) in fold(md)]
    report(not leaked, "no rejected or private claims appear" + (f": {leaked}" if leaked else ""))

    if a.type == "letter":
        m = re.search(r"Dear .*?,(.*?)Sincerely", md, re.S)
        report(bool(m), "letter has a salutation and a sign-off")
        if m:
            n = len(m.group(1).split())
            report(n < 250, f"letter body under 250 words ({n})")
        report(not re.search(r"\[[^\]]*\]|Company Name|Your Name|Job Title", md), "no leftover placeholders")

    bullets = [l[2:].strip() for l in md.splitlines() if l.startswith("- ")]
    firsts = [b.split()[0].lower() for b in bullets if b.split()]
    dupes = sorted({w for w in firsts if firsts.count(w) > 1})
    report(not dupes, "bullet openings vary" + (f" (repeated: {dupes})" if dupes else ""), hard=False)
    long = [b for b in bullets if len(b.split()) > 38]
    report(not long, "bullets are one sentence of reasonable length" + (f" ({len(long)} too long)" if long else ""),
           hard=False)
    summary = a.type == "resume" and re.search(r"## (?:SUMMARY|RESUMEN|PERFIL|R[EÉ]SUM[EÉ]|PROFIL|PROFESSIONAL SUMMARY)\n(.+?)(\n## |\Z)", md, re.S)
    if summary:
        report(len(summary.group(1).split()) <= 75, "summary is about 3 lines or fewer", hard=False)

    if a.profile:
        prof = Path(a.profile).read_text(encoding="utf-8")
        known = numbers(prof)
        body = md
        if a.type == "resume":
            body = md.split("\n## ", 1)[1] if "\n## " in md else md  # skip the contact header
        else:
            m2 = re.search(r"Dear .*?,(.*?)Sincerely", md, re.S)
            body = m2.group(1) if m2 else md
        unknown = sorted(n for n in numbers(body) if n not in known and not re.fullmatch(r"(19|20)\d\d", n))
        report(not unknown, "every number appears in profile.md" + (f": check {unknown}" if unknown else ""))
        report("CONFIRM" not in md, "no unresolved CONFIRM marks in the resume")
        used = [x for x in AI_TOOLS if x in low and x not in prof.lower()]
        report(not used, "AI tools named here are confirmed in profile.md" + (f": not in profile {used}" if used else ""))

    if a.posting and a.type == "resume":
        raw = Path(a.posting).read_text(encoding="utf-8", errors="ignore")
        post = "\n".join(l for l in raw.splitlines() if not l.lstrip().startswith(("#", ">", "NOTE")))
        freq = {}
        for w in words(post):
            if w not in STOP:
                freq[w] = freq.get(w, 0) + 1
        terms = [w for w, n in sorted(freq.items(), key=lambda x: -x[1]) if n >= 2][:25]
        if len(terms) < 8:  # short posting: fall back to every meaningful word
            terms = [w for w, n in sorted(freq.items(), key=lambda x: (-x[1], -len(x[0]))) if len(w) >= 3][:25]
        doc = fold(md)
        have = [x for x in terms if re.search(r"(?<![a-z0-9])" + re.escape(x) + r"(?![a-z0-9])", doc)]
        miss = [x for x in terms if x not in have]
        pct = round(100 * len(have) / len(terms)) if terms else 0
        print(f"INFO keyword coverage {pct}% of {len(terms)} posting terms (whole words, accents ignored)")
        print(f"INFO matched: {have}")
        print(f"INFO missing (add only if TRUE, otherwise list in needs-input.md): {miss}")
        print("INFO coverage is a rough guide: read the missing list yourself; it is not run on letters because negations like 'I have not used X' would count as matches")

    print("ALL HARD CHECKS PASSED" if fails == 0 else f"{fails} HARD CHECK(S) FAILED")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
