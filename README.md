# Resume Builder skill for Claude

A skill that takes you from **zero to a finished, honest application package**: resume, cover letter and interview prep sheet. Claude interviews you with about 48 questions in short rounds, saves a fact sheet, drafts your documents, tailors them to real job postings, builds PDFs and checks them. **You decide** what you want; Claude advises and tells you, with the reason, if a choice works against the process.

It came out of a real job search, so it bakes in the lessons that mattered:

- **Facts first, writing second.** Claude only writes what you tell it. It asks about every number and never guesses.
- **Honest skills.** A tool goes on the resume only if you can use it or a project proves it.
- **ATS friendly.** One column, plain text PDF, standard headings, no tables or images.
- **Tailored, not rewritten.** Each posting gets keyword matching from your saved fact sheet. Gaps are listed for you, not hidden.
- **AI use stated plainly.** If you used AI at a step, the resume says which step and what you did yourself.
- **Checked.** A script verifies one page, no em dashes or buzzwords, and that every number on the resume exists in your fact sheet.

It never submits applications for you, and it will not invent facts (see `resume-builder/references/pushback.md` for what it will and will not do).

**See how it works:** open `docs/index.html` (a one-page visual walkthrough).

## What you get

```
resume-builder/
  SKILL.md                  the workflow Claude follows (8 phases)
  references/
    question-bank.md        the 48 questions, in 8 rounds
    writing-rules.md        bullets, summary, skills, banned words, ATS
    format.md               the simple markdown resume format
    targeting.md            turning goals into job "lanes" and checking fit
    tailoring.md            matching a posting honestly
    cover-letter.md         the 5-part, under-250-word cover letter
    prep-sheet.md           interview prep sheet
    pushback.md             what to do when a request goes against the process
    special-cases.md        students, career changers, gaps, newcomers
    ai-disclosure.md        how to say where AI helped
  assets/                   fact sheet and resume templates
  scripts/
    check_setup.py          checks your computer can run it
    build_resume.py         resume or letter .md to PDF (headless Chrome, no packages)
    check_resume.py         rule checks, letter checks and keyword coverage
examples/                   a fictional sample fact sheet, resume and cover letter
docs/index.html             visual how-it-works page
```

## Quick start (3 steps)

1. Install (below).
2. Open Claude and say: `Use the resume-builder skill. Start with the setup check.`
3. Answer the questions in your own words. Say "skip" or "change that" any time.

## Install

**Claude Code (terminal or desktop app):** copy the `resume-builder` folder into your skills folder.

```bash
mkdir -p ~/.claude/skills
cp -r resume-builder ~/.claude/skills/
```

**Claude.ai:** zip the `resume-builder` folder (the folder itself at the top of the zip) and upload it under Settings, Capabilities, Skills.

Requirements: Python 3 and Google Chrome, Chromium or Edge (used to print the PDF). No other packages.

## Use it

Open Claude and say something like:

> Use the resume-builder skill. I'm a second-year business student looking for a summer 2027 internship. Start the interview.

or paste a job link:

> Build me a resume for this posting: https://example.com/jobs/123

Claude will:

1. Explain the plan and ask Round 1 (basics) and so on through 8 rounds. Say "skip" any time.
2. Save your answers to `profile.md` and read them back so you can fix anything wrong.
3. Help you pick 1 to 3 target "lanes" and check postings are still open.
4. Draft `resume.md`, then build `resume.pdf`.
5. For each posting, tailor a copy, run the checks and write a short "needs your input" list (eligibility, missing numbers, gaps).

You always apply yourself. Claude never submits anything or enters passwords.

## The question rounds

| Round | Topic |
|---|---|
| 1 | Basics and situation |
| 2 | What you want (roles, industries, constraints) |
| 3 | Education |
| 4 | Work experience, with numbers (repeated per job) |
| 5 | Projects |
| 6 | Skills and tools, with honest levels |
| 7 | Extras and AI use |
| 8 | Style, format and the postings to target |

## Run the scripts yourself

```bash
python3 resume-builder/scripts/build_resume.py my-resume/resume.md my-resume/resume.pdf
python3 resume-builder/scripts/check_resume.py my-resume/resume.md \
  --profile my-resume/profile.md --pdf my-resume/resume.pdf --posting my-resume/jobs/acme/posting.txt
```

Try the sample first: `examples/sample-resume.md` (a fictional person).

## Privacy

Your fact sheet and resumes stay in the folder you choose on your own machine. Do not commit `profile.md` or your resumes to a public repo. The included `.gitignore` ignores `my-resume/`.

## Limits

- Claude gives advice but you choose. It will not write false facts, and it will say why.
- Built for one-page resumes in the North American style. Other countries, academic CVs and longer formats are mentioned in `references/special-cases.md` but not templated.
- It does not guarantee interviews. It makes your resume truthful, clear and matched to the posting.
- Check every claim before you send. You are the one who has to explain it.

## Contributing

Issues and pull requests are welcome, especially: questions that were missing for your field, other countries' resume norms, and better special cases. Keep the rule that the skill never invents facts.

## License

MIT. See `LICENSE`.
