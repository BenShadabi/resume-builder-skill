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
from pathlib import Path

BANNED = ["spearheaded", "leveraged", "utilized", "synergy", "pivotal", "intricate", "realm", "showcasing",
          "delve", "robust", "seamless", "dynamic", "results-driven", "passionate", "proven track record",
          "detail-oriented", "fast-paced", "team player", "go-getter", "hard-working"]
STOP = set("a an the and or of to in for with on at by from as is are be your you we our will can must have has "
           "this that these those it its their they who what which about into over more other than such not".split())


def numbers(text):
    return set(re.findall(r"\$?\d[\d,]*\.?\d*%?", text))


def words(text):
    return re.findall(r"[a-z][a-z+#.\-]{2,}", text.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume")
    ap.add_argument("--profile")
    ap.add_argument("--posting")
    ap.add_argument("--pdf")
    ap.add_argument("--type", choices=["resume", "letter"], default="resume")
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
        report(pages == 1, f"resume is one page ({pages} found)")
        report(len(Path(a.pdf).name) <= 50, f"file name {len(Path(a.pdf).name)} characters (max 50)")

    report("—" not in md and "–" not in md, "no em or en dashes")
    hits = [w for w in BANNED if w in low]
    report(not hits, "no banned words" + (f": {hits}" if hits else ""))

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
    summary = a.type == "resume" and re.search(r"## SUMMARY\n(.+?)(\n## |\Z)", md, re.S)
    if summary:
        report(len(summary.group(1).split()) <= 75, "summary is about 3 lines or fewer", hard=False)

    if a.profile:
        prof = Path(a.profile).read_text(encoding="utf-8")
        known = numbers(prof)
        # ignore years and dates-style numbers; they are checked by eye
        unknown = sorted(n for n in numbers(md) if n not in known and not re.fullmatch(r"(19|20)\d\d", n)
                         and n not in {"1", "2", "3", "0", "10", "10.5", "11"})
        report(not unknown, "every number appears in profile.md" + (f": check {unknown}" if unknown else ""))
        report("CONFIRM" not in md, "no unresolved CONFIRM marks in the resume")

    if a.posting:
        post = Path(a.posting).read_text(encoding="utf-8", errors="ignore")
        freq = {}
        for w in words(post):
            if w not in STOP:
                freq[w] = freq.get(w, 0) + 1
        terms = [w for w, n in sorted(freq.items(), key=lambda x: -x[1]) if n >= 2][:25]
        have = [t for t in terms if t in low]
        miss = [t for t in terms if t not in low]
        pct = round(100 * len(have) / len(terms)) if terms else 0
        print(f"INFO keyword coverage {pct}% of {len(terms)} frequent posting terms")
        print(f"INFO matched: {have}")
        print(f"INFO missing (add only if TRUE, otherwise list in needs-input.md): {miss}")

    print("ALL HARD CHECKS PASSED" if fails == 0 else f"{fails} HARD CHECK(S) FAILED")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
