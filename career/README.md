# Career copy — source content (draft)

This directory holds the **editorial source of truth** for CVs, portfolio descriptions, and targeted applications. It is intentionally separate from the existing Hugo/Toha presentation layer (data/en/sections/*.yaml). Nothing here is automatically published on the website.

## Files

- [profile.en.md](profile.en.md) — canonical English professional profile, selected experience, skills, and career history.
- [projects/bikeparks.en.md](projects/bikeparks.en.md) — reusable project case study with short CV copy and a longer portfolio version.
- [variants.en.md](variants.en.md) — three targeted versions (architecture, engineering leadership, senior backend) derived from the canonical facts.

## Editorial contract

1. **Facts first.** Professional history and technologies must be supported by the existing portfolio, the provided CV, or the candidate's confirmation. Never invent team sizes, revenue, client names, deployment status, numerical outcomes, or formal job titles.
2. **One canonical history.** Role variants may re-order and condense verified material but must not change facts or employment dates.
3. **Separate shipped from in-progress.** Especially important for Bikeparks intelligence and operational-status capabilities.
4. **Human accountable for AI.** Describe agent-assisted development as an engineering workflow with human architecture ownership, QA, reviews, and validation — not as autonomous output without oversight.
5. **No sensitive unpublished data.** This is a public GitHub repository. Do not add private employer/client information or direct personal contact details not already public.
6. **Readable and ATS-friendly.** Plain text, conventional section headings, outcome-led bullets, no fake keyword stuffing, and no graphics in CV output.
7. **Avoid duplication.** The portfolio is a longer narrative; the final PDF CV should usually fit in two pages.

## Verification queue (before publishing a CV)

- Confirm Nord Partner employment **start and end dates**: the old CV screenshot says Jan 2025–current, while the existing Hugo experience data says Jan 2024–present; both need correction to the true period.
- Confirm whether independent consulting ran continuously alongside employment and which projects are appropriate to disclose.
- Confirm exact leadership scope and team sizes at KISS digital, Fashion Trends Group, and ONWELO, if available.
- Gather at least 2–3 quantified, defensible outcomes from paid professional work.
- Confirm academic institution spelling and whether the Computer Science period resulted in a degree. Current draft does **not** claim a completed degree.
- Recheck which Bikeparks features have been **deployed** versus implemented/in review at the time of a specific application.
- Decide whether CV contact information should include a phone number; it is intentionally omitted from this public editorial draft.

## Future rendering workflow

1. Edit and approve this Markdown content.
2. Optionally add structured YAML/JSON front matter or an intermediate data model once the editorial structure stabilizes.
3. Render targeted CV variants to HTML and PDF; reuse the same fact bank for Hugo (currently YAML-based) and LinkedIn.
4. Keep generated PDFs out of the canonical copy directory.

_Status: editorial draft, 10 November 2026. No live website content or deployment configuration changed._
