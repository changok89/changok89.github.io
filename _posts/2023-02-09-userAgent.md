---
title:  "WKWebView userAgent"
excerpt: "WKWebView에서 User-Agent 값을 추가, 변경, 확인하는 방법과 실무상 주의점을 정리"

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

# WKWebView UserAgent 다루기

웹 요청에는 보통 브라우저나 디바이스 정보를 담은 `User-Agent` 헤더가 포함된다. 하이브리드 앱이나 앱 내 WebView를 운영하다 보면 이 값을 수정해야 할 일이 생각보다 자주 생긴다.

예를 들면 아래와 같은 경우다.

- 앱 내 WebView 요청과 일반 모바일 Safari 요청을 구분하고 싶을 때
- 서버 로그에서 앱 버전이나 앱 전용 트래픽을 식별하고 싶을 때
- 특정 스크립트나 페이지에서 앱 전용 분기를 하고 싶을 때
- 외부 SDK 또는 내부 시스템이 특정 UA 문자열을 요구할 때

이 글에서는 `WKWebView`에서 User-Agent 값을 **추가**, **변경**, **확인**하는 방법을 각각 정리한다.

## User-Agent란?

User-Agent는 HTTP 요청 헤더 중 하나로, 현재 요청을 보내는 클라이언트 정보 일부를 담고 있다. 보통 아래 성격의 정보가 섞여 있다.

- 브라우저 엔진 정보
- OS 정보
- 기기 타입 정보
- Safari/Chrome 호환 문자열

Safari나 WebView 콘솔에서 `navigator.userAgent`를 실행하면 아래처럼 보인다.

```javascript
navigator.userAgent
// 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
```

## 1. WKWebView User-Agent에 값 추가하기

가장 안전한 방식은 기존 UA는 유지한 채, 앱 식별용 문자열을 뒤에 덧붙이는 것이다. 하이브리드 앱과 모바일 브라우저를 구분할 때 많이 쓴다.

```swift
let configuration = WKWebViewConfiguration()
configuration.applicationNameForUserAgent = "changok89"
let webView = WKWebView(frame: .zero, configuration: configuration)
```

`applicationNameForUserAgent`는 기존 UA를 완전히 버리는 것이 아니라, 뒤쪽에 앱 식별 문자열을 추가하는 용도로 이해하면 된다.

![Image Alt userAgent1](/assets/img/contents/userAgent/userAgent1.png)

### 이 방식이 좋은 이유

- 기본 Safari/WKWebView 구조를 최대한 유지한다.
- 외부 웹사이트 호환성이 상대적으로 높다.
- 서버에서 앱 요청을 식별하기 쉽다.

예를 들어 로그에서 `changok89` 포함 여부만으로 앱 내 요청을 구분할 수 있다.

## 2. WKWebView User-Agent 값을 완전히 변경하기

기존 UA를 제거하고 완전히 새로운 문자열로 바꾸고 싶다면 `customUserAgent`를 사용할 수 있다.

```swift
let configuration = WKWebViewConfiguration()
let webView = WKWebView(frame: .zero, configuration: configuration)
webView.customUserAgent = "changok89"
```

![Image Alt userAgent2](/assets/img/contents/userAgent/userAgent2.png)

### 언제 이 방식을 쓰나

- 내부 시스템이 고정된 UA 값만 요구할 때
- 사내 전용 웹 페이지에서만 사용할 때
- 브라우저 호환성보다 명확한 식별이 더 중요할 때

### 주의할 점

이 방식은 외부 웹과의 호환성에 영향을 줄 수 있다. 일부 라이브러리나 웹사이트는 User-Agent를 보고 동작을 분기하기 때문에, 너무 단순한 문자열로 바꾸면 예상치 못한 문제가 생길 수 있다.

예를 들어:
- 모바일 브라우저로 인식하지 못함
- 특정 기능을 차단함
- 스크립트가 브라우저 호환 로직을 잘못 선택함

그래서 일반적으로는 **완전 교체보다 추가 방식이 더 안전**하다.

## 3. 현재 User-Agent 값 가져오기

디버깅이나 확인용으로 현재 UA를 가져와 로그로 보고 싶을 수도 있다.

```swift
let configuration = WKWebViewConfiguration()
configuration.applicationNameForUserAgent = "changok89"
let webView = WKWebView(frame: .zero, configuration: configuration)

if let userAgent = webView.value(forKey: "userAgent") {
  print("\(userAgent)")
}
```

![Image Alt userAgent3](/assets/img/contents/userAgent/userAgent3.png)

실제 프로젝트에서는 JavaScript `navigator.userAgent`를 실행해서 웹 레이어에서 보는 UA와 비교해보는 것도 도움이 된다.

## 어떤 방법을 선택할까

내 기준으로는 아래처럼 정리한다.

### 추가 방식 추천 상황
- 외부 웹사이트를 로드함
- 일반 브라우저와의 호환성이 중요함
- 앱 식별만 추가로 필요함

### 완전 변경 방식 추천 상황
- 내부 웹 시스템 전용
- UA 기반 분기가 강하게 필요함
- 브라우저 호환성을 직접 통제할 수 있음

대부분의 앱에서는 **기존 UA 유지 + 앱 식별 문자열 추가**가 가장 실용적이다.

## 실무 팁

### 앱 버전도 함께 붙이기
가능하면 단순 문자열보다 앱 버전도 같이 넣는 편이 로그 분석에 유용하다.

예:

```swift
configuration.applicationNameForUserAgent = "changok89-app/1.0.0"
```

### 서버에서 분리 처리하기
서버 쪽에서는 UA 전체 문자열을 정규식으로 강하게 해석하기보다, 특정 토큰 포함 여부만 확인하는 편이 유지보수에 유리하다.

### 외부 서비스는 너무 공격적으로 바꾸지 않기
로그인, 결제, 인증, 소셜 로그인처럼 예민한 페이지를 WebView로 여는 경우에는 UA 완전 변경이 예상치 못한 문제를 만들 수 있다.

## 마무리

`WKWebView`에서 User-Agent를 조정하는 건 어렵지 않지만, **추가와 변경은 목적이 다르다**.

- 앱 식별만 필요하다 → `applicationNameForUserAgent`
- 완전히 다른 UA가 필요하다 → `customUserAgent`
- 현재 값을 보고 싶다 → 로그 또는 JS로 확인

실무에서는 대부분 기본 UA를 유지하면서 앱 식별 문자열만 덧붙이는 방식이 가장 안전하고 관리하기 좋다.
