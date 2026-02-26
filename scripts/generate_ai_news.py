#!/usr/bin/env python3
"""
generate_ai_news.py

변경 사항:
- 기존에는 외부 기사 요약을 생성했으나, 요청에 맞춰 Hada.io에서 주제(제목)를 추출한 뒤
  각 주제를 '튜토리얼/가이드' 스타일의 원본 포스트로 생성하도록 변경했습니다.
- 가능하면 codex-cli를 사용해 글을 생성하고, 없으면 템플릿 기반으로 생성합니다.

동작 방식:
1) Hada.io에서 최신 제목들을 수집(주제 후보)
2) 각 제목을 주제로 codex-cli generate를 호출해 포스트 본문을 생성(또는 로컬 템플릿)
3) _posts/YYYY-MM-DD-<slug>.md 파일로 저장

주의:
- codex-cli가 설치되어 있고 PATH에 있어야 실제 모델 기반 생성을 수행합니다.
- 워크플로(또는 로컬)의 권한/환경에 맞게 테스트 후 사용하세요.
"""
import os
import re
import shlex
import subprocess
from datetime import datetime
import requests
from bs4 import BeautifulSoup

POSTS_DIR = '_posts'
HADA_URL = 'https://news.hada.io'
MAX_TOPICS = 3


def slugify(text):
    s = text.lower()
    s = re.sub(r'[^a-z0-9\- ]+', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:60]


def fetch_hada_topics(hada_url):
    try:
        r = requests.get(hada_url, timeout=10)
        r.raise_for_status()
    except Exception:
        return []
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = []
    # 선택자 유연하게 시도: h2, h3, a 등
    for tag in soup.select('h1, h2, h3, a'):
        text = tag.get_text(strip=True)
        if not text:
            continue
        # 필터: 너무 짧거나 너무 긴 텍스트는 제외
        if len(text) < 12 or len(text) > 120:
            continue
        # 중복 제거
        if text in titles:
            continue
        titles.append(text)
        if len(titles) >= MAX_TOPICS:
            break
    return titles


def generate_with_codex(prompt, timeout=30):
    # codex-cli가 설치돼 있으면 사용
    cmd = f'codex-cli generate --prompt {shlex.quote(prompt)} --language markdown --max-tokens 800'
    try:
        res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, text=True)
        return res.stdout.strip()
    except Exception as e:
        return None


def build_post_from_topic(topic):
    today = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(topic)
    filename = f"{today}-{slug}.md"
    # Prompt: 튜토리얼/가이드 형식
    prompt = (
        f"Write a clear, friendly Korean tutorial article about the following topic:\n\n"
        f"{topic}\n\n"
        "Structure:\n- Short intro (what and why)\n- Step-by-step guide or explanation with code/examples if relevant\n- Practical tips and common pitfalls\n- Short summary and further resources\n\n"
        "Tone: Helpful, senior developer, concise but friendly. Output in Markdown."
    )
    content = generate_with_codex(prompt)
    if not content:
        # fallback: simple template
        content_lines = [
            '---',
            f'title: "{topic}"',
            f'date: {today}',
            'categories: [AI, Tutorial]',
            'tags: [AI, tutorial, guide]',
            'layout: post',
            '---\n',
            f'# {topic}\n',
            '## 소개\n',
            '이 글은 위 주제에 대해 실전에서 바로 적용할 수 있는 튜토리얼 형식으로 정리한 내용입니다.\n',
            '## 단계별 가이드\n',
            '1. 준비: 필요한 도구와 환경 설정을 설명합니다.\n',
            '2. 실행: 핵심 단계와 예시 명령어를 제공합니다.\n',
            '3. 검증: 동작 확인 방법과 테스트 팁을 안내합니다.\n',
            '## 실전 팁\n',
            '- 팁 1: ...\n',
            '- 팁 2: ...\n',
            '## 마무리\n',
            '간단 요약 및 다음 단계 제안.'
        ]
        content = '\n'.join(content_lines)
    return filename, content


def save_post(filename, content):
    os.makedirs(POSTS_DIR, exist_ok=True)
    path = os.path.join(POSTS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def main():
    topics = fetch_hada_topics(HADA_URL)
    if not topics:
        print('No topics found, exiting')
        return
    created = []
    for topic in topics:
        filename, content = build_post_from_topic(topic)
        path = save_post(filename, content)
        print('Created', path)
        created.append(path)
    # Optionally print created files
    for p in created:
        print(p)

if __name__ == '__main__':
    main()
