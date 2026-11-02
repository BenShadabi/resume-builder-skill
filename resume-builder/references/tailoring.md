# Tailoring a resume to a posting (honest ATS matching)

Goal: pass the applicant tracking system and speak to the human, without adding anything untrue.

## Procedure
1. Save the posting text to `jobs/<company-role>/posting.txt` (ask the person to paste it if the site blocks you).
2. Extract:
   - Must-have keywords (required skills, tools, responsibilities repeated several times).
   - Nice-to-have keywords.
   - Eligibility lines (graduation window, work authorization, language, location, term dates, GPA minimum).
   - Tone: formal (bank, law), analytical (consulting), warm and direct (startup).
3. Compare with `profile.md`:
   - **Match**: the person truly has it. Use the posting's exact spelling once in Skills and once in a bullet or the summary.
   - **Gap**: the person does not have it. Do NOT add it. Put it in `needs-input.md` and tell them.
   - **Learning**: show in brackets, for example "Power BI (learning)".
4. Tailor only these parts: summary wording, skills order and labels, which bullets come first, and the projects chosen. Keep everything else identical to the master.
5. Pick projects by relevance to the posting. A strong project that matches the job beats a weaker one that is more recent.
6. Build the PDF, then run `scripts/check_resume.py` with `--posting jobs/<x>/posting.txt` to get keyword coverage.

## Coverage numbers
- 60 percent or more coverage is good. Lower is fine if every missing term is a real gap, because adding untrue keywords is worse than a low score.
- Never hide white text, stuff keywords, or add a skill "just in case". Recruiters and interviewers notice, and it can disqualify.

## `needs-input.md` (create one per posting)
List, in plain words:
- Eligibility questions (work permit, graduation window, GPA minimum, relocation, availability for the whole term).
- Numbers or facts still missing.
- Skills the posting asks for that the person does not have, and whether to mention them as "learning".
- The deadline and the portal's own rules (extra documents, assessments, video interviews).
- Anything the person must do themselves (the application itself).

## Voice
Use the tone from step 2 for the summary only. The resume body stays plain in every tone.
