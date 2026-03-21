---
title:  "Charles Web Proxy 사용법"
excerpt: "Charles Proxy 설치부터 macOS와 iPhone에서 HTTPS 트래픽을 확인하기 위한 기본 설정까지 정리"

categories:
  - Proxy
tags:
  - [Charles, Proxy, HTTPS, iOS, Debugging]

toc: true
toc_sticky : true
toc_label : Charles Proxy

date: 2023-01-29
last_modified_at: 2026-03-21
---

# Charles Web Proxy 란?

Charles는 HTTP/HTTPS 트래픽을 가로채고 확인할 수 있는 대표적인 디버깅 프록시 도구다. 모바일 앱, 웹 브라우저, WebView, API 호출 흐름을 분석할 때 자주 사용한다.

예를 들어 아래 같은 상황에서 특히 유용하다.

- 앱에서 어떤 API를 호출하는지 확인
- 요청/응답 헤더와 바디 점검
- 인증서 문제 분석
- 특정 응답을 재현하거나 변조해서 테스트
- 모바일 기기 트래픽을 Mac에서 집중적으로 확인

## Charles를 쓰는 이유

브라우저 개발자도구만으로는 앱 내부 네트워크 요청까지 보기 어렵다. 특히 iPhone이나 Android 앱의 HTTPS 요청을 분석하려면 별도 프록시 도구가 필요하다. Charles는 그 과정이 비교적 직관적이라 실무에서 많이 쓰인다.

## 1. Charles 설치

Charles는 Windows, macOS, Linux를 지원한다.

- 공식 사이트에서 설치 파일 다운로드
- 라이선스가 없으면 체험판으로 사용 가능
- 체험판은 일정 시간 제한이 있다

[다운로드](https://www.charlesproxy.com/download/latest-release/){:target="_blank"}

## 2. macOS에서 기본 설정

### Charles 실행

Charles를 실행하면 기본적으로 Recording 상태라서, HTTP/HTTPS 요청이 발생하면 왼쪽 패널에 바로 표시된다.

![Image Alt charles1](/assets/img/contents/charles/charles1.png)

### Proxy 포트 확인

상단 메뉴 **Proxy > Proxy Settings** 에서 포트를 확인한다. 기본 포트는 보통 `8888`이다.

![Image Alt charles2](/assets/img/contents/charles/charles3.png)

### SSL Proxying 활성화

HTTPS 요청 내용을 보려면 SSL Proxying이 필요하다.

- **Proxy > SSL Proxy Settings**
- **Enable SSL Proxying** 체크 여부 확인

![Image Alt charles4](/assets/img/contents/charles/charles4.png)

### macOS에 Charles 인증서 설치

- **Help > SSL Proxying > Install Charles Root Certificate** 선택
- 키체인 접근에서 설치된 **Charles Proxy CA** 인증서를 연다.
- 신뢰 설정을 **항상 신뢰**로 변경한다.

![Image Alt charles4](/assets/img/contents/charles/charles6.png)
![Image Alt charles4](/assets/img/contents/charles/charles5.png)

이 단계까지 해야 Mac 자체 브라우저 트래픽과 HTTPS 복호화가 훨씬 자연스럽다.

## 3. iPhone에서 Charles 사용하기

이제 iPhone 트래픽을 Mac의 Charles로 보내야 한다.

### iPhone 프록시 설정

1. iPhone에서 **설정 > Wi‑Fi** 로 이동한다.
2. 현재 연결 중인 Wi-Fi의 상세 설정을 연다.
3. 아래쪽 **HTTP 프록시**를 **수동**으로 바꾼다.
4. 서버 주소에 Charles가 실행 중인 Mac의 IP를 입력한다.
5. 포트에는 Charles에서 확인한 포트(보통 `8888`)를 입력한다.

즉 iPhone의 모든 네트워크 요청을 Mac의 Charles를 경유하게 만드는 것이다.

### iPhone에 Charles 인증서 설치

HTTPS 내용을 보려면 iPhone도 Charles 루트 인증서를 신뢰해야 한다.

1. iPhone Safari에서 `https://charlesproxy.com/getssl` 접속
2. 프로파일 다운로드 허용
3. **설정 > 일반 > VPN 및 기기 관리** 로 이동
4. 다운로드된 인증서를 설치
5. **설정 > 일반 > 정보 > 인증서 신뢰 설정** 으로 이동
6. **Charles Root Certificate** 에 대해 전체 신뢰를 활성화

![Image Alt charles9](/assets/img/contents/charles/charles9.png)
![Image Alt charles9](/assets/img/contents/charles/charles7.png)
![Image Alt charles9](/assets/img/contents/charles/charles8.png)

이 과정을 빠뜨리면 HTTPS 요청은 보이더라도 내용이 복호화되지 않거나 인증서 오류가 발생한다.

## 4. 모바일 기기 연결 확인

설정이 끝난 뒤 iPhone에서 웹페이지를 열거나 앱에서 네트워크 요청을 발생시키면 Charles에 연결 허용 팝업이 뜰 수 있다. 허용하면 이후부터 Mac에서 iPhone 트래픽을 확인할 수 있다.

즉 흐름은 아래와 같다.

1. Mac에서 Charles 실행
2. iPhone Wi-Fi 프록시를 Mac으로 설정
3. Charles 인증서 설치 및 신뢰
4. iPhone에서 네트워크 요청 발생
5. Mac의 Charles에서 요청 확인

## Charles에서 자주 보는 기능

- Structure / Sequence 보기 전환
- 요청/응답 헤더 확인
- Body / JSON 응답 확인
- SSL Proxying 대상 추가
- Throttle / Rewrite / Breakpoint 기능

처음엔 단순 모니터링만 써도 충분하지만, 익숙해지면 응답 변조나 속도 제한까지 가능하다.

## 잘 안 될 때 체크리스트

### iPhone 트래픽이 안 보인다
- iPhone 프록시가 수동 설정으로 바뀌었는지
- Mac과 iPhone이 같은 네트워크에 있는지
- Mac 방화벽이나 보안 앱이 막는지
- Charles 연결 허용 팝업을 승인했는지

### HTTPS 내용이 안 보인다
- Mac에 Charles 루트 인증서를 신뢰했는지
- iPhone에도 인증서를 설치하고 전체 신뢰를 켰는지
- SSL Proxying이 활성화됐는지

### 특정 앱만 안 된다
- 앱이 certificate pinning을 쓰는 경우 Charles로 복호화가 막힐 수 있다.
- 이 경우 단순 프록시 설정만으로는 충분하지 않다.

## 언제 가장 유용한가

- 모바일 앱 API 디버깅
- WebView 요청 분석
- 인증서 에러 원인 파악
- 서버 응답이 이상한지 앱 처리 로직이 이상한지 구분
- 개발/QA 환경에서 요청 재현

## 마무리

Charles는 모바일 네트워크 디버깅에서 가장 먼저 손이 가는 도구 중 하나다. 특히 iPhone 트래픽을 Mac에서 집중적으로 보고 싶을 때 설정만 제대로 해두면 매우 강력하다.

핵심만 정리하면:

1. Mac에 Charles 설치
2. SSL Proxying 활성화
3. Charles Root Certificate 신뢰
4. iPhone 프록시를 Charles로 지정
5. iPhone에도 인증서 설치 및 신뢰

이 흐름만 익히면 모바일 앱의 HTTP/HTTPS 통신을 훨씬 수월하게 분석할 수 있다.
