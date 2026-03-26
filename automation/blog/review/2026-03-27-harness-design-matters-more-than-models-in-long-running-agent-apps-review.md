# Review Note — 장기 실행 AI 에이전트 앱에서는 모델보다 하네스 설계가 더 중요하다

- Draft: `automation/blog/drafts/2026-03-27-harness-design-matters-more-than-models-in-long-running-agent-apps.md`
- Date: 2026-03-27
- Status: needs_review
- Source angle: GeekNews/news.hada.io front-page discussion around long-running application harness design, AI coding agents, local execution, and operational reliability in March 2026

## Search intent check

- Intended queries:
  - AI 에이전트 하네스 설계
  - 장기 실행 AI 앱 안정성
  - AI 에이전트 앱 실패 복구 구조
- Intro states the thesis early: long-running agent apps are limited more by harness design than by raw model quality.

## Depth check

- Covers:
  - what harness means in practical product terms
  - why long-running systems surface non-model failures first
  - state transitions, retries, checkpointing, and user-visible progress
  - why session boundaries and task boundaries should be separated
  - a concrete messenger-driven automation flow example
- Should clear thin-content threshold.

## Originality check

- Not a summary of one article.
- Reframes current discussion into a practical engineering lens tied to agent operations.
- Strong fit with existing themes: OpenClaw, automation, agent reliability, and operations.

## Helpfulness check

- Gives readers a concrete checklist for architecture decisions:
  - define state transitions
  - separate session from execution units
  - make retries conditional
  - show actionable status to users
  - decide where human approval belongs
- Useful for developers turning agent demos into actual products.

## AdSense / quality gate check

- Substantive and opinionated without sounding like generic AI trend commentary.
- Practical enough to feel experience-based.
- Topic overlaps adjacent posts on agent reliability, but angle is distinct enough because the focus is harness architecture rather than only failure recovery.

## Recommended next edits before publish

1. Add one short comparison table or bullet contrast between "좋은 모델 / 약한 하네스" and "충분한 모델 / 강한 하네스".
2. Tighten repeated uses of 하네스 and 장기 실행 in consecutive paragraphs.
3. Consider one explicit OpenClaw-like example for session orchestration, approvals, or background runs if you want stronger practitioner flavor.
