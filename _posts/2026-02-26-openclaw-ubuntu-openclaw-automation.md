---
title: Ubuntu에 OpenClaw 자동화 시스템 구축하고 Telegram/코딩 자동화 연결하기
excerpt: Mini PC에 Ubuntu를 깔고 OpenClaw 설치, Telegram 연동, codex-cli 등으로 코딩 자동화를 구성하는
  방법을 단계별로 설명합니다.
permalink: /openclaw-ubuntu-openclaw-automation/
categories:
- DevOps
- Automation
tags:
- OpenClaw
- Ubuntu
- Telegram
- Automation
- codex-cli
toc: true
toc_sticky: true
toc_label: OpenClaw 설치 가이드
date: 2026-02-26
last_modified_at: 2026-03-21
---

# Ubuntu에 OpenClaw 자동화 시스템 구축하고 Telegram/코딩 자동화 연결하기

이 글은 Mini PC(또는 일반 PC)에 Ubuntu를 설치한 뒤 OpenClaw를 올리고, Telegram 연동 및 `codex-cli` 같은 도구로 코딩 자동화를 구성하는 실전 가이드다. 가능한 한 바로 따라할 수 있게 명령어 예시 중심으로 정리했다.

## 준비물 및 전제

- Mini PC 또는 일반 PC
- Ubuntu 22.04 LTS 이상 권장
- 인터넷 연결
- Telegram 계정
- Git 계정 및 GitHub 리포지터리(선택)

## 1) Ubuntu 설치

가볍게 요약하면 아래 순서다.

- 공식 Ubuntu 이미지 다운로드
- 부팅 USB 생성(Etcher, Rufus 등)
- BIOS/UEFI에서 부팅 순서 설정 후 설치 진행
- 원격 접속을 쓸 예정이면 설치 중 `OpenSSH Server` 선택

처음부터 headless 운영을 생각한다면 SSH가 바로 되도록 준비해두는 편이 편하다.

## 2) 시스템 초기 설정

기본 패키지와 필수 도구를 먼저 설치한다.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential ca-certificates
```

필요하면 `htop`, `jq`, `unzip` 같은 기본 운영 도구도 같이 넣어두면 나중에 편하다.

## 3) Node.js 및 npm 설치

OpenClaw과 일부 자동화 도구는 Node.js 환경을 사용하므로 LTS 버전을 설치한다.

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

버전 확인까지 끝나면 다음 단계로 넘어간다.

## 4) OpenClaw 설치

OpenClaw은 npm 전역 설치로 시작할 수 있다.

```bash
sudo npm install -g openclaw
openclaw --version
```

설치 중 권한 문제가 발생하면 npm 전역 설치 경로를 사용자 소유로 바꾸는 방식도 고려할 수 있다.

## 5) OpenClaw 기본 설정

Gateway(데몬) 시작과 상태 확인:

```bash
openclaw gateway start
openclaw gateway status
```

설정 파일과 인증 토큰, 외부 연동 정보는 환경변수나 config 파일로 관리하는 편이 안전하다.

## 6) Telegram 연동

### Bot 생성

1. Telegram에서 `BotFather`를 찾는다.
2. `/newbot` 명령으로 봇을 생성한다.
3. 봇 이름과 아이디를 입력한다.
4. 발급된 API 토큰을 보관한다.

### OpenClaw에 토큰 등록

환경변수 방식 예시:

```bash
export OPENCLAW_TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
```

설정 후 필요한 Connector/채널 설정을 맞추고 Gateway를 재시작한다.

> 토큰은 민감 정보다. 공개 저장소나 스크립트에 하드코딩하지 않는 편이 좋다.

## 7) codex-cli 및 기타 코딩 자동화 도구

예시로 `codex-cli`를 설치할 수 있다.

```bash
sudo npm install -g codex-cli
```

Python 기반 도구를 추가하는 경우 예시:

```bash
pip install some-cli-tool
```

이런 CLI 도구는 초안 생성, 코드 보조, 반복 작업 자동화 같은 용도로 스크립트와 결합하기 좋다.

## 8) 자동화 워크플로 예시: 블로그 포스트 생성 → 커밋 → 푸시

목표는 명령 한 줄로 새 포스트 초안을 만들고, Git 작업까지 이어가는 것이다.

예시 스크립트 `create-post.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

TITLE="$1"
if [ -z "$TITLE" ]; then
  echo "Usage: $0 \"Post Title\""
  exit 1
fi

DATE=$(date +%F)
DIR="_posts"
mkdir -p "$DIR"
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g')
FILE="$DIR/${DATE}-${SLUG}.md"

cat > "$FILE" <<EOF
---
title: "$TITLE"
excerpt: "자동 생성된 초안"
date: $DATE
---

# $TITLE

초안: 여기에 본문을 입력하세요.
EOF

git add "$FILE"
git commit -m "Add blog post: $TITLE"
git push origin main
```

이 스크립트는 가장 단순한 형태다. 실제로는 여기에 템플릿 삽입, 카테고리 지정, AI 초안 생성, 이미지 폴더 생성 같은 흐름을 더 붙일 수 있다.

예를 들면:

- 제목 기반 slug 자동 생성
- 기본 frontmatter 템플릿 적용
- AI 도구로 초안 생성
- 커밋 메시지 자동화

## 9) 보안 및 운영 팁

### 방화벽 설정

UFW를 사용하는 경우 예시:

```bash
sudo apt install -y ufw
sudo ufw allow OpenSSH
# OpenClaw에 필요한 포트가 있으면 추가 허용
sudo ufw allow 8443/tcp
sudo ufw enable
```

### 민감 정보 관리

- 토큰, API 키는 환경변수 또는 비밀 저장소에 보관
- 공개 저장소에 직접 넣지 않기
- `.env` 파일을 쓴다면 git ignore 확인

### 서비스 관리

장기 운영이라면 systemd로 관리하는 편이 좋다. 재부팅 후 자동 시작, 장애 복구, 로그 확인이 훨씬 편해진다.

## 10) 확장 아이디어

다음 단계로는 아래 같은 걸 붙일 수 있다.

- GitHub Actions로 게시 전 검증 자동화
- PR 기반 리뷰 워크플로
- OpenClaw를 통한 원격 명령 실행 및 상태 알림
- Telegram에서 명령을 받고 codex-cli 작업 실행
- cron 또는 timer 기반 정기 작업

## 마무리

OpenClaw를 Ubuntu Mini PC 위에 올리고 Telegram과 코딩 자동화 도구를 연결하면, 단순한 챗봇을 넘어서 **개인용 자동화 허브**처럼 쓸 수 있다. 핵심은 처음부터 모든 걸 붙이기보다, 설치 → 메시징 연동 → 기본 자동화 → 운영 안정화 순서로 천천히 넓혀 가는 것이다.

원하면 다음 단계로는 `create-post.sh` 같은 실제 스크립트를 리포지터리에 맞게 더 구체화해서 붙일 수 있다.
