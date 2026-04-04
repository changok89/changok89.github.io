---
title: Charles Web Proxy 사용법
excerpt: 모바일 앱 디버깅에서 Charles는 요청과 응답을 눈으로 확인할 수 있게 해주는 가장 실전적인 도구 중 하나다. 설치부터 iPhone
  연결, HTTPS 복호화, 자주 막히는 지점까지 정리한다.
categories:
- Proxy
tags:
- Charles
- Proxy
- iOS
- Debugging
- Mobile
toc: true
toc_sticky: true
toc_label: Charles Web Proxy 사용법
date: 2026-03-18
last_modified_at: 2026-03-18
---

모바일 앱 개발을 하다 보면 “분명 API는 호출했는데 왜 값이 다르지?”, “앱에서는 401이 나는데 Postman에서는 왜 정상이지?” 같은 상황을 자주 만난다. 이럴 때 로그만으로는 부족하고, 실제 요청과 응답을 눈으로 봐야 해결이 빨라진다. Charles는 바로 그럴 때 가장 손이 많이 가는 도구 중 하나다.

특히 iOS 앱이나 모바일 웹뷰를 디버깅할 때는 서버 로그, 앱 로그, 화면 증상만으로는 원인이 안 잡히는 경우가 많다. **헤더가 빠졌는지**, **리다이렉트가 있었는지**, **SSL 프록시가 제대로 풀렸는지**를 확인하려면 프록시 도구가 필요하다.

## Charles를 쓰는 이유

Charles는 HTTP/HTTPS 트래픽을 중간에서 받아서 보여주는 디버깅 프록시다. 장점은 단순하다.

- 앱이 실제로 보낸 요청을 볼 수 있음
- 응답 헤더, 바디, 상태 코드 확인 가능
- HTTPS도 인증서 설정 후 복호화 가능
- 요청 재실행, 수정, 매핑 같은 고급 기능도 제공

개인적으로는 단순 네트워크 확인만 할 때도 좋지만, **모바일 기기와 백엔드 사이에서 무엇이 달라지는지** 볼 수 있다는 점 때문에 가치가 크다고 본다.

## 기본 설치와 Mac 설정

설치 자체는 어렵지 않다. macOS 기준으로 Charles를 설치하고 실행한 뒤, 기본 포트가 보통 `8888`인지 확인하면 된다. 그리고 HTTPS를 보려면 SSL Proxying을 켜고 루트 인증서를 신뢰해야 한다.

핵심 순서는 아래 정도로 정리된다.

1. Charles 설치 및 실행
2. `Proxy > Proxy Settings`에서 포트 확인
3. `Proxy > SSL Proxying Settings`에서 SSL Proxying 활성화
4. `Help > SSL Proxying > Install Charles Root Certificate`
5. 키체인 접근에서 Charles 인증서를 **항상 신뢰**로 변경

여기까지는 Mac 자체 브라우저 디버깅 기준이고, iPhone까지 붙이려면 기기 쪽 설정이 추가된다.

## iPhone을 Charles에 연결하는 방법

같은 네트워크에 Mac과 iPhone이 있어야 하고, iPhone Wi‑Fi의 HTTP 프록시를 수동으로 잡아주면 된다.

1. iPhone에서 현재 연결된 Wi‑Fi 상세 설정 진입
2. **HTTP 프록시 > 수동** 선택
3. 서버에 Mac의 IP 주소 입력
4. 포트는 Charles에서 확인한 `8888` 입력
5. Safari에서 `https://charlesproxy.com/getssl` 접속
6. 프로파일 설치 후 **루트 인증서 전체 신뢰** 활성화

여기까지 끝나면 Charles에서 연결 허용 팝업이 뜨고, 승인 후부터 iPhone 트래픽이 보인다.

## 실전에서 꼭 확인하는 화면

Charles를 처음 쓰면 좌측 트리만 멍하니 보게 되는데, 실무에서는 보통 아래 탭 위주로 본다.

- **Structure**: 도메인 단위로 요청 흐름 확인
- **Sequence**: 시간 순서로 어떤 요청이 먼저 나갔는지 확인
- **Headers**: 인증/캐시/쿠키 헤더 확인
- **Body/JSON/Text**: 실제 응답 내용 확인
- **SSL Proxying**: HTTPS가 제대로 풀리고 있는지 확인

개인적으로 앱 인증 이슈를 볼 때는 `Authorization`, `Cookie`, `User-Agent`, 커스텀 헤더를 가장 먼저 체크한다. 생각보다 서버 문제보다 **클라이언트가 다른 헤더를 보내는 문제**가 많다.

## 자주 겪는 문제와 해결

### HTTPS 요청이 안 보이거나 깨져 보인다

SSL Proxying이 켜져 있지 않거나, Charles 루트 인증서를 Mac/iPhone에서 신뢰하지 않은 경우다. 특히 iPhone에서는 프로파일 설치만 해 놓고 **인증서 신뢰 활성화**를 빼먹는 경우가 많다.

### 앱은 인터넷이 되는데 Charles에는 안 잡힌다

프록시 대상 Wi‑Fi가 아닌 셀룰러로 빠지거나, 앱이 자체 네트워크 정책으로 프록시를 우회할 수 있다. 일부 보안 민감 앱은 certificate pinning 때문에 프록시 복호화가 안 되기도 한다.

### 회사망이나 VPN에서 연결이 이상하다

사내 VPN, 보안 제품, DNS 정책이 프록시 흐름과 충돌할 수 있다. 이런 경우는 Charles 자체 문제로 보기보다 네트워크 레이어를 의심해야 한다.

## Charles를 언제 쓰고 언제 안 쓰는가

나는 아래처럼 구분하는 편이다.

### Charles가 좋은 경우

- 모바일 앱 API 디버깅
- 로그인/토큰/리다이렉트 확인
- 서버와 클라이언트 요청 차이 비교
- QA 환경 응답 재현

### Charles보다 다른 도구가 나은 경우

- 웹 프론트 DOM/CSS/JS 디버깅: `Chrome Inspector`
- 터미널 기반 간단한 재현: `curl`, `httpie`
- 서버 로그가 충분하고 트래픽 변형이 필요 없을 때: APM/로그 도구

## 실무 팁

- 프록시를 끄지 않고 회의실 Wi‑Fi로 이동하면 엉뚱한 문제처럼 보일 수 있다.
- 인증서 설정 후 테스트가 끝나면 정리해 두는 것이 좋다.
- 팀 공용 문서에는 Mac IP 확인 방법, 사내망 주의사항, 인증서 신뢰 경로를 같이 적어두는 편이 좋다.

## 빠른 체크리스트

- [ ] Charles 포트가 확인되었다
- [ ] SSL Proxying이 활성화되었다
- [ ] Mac 키체인에서 Charles 인증서를 신뢰했다
- [ ] iPhone Wi‑Fi 프록시를 수동 설정했다
- [ ] iPhone에서 루트 인증서 전체 신뢰를 켰다
- [ ] 테스트 후 프록시를 원복했다

## 마무리

Charles는 설치 자체보다 **정확한 연결 상태를 만들고 HTTPS를 제대로 푸는 것**이 핵심이다. 한 번만 감을 잡으면 모바일 앱 네트워크 디버깅 속도가 꽤 빨라진다. 특히 iOS 디버깅 문서에는 `iMazing`, `Chrome Inspector`, `Developer Mode`와 함께 묶어서 관리하면 팀 온보딩 품질이 좋아진다.
