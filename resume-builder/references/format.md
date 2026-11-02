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
- Keep it to one page. The builder reports the page count.

Order of sections:
- Students and recent graduates: Summary, Education, Skills, Experience, Projects.
- Experienced people: Summary, Experience, Skills, Projects, Education.
- Career changers: Summary, Skills, Projects or relevant experience, Experience, Education.

Fitting one page: first cut the oldest or least relevant bullets, then shorten the summary, then merge skill lines. Do not shrink the font below 10 pt or the margins below 0.5 in; recruiters read on small screens.
