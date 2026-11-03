---
name: resume-builder
description: Build a truthful, ATS-friendly resume, cover letter and interview prep sheet from zero. Interviews the person with a short question set (8 quick, about 10 standard, more for complex cases; or reads files they send first), saves a fact sheet, drafts a master resume, tailors it and a cover letter to real job postings, builds PDFs and runs checks. Use whenever someone wants a resume, CV, cover letter or job-application package made, rewritten, improved or tailored, even if they only say "help me apply for jobs", "my resume is bad", "I'm a student with no experience" or paste a job link.
---

# Resume Builder

Goal: take someone from nothing to application documents that are honest, one page each, pass applicant tracking systems (ATS), and fit the jobs they actually want. Everything in them comes from the person's own answers.

## Why the method looks like this

Most bad application documents fail for three reasons: they claim things the person cannot explain in an interview, they list duties instead of results, and they are not matched to the posting. So this skill (1) collects facts first and writes second, (2) never invents a number or a skill, and (3) tailors from a saved fact sheet instead of rewriting from memory each time.

## The person decides, you advise

The person owns their documents. Offer choices, give a recommendation with the reason, then follow what they choose. The only exceptions are the **hard rules** below, which protect them (and others) from harm. For choices that go against the project's process but are theirs to make, use the pushback pattern in `references/pushback.md`: explain once, briefly, with the reason, then do what they decide.

## Sources: only what the person gave you
Every fact comes from the person's answers, files they send (old resume, LinkedIn text, transcripts, project write-ups, postings) or text they paste. No web searching, no outside facts, no "typical" achievements, unless they explicitly ask, and then label it as researched and tell them to verify. Details: `references/sources-and-files.md`.

## Working on Claude.ai (or any chat without a local folder)
- **Attached files** are usually under `/mnt/user-data/uploads/`. Read them there; if you cannot find them, ask the person to paste the text.
- **Save finished files** (PDFs, `profile.md`) in `/mnt/user-data/outputs/` when that folder exists, otherwise the working folder, and hand them to the person as downloads.
- **Chats do not keep files.** At the end, give the person `profile.md` and tell them to attach it next time to skip the interview.
- **No Chrome needed.** `scripts/build_resume.py` falls back to a built-in PDF writer (plain Helvetica, one column) when Chrome is missing. If code cannot run at all, deliver `resume.md` as plain text and tell them to paste it into Word or Google Docs.
- **No web.** Do not assume internet access; this skill never needs it (see Sources above).

## Working files

Ask where to save (default `./my-applications/`):

```
my-applications/
  profile.md                 fact sheet built from the interview (source of truth)
  resume.md                  master resume (simple markdown, see references/format.md)
  First_Last_Resume.pdf      master PDF
  sources/                   files the person sends (copies, kept local)
  jobs/<company-role>/
      posting.txt  resume.md  needs-input.md  prep.md
      First_Last_Resume_<Company>.pdf   First_Last_CoverLetter_<Company>.pdf   (file names under 50 characters)
```

Scripts live in `scripts/` next to this file. Run with `python3` (standard library only).

## The flow

Tell the person which phase they are in. Keep a task list.

### Phase 0: Set up (2 minutes)
1. If you can run code, run `python3 scripts/check_setup.py`. It checks Python and whether Chrome is available (not required) and prints what is missing in plain words. If you cannot run code, skip it and plan to deliver the resume as text.
2. Give the person this short briefing (adapt the words, keep it brief):
   - **What you need:** 5 to 15 minutes (more only for the Deep path), and any files you can send (old resume, LinkedIn text, transcripts, project write-ups, performance reviews with numbers), 1 to 3 job postings if you already know them, and honest numbers from your work (percent, dollars, hours, counts). No numbers is fine.
   - **How it works:** 8 to 11 questions in short rounds. Answer in your own words, dictate if you like. Say "skip", "I don't know" or "change that" at any time.
   - **The one rule:** I only write what you tell me, and I will ask about every number. That keeps you safe in interviews.
   - **Your choices:** which documents you want (resume, cover letter, interview prep sheet), what you want to apply for, and how it looks. You can say no to any suggestion of mine.
3. Offer the three paths in `references/paths.md` (Quick: 8 questions, Standard: up to 11, Deep: more for complex cases), recommend one, and follow their pick. Ask which documents they want.
4. If they are in a hurry (an interview or deadline within about a week, or they say so), recommend the Quick path.

### Phase 1: Interview
Follow `references/question-bank.md` for the chosen path. Ask for files early (Q3): reading what they already have saves the most time. Ask 3 to 5 questions at a time, only follow up on things they mentioned, and after each round:
- Write the answers into `profile.md` (layout in `assets/profile-template.md`). Mark uncertain items `CONFIRM`.
- For experience and projects, ask for numbers (before, after, how measured). If none exist, record "no number" and write the result in words. Never estimate for them.
- If they have little or no work experience, use `references/special-cases.md`.

### Phase 2: Read it back
Show a short summary of `profile.md`: who they are, target roles, every claim that has a number, every `CONFIRM`. Sanity-check dates against the story (for example, an expected graduation date before the target term, "first-year" with a start date two years ago, or overlapping jobs) and ask. If they said "about" for a number, keep the word "about" everywhere and offer a chance to check records before it goes out. Do not draft until they say it is accurate. This is where inflated or invented claims get caught. Start a "Never write" list in `profile.md` for anything you decline.

### Phase 3: Pick the target
Use `references/targeting.md`. Turn goals into 1 to 3 lanes (groups of similar jobs that can share one resume), rank them, collect real postings and check each is still open.

### Phase 4: Master resume
Draft `resume.md` with `references/format.md` and `references/writing-rules.md`. Show it as text, take edits, then build the PDF with `scripts/build_resume.py`.

### Phase 5: Tailor per posting
Follow `references/tailoring.md` for the resume. If they want a cover letter, follow `references/cover-letter.md`; if they want prep, follow `references/prep-sheet.md`. One folder per posting. Always write `needs-input.md`.

### Phase 6: Check and finish
Run `scripts/check_resume.py` on each resume (`--type letter` for letters, `--lang es` or similar for other languages) and fix until it passes. The checker catches numbers not in the fact sheet, banned words, claims on the "Never write" list and unconfirmed AI tools. It cannot judge truth, so you still read every line against `profile.md`. Then hand over: file paths, keyword coverage and gaps, the "needs your input" list (eligibility, missing numbers, deadlines, portal rules), a reminder that they submit applications themselves, and a plain note that Claude drafted the documents from their answers and that they must review every line before sending.

## Hard rules (these are not negotiable, reasons in references/pushback.md)
- Facts only. Never invent, round up or guess a number, tool, title, date or skill. Ask.
- A skill goes on only if the person can use it or a project of theirs proves it.
- Say where AI helped and what the person did. Never present AI output as unaided work or add an AI tool they did not name.
- Never submit an application, enter a password or send anything for them.
- Use only the person's answers, files and pasted postings as sources. Nothing from the web or your own assumptions unless they ask, and then labeled.
- Their personal data stays on their machine. Do not post it or paste it into outside tools.

## Defaults the person may change
One page, one column, plain text PDF, standard headings, no em dashes, no banned buzzwords, GPA and photo off, file name `First_Last_Resume_<Company>.pdf` under 50 characters. If a person's real content fills well under a page, say so and recommend a short resume over padding; never add filler. Short resumes scale the layout to look balanced; we never add filler words. (`--no-fill` keeps the compact layout.) See `references/pushback.md` for how to handle a request to change these.

## When to read which reference
| Need | File |
|---|---|
| The questions (core 11 and add-ons) | `references/question-bank.md` |
| Resume markdown format | `references/format.md` |
| Bullets, summary, skills, banned words, ATS | `references/writing-rules.md` |
| Lanes, fit score, open postings | `references/targeting.md` |
| Matching a posting honestly | `references/tailoring.md` |
| Cover letter | `references/cover-letter.md` |
| Interview prep sheet | `references/prep-sheet.md` |
| When the person asks for something against the process | `references/pushback.md` |
| Choosing Quick, Standard or Deep | `references/paths.md` |
| Files people can send, and the "only what they gave you" rule | `references/sources-and-files.md` |
| Students, thin profiles, changers, gaps, newcomers, academics, managers, non-English | `references/special-cases.md` |
| Saying where AI was used | `references/ai-disclosure.md` |
| Templates | `assets/` |
