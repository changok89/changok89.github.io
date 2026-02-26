---
title: "Ubuntu에 OpenClaw 자동화 시스템 구축하고 Telegram/코딩 자동화 연결하기"
date: 2026-02-26
layout: post
---

이 글에서는 Mini PC(또는 일반 PC)에 Ubuntu를 설치한 뒤 OpenClaw을 설치하고 Telegram 연동, 그리고 codex-cli 등 도구를 이용해 코딩 자동화 워크플로를 구성하는 방법을 단계별로 안내합니다. 실전에서 바로 따라할 수 있도록 명령어와 설정 예시를 제공합니다.

1) 준비물 및 전제
- Mini PC 또는 PC
- Ubuntu 22.04 LTS 이상 (권장)
- 인터넷 연결
- Git 계정 및 GitHub 리포지터리 (블로그 등 배포용)

2) Ubuntu 설치(요약)
- 공식 Ubuntu 이미지 다운로드 및 부팅 USB 생성(Etcher, Rufus 등)
- BIOS/UEFI에서 부팅 순서 설정 후 설치 진행
- SSH로 원격 접근하려면 "OpenSSH Server" 설치 체크

3) 시스템 초기 설정
```bash
# 업데이트
sudo apt update && sudo apt upgrade -y
# 필수 도구 설치
sudo apt install -y git curl build-essential ca-certificates
```

4) Node.js 및 npm 설치 (OpenClaw과 일부 툴 의존)
```bash
# NodeSource 사용 예 (LTS)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
# 확인
node -v
npm -v
```

5) OpenClaw 설치
OpenClaw는 NPM을 통해 설치되는 툴(또는 제공된 설치 방법)을 사용합니다. 일반적으로 전역 설치를 권장합니다.

```bash
# 전역으로 설치 (예시)
sudo npm install -g openclaw
# 설치 확인
openclaw --version
```

설치 경로와 권한 문제가 있으면 --unsafe-perm 또는 npm 전역 경로를 사용자 로컬로 변경하는 방법을 고려하세요.

6) OpenClaw 기본 설정
- Gateway(데몬) 시작, 상태 확인
```bash
openclaw gateway start
openclaw gateway status
```
- 필요한 설정 파일(토큰, webhook 등)은 OpenClaw 문서에 따라 구성합니다.

7) Telegram 연동 (bot 생성 및 토큰 등록)
- BotFather로 봇 생성: /newbot → 이름/아이디 지정 → 토큰 수신
- OpenClaw에 토큰 등록(예: 환경변수 또는 설정 파일)

예: 환경변수 방식
```bash
export OPENCLAW_TELEGRAM_TOKEN="<your-bot-token>"
# 또는 systemd 서비스 환경에 넣기
```

OpenClaw이 Telegram 통합을 지원한다면 안내 문서대로 Gateway/Connector에 토큰을 넣고 재시작하세요.

8) codex-cli 및 코딩 자동화 도구 설치
- codex-cli (사용 가능한 경우) 또는 다른 커맨드라인 코드 생성 도구 설치

```bash
# 예시: 전역 설치
sudo npm install -g codex-cli
# 또는 pip 기반 도구
pip install some-cli-tool
```

9) 자동화 워크플로 예시: 블로그 포스트 생성 → 커밋 → 푸시
- 목표: 명령 하나로 새 포스트 초안 생성, 커밋 메시지 자동화, git push

예시 스크립트 (bash):
```bash
#!/usr/bin/env bash
# create-post.sh
TITLE="$1"
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g')
DATE=$(date +%F)
DIR="_posts"
mkdir -p "$DIR"
FILE="$DIR/${DATE}-${SLUG}.md"
cat > "$FILE" <<EOF
---
title: "$TITLE"
date: $DATE
layout: post
---

초안 작성: 여기에 내용을 채우세요.
EOF

git add "$FILE"
git commit -m "Add blog post: $TITLE"
git push origin main
```
- 위 스크립트를 codex-cli나 GPT 기반 생성기로 본문 초안 자동 생성하도록 확장할 수 있습니다.

10) 자동 초안 생성 (codex-cli/GPT 연결)
- codex-cli가 프롬프트를 받아 텍스트 파일을 생성할 수 있다면, create-post.sh에서 codex-cli를 호출해 본문을 자동으로 채웁니다.

예시:
```bash
# codex-cli generate --prompt "블로그 포스트: Ubuntu에 OpenClaw 설치 및 Telegram 연동" > "$FILE"
```
- 또는 OpenClaw의 TTS/agent 기능을 사용해 더 복잡한 파이프라인 구성 가능

11) 서비스 및 안전 고려사항
- OpenClaw 게이트웨이는 외부 접근 포인트가 될 수 있으니 방화벽(UFW)을 설정하세요.
```bash
sudo apt install ufw
sudo ufw allow OpenSSH
sudo ufw allow 8443/tcp # 예시 포트
sudo ufw enable
```
- 자동 푸시 스크립트에 민감한 토큰(예: Git credential, Telegram token)을 직접 하드코딩하지 말고, 환경변수나 Vault를 사용하세요.

12) 자동화 확장 아이디어
- CI(예: GitHub Actions)와 연계해 검증/빌드 단계 추가
- PR 템플릿 자동 생성 및 리뷰 요청 자동화
- OpenClaw를 통해 원격 명령 실행/모니터링 및 알림 전송

마무리
이 튜토리얼은 실무 바로 적용 가능한 기본 흐름을 제공합니다. 필요하시면 제가 위 스크립트를 직접 파일로 생성하고, 로컬 리포지터리에 커밋·푸시까지 진행하겠습니다. 지금 바로 진행할까요? 혹은 포스트에 포함할 세부 명령어(예: Node 버전, 포트, 시스템 사용자 이름)를 알려주세요.