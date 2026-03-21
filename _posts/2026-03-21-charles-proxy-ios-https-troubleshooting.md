---
title: "Charles Proxy에서 iPhone HTTPS 트래픽이 안 보일 때 점검 순서"
excerpt: "Charles Proxy로 iPhone HTTPS 요청을 보려는데 안 잡히거나 인증서 오류가 날 때 확인할 설정들을 정리합니다."
categories:
  - Proxy
tags:
  - Charles
  - iPhone
  - HTTPS
  - Proxy
  - Debugging
toc: true
toc_sticky: true
toc_label: Charles iPhone HTTPS Troubleshooting
date: 2026-03-21
last_modified_at: 2026-03-21
---

# Charles Proxy에서 iPhone HTTPS 트래픽이 안 보일 때 점검 순서

Charles Proxy는 iPhone 앱이나 Safari의 HTTP/HTTPS 요청을 확인할 때 가장 자주 쓰는 도구 중 하나다. 그런데 막상 설정을 해보면 아래 같은 문제를 꽤 자주 만난다.

- HTTP는 보이는데 HTTPS는 안 보인다
- Safari에서 인증서 오류가 난다
- 앱 요청이 아예 Charles에 안 잡힌다
- 일부 API만 실패한다
- 프록시는 연결된 것 같은데 응답이 이상하다

이 글은 **iPhone에서 Charles Proxy HTTPS 디버깅이 잘 안 될 때 어떤 순서로 확인하면 되는지**를 정리한 체크리스트다.

## 먼저 결론: 가장 자주 빠지는 4가지

Charles가 iPhone HTTPS를 못 보는 경우는 보통 아래 4가지 중 하나다.

1. Mac에 Charles Root Certificate를 설치했지만 **항상 신뢰**로 바꾸지 않았다
2. iPhone에 Charles 인증서는 설치했지만 **루트 인증서 전체 신뢰 활성화**를 안 했다
3. iPhone Wi-Fi 프록시가 Charles가 실행 중인 Mac을 제대로 가리키지 않는다
4. 앱에서 **certificate pinning**을 사용하고 있다

즉, 대부분은 Charles 자체 문제보다 **인증서 신뢰**나 **프록시 경로** 설정 문제다.

## 점검 1: Mac에서 Charles SSL Proxying이 켜져 있는지

먼저 Charles에서 HTTPS 복호화 자체가 켜져 있는지 본다.

경로:
- **Proxy > SSL Proxy Settings**
- **Enable SSL Proxying** 체크 여부 확인

이게 꺼져 있으면 HTTPS 요청은 지나가더라도 내부 내용을 볼 수 없다.

## 점검 2: Mac에 Charles Root Certificate 설치 및 신뢰 설정

Charles 메뉴에서 아래를 실행한다.

- **Help > SSL Proxying > Install Charles Root Certificate**

설치 후 **키체인 접근(Keychain Access)** 에서 `Charles Proxy CA`를 찾아서 반드시 **Always Trust(항상 신뢰)** 로 바꿔야 한다.

이 단계를 빼먹으면 Mac 쪽 브라우저나 일부 도구에서 HTTPS가 계속 깨질 수 있다.

## 점검 3: iPhone 프록시가 Mac Charles를 제대로 바라보는지

iPhone에서 현재 연결된 Wi-Fi의 프록시 설정을 확인한다.

경로:
- **설정 > Wi‑Fi > 현재 연결된 네트워크 > HTTP 프록시**

설정 예:
- 구성: 수동
- 서버: Charles를 실행 중인 Mac의 IP
- 포트: 보통 `8888`

여기서 자주 생기는 실수는:
- Mac IP 주소를 잘못 넣음
- Charles 포트를 다른 값으로 쓰고 있음
- Mac과 iPhone이 서로 다른 네트워크에 있음

## 점검 4: iPhone에 Charles 인증서 설치

iPhone Safari에서 아래 주소를 열어 Charles 인증서를 설치한다.

- `https://charlesproxy.com/getssl`

프로파일 다운로드 후 아래 경로에서 설치한다.

- **설정 > 일반 > VPN 및 기기 관리**

여기까지만 하면 끝난 것 같지만, 실제로는 아직 하나 더 남아 있다.

## 점검 5: 루트 인증서 전체 신뢰 활성화

이 단계가 가장 자주 빠진다.

경로:
- **설정 > 일반 > 정보 > 인증서 신뢰 설정**

여기서 `Charles Proxy CA`에 대해 **루트 인증서 전체 신뢰 활성화**를 켜야 한다.

이걸 하지 않으면 인증서를 설치했어도 HTTPS 요청이 제대로 복호화되지 않는다.

## 점검 6: Charles에 기기 접근 허용 팝업이 떴는지

프록시를 타는 첫 순간 Mac Charles 쪽에서 이 기기의 연결을 허용할지 묻는 팝업이 뜰 수 있다.

이걸 거부했거나 지나쳤다면 요청이 안 보일 수 있다.

따라서:
- Charles를 미리 실행
- iPhone에서 Safari로 아무 HTTPS 페이지 열기
- Mac 쪽 허용 팝업 확인

이 흐름으로 한 번 테스트해보는 게 좋다.

## 점검 7: Safari는 되는데 특정 앱만 안 되는 경우

이 경우는 **certificate pinning** 가능성이 높다.

certificate pinning이 걸려 있으면 앱이 서버 인증서를 자체 검증해서 중간에 Charles 인증서를 끼우는 방식이 통하지 않는다.

이럴 때는:
- Safari 요청은 보임
- 일반 웹 요청도 보임
- 특정 앱 API만 SSL 오류 또는 연결 실패

형태로 나타난다.

즉, Charles 설정이 틀린 게 아니라 앱 보안 정책 때문에 안 보이는 걸 수 있다. 이 경우 Charles 설정을 계속 바꾸기보다 pinning 여부를 먼저 의심하는 편이 시간을 훨씬 덜 잡아먹는다. 개발 빌드나 디버그 빌드에서만 우회 가능한 경우도 많다.

## 점검 8: 회사 Wi-Fi / VPN / 보안 앱 영향

사내망이나 VPN 환경에서는 아래 요소 때문에 Charles 연결이 꼬일 수 있다.

- 프록시 우회 정책
- 회사 보안 인증서
- VPN이 트래픽 경로를 바꿔버림
- 네트워크 격리

이럴 때는 개인 핫스팟이나 단순한 동일 Wi-Fi 환경에서 먼저 테스트해보는 게 원인 분리에 좋다.

## 내가 추천하는 실제 점검 순서

처음부터 복잡하게 보지 말고 아래 순서대로 보면 된다.

1. Mac에서 Charles 실행
2. SSL Proxying 활성화 확인
3. Mac Keychain에서 Charles 인증서 항상 신뢰 확인
4. iPhone Wi-Fi 프록시 수동 설정
5. iPhone Safari에서 getssl 접속 후 인증서 설치
6. iPhone 인증서 신뢰 설정에서 루트 인증서 전체 신뢰 활성화
7. Safari 요청으로 먼저 테스트
8. 앱 요청 테스트
9. 앱만 안 되면 pinning 의심

## 확인 방법

설정이 제대로 되면 보통 아래처럼 보인다.

- Safari에서 여는 HTTPS 페이지 요청이 Charles에 나타남
- 요청/응답 헤더와 body를 볼 수 있음
- SSL handshake 관련 오류가 줄어듦

반대로 여전히 안 되면:
- 프록시 경로 문제
- 인증서 신뢰 문제
- 앱 pinning 문제
중 하나로 좁힐 수 있다.

## 마무리

Charles Proxy에서 iPhone HTTPS가 안 보일 때는 대부분 설정 하나가 빠진 경우다. 특히 **iPhone 인증서 설치만 하고 “루트 인증서 전체 신뢰”를 안 켠 상태**가 정말 흔하다.

빠르게 정리하면:

- Mac 인증서 신뢰
- iPhone 인증서 설치
- iPhone 루트 인증서 신뢰
- 프록시 IP/포트 확인
- 앱만 안 되면 pinning 의심

이 순서로 보면 대부분의 문제를 꽤 빨리 해결할 수 있다.
�하면:

- Mac 인증서 신뢰
- iPhone 인증서 설치
- iPhone 루트 인증서 신뢰
- 프록시 IP/포트 확인
- 앱만 안 되면 pinning 의심

이 순서로 보면 대부분의 문제를 꽤 빨리 해결할 수 있다.
HTTPS가 안 보일 때는 대부분 설정 하나가 빠진 경우다. 특히 **iPhone 인증서 설치만 하고 “루트 인증서 전체 신뢰”를 안 켠 상태**가 정말 흔하다.

빠르게 정리하면:

- Mac 인증서 신뢰
- iPhone 인증서 설치
- iPhone 루트 인증서 신뢰
- 프록시 IP/포트 확인
- 앱만 안 되면 pinning 의심

이 순서로 보면 대부분의 문제를 꽤 빨리 해결할 수 있다.
