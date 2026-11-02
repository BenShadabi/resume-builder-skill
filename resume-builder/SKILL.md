---
name: resume-builder
description: Build a truthful, ATS-friendly resume, cover letter and interview prep sheet from zero. Interviews the person with about 48 questions in rounds (goals, target roles, education, experience, projects, skills, AI use), saves a fact sheet, drafts a master resume, tailors it and a cover letter to real job postings, builds PDFs and runs checks. Use whenever someone wants a resume, CV, cover letter or job-application package made, rewritten, improved or tailored, even if they only say "help me apply for jobs", "my resume is bad", "I'm a student with no experience" or paste a job link.
---

# Resume Builder

Goal: take someone from nothing to application documents that are honest, one page each, pass applicant tracking systems (ATS), and fit the jobs they actually want. Everything in them comes from the person's own answers.

## Why the method looks like this

Most bad application documents fail for three reasons: they claim things the person cannot explain in an interview, they list duties instead of results, and they are not matched to the posting. So this skill (1) collects facts first and writes second, (2) never invents a number or a skill, and (3) tailors from a saved fact sheet instead of rewriting from memory each time.

## The person decides, you advise

The person owns their documents. Offer choices, give a recommendation with the reason, then follow what they choose. The only exceptions are the **hard rules** below, which protect them (and others) from harm. For choices that go against the project's process but are theirs to make, use the pushback pattern in `references/pushback.md`: explain once, briefly, with the reason, then do what they decide.

## Working files

Ask where to save (default `./my-applications/`):

```
my-applications/
  profile.md        fact sheet built from the interview (source of truth)
  resume.md         master resume (simple markdown, see references/format.md)
  jobs/<company-role>/
      posting.txt  resume.md  resume.pdf  cover-letter.md  cover-letter.pdf  prep.md  needs-input.md
```

Scripts live in `scripts/` next to this file. Run with `python3` (standard library only).

## The flow

Tell the person which phase they are in. Keep a task list.

### Phase 0: Set up (2 minutes)
1. Run `python3 scripts/check_setup.py`. It checks Python and a browser for PDFs and prints what is missing in plain words. Fix or explain anything missing.
2. Give the person this short briefing (adapt the words, keep it brief):
   - **What you need:** 20 to 40 minutes, your old resume or LinkedIn if you have one, 1 to 3 job postings if you already know them, and honest numbers from your work (percent, dollars, hours, counts). No numbers is fine.
   - **How it works:** about 48 questions in 8 short rounds. Answer in your own words, dictate if you like. Say "skip", "I don't know" or "change that" at any time.
   - **The one rule:** I only write what you tell me, and I will ask about every number. That keeps you safe in interviews.
   - **Your choices:** which documents you want (resume, cover letter, interview prep sheet), what you want to apply for, and how it looks. You can say no to any suggestion of mine.
3. Ask which documents they want and which situation applies (student, graduate, career changer, returning, experienced).

### Phase 1: Interview (Rounds 1 to 8)
Follow `references/question-bank.md`. Ask 5 to 8 questions at a time and wait. After each round:
- Write the answers into `profile.md` (layout in `assets/profile-template.md`). Mark uncertain items `CONFIRM`.
- For experience and projects, ask for numbers (before, after, how measured). If none exist, record "no number" and write the result in words. Never estimate for them.
- If they have little or no work experience, use `references/special-cases.md`.

### Phase 2: Read it back
Show a short summary of `profile.md`: who they are, target roles, every claim that has a number, every `CONFIRM`. Do not draft until they say it is accurate. This is where inflated or invented claims get caught.

### Phase 3: Pick the target
Use `references/targeting.md`. Turn goals into 1 to 3 lanes (groups of similar jobs that can share one resume), rank them, collect real postings and check each is still open.

### Phase 4: Master resume
Draft `resume.md` with `references/format.md` and `references/writing-rules.md`. Show it as text, take edits, then build the PDF with `scripts/build_resume.py`.

### Phase 5: Tailor per posting
Follow `references/tailoring.md` for the resume. If they want a cover letter, follow `references/cover-letter.md`; if they want prep, follow `references/prep-sheet.md`. One folder per posting. Always write `needs-input.md`.

### Phase 6: Check and finish
Run `scripts/check_resume.py` on each resume (`--type letter` for letters) and fix until it passes. Then hand over: file paths, keyword coverage and gaps, the "needs your input" list (eligibility, missing numbers, deadlines, portal rules), and a reminder that they submit applications themselves.

## Hard rules (these are not negotiable, reasons in references/pushback.md)
- Facts only. Never invent, round up or guess a number, tool, title, date or skill. Ask.
- A skill goes on only if the person can use it or a project of theirs proves it.
- Say where AI helped and what the person did. Never present AI output as unaided work or add an AI tool they did not name.
- Never submit an application, enter a password or send anything for them.
- Their personal data stays on their machine. Do not post it or paste it into outside tools.

## Defaults the person may change
One page, one column, plain text PDF, standard headings, no em dashes, no banned buzzwords, GPA and photo off, file name under 50 characters. See `references/pushback.md` for how to handle a request to change these.

## When to read which reference
| Need | File |
|---|---|
| Questions for each round | `references/question-bank.md` |
| Resume markdown format | `references/format.md` |
| Bullets, summary, skills, banned words, ATS | `references/writing-rules.md` |
| Lanes, fit score, open postings | `references/targeting.md` |
| Matching a posting honestly | `references/tailoring.md` |
| Cover letter | `references/cover-letter.md` |
| Interview prep sheet | `references/prep-sheet.md` |
| When the person asks for something against the process | `references/pushback.md` |
| Students, changers, gaps, newcomers | `references/special-cases.md` |
| Saying where AI was used | `references/ai-disclosure.md` |
| Templates | `assets/` |
