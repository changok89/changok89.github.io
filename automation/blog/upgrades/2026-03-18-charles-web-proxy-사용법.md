# 업그레이드 작업지시서 — Charles Web Proxy 사용법

- 원본 경로: `_posts/2023-01-29-CharlesProxy.md`
- 현재 점수: 45
- 현재 단어 수: 243
- 현재 카테고리: Proxy
- 현재 태그: [Charles, Proxy]
- 업그레이드 사유: 본문 길이가 짧음, 핵심 블로그 주제와의 연결이 약함, 짧은 글인데 목록 위주 구성

## 목표
이 글을 AdSense 관점에서 "빈약한 콘텐츠"로 보이지 않도록 확장한다.

## 최소 목표
- 최종 단어 수 700~1200+ 단어
- 실전 맥락 추가
- 왜 필요한지 설명 추가
- 실패 사례 / 주의점 / 트러블슈팅 2개 이상 추가
- 내부 링크 2개 이상 검토
- 결론/요약 추가

## 권장 구조
1. 문제 상황
2. 왜 이 방법이 필요한가
3. 테스트 환경 / 버전 / 대상
4. 실제 단계별 방법
5. 자주 겪는 문제와 해결
6. 언제 쓰면 좋고 언제 안 쓰면 좋은가
7. 요약

## 반드시 보강할 것
- 기존 짧은 명령어/메모 스타일에서 탈피
- 단순 복붙 글처럼 보이지 않게 개인적 판단/실무 관점 추가
- Android / iOS / mobile / AI / on-device AI / SDD / vibe coding 중 관련되는 축이 있으면 자연스럽게 연결
- 제목과 본문이 정확히 맞아야 함

## 초안 작성용 참고 템플릿

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

