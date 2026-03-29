# Review Note — 메타 스킬과 에이전트 팀 설계가 중요한 이유

- Draft: `automation/blog/drafts/2026-03-30-meta-skills-and-agent-team-design.md`
- Date: 2026-03-30
- Status: needs_review
- Source angle: recent GeekNews front-page discussion around revfactory/harness, `.claude/` structure analysis, and long-running agent harness design posts; additionally framed through recurring practical concerns in AI automation workflows

## Search intent check

- Intended queries:
  - 메타 스킬이란 무엇인가
  - 에이전트 팀 설계 방법
  - AI 에이전트에서 생성과 검토를 분리해야 하는 이유
- Intro states the main claim early: strong agent operations depend less on one prompt and more on role separation, evaluation loops, and reusable operating structure.

## Depth check

- Covers:
  - what a meta-skill is and how it differs from a task-specific skill
  - why single-agent flows hit limits
  - common practical team patterns such as pipeline and producer-reviewer
  - why generated skills matter for context narrowing and reuse
  - how the same idea applies to blog automation and other repeatable workflows
- Should comfortably clear thin-content threshold.

## Originality check

- Not written as a summary of one plugin release.
- Uses the source topics as a trigger, then reframes them as an operational design discussion.
- Strong match with the blog’s existing themes: OpenClaw, AI automation, skills, tooling, and practical agent operations.

## Helpfulness check

- Gives readers a concrete way to think about adopting multi-agent patterns:
  - separate generation from evaluation first
  - add parallelism only where it pays off
  - treat skills as context-narrowing tools
  - use meta-skills to preserve working methods across projects
- Useful for developers experimenting with Claude Code, Codex, OpenClaw, or other agent tooling.

## AdSense / quality gate check

- Specific and experience-oriented rather than trend-chasing.
- Avoids shallow hype framing.
- Contains practical distinctions and reusable decision criteria.

## Recommended next edits before publish

1. Add one compact comparison table or bullet contrast between task skill vs meta-skill for faster scanning.
2. Consider one short real-world example showing how a producer-reviewer loop improves a blog or coding task.
3. Final proofread for repeated uses of “구조”, “운영”, and “분리” to tighten rhythm.
