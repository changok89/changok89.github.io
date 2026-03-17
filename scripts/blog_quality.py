#!/usr/bin/env python3
"""Scan Jekyll posts and detect thin / upgrade-worthy content."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO_ROOT / "_posts"
DEFAULT_REPORT = REPO_ROOT / "automation" / "blog" / "reports" / "latest-quality-report.md"
TOPIC_KEYWORDS = [
    "android",
    "ios",
    "iphone",
    "ipad",
    "swift",
    "swiftui",
    "xcode",
    "mobile",
    "ai",
    "llm",
    "on-device",
    "on device",
    "vibe coding",
    "sdd",
    "adb",
    "gradle",
    "jetpack",
    "compose",
    "coreml",
    "mlkit",
]


@dataclass
class PostReport:
    path: str
    title: str
    date: str
    categories: List[str]
    tags: List[str]
    word_count: int
    headings: int
    code_blocks: int
    links: int
    images: int
    list_items: int
    excerpt_present: bool
    topic_match: bool
    score: int
    band: str
    reasons: List[str]


def parse_front_matter(text: str) -> Tuple[Dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    raw_front, body = parts
    lines = raw_front.splitlines()[1:]
    front: Dict[str, object] = {}
    current_key = None
    current_list: List[str] = []
    for line in lines:
        if re.match(r"^[A-Za-z0-9_]+:\s*", line):
            if current_key is not None:
                front[current_key] = current_list
                current_key = None
                current_list = []
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if not value:
                current_key = key
                current_list = []
            elif value.startswith("[") and value.endswith("]"):
                items = [item.strip(" []\"'") for item in value.split(",") if item.strip(" []\"'")]
                front[key] = items
            else:
                front[key] = value.strip('"')
        elif current_key and line.strip().startswith("-"):
            current_list.append(line.strip().lstrip("-").strip().strip('"'))
    if current_key is not None:
        front[current_key] = current_list
    return front, body


def score_post(path: Path) -> PostReport:
    text = path.read_text(encoding="utf-8")
    front, body = parse_front_matter(text)
    body_text = re.sub(r"```.*?```", " ", body, flags=re.S)
    words = re.findall(r"[A-Za-z0-9가-힣_\-/]+", body_text)
    headings = len(re.findall(r"^#{1,6}\s+", body, flags=re.M))
    code_blocks = len(re.findall(r"```", body)) // 2
    links = len(re.findall(r"\[[^\]]+\]\([^)]+\)", body))
    images = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", body)) + len(re.findall(r"!\[[^\]]*\]\[[^\]]+\]", body))
    list_items = len(re.findall(r"^\s*[-*]\s+", body, flags=re.M))
    title = str(front.get("title", path.stem))
    excerpt = str(front.get("excerpt", "")).strip()
    categories = front.get("categories", [])
    tags = front.get("tags", [])
    if isinstance(categories, str):
        categories = [categories]
    if isinstance(tags, str):
        tags = [tags]

    combined = f"{title} {excerpt} {' '.join(categories)} {' '.join(tags)} {body[:1000]}".lower()
    topic_match = any(keyword in combined for keyword in TOPIC_KEYWORDS)

    score = 0
    reasons: List[str] = []
    word_count = len(words)

    if word_count >= 1200:
        score += 35
    elif word_count >= 900:
        score += 30
    elif word_count >= 700:
        score += 22
    elif word_count >= 450:
        score += 12
    else:
        score += 2
        reasons.append("본문 길이가 짧음")

    if headings >= 4:
        score += 15
    elif headings >= 2:
        score += 8
    else:
        score += 2
        reasons.append("구조화된 섹션이 부족함")

    if code_blocks >= 2:
        score += 15
    elif code_blocks == 1:
        score += 9
    elif links >= 2 or images >= 1:
        score += 5
    else:
        reasons.append("코드/링크/이미지 같은 실전 요소가 약함")

    if excerpt:
        score += 8
    else:
        reasons.append("excerpt 누락")

    if categories:
        score += 5
    else:
        reasons.append("categories 누락")

    if tags:
        score += 5
    else:
        reasons.append("tags 누락")

    if topic_match:
        score += 10
    else:
        reasons.append("핵심 블로그 주제와의 연결이 약함")

    if 0 < list_items <= 3:
        score += 4
    elif list_items > 12 and word_count < 700:
        reasons.append("짧은 글인데 목록 위주 구성")

    if links >= 2:
        score += 3
    if images >= 2:
        score += 2

    score = min(score, 100)
    if score >= 75:
        band = "good"
    elif score >= 55:
        band = "needs-work"
    else:
        band = "thin"

    return PostReport(
        path=str(path.relative_to(REPO_ROOT)),
        title=title,
        date=str(front.get("date", "")),
        categories=list(categories),
        tags=list(tags),
        word_count=word_count,
        headings=headings,
        code_blocks=code_blocks,
        links=links,
        images=images,
        list_items=list_items,
        excerpt_present=bool(excerpt),
        topic_match=topic_match,
        score=score,
        band=band,
        reasons=reasons,
    )


def scan_posts() -> List[PostReport]:
    reports = [score_post(path) for path in sorted(POSTS_DIR.glob("*.md"))]
    reports.sort(key=lambda item: (item.score, item.word_count))
    return reports


def render_markdown(reports: List[PostReport]) -> str:
    total = len(reports)
    thin = [r for r in reports if r.band == "thin"]
    needs_work = [r for r in reports if r.band == "needs-work"]
    good = [r for r in reports if r.band == "good"]
    lines = [
        "# Blog Quality Report",
        "",
        f"- Total posts: {total}",
        f"- Good: {len(good)}",
        f"- Needs work: {len(needs_work)}",
        f"- Thin / upgrade candidates: {len(thin)}",
        "",
        "## Upgrade candidates",
        "",
    ]
    for report in thin[:20]:
        lines.extend(
            [
                f"### {report.title}",
                f"- Path: `{report.path}`",
                f"- Score: {report.score}",
                f"- Words: {report.word_count}",
                f"- Reasons: {', '.join(report.reasons) or 'n/a'}",
                "",
            ]
        )
    lines.append("## Full results")
    lines.append("")
    for report in reports:
        lines.append(f"- [{report.band}] {report.score:>3} - {report.path} ({report.word_count} words)")
    lines.append("")
    return "\n".join(lines)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Blog quality scanner")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_parser = sub.add_parser("scan", help="scan all posts")
    scan_parser.add_argument("--report", default=str(DEFAULT_REPORT))
    scan_parser.add_argument("--json", dest="json_path")

    suggest_parser = sub.add_parser("suggest-upgrades", help="show upgrade candidates")
    suggest_parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()
    reports = scan_posts()

    if args.command == "scan":
        report_path = Path(args.report)
        ensure_parent(report_path)
        report_path.write_text(render_markdown(reports), encoding="utf-8")
        print(f"Wrote markdown report: {report_path}")
        if args.json_path:
            json_path = Path(args.json_path)
            ensure_parent(json_path)
            json_path.write_text(json.dumps([asdict(r) for r in reports], ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Wrote JSON report: {json_path}")
    elif args.command == "suggest-upgrades":
        upgrades = [r for r in reports if r.band == "thin"][: args.limit]
        for idx, report in enumerate(upgrades, start=1):
            print(f"{idx}. {report.title}")
            print(f"   path: {report.path}")
            print(f"   score: {report.score}, words: {report.word_count}")
            print(f"   why: {', '.join(report.reasons) or 'n/a'}")


if __name__ == "__main__":
    main()
