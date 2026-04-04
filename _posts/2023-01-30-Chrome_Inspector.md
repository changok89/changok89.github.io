---
title: Chrome Inspector 사용법
excerpt: Android Chrome과 WebView를 PC에서 원격 디버깅할 때 쓰는 chrome://inspect 사용법 정리
categories:
- Inspector
tags:
- Chrome
- Inspector
- Web Debugging
- Android
- WebView
toc: true
toc_sticky: true
toc_label: Chrome Inspector
date: 2023-01-30
last_modified_at: 2026-03-21
---

모바일 웹이나 Android WebView를 디버깅할 때는 PC 브라우저 개발자 도구만으로는 한계가 있다. 이때 자주 쓰는 도구가 **Chrome Inspector**다.

정확히는 PC Chrome의 `chrome://inspect/#devices` 화면을 통해, USB로 연결한 Android 기기에서 열려 있는 Chrome 탭이나 WebView를 원격으로 확인하고 DevTools를 붙이는 방식이다.

이 기능이 유용한 대표 상황은 아래와 같다.

- 모바일 Chrome에서만 발생하는 레이아웃 문제 확인
- 실제 Android WebView 안에서 실행 중인 웹 페이지 디버깅
- 모바일 기기 네트워크 요청/콘솔 로그/DOM 상태 확인
- 반응형 레이아웃이 아니라 **실기기 환경** 자체를 보고 싶을 때

## Chrome Inspector로 할 수 있는 것

원격 디버깅이 붙으면 PC의 DevTools와 비슷하게 아래 작업을 할 수 있다.

- Elements 탭에서 DOM 확인
- Console 실행 및 로그 확인
- Network 요청 확인
- Sources/Debugger 사용
- 모바일 Chrome 탭 상태 점검
- Android 앱 안 WebView 디버깅

즉, 모바일에서 열려 있는 웹 콘텐츠를 **PC DevTools 인터페이스로 보는 것**이라고 이해하면 된다.

## 사용 전 준비사항

Chrome Inspector가 동작하려면 아래 준비가 필요하다.

### 1. Android 개발자 옵션 활성화
Android 기기에서 개발자 옵션을 먼저 켜야 한다.

- 설정에서 `빌드 번호`를 찾아 7번 탭
- 또는 설정 검색에서 `빌드 번호` 검색

### 2. USB 디버깅 허용
개발자 옵션이 열린 뒤에는 **USB 디버깅**을 켜야 한다.

- 설정 > 개발자 옵션 > USB 디버깅 ON

### 3. PC에서 adb 사용 가능 상태
PC에서 `adb` 명령이 동작해야 한다. Android SDK 전체를 설치하지 않아도 `platform-tools`만 설치해서 adb를 쓸 수 있다.

터미널에서 아래를 먼저 확인한다.

```bash
adb devices
```

기기가 보이면 기본 연결은 된 것이다.

### 4. 모바일 기기에서 대상 페이지 열기
- 모바일 Chrome에 디버깅할 페이지를 띄운다.
- 또는 WebView가 포함된 앱을 실행해서 해당 화면을 연다.

## 실제 사용 방법

### 1. Android 기기를 USB로 연결
기기를 PC에 연결하고, 처음 연결이라면 기기에서 RSA 디버깅 허용 팝업을 수락한다.

### 2. PC Chrome에서 inspect 페이지 열기
주소창에 아래를 입력한다.

```text
chrome://inspect/#devices
```

### 3. 연결된 기기 확인
정상 연결이면 기기 이름과 함께 열려 있는 Chrome 탭 또는 WebView 목록이 표시된다.

### 4. `inspect` 버튼 선택
원하는 항목 옆의 `inspect` 버튼을 누르면 DevTools 창이 열리고, 해당 모바일 페이지를 원격으로 디버깅할 수 있다.

![Image Alt inspector](/assets/img/contents/chromeInspector/inspector.png)

## WebView 디버깅 시 주의점

앱 안의 WebView를 디버깅하려면 Android 앱 쪽에서 WebView 디버깅이 허용되어 있어야 한다.

보통 개발 빌드에서는 아래 코드가 들어간 경우가 많다.

```kotlin
WebView.setWebContentsDebuggingEnabled(true)
```

이 설정이 없으면 Chrome Inspector에서 기기 연결은 보여도 원하는 WebView가 안 뜰 수 있다.

## 잘 안 될 때 확인할 것

### 1. `adb devices` 에서 기기가 안 보인다
- 케이블이 충전 전용인지 확인
- USB 디버깅이 켜져 있는지 확인
- RSA 허용 팝업을 수락했는지 확인
- PC에서 adb가 정상 설치되었는지 확인

### 2. 기기는 보이는데 inspect 대상이 안 보인다
- 모바일 Chrome에서 페이지가 실제로 열려 있는지 확인
- 앱 WebView라면 디버깅 활성화 코드가 들어갔는지 확인
- 화면이 백그라운드로 가면 목록에서 사라질 수 있음

### 3. 인터넷이 안 되는 환경에서 inspector가 불안정하다
기존 경험상 Chrome은 버전이나 환경에 따라 오프라인에서 inspector가 불안정한 경우가 있었다. 이럴 때는 `inspector fallback` 또는 다른 Chromium 계열 브라우저를 시도할 수 있다.

### 4. Edge에서도 가능한가
네. Microsoft Edge도 비슷한 원격 inspect 기능을 제공한다. 환경에 따라 Edge 쪽이 더 안정적으로 느껴질 때도 있다.

## 어떤 상황에서 가장 유용한가

내 기준으로 Chrome Inspector는 아래 상황에서 특히 효율적이다.

- Android 실기기에서만 재현되는 CSS 문제
- 모바일 브라우저 콘솔 확인
- 앱 내부 WebView 스크립트 에러 추적
- 네트워크 요청 헤더/응답 확인
- 모바일에서만 발생하는 login/session 문제 추적

## 같이 알아두면 좋은 도구

Chrome Inspector를 쓰기 전에 또는 함께 자주 쓰는 도구는 아래와 같다.

- `adb`
- Android USB debugging
- Charles Proxy
- Android Studio logcat
- 모바일 브라우저 자체 콘솔 로그

## 마무리

Chrome Inspector는 Android 모바일 웹과 WebView를 디버깅할 때 가장 기본적이면서도 강력한 도구 중 하나다. 핵심은 복잡하지 않다.

1. Android 개발자 옵션 활성화
2. USB 디버깅 켜기
3. adb 연결 확인
4. `chrome://inspect/#devices` 접속
5. `inspect`로 DevTools 열기

이 흐름만 익숙해져도 모바일 웹 디버깅 시간이 꽤 줄어든다.

# Android SDK 플랫폼 도구
[SDK 플랫폼 도구](https://developer.android.com/studio/releases/platform-tools?hl=ko){:target="_blank"}
