# Review Note — 도메인 특화 MCP가 일반 프롬프트보다 실무적인 이유

- Draft: `automation/blog/drafts/2026-03-31-domain-specific-mcp-beats-generic-prompting.md`
- Date: 2026-03-31
- Status: needs_review
- Source angle: GeekNews discussion around `Korean Law MCP` and broader MCP/tooling trends; reframed as an operational design article about domain-specific interfaces rather than a project announcement summary

## Search intent check

- Intended queries:
  - MCP 실무 활용
  - 도메인 특화 MCP가 필요한 이유
  - 법률 AI 도구는 왜 일반 프롬프트보다 구조화된 조회가 중요한가
- Intro states the thesis early: in structured domains, practical reliability comes from turning repeated lookups into tool flows, not from writing longer prompts.

## Depth check

- Covers:
  - why generic prompting becomes unreliable in complex domains
  - what domain-specific MCP changes in actual workflows
  - what the Korean Law MCP example illustrates about good domain tooling
  - how the same design applies to policy, tax, and internal technical documentation
  - a checklist for evaluating or designing domain-specific MCP tools
- Should clear thin-content threshold comfortably.

## Originality check

- Not a project summary or repo introduction only.
- Uses one repo as a trigger, then extracts broader lessons about interface design, operational reliability, and structured retrieval.
- Strong fit with the blog themes: AI tooling, automation, OpenClaw-adjacent workflows, and practical engineering trade-offs.

## Helpfulness check

- Gives readers concrete evaluation criteria:
  - separate interpretation from retrieval
  - prefer workflows over one-shot answers
  - support aliases, history, related-doc links, and verification paths
  - treat MCP as a domain interface, not just an API wrapper
- Useful for developers building internal AI systems or evaluating MCP opportunities.

## AdSense / quality gate check

- Specific, practical, and not hype-driven.
- Avoids legal-advice framing; focuses on tooling architecture and workflow design.
- Contains reusable guidance beyond the featured example.

## Recommended next edits before publish

1. Add one short end-to-end example such as “관세법 제38조 → 조문 조회 → 개정 비교 → 관련 판례” for faster scanning.
2. Consider a compact subsection contrasting generic prompt vs domain MCP as bullets.
3. Final proofread for repeated uses of “실무”, “정확한”, and “구조” to tighten rhythm.
