# Review Note — AI 코딩 에이전트에게 일을 맡길수록 완료 조건을 검증 가능하게 써야 하는 이유

- Draft: `automation/blog/drafts/2026-04-02-verifiable-done-criteria-for-ai-coding-agents.md`
- Date: 2026-04-02
- Status: needs_review
- Source angle: ongoing developer discussions around agentic coding, software factory workflows, and the shift from code generation speed to verification quality

## Search intent check

- Intended queries:
  - AI 코딩 에이전트 완료 조건
  - AI 코딩 프롬프트보다 중요한 것
  - AI 코딩 검증 기준
  - 에이전트 작업 지시 방법
- Intro states the core claim early: implementation gets cheaper, so verifiable done criteria matter more.

## Depth check

- Covers:
  - why completion criteria matter more in agent workflows
  - why vague requests create longer correction loops
  - how to define observable success states
  - why scope, validation, and reporting format should be part of the request
  - reusable patterns for bugs, feature work, refactoring, and documentation tasks
  - why teams should externalize done criteria into repeatable operating rules
- Should clear thin-content threshold.

## Originality check

- Not a summary of one external article.
- Strong practical framing based on software delivery and review cost.
- Fits the blog’s AI automation / developer workflow theme well.

## Helpfulness check

- Includes immediately reusable structure:
  - goal
  - scope
  - done criteria
  - validation
  - reporting
- Gives concrete examples instead of only trend commentary.
- Useful for developers already trying agent-assisted coding in real repositories.

## AdSense / quality gate check

- Substantive and specific.
- Not thin trend-chasing content.
- Strong enough for review-stage draft status.

## Recommended next edits before publish

1. Add one short concrete repository example with file names or pseudo-diff context.
2. Consider adding a compact checklist box titled `AI 작업 지시 전 확인할 5가지`.
3. Final proofread for repeated phrases around 검증 가능 / 완료 조건 to tighten rhythm.
