---
title: Charles Web Proxy 사용법
excerpt: Charles Proxy 설치부터 macOS와 iPhone에서 HTTPS 트래픽을 확인하기 위한 기본 설정 정리
categories:
- Proxy
tags:
- Charles
- Proxy
- HTTPS
- Debugging
toc: true
toc_sticky: true
toc_label: Charles Proxy
date: 2023-01-29
last_modified_at: 2026-03-21
---

Charles는 HTTP/HTTPS 트래픽을 확인하고 디버깅할 때 많이 쓰는 프록시 도구다. 브라우저나 모바일 앱에서 발생하는 요청과 응답을 중간에서 캡처해볼 수 있어서, 네트워크 디버깅이 필요할 때 거의 기본 도구처럼 쓰인다.

특히 아래 같은 상황에서 유용하다.

- 모바일 앱 API 요청 확인
- 서버 응답값 디버깅
- HTTPS 요청/응답 헤더 점검
- 이미지, JSON, 인증 토큰 등 실제 트래픽 확인
- 특정 API의 요청 순서나 실패 지점 분석

## Charles가 좋은 이유

- macOS, Windows, Linux 지원
- UI가 비교적 직관적
- HTTPS Proxying 설정이 쉬운 편
- 브라우저뿐 아니라 모바일 앱 트래픽도 볼 수 있음

트라이얼 버전은 30일 사용 가능하고, 세션당 시간 제한이 있어도 간단한 디버깅에는 충분하다.

## Charles 설치

- [다운로드](https://www.charlesproxy.com/download/latest-release/){:target="_blank"}
- 운영체제에 맞는 설치 파일을 내려받아 설치한다.

## macOS에서 기본 설정

### 1. Charles 실행
Charles를 실행하면 기본적으로 Recording 상태로 시작한다. 이 상태에서 프록시를 거치는 HTTP 요청이 발생하면 좌측 트리 영역에 바로 표시된다.

![Image Alt charles1](/assets/img/contents/charles/charles1.png)

### 2. Proxy 포트 확인
메뉴에서 **Proxy > Proxy Settings** 로 들어가 포트를 확인한다. 기본값은 보통 `8888`이다.

![Image Alt charles2](/assets/img/contents/charles/charles3.png)

이 값은 iPhone 프록시 설정 시 그대로 사용하게 된다.

### 3. SSL Proxying 켜기
HTTPS 트래픽까지 제대로 보려면 **Proxy > SSL Proxy Settings** 에서 `Enable SSL Proxying` 이 체크되어 있는지 확인한다.

![Image Alt charles4](/assets/img/contents/charles/charles4.png)

### 4. Mac에 Charles Root Certificate 설치
메뉴에서 **Help > SSL Proxying > Install Charles Root Certificate** 를 선택해 Charles 인증서를 설치한다.

![Image Alt charles4](/assets/img/contents/charles/charles6.png)

### 5. 키체인에서 항상 신뢰로 변경
macOS 키체인 접근 앱에서 `Charles Proxy CA` 인증서를 찾아 **항상 신뢰** 로 바꾼다.

![Image Alt charles4](/assets/img/contents/charles/charles5.png)

이 단계가 빠지면 HTTPS 요청이 브라우저나 앱에서 정상적으로 복호화되지 않을 수 있다.

## iPhone 설정

이제 iPhone이 Mac의 Charles 프록시를 바라보게 만들어야 한다.

### 1. iPhone Wi-Fi 프록시를 수동 설정

- **설정 > Wi‑Fi > 현재 연결된 네트워크 > HTTP 프록시**
- `수동` 으로 변경
- 서버: Charles가 실행 중인 Mac의 IP 주소
- 포트: Charles에서 확인한 `8888`

이렇게 하면 iPhone의 HTTP/HTTPS 트래픽이 Charles를 통해 전달된다.

### 2. iPhone에 Charles 인증서 설치
Safari에서 아래 주소로 접속한다.

- `https://charlesproxy.com/getssl`

![Image Alt charles9](/assets/img/contents/charles/charles9.png)

인증서 다운로드 후 아래 경로에서 설치한다.

- **설정 > 일반 > VPN 및 기기 관리**
- 다운로드한 프로파일 설치

![Image Alt charles9](/assets/img/contents/charles/charles7.png)

### 3. 루트 인증서 신뢰 활성화
설치만으로 끝나지 않고, iPhone에서 루트 인증서를 신뢰하도록 켜야 한다.

- **설정 > 일반 > 정보 > 인증서 신뢰 설정**
- `Charles Proxy CA` 전체 신뢰 활성화

![Image Alt charles9](/assets/img/contents/charles/charles8.png)

## 실제 모바일 프록시 연결

설정이 끝나면 Charles를 켜 둔 상태에서 iPhone에서 웹페이지를 열거나 앱을 실행해 네트워크 요청을 발생시킨다.

처음 연결될 때 Mac Charles 쪽에서 해당 기기를 허용할지 묻는 팝업이 뜰 수 있다. 허용하면 그 시점부터 iPhone 트래픽이 Charles에 표시된다.

## 잘 안 될 때 체크리스트

### HTTPS 내용이 안 보인다
- Mac에 Charles 인증서가 설치되어 있는지 확인
- Mac 키체인에서 항상 신뢰 상태인지 확인
- iPhone에 인증서를 설치했는지 확인
- iPhone의 루트 인증서 전체 신뢰를 켰는지 확인
- SSL Proxying이 활성화되어 있는지 확인

### iPhone이 프록시를 못 탄다
- iPhone과 Mac이 같은 네트워크에 있는지 확인
- Mac IP 주소가 바뀌지 않았는지 확인
- Charles 포트가 `8888`인지 확인
- macOS 방화벽 또는 보안 정책이 막지 않는지 확인

### 앱에서만 안 된다
- 일부 앱은 certificate pinning 때문에 Charles로 복호화가 안 될 수 있다.
- 이 경우 브라우저/Safari는 되는데 특정 앱만 실패하는 현상이 나타난다.

## Charles가 특히 잘 맞는 상황

- 앱 API 응답 구조 확인
- 로그인/토큰 흐름 디버깅
- 헤더와 쿠키 값 확인
- HTTPS 요청이 실제로 어떤 값을 보내는지 검증
- 이미지/정적 리소스 캐싱 문제 분석

## 마무리

Charles Proxy는 모바일 네트워크 디버깅에서 가장 먼저 떠올릴 만한 도구 중 하나다. 핵심은 크게 네 단계다.

1. Mac에 Charles 설치
2. SSL Proxying 활성화
3. Mac/iPhone 양쪽에 인증서 신뢰 설정
4. iPhone 프록시를 Mac Charles로 지정

이 흐름만 잡아두면 iPhone에서 발생하는 HTTP/HTTPS 트래픽을 꽤 안정적으로 분석할 수 있다.
