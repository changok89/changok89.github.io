#!/usr/bin/env python3
"""
generate_ai_news.py

간단한 AI 뉴스 요약 스크립트
- Google News 검색 RSS에서 AI 관련 기사 상위 N개 수집
- https://news.hada.io 의 최신 글 목록에서 타이틀 수집
- 간단 추출식 요약(문장 빈도 기반)
- _posts/YYYY-MM-DD-ai-news.md 파일 생성

노트: 이 스크립트는 외부 LLM을 사용하지 않고 로컬 룰 기반 요약을 사용합니다.
"""
import os
import sys
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import feedparser

# 설정
GOOGLE_NEWS_RSS = 'https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko'
HADA_URL = 'https://news.hada.io'
POSTS_DIR = '_posts'
MAX_ITEMS = 6

# 유틸: 간단 요약 (문장 중요도 기반)
def summarize_text(text, max_sents=3):
    # 문장 분리
    sents = re.split(r'(?<=[.?!])\s+', text)
    if len(sents) <= max_sents:
        return ' '.join(sents).strip()
    # 단어 빈도 계산
    words = re.findall(r"\w+", text.lower())
    freq = {}
    for w in words:
        if len(w) <= 2:
            continue
        freq[w] = freq.get(w, 0) + 1
    scores = []
    for s in sents:
        s_words = re.findall(r"\w+", s.lower())
        score = sum(freq.get(w,0) for w in s_words)
        scores.append((score, s))
    scores.sort(reverse=True)
    chosen = [s for _, s in scores[:max_sents]]
    return ' '.join(chosen).strip()


def fetch_google_news(rss_url):
    d = feedparser.parse(rss_url)
    items = []
    for entry in d.entries[:MAX_ITEMS]:
        title = entry.get('title')
        link = entry.get('link')
        summary = entry.get('summary', '')
        items.append({'title': title, 'link': link, 'summary': summary})
    return items


def fetch_hada_news(hada_url):
    try:
        r = requests.get(hada_url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return []
    soup = BeautifulSoup(r.text, 'html.parser')
    items = []
    # 시도: 기사 목록에서 링크와 제목 추출 (일반적인 구조에 유연하게 대응)
    for a in soup.select('a')[:MAX_ITEMS*2]:
        href = a.get('href')
        text = a.get_text(strip=True)
        if not href or not text:
            continue
        if len(text) < 10:
            continue
        # 절대 URL로 변환
        if href.startswith('/'):
            href = hada_url.rstrip('/') + href
        if 'http' not in href:
            continue
        items.append({'title': text, 'link': href})
        if len(items) >= MAX_ITEMS:
            break
    return items


def build_markdown(google_items, hada_items):
    today = datetime.now().strftime('%Y-%m-%d')
    title = f"AI 뉴스 요약 — {today}"
    filename = f"{today}-ai-news.md"
    lines = []
    lines.append('---')
    lines.append(f'title: "{title}"')
    lines.append(f'date: {today}')
    lines.append('categories: [AI, News]')
    lines.append('tags: [AI, News, daily]')
    lines.append('layout: post')
    lines.append('---\n')
    lines.append(f'# 오늘의 AI 뉴스 요약 ({today})\n')
    lines.append('## 핵심 포인트\n')
    # 합쳐서 간단 키워드 요약
    if google_items:
        top = google_items[0]
        lines.append(f'- 주요 헤드라인: [{top["title"]}]({top["link"]})')
    lines.append('\n')
    lines.append('## 주요 기사\n')
    idx = 1
    for it in google_items:
        summary = summarize_text(it.get('summary','') or it.get('title',''), max_sents=2)
        lines.append(f'{idx}. [{it["title"]}]({it["link"]})')
        lines.append(f'   \n   요약: {summary}\n')
        idx += 1

    if hada_items:
        lines.append('\n## Hada.io 최신글\n')
        for it in hada_items:
            lines.append(f'- [{it["title"]}]({it["link"]})')

    lines.append('\n---\n')
    lines.append('원문 링크는 각 항목을 확인하세요. 자동 수집된 요약이므로 원문을 참고하시길 권장합니다.')

    content = '\n'.join(lines)
    return filename, content


def save_post(filename, content):
    os.makedirs(POSTS_DIR, exist_ok=True)
    path = os.path.join(POSTS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def main():
    google_items = fetch_google_news(GOOGLE_NEWS_RSS)
    hada_items = fetch_hada_news(HADA_URL)
    filename, content = build_markdown(google_items, hada_items)
    path = save_post(filename, content)
    print(path)

if __name__ == '__main__':
    main()
