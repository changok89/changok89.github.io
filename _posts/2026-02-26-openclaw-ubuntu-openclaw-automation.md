---
title: "Ubuntu에 OpenClaw 자동화 시스템 구축하고 Telegram/코딩 자동화 연결하기"
excerpt: "Mini PC에 Ubuntu를 깔고 OpenClaw 설치, Telegram 연동, codex-cli 등으로 코딩 자동화를 구성하는 방법을 단계별로 설명합니다."
permalink: /openclaw-ubuntu-openclaw-automation/
categories:
  - DevOps
  - Automation
tags:
  - [OpenClaw, Ubuntu, Telegram, Automation, codex-cli]

toc: true
toc_sticky: true
toc_label: OpenClaw 설치 가이드

date: 2026-02-26
last_modified_at: 2026-02-26
layout: post
---

# 소개

이 글은 Mini PC(또는 일반 PC)에 Ubuntu를 설치한 뒤 OpenClaw을 올리고, Telegram 연동 및 codex-cli 같은 도구로 코딩 자동화를 구성하는 실전 가이드입니다. 가능한 한 명령어 예시와 스크립트를 포함하여 바로 따라할 수 있게 작성했습니다.

---

# 준비물 및 전제

- Mini PC 또는 PC
- Ubuntu 22.04 LTS 이상 권장
- 인터넷 연결
- Git 계정 및 GitHub 리포지터리(배포용)

---

# 1) Ubuntu 설치(간단 요약)

- 공식 Ubuntu 이미지 다운로드 후 부팅 USB 생성(Etcher, Rufus 등)
- BIOS/UEFI에서 부팅 순서 설정 후 설치 진행
- SSH로 원격 접속을 사용할 경우 설치 시 "OpenSSH Server" 선택

---

# 2) 시스템 초기 설정

터미널에서 기본 패키지와 필수 도구를 설치합니다.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential ca-certificates
```

---

# 3) Node.js 및 npm 설치

OpenClaw과 일부 자동화 도구는 Node.js를 사용하므로 LTS 버전을 설치합니다.

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

---

# 4) OpenClaw 설치

OpenClaw은 NPM 패키지 또는 공식 설치 방법을 통해 설치할 수 있습니다. 전역 설치 예시는 다음과 같습니다.

```bash
sudo npm install -g openclaw
openclaw --version
```

설치 중 권한 문제가 발생하면 --unsafe-perm 플래그를 고려하거나, npm 전역 설치 경로를 사용자 소유로 변경하세요.

---

# 5) OpenClaw 기본 설정

Gateway(데몬) 시작과 상태 확인:

```bash
openclaw gateway start
openclaw gateway status
```

설정 파일(토큰, webhook 등)은 OpenClaw 문서를 참고하여 environment 또는 config 파일로 관리하세요.

---

# 6) Telegram 연동

1. Telegram Bot 생성
   - BotFather에서 /newbot 명령으로 봇 생성
   - 봇 이름과 아이디 입력 후 API 토큰 수신

2. OpenClaw에 토큰 등록
   - 환경변수 방식 권장:

```bash
export OPENCLAW_TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
```

3. OpenClaw 설정(문서에 따른 Connector 구성) 후 Gateway 재시작

> 주의: 토큰은 민감 정보입니다. 절대 공개 저장소에 하드코딩하지 마세요.

---

# 7) codex-cli 및 기타 코딩 자동화 도구

codex-cli(예시)를 전역으로 설치하거나, 사용 환경에 맞는 CLI 도구를 설치합니다.

```bash
sudo npm install -g codex-cli
# 또는 Python 기반 도구 예시
pip install some-cli-tool
```

codex-cli나 유사 도구는 프롬프트 기반으로 텍스트/코드 파일을 생성하는 데 사용합니다. 이를 스크립트와 결합하면 자동 초안 생성, 테스트 코드 작성 등을 자동화할 수 있습니다.

---

# 8) 자동화 워크플로 예시: 블로그 포스트 생성 → 커밋 → 푸시

목표: 명령 한 줄로 새 포스트 초안 생성, 커밋, 푸시까지 진행.

예시 스크립트 (create-post.sh):

```bash
#!/usr/bin/env bash
TITLE="$1"
if [ -z "$TITLE" ]; then
  echo "Usage: $0 \"Post Title\""
  exit 1
fi
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g')
DATE=$(date +%F)
DIR="_posts"
mkdir -p "$DIR"
FILE="$DIR/${DATE}-${SLUG}.md"

cat > "$FILE" <<EOF
---
title: "$TITLE"
excerpt: "자동 생성된 초안"
date: $DATE
layout: post
---

초안: 여기에 본문을 입력하세요.
EOF

# optional: generate content with codex-cli
# codex-cli generate --prompt "블로그 포스트: $TITLE" >> "$FILE"

git add "$FILE"
git commit -m "Add blog post: $TITLE"
git push origin main
```

- 위 스크립트에서 codex-cli 호출을 활성화하면 GPT/모델로 초안을 자동 생성하여 파일에 추가할 수 있습니다.

---

# 9) 보안 및 운영 팁

- 방화벽 설정(UFW):

```bash
sudo apt install ufw
sudo ufw allow OpenSSH
# OpenClaw이 사용하는 포트가 있다면 허용
sudo ufw allow 8443/tcp
sudo ufw enable
```

- 민감 정보(토큰, 키)는 환경변수나 Vault에 보관하세요.
- 서비스는 systemd로 관리하면 편리합니다. 예: OpenClaw gateway를 systemd 서비스로 등록

---

# 10) 확장 아이디어

- GitHub Actions 등 CI와 연계하여 게시 전 검증(문법 검사, 링크 검사) 단계 추가
- PR 기반 워크플로로 리뷰 자동화
- OpenClaw를 이용해 원격 명령 실행 및 상태 알림 자동화

---

# 마무리

이 가이드는 실무 적용 가능한 기본 흐름을 제공합니다. 원하시면 제가 create-post.sh 같은 스크립트를 리포지터리에 추가하고 커밋·푸시해드리겠습니다. 수정할 원하는 포인트(예: Node 버전, 포트, system user 등)를 알려주세요.
