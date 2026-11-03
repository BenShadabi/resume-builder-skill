# Resume markdown format

The builder reads a tiny markdown format so people can edit the resume in any text editor.

```
# Full Name
City, Country  |  phone  |  email  |  linkedin.com/in/name
github.com/name

## SUMMARY
Two or three lines.

## EDUCATION
### Degree, Program :: Expected Apr 2028
School, City, Country
Relevant coursework: A, B, C

## SKILLS
**Tools:** Excel (pivot tables), SQL, Python
**Languages:** English, Spanish

## EXPERIENCE
### Job Title :: May 2020 to Jun 2023
Employer, City, Country
- Bullet one.
- Bullet two.

## PROJECTS
### Project name :: github.com/name/repo
- Bullet one.
```

Rules:
- `# ` is the name (once). The next non-empty lines are the contact lines.
- `## ` starts a section. Use the standard headings.
- `### Left :: Right` makes a bold left part and a right-aligned part (dates or a link).
- Plain lines are paragraphs (employer line, coursework line). `**Label:** text` bolds the label.
- `- ` lines are bullets.
- Keep it to one page. The builder reports the page count. Short resumes scale the layout to look balanced; we never add filler words.

Order of sections:
- Students and recent graduates: Summary, Education, Skills, Experience, Projects.
- Experienced people: Summary, Experience, Skills, Projects, Education.
- Career changers: Summary, Skills, Projects or relevant experience, Experience, Education.

Fitting one page: first cut the oldest or least relevant bullets, then shorten the summary, then merge skill lines. Do not shrink the font below 10 pt or the margins below 0.5 in; recruiters read on small screens.

## Optional sections, other languages, paper size
- Extra sections you may add after the main ones: CERTIFICATIONS, PUBLICATIONS (selected, for industry resumes), VOLUNTEERING. **Omit any section the person has nothing for** (for example no PROJECTS).
- Headings may be translated (RESUMEN, EXPERIENCIA, EDUCACION). Build with `--lang es` so the PDF is tagged correctly.
- Paper: `--paper A4` for most countries outside North America (default is Letter).
- Personal data lines (date of birth, nationality) only if the person insists, which is their call. Put them on the contact lines, never invent them, and note in `needs-input.md` if they have not supplied them.
- The builder cannot place a photo. Say so if asked.
- Section order for academics moving to industry: Summary, Education, Experience (research and teaching, in plain industry language), Skills, Selected publications (2 to 3), Projects.
