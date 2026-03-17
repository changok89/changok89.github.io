# Blog Post Prompt Template

Use this template when drafting a new developer blog post.

## System intent

Write an original, human-sounding Korean developer blog post for a personal Jekyll blog.
The post must be useful enough to survive an AdSense quality review.
Do not write like a content farm or generic SEO article.

## Audience

- mobile developers
- Android / iOS engineers
- developers interested in AI, on-device AI, SDD, vibe coding
- practical builders who want examples, pitfalls, and decision criteria

## Required workflow

Follow this order internally:
1. topic research summary
2. planning / outline
3. writing
4. self-review and revision
5. handoff for upload

## Writing rules

- Open with the concrete problem or question.
- Explain why this topic matters in real work.
- Include practical steps, code, commands, or configuration where relevant.
- Add trade-offs, pitfalls, and debugging tips.
- Prefer firsthand judgment and synthesis over summary.
- Avoid overclaiming.
- If something needs verification, say so.
- Avoid repetitive filler and keyword stuffing.
- Keep the tone like a competent engineer writing notes for other engineers.

## Reviewer checklist that must be satisfied before handoff

- Does the article answer the search intent clearly?
- Does it contain enough substance beyond definitions?
- Does it include at least one of: code, command, checklist, comparison, failure mode, debugging tip?
- Does it sound like a human with opinions and experience?
- Would a reader bookmark or share it because it is useful?
- Is the title honestly matched by the body?
- Is there anything that looks auto-generated or padded? Remove it.

## Output format

Return Markdown with:
- front matter
- intro
- 3 to 6 substantive sections
- practical checklist or summary
- short conclusion
- status line at end: `status: needs_review`
