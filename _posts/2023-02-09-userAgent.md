---
title:  "WKWebView userAgent"
excerpt: "WKWebView에서 User-Agent를 추가, 변경, 확인하는 방법과 실제로 어떤 상황에서 쓰는지 정리"

categories:
  - iOS
tags:
  - [WKWebView, userAgent, iOS, WebView]

toc: true
toc_sticky : true
toc_label : WKWebView userAgent

date: 2023-02-09
last_modified_at: 2026-03-21
---

# User-Agent란?

User-Agent는 HTTP 요청 시 클라이언트 환경 정보를 담아 보내는 헤더다. 대략 아래 같은 정보가 들어간다.

- 브라우저 계열 정보
- 운영체제 정보
- 렌더링 엔진 정보
- 모바일/데스크톱 구분 정보

브라우저 콘솔이나 WebView 환경에서 `navigator.userAgent`를 찍어보면 아래와 비슷한 문자열을 볼 수 있다.

> navigator.userAgent  
> `Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148`

실무에서는 이 값을 이용해 앱과 모바일 브라우저를 구분하거나, 서버 로그에서 특정 앱 요청만 식별하거나, 웹 페이지 쪽 분기 처리를 하기도 한다.

## WKWebView에서 User-Agent를 만지는 이유

대표적인 목적은 아래와 같다.

- 앱 내 WebView 요청임을 식별
- 하이브리드 앱과 모바일 브라우저를 구분
- 서버에서 앱 전용 동작 분기
- 로그 분석 시 앱 버전/채널 식별

## 1. 기존 User-Agent에 문자열 추가하기

가장 많이 쓰는 방법이다. 기본 UA는 유지하고, 뒤에 앱 식별 문자열만 붙인다.

```swift
let configuration = WKWebViewConfiguration()
configuration.applicationNameForUserAgent = "changok89"
let webView = WKWebView(frame: .zero, configuration: configuration)
```

사파리 인스펙터로 확인
![Image Alt userAgent1](/assets/img/contents/userAgent/userAgent1.png)

### 이 방식의 장점

- 기본 Safari/WKWebView 호환성을 크게 해치지 않는다.
- 서버에서 특정 토큰만 보고 앱 요청을 구분하기 쉽다.
- 외부 웹사이트를 로드하는 경우에도 부작용이 적다.

### 추천 사용 예

- `myapp`
- `myapp/1.0.0`
- `changok89-app production`

즉 기본 UA를 유지하면서 "이 요청은 우리 앱 WebView에서 왔다"는 신호만 추가하는 게 핵심이다.

## 2. User-Agent를 완전히 바꾸기

기존 문자열을 버리고 커스텀 UA로 교체할 수도 있다.

```swift
let configuration = WKWebViewConfiguration()
let webView = WKWebView(frame: .zero, configuration: configuration)
webView.customUserAgent = "changok89"
```

사파리 인스펙터로 확인  
![Image Alt userAgent2](/assets/img/contents/userAgent/userAgent2.png)

### 언제 쓰나

- 사내 전용 웹 시스템이 특정 UA만 기대할 때
- 완전히 통제된 내부 환경에서만 사용할 때
- 외부 호환성보다 식별이 더 중요할 때

### 주의할 점

이 방식은 위험하다. 일부 웹 페이지나 JavaScript 라이브러리는 브라우저 기능 판단에 UA를 참고하기 때문에, 너무 짧거나 비표준적인 문자열로 교체하면 예상치 못한 문제가 생길 수 있다.

예:
- 모바일 브라우저로 인식되지 않음
- 특정 CSS/JS 분기 실패
- 브라우저 호환성 판별 로직 오동작

그래서 외부 웹사이트를 보여주는 일반적인 앱이라면, 완전 교체보다 **추가 방식**이 더 안전하다.

## 3. 현재 User-Agent 값 가져오기

현재 설정된 값을 코드에서 확인하고 싶을 때도 있다.

```swift
let configuration = WKWebViewConfiguration()
configuration.applicationNameForUserAgent = "changok89"
let webView = WKWebView(frame: .zero, configuration: configuration)

if let userAgent = webView.value(forKey: "userAgent") {
  print("\(userAgent)")
}
```

로그확인
![Image Alt userAgent3](/assets/img/contents/userAgent/userAgent3.png)

실무에서는 단순 출력보다는 서버 요청 로그와 같이 확인하는 편이 더 정확하다.

## 어떤 방식을 고르는 게 좋나

### 기본 추천
대부분의 경우는 **기존 UA에 값 추가**가 가장 좋다.

이유:
- 호환성이 좋음
- 식별이 쉬움
- 외부 웹 서비스와 충돌 가능성이 낮음

### 예외적으로 전체 변경
앱 내부에서만 쓰는 웹, 완전히 제어 가능한 서버, UA 분기가 명확한 내부 도구라면 커스텀 UA 전체 교체도 가능하다.

## 확인 방법

설정 후에는 아래 방식으로 실제 반영 여부를 체크하면 된다.

- Safari Web Inspector
- 서버 로그 확인
- 웹 페이지에서 `navigator.userAgent` 출력
- 프록시 도구(Charles 등)로 요청 헤더 확인

## 실무 팁

### 앱 버전까지 같이 넣으면 편하다
문제 재현이나 로그 분석이 필요하면 앱 이름만 넣는 것보다 버전도 같이 넣는 편이 좋다.

예:

```swift
configuration.applicationNameForUserAgent = "changok89/1.2.3"
```

### 서버 로직은 contains 기반으로 단순하게
UA는 브라우저 버전에 따라 앞부분이 바뀔 수 있다. 따라서 서버에서는 완전 일치보다 특정 토큰 포함 여부로 판단하는 편이 낫다.

### 브라우저 차단 정책을 만들 때는 신중하게
UA는 식별 힌트로는 유용하지만 보안 수단으로 과신하면 안 된다.

## 마무리

WKWebView에서 User-Agent를 다루는 목적은 보통 "우리 앱에서 온 요청을 식별하고 싶다"에 가깝다. 그래서 대부분의 경우에는 기존 UA를 유지한 채 토큰만 추가하는 방식이 가장 실용적이다.

정리하면:

- 가장 안전한 방법 → `applicationNameForUserAgent` 로 추가
- 완전 변경이 필요할 때 → `customUserAgent`
- 반영 확인 → Inspector / 로그 / `navigator.userAgent`

실제 서비스에서 안정성을 원한다면 **추가 방식 우선, 전체 변경은 최소화**가 좋다.
