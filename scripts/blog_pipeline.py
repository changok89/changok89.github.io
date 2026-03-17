#!/usr/bin/env python3
"""Prepare one daily blog task: either a publishable-review draft or an upgrade task."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List

from blog_quality import scan_posts

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = REPO_ROOT / "automation" / "blog"
REPORTS_DIR = AUTOMATION_DIR / "reports"
PLANS_DIR = AUTOMATION_DIR / "plans"
DRAFTS_DIR = AUTOMATION_DIR / "drafts"
UPGRADES_DIR = AUTOMATION_DIR / "upgrades"
REVIEW_DIR = AUTOMATION_DIR / "review"
STATE_PATH = AUTOMATION_DIR / "state.json"
TOPIC_BACKLOG_PATH = AUTOMATION_DIR / "topic_backlog.json"
PROMPT_TEMPLATE_PATH = REPO_ROOT / "templates" / "blog_post_prompt.md"
REVIEW_TEMPLATE_PATH = REPO_ROOT / "templates" / "blog_review_checklist.md"

DEFAULT_TOPICS = [
    {
        "title": "Android Studio에서 ADB와 scrcpy 조합으로 실기기 디버깅 시간을 줄이는 방법",
        "category": "Android",
        "tags": ["Android", "adb", "scrcpy", "debugging"],
        "intent": "실기기 디버깅 세팅을 빠르게 반복하는 개발자를 위한 가이드",
    },
    {
        "title": "SwiftUI 프로젝트에 온디바이스 AI 기능을 얹을 때 먼저 결정해야 하는 것들",
        "category": "iOS",
        "tags": ["iOS", "SwiftUI", "on-device AI", "Core ML"],
        "intent": "온디바이스 AI 기능 도입 전 판단 포인트 정리",
    },
    {
        "title": "모바일 앱 개발에서 vibe coding을 써도 되는 영역과 위험한 영역",
        "category": "Mobile",
        "tags": ["mobile", "vibe coding", "AI", "workflow"],
        "intent": "AI 코딩 보조를 실무에 적용할 때 경계선을 설명",
    },
    {
        "title": "SDD 방식으로 Android와 iOS 기능 명세를 가볍게 유지하는 템플릿",
        "category": "Engineering",
        "tags": ["SDD", "Android", "iOS", "planning"],
        "intent": "기능 명세와 구현 사이의 마찰을 줄이는 실전 템플릿 소개",
    },
    {
        "title": "LLM API 대신 온디바이스 AI를 선택해야 하는 모바일 기능 5가지",
        "category": "AI",
        "tags": ["AI", "on-device AI", "mobile", "privacy"],
        "intent": "모바일 제품에서 온디바이스 AI 적합 사례 설명",
    },
]


def ensure_dirs() -> None:
    for path in [AUTOMATION_DIR, REPORTS_DIR, PLANS_DIR, DRAFTS_DIR, UPGRADES_DIR, REVIEW_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def slugify(text: str) -> str:
    lowered = text.lower()
    lowered = lowered.replace("on-device", "on-device")
    lowered = re.sub(r"[^a-z0-9가-힣\s-]", "", lowered)
    lowered = re.sub(r"\s+", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-")
    return lowered[:80] or "post"


def initialize_backlog() -> List[Dict[str, object]]:
    if not TOPIC_BACKLOG_PATH.exists():
        save_json(TOPIC_BACKLOG_PATH, DEFAULT_TOPICS)
    return load_json(TOPIC_BACKLOG_PATH, DEFAULT_TOPICS)


def load_state() -> Dict[str, object]:
    return load_json(STATE_PATH, {"history": [], "approved": []})


def choose_upgrade_candidate():
    reports = scan_posts()
    candidates = [r for r in reports if r.band == "thin"]
    if not candidates:
        return None
    return candidates[0]


def choose_new_topic(backlog: List[Dict[str, object]], state: Dict[str, object]):
    used_titles = {item.get("title") for item in state.get("history", [])}
    for item in backlog:
        if item["title"] not in used_titles:
            return item
    return backlog[0] if backlog else None


def build_plan(topic: Dict[str, object], today: str) -> str:
    tags = ", ".join(topic.get("tags", []))
    return f"""# Planning

- Date: {today}
- Topic: {topic['title']}
- Search intent: {topic.get('intent', '')}
- Primary category: {topic.get('category', '')}
- Tags: {tags}

## Target reader problem
독자는 실무에서 바로 쓸 수 있는 판단 기준, 설정 방법, 함정 회피 포인트를 원한다.

## Article angle
- 단순 개념 설명보다 실무 관점으로 접근한다.
- 선택 기준과 실패 포인트를 반드시 넣는다.
- 모바일 개발자 관점에서 왜 중요한지 설명한다.

## Proposed outline
1. 문제 정의 / 왜 지금 중요한가
2. 실제 적용 상황
3. 단계별 설정 또는 구현 방법
4. 실패하기 쉬운 부분 / 디버깅 포인트
5. 대안 비교 또는 선택 기준
6. 결론 / 언제 이 방법을 쓰면 좋은가

## Evidence to include
- 코드 또는 명령어 예시 1개 이상
- 실무 팁 3개 이상
- 흔한 함정 2개 이상
- 링크/참고자료 필요 시 최소한만 추가

## Status
needs_review
"""


def build_draft(topic: Dict[str, object], today: str) -> str:
    prompt_rules = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    review_rules = REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8")
    slug = slugify(topic['title'])
    tag_list = ", ".join(topic.get("tags", []))
    return f"""---
title: "{topic['title']}"
excerpt: "{topic.get('intent', '실무형 개발자 가이드')}"
categories:
  - {topic.get('category', 'Engineering')}
tags:
  - [{tag_list}]
layout: post
date: {today}
last_modified_at: {today}
status: needs_review
---

> 이 문서는 자동화 파이프라인이 준비한 **리뷰 대기 초안**입니다. 품질 확인 후 `_posts/{today}-{slug}.md`로 이동해 발행하세요.

# 초안 방향

- 독자 문제: {topic.get('intent', '')}
- 포지션: 실무형 개발자 블로그
- 주제 축: {topic.get('category', '')}

## 작성 메모

이 초안은 intentionally verbose한 구조를 사용합니다. 실제 발행 전에는 개인 경험, 사용한 버전, 실패 사례, 코드 예시를 반드시 채워 넣어야 합니다.

## 추천 아웃라인

### 1. 왜 이 주제가 지금 중요한가
- 모바일 개발/AI/자동화 맥락에서 배경 설명
- 이 글을 읽으면 무엇을 줄일 수 있는지 설명

### 2. 기본 개념보다 먼저 알아야 할 판단 기준
- 언제 이 방법이 맞는지
- 언제 과한지
- 팀/개인 프로젝트에서 다르게 볼 점

### 3. 실제 설정/구현/워크플로 예시
```bash
# TODO: 실제 명령어나 코드 예시 추가
```

### 4. 자주 막히는 지점
- 버전 차이
- 디버깅 포인트
- 잘못된 기대치

### 5. 내 기준의 추천안
- 대안 비교
- 선택 기준
- 운영 팁

## 셀프 리뷰 규칙

{prompt_rules}

## 최종 리뷰 체크리스트

{review_rules}

status: needs_review
"""


def build_upgrade_task(candidate, today: str) -> str:
    review_rules = REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8")
    slug = slugify(candidate.title)
    return f"""# Upgrade Task

- Date: {today}
- Target post: `{candidate.path}`
- Title: {candidate.title}
- Score: {candidate.score}
- Word count: {candidate.word_count}
- Status: needs_review

## Why this post was selected

이 글은 현재 thin post 후보입니다.

- 사유: {', '.join(candidate.reasons) or 'n/a'}
- 구조 섹션 수: {candidate.headings}
- 코드 블록 수: {candidate.code_blocks}
- 링크 수: {candidate.links}

## Upgrade direction

1. 검색 의도를 더 직접적으로 답하는 서론으로 수정
2. 실제 사용 사례 / 실패 사례 / 주의점 추가
3. 코드, 명령어, 설정 예시 보강
4. 최신 도구/버전 기준으로 설명 업데이트
5. 결론에 선택 기준과 추천 시나리오 추가

## Suggested new sections

- 왜 이 주제가 아직도 중요한가
- 빠른 시작
- 실전 예시
- 흔한 오류와 해결 방법
- 언제 다른 대안을 선택할지

## Publish rule

이 작업지는 업그레이드 준비용이다. 원문 수정 후 품질 점수를 다시 확인하기 전까지 발행 완료로 간주하지 않는다.

## Review checklist

{review_rules}
"""


def write_task_files(today: str, mode: str, payload: Dict[str, object] | None = None, candidate=None):
    if mode == "new":
        topic = payload
        slug = slugify(topic["title"])
        plan_path = PLANS_DIR / f"{today}-{slug}.md"
        draft_path = DRAFTS_DIR / f"{today}-{slug}.md"
        review_path = REVIEW_DIR / f"{today}-{slug}-review.md"
        plan_path.write_text(build_plan(topic, today), encoding="utf-8")
        draft_path.write_text(build_draft(topic, today), encoding="utf-8")
        review_path.write_text(REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        return {"mode": mode, "plan": str(plan_path.relative_to(REPO_ROOT)), "draft": str(draft_path.relative_to(REPO_ROOT)), "review": str(review_path.relative_to(REPO_ROOT)), "title": topic["title"]}

    slug = slugify(candidate.title)
    upgrade_path = UPGRADES_DIR / f"{today}-{slug}.md"
    review_path = REVIEW_DIR / f"{today}-{slug}-review.md"
    upgrade_path.write_text(build_upgrade_task(candidate, today), encoding="utf-8")
    review_path.write_text(REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    return {"mode": mode, "upgrade": str(upgrade_path.relative_to(REPO_ROOT)), "review": str(review_path.relative_to(REPO_ROOT)), "title": candidate.title}


def prepare(day: str | None = None, prefer: str = "auto") -> Dict[str, object]:
    ensure_dirs()
    backlog = initialize_backlog()
    state = load_state()
    today = day or date.today().isoformat()

    reports = scan_posts()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "latest-quality-report.json").write_text(
        json.dumps([r.__dict__ for r in reports], ensure_ascii=False, indent=2), encoding="utf-8"
    )

    upgrade_candidate = choose_upgrade_candidate()
    mode = "upgrade" if upgrade_candidate else "new"
    if prefer in {"new", "upgrade"}:
        mode = prefer

    if mode == "upgrade" and upgrade_candidate:
        result = write_task_files(today=today, mode="upgrade", candidate=upgrade_candidate)
    else:
        topic = choose_new_topic(backlog, state)
        result = write_task_files(today=today, mode="new", payload=topic)

    state.setdefault("history", []).append(
        {
            "date": today,
            "mode": result["mode"],
            "title": result["title"],
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_json(STATE_PATH, state)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily blog pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_parser = sub.add_parser("prepare", help="prepare one daily task")
    prepare_parser.add_argument("--date")
    prepare_parser.add_argument("--prefer", choices=["auto", "new", "upgrade"], default="auto")

    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(day=args.date, prefer=args.prefer)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\nNo post was auto-published. Review is required before upload.")


if __name__ == "__main__":
    main()
