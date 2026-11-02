# Cover letter

Write one only if the person wants it and the posting does not say "resume only". Everything comes from `profile.md` and from company text the person provided.

## Why this structure
Recruiters skim a letter in under a minute. It should prove three things fast: you read about this company, you can do the job, and you can be honest and clear. Five short parts, about 2 sentences each, under 250 words, one page, same font as the resume.

## The 5 parts
1. **Header block:** date, contact name (or "Hiring Manager"), company, location, and a "Re:" line with the job title and ID.
2. **Opening:** the role, where you saw it, and one sentence on why THIS company, from real research (a recent project, product, deal or mission statement with a date). Not "I am excited".
3. **Education or background:** what you studied or learned and one project that matches the job.
4. **Experience:** your strongest relevant result with a real number from `profile.md`.
5. **Close:** the company's mission or value you actually share, what you would bring, and a plain thank-you.

## Company facts: only what the person gave you
Use the posting's own wording, and any company text or news the person pasted or sent. Do not search the web unless they ask. If they ask, add one verified, dated item, mark it `researched: <URL, date>`, and list it in `needs-input.md` to verify before sending. With nothing to use, write the opening from the posting and say so (see the last section).

## Rules
- Date: write the real date of sending (ask if unsure). Use "Month D, YYYY".
- If the school city or other small detail is missing from `profile.md`, ask or leave it out; do not guess.
- Do not raise a skill level in the letter. A beginner course stays "a beginner course", not "the work I do now".
- Under 250 words in the body. One page. No bullet lists.
- Plain sentences. Do not start every sentence with "I". No buzzwords, no em dashes.
- Be honest about gaps; do not apologise for them.
- Same facts as the resume, different angle. Do not introduce a claim that is not in `profile.md`.
- "Dear <Name>," if you know the name, else "Dear Hiring Manager,". Sign off "Sincerely," and the name.

## File format
Use the same markdown builder as the resume. Template: `assets/cover-letter-template.md`. Build with `scripts/build_resume.py cover-letter.md cover-letter.pdf`, check with `scripts/check_resume.py cover-letter.md --type letter`.

## When the company cannot be researched
If the company is unknown, fictional or you cannot verify anything, do not invent news. Use the posting's own wording for the opening and add a line to `needs-input.md`: "Company research not done: verify and add one real, dated item before sending."
