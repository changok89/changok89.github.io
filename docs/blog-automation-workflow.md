# Blog Automation Workflow

이 저장소의 블로그 자동화는 아래 **고정 5단계**만 사용합니다.

1. **Topic research**
2. **Planning**
3. **Writing**
4. **Review / Revision**
5. **Upload**

핵심 원칙은 간단합니다.

- 자동화는 **아이디어 정리와 초안 준비**까지는 적극적으로 돕는다.
- 하지만 **품질 게이트를 통과하지 못한 글은 절대 자동 발행하지 않는다.**
- 매일 1건만 준비한다.
  - 새 글 초안 1건 **또는**
  - 기존 얇은 글(thin post) 업그레이드 작업 1건
- 주제는 개발자 블로그 중심으로 유지한다.
  - Android
  - iOS
  - Mobile engineering
  - AI
  - On-device AI
  - SDD
  - Vibe coding

---

## Directory layout

```text
automation/blog/
  topic_backlog.json        # 새 글 주제 후보 큐
  state.json                # 마지막 실행/선택 이력
  reports/                  # 품질 분석 결과
  plans/                    # 주제별 아웃라인/계획
  drafts/                   # 발행 전 초안
  upgrades/                 # 기존 글 개선 작업지시서
  review/                   # 리뷰 체크리스트/승인 메모

docs/
  blog-automation-workflow.md
  blog-quality-gates.md

templates/
  blog_post_prompt.md
  blog_review_checklist.md
```

---

## Step 1. Topic research

입력 소스:

- `automation/blog/topic_backlog.json`
- 기존 `_posts/` 품질 분석 결과
- 최근 작성 이력(`automation/blog/state.json`)

규칙:

- 다음 글 후보는 블로그 방향성과 맞아야 한다.
- 단순 뉴스 재탕보다 **경험 기반 가이드 / 비교 / 문제 해결형 주제**를 우선한다.
- 기존 글 중 내용이 얇고 업데이트 가치가 크면 새 글보다 **업그레이드 작업을 우선**할 수 있다.

자동화 결과물:

- 새 글 후보 선정 또는 업그레이드 후보 선정

---

## Step 2. Planning

새 글이면 다음을 만든다.

- 독자 문제 정의
- 검색 의도
- 핵심 주장 2~4개
- 실전 예제/명령어/체크포인트
- 피해야 할 얇은 구성 요소

업그레이드 작업이면 다음을 만든다.

- 기존 글의 부족한 점
- 추가해야 할 섹션
- 실제 예시/스크린샷/코드/주의사항
- 최신화가 필요한 명령어와 버전 정보

자동화 결과물:

- `automation/blog/plans/*.md`
- 또는 `automation/blog/upgrades/*.md`

---

## Step 3. Writing

작성 규칙:

- 사람처럼 읽혀야 한다.
- 외부 문서를 짜깁기하지 않는다.
- 경험 기반 문장, 판단, 비교, 주의점이 있어야 한다.
- 코드/명령어/체크리스트가 가능하면 포함된다.
- 제목만 그럴듯하고 본문이 빈약한 글은 금지한다.

자동화는 초안을 만들 때 `templates/blog_post_prompt.md`의 규칙을 사용한다.

자동화 결과물:

- `automation/blog/drafts/*.md`
- 상태는 항상 **needs_review**

---

## Step 4. Review / Revision

리뷰 단계는 필수다.

반드시 확인할 것:

- 검색 의도에 실제로 답하는가?
- 본문이 너무 짧지 않은가?
- 중복/상투 표현이 많은가?
- 개인적 판단, 실무 맥락, 예시가 충분한가?
- 광고 친화성(AdSense) 관점에서 얇은 페이지처럼 보이지 않는가?
- 클릭 유도형 제목인데 내용이 약하지 않은가?
- 사실 확인이 필요한 내용은 표시했는가?

자동화가 할 수 있는 일:

- 품질 점수 산출
- 얇은 글 경고
- 업그레이드 제안
- 리뷰 체크리스트 파일 생성

자동화가 **하지 않는 일**:

- 리뷰 없이 발행 처리
- 낮은 점수 글 자동 업로드

---

## Step 5. Upload

업로드는 수동 승인 이후에만 한다.

권장 절차:

1. 초안 또는 업그레이드 작업 결과를 검토
2. 필요 수정 반영
3. Jekyll front matter 확인
4. 로컬 preview 확인
5. Git 커밋
6. GitHub에 push / PR / publish

자동화 원칙:

- 기본 파이프라인은 `_posts/`에 직접 새 글을 자동 저장하지 않는다.
- 먼저 `automation/blog/drafts/` 또는 `automation/blog/upgrades/`에 준비한다.
- 발행은 사람이 마지막으로 확인한 뒤 진행한다.

---

## Recommended daily cadence

매일 실행:

```bash
python3 scripts/blog_pipeline.py prepare
```

품질 점검:

```bash
python3 scripts/blog_quality.py scan --report automation/blog/reports/latest-quality-report.md
```

얇은 글 업그레이드 후보 보기:

```bash
python3 scripts/blog_quality.py suggest-upgrades --limit 10
```

---

## What “done” means

하루 작업이 완료된 상태는 아래 둘 중 하나입니다.

- 발행 가능한 수준의 **리뷰 대기 초안 1건**이 준비됨
- 개선 가치가 높은 **업그레이드 작업지시서 1건**이 준비됨

즉, 이 자동화의 목적은 “무조건 매일 자동 발행”이 아니라,
**매일 블로그 품질을 올릴 수 있는 다음 액션 1건을 준비하는 것**입니다.
