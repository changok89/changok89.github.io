---
title: Chrome NET::ERR_CERT_AUTHORITY_INVALID 해결방법
excerpt: 사설 인증서 또는 self-signed 인증서 환경에서 Chrome의 NET::ERR_CERT_AUTHORITY_INVALID 오류를
  우회하거나 올바르게 해결하는 방법
categories:
- Browser
tags:
- self-signed certificate
- Chrome
- TLS
- HTTPS
toc: true
toc_sticky: true
toc_label: self-signed certificate
date: 2023-02-02
last_modified_at: 2026-03-21
---

로컬 서버, 개발용 테스트 서버, 사내망 Tomcat 서버 같은 환경에 접속하다 보면 Chrome에서 아래 오류를 자주 보게 된다.

- `NET::ERR_CERT_AUTHORITY_INVALID`

이 오류는 대개 **브라우저가 현재 서버 인증서를 신뢰할 수 없다고 판단할 때** 발생한다. 가장 흔한 원인은 아래와 같다.

- self-signed certificate를 사용 중인 경우
- 사내 CA로 발급했지만 로컬 PC에 신뢰 루트가 설치되지 않은 경우
- 프록시 도구(예: Charles)가 HTTPS를 가로채는데 인증서 신뢰가 안 된 경우
- 인증서 체인이 중간에서 끊긴 경우

개발 환경에선 꽤 흔한 문제라서, 무작정 우회하기보다 **언제 임시 우회하고, 언제 인증서를 제대로 신뢰 처리해야 하는지** 구분하는 것이 중요하다.

## 가장 빠른 임시 우회: `thisisunsafe`

예전 Chrome에는 경고 페이지에서 "고급 > 계속 진행" 버튼이 더 잘 보였는데, 지금은 상황에 따라 직접 진행 버튼이 드러나지 않는 경우가 있다. 이때 개발 환경에서 빠르게 확인만 해야 한다면 Chrome 경고 페이지에서 아래 문자열을 입력해 우회할 수 있다.

- `thisisunsafe`

### 사용 방법

1. 인증서 오류 페이지를 연다.
2. 페이지 아무 곳이나 클릭해서 Chrome 창에 포커스를 준다.
3. 키보드로 `thisisunsafe` 를 입력한다.
4. 정상적으로 인식되면 경고 페이지를 우회해 대상 페이지로 이동한다.

![Image Alt chrome_cert_authority_invalid](/assets/img/contents/chrome_cert_authority_invalid/chrome_cert_authority_invalid.png)

### 주의할 점

이 방법은 **보안 경고를 임시로 무시하는 우회**일 뿐이다. 따라서 아래 상황에서만 제한적으로 쓰는 편이 낫다.

- 로컬 개발 서버
- 내 PC에서만 쓰는 테스트 환경
- 신뢰 가능한 사내 테스트 서버
- 인증서가 왜 깨졌는지 이미 알고 있는 상태

반대로 운영 환경이나 공개 서비스에서는 이 우회를 권장하지 않는다.

## Chrome 실행 옵션으로 무시하기

반복적으로 테스트해야 해서 매번 오류 페이지를 통과하는 것이 번거롭다면 Chrome을 인증서 무시 옵션과 함께 실행할 수 있다.

대표 옵션은 다음과 같다.

- `--ignore-certificate-errors`

다만 이 방법은 브라우저 전체 보안 수준을 낮추는 효과가 있으므로, **개발 전용 프로필 또는 별도 실행 환경**에서만 사용하는 것이 안전하다.

## Windows에서 실행하는 방법

1. `WIN + R` 로 실행 창을 연다.
2. 아래처럼 Chrome 실행 파일 경로와 옵션을 입력한다.

```bash
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --ignore-certificate-errors
```

3. 엔터를 누르면 인증서 오류를 무시하는 Chrome 인스턴스를 실행할 수 있다.

실행 후에는 현재 세션이 보안적으로 느슨해진 상태라는 점을 잊지 않는 것이 좋다.

![Image Alt ignore_certificate_errors](/assets/img/contents/chrome_cert_authority_invalid/ignore_certificate_errors.png)

## macOS에서 실행하는 방법

Spotlight에서 터미널을 열고 아래처럼 실행한다.

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ignore-certificate-errors --ignore-urlfetcher-cert-requests &> /dev/null
```

필요하면 별도 Chrome 프로필을 만들어 개발용으로만 쓰는 편이 더 안전하다.

## 우회보다 더 좋은 해결: 인증서를 신뢰 저장소에 설치

개발 환경을 자주 쓰는 사람이라면, 매번 `thisisunsafe`를 입력하는 것보다 **루트 인증서를 OS나 브라우저가 신뢰하도록 등록**하는 편이 낫다.

예를 들면 아래 같은 경우다.

- Charles Proxy HTTPS 디버깅
- 사내 프록시/개발용 인증서
- 로컬 TLS 개발 환경
- 자체 CA로 서명한 테스트 서버

이렇게 신뢰 루트를 제대로 설치하면 브라우저 경고가 사라지고, 모바일 디바이스 테스트까지 훨씬 자연스러워진다.

## 언제 우회해도 되고, 언제 안 되는가

### 우회해도 되는 경우
- 내가 직접 띄운 로컬 서버
- 폐쇄망 테스트 서버
- 인증서 원인을 내가 명확히 알고 있는 환경

### 우회하면 안 되는 경우
- 외부 서비스 운영 환경
- 누구나 접근하는 공개 서버
- 인증서 문제 원인을 모르는 상태
- 피싱/중간자 공격 가능성을 배제할 수 없는 환경

## 실무 팁

### 1. 개발용 브라우저를 분리하기
인증서 무시 옵션이 필요한 경우, 메인 Chrome 대신 개발 전용 프로필이나 Canary/별도 브라우저를 쓰는 것이 좋다.

### 2. 반복 테스트는 인증서 신뢰를 먼저 해결하기
프록시 디버깅이나 로컬 HTTPS 테스트를 자주 한다면 루트 인증서를 제대로 설치하는 편이 결국 시간을 아낀다.

### 3. 모바일까지 같이 테스트할 계획이면 CA 관리를 신경 쓰기
PC에서는 보이는데 모바일에서는 안 되는 경우가 많다. 기기별 신뢰 저장소와 사용자 인증서 정책까지 같이 확인해야 한다.

## 빠른 체크리스트

- 이 서버는 내가 신뢰할 수 있는 개발 서버인가?
- 지금 필요한 것은 임시 우회인가, 근본 해결인가?
- 브라우저 전체 보안을 낮추는 옵션을 오래 켜둘 필요가 없는가?
- 프록시/로컬 CA를 신뢰 저장소에 설치하는 게 더 나은가?

## 마무리

`NET::ERR_CERT_AUTHORITY_INVALID`는 개발 환경에서 정말 자주 만나는 오류다. 빠르게 확인만 필요하면 `thisisunsafe`가 편하지만, 반복적으로 쓰는 환경이라면 인증서를 올바르게 신뢰 처리하는 쪽이 장기적으로 훨씬 낫다.

한 줄로 정리하면:

- **급한 확인** → `thisisunsafe`
- **반복 테스트** → 인증서 신뢰 저장소 등록
- **운영 환경** → 절대 임시 우회에 의존하지 않기
