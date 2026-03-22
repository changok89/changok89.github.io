# Review Note — 에이전트 자동화에서 실패 복구를 먼저 설계해야 하는 이유

- Draft: `automation/blog/drafts/2026-03-23-design-failure-recovery-first-in-agent-automation.md`
- Date: 2026-03-23
- Status: needs_review
- Source angle: GeekNews/news.hada.io discussions around agentic tooling, orchestration, and reliability-minded workflows

## Search intent check

- Intended queries:
  - 에이전트 자동화 장애 복구
  - AI agent reliability
  - 헬스체크 재시도 롤백 설계
- Intro establishes early that operations are judged by recovery, not demo success.

## Depth check

- Covers:
  - why demo thinking fails in production
  - common failure surfaces in agent automation
  - retry, health check, rollback, timeout, observability
  - practical rollout order and common mistakes
- Should meet non-thin content bar.

## Originality check

- Framed as operations guidance from an operator point of view, not as a summary of one external article.
- Strong continuity with OpenClaw/agent orchestration themes without depending on product-specific jargon too heavily.

## Helpfulness check

- Gives readers concrete mental models and implementation checkpoints.
- Could later be strengthened with one short incident-style example (e.g. stalled worker / silent channel failure / auth expiry).

## AdSense / quality gate check

- Helpful, specific, and not keyword-stuffed.
- Practical enough for a technical audience looking for operational advice.

## Recommended next edits before publish

1. Add a compact real-world failure timeline example.
2. Optionally include a small checklist block for "minimum production readiness".
3. Final proofread to trim repeated references to recovery and observability where wording overlaps.
