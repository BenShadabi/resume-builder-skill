# Cover letter

Write one only if the person wants it and the posting does not say "resume only". Everything comes from `profile.md` and real research about the company.

## Why this structure
Recruiters skim a letter in under a minute. It should prove three things fast: you read about this company, you can do the job, and you can be honest and clear. Five short parts, about 2 sentences each, under 250 words, one page, same font as the resume.

## The 5 parts
1. **Header block:** date, contact name (or "Hiring Manager"), company, location, and a "Re:" line with the job title and ID.
2. **Opening:** the role, where you saw it, and one sentence on why THIS company, from real research (a recent project, product, deal or mission statement with a date). Not "I am excited".
3. **Education or background:** what you studied or learned and one project that matches the job.
4. **Experience:** your strongest relevant result with a real number from `profile.md`.
5. **Close:** the company's mission or value you actually share, what you would bring, and a plain thank-you.

## Research step
Search the company: recent news, product launches, reports, mission or values page. Use 1 verified item with its date. If sources disagree or you could not confirm, say less or hedge, and list the item in `needs-input.md` as "verify before quoting". If you cannot find anything real, use the posting's own wording instead of inventing.

## Rules
- Under 250 words in the body. One page. No bullet lists.
- Plain sentences. Do not start every sentence with "I". No buzzwords, no em dashes.
- Be honest about gaps; do not apologise for them.
- Same facts as the resume, different angle. Do not introduce a claim that is not in `profile.md`.
- "Dear <Name>," if you know the name, else "Dear Hiring Manager,". Sign off "Sincerely," and the name.

## File format
Use the same markdown builder as the resume. Template: `assets/cover-letter-template.md`. Build with `scripts/build_resume.py cover-letter.md cover-letter.pdf`, check with `scripts/check_resume.py cover-letter.md --type letter`.
