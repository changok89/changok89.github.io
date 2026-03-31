# Review Note — AI 에이전트에서 재사용 가능한 Skills를 나누는 방법

- Draft: `automation/blog/drafts/2026-04-01-reusable-skills-beat-one-off-agent-prompts.md`
- Date: 2026-04-01
- Status: needs_review
- Source angle: recent agent tooling discussions around reusable skills, Claude Code/OpenClaw-style skill packaging, and the operational need to separate prompts, templates, and workflow rules

## Search intent check

- Intended queries:
  - AI 에이전트 skill 설계
  - reusable skills 만드는 방법
  - 프롬프트와 skill 차이
- Intro states the problem clearly: once agent usage becomes repetitive, skill boundaries matter more than growing one giant prompt.

## Depth check

- Covers:
  - why giant prompts become fragile in long-running use
  - what a skill should actually contain
  - practical criteria for splitting skill boundaries
  - how to separate prompt vs template vs skill responsibilities
  - common failure modes: one giant skill vs too many tiny skills
  - a practical checklist readers can use immediately
- Should comfortably clear thin-content threshold.

## Originality check

- Not a summary of a single tool release.
- Reframes current skill/tooling conversations into an operations design article.
- Strong alignment with the blog’s existing themes: AI automation, OpenClaw-style workflows, reusable operating patterns.

## Helpfulness check

- Gives readers concrete criteria for splitting skills:
  - task goal
  - tool priority
  - safety rules
  - success criteria
- Gives a reusable mental model for separating prompts, templates, and skills.
- Useful for solo builders and small teams operating agents repeatedly.

## AdSense / quality gate check

- Specific, opinionated, and practical.
- Not generic AI hype or padded content.
- Good fit for the blog’s trust/quality direction.

## Recommended next edits before publish

1. Add one short concrete walkthrough, such as a blog-writing workflow evolving from single prompt → template → dedicated skill.
2. Consider tightening a few repeated uses of “반복”, “구조”, and “경계” for rhythm.
3. Final proofread on English capitalization: decide whether to standardize `Skills` vs `skill` in the body.
