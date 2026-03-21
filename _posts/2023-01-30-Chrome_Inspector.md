---
title:  "Chrome Inspector 사용법"
excerpt: "Android Chrome과 WebView를 PC에서 원격 디버깅할 때 쓰는 chrome://inspect 사용 흐름 정리"

categories:
  - Inspector
tags:
  - [Chrome, Inspector, Web Debugging, Android, WebView]

toc: true
toc_sticky : true
toc_label : Chrome Inspector

date: 2023-01-30
last_modified_at: 2026-03-21
---

# Chrome Inspector란?

PC 브라우저에서는 개발자 도구를 열어 HTML, CSS, Network, Console을 바로 볼 수 있지만, 모바일 Chrome이나 Android 앱 안의 WebView는 같은 방식으로 접근할 수 없다. 이럴 때 사용하는 것이 **Chrome Inspector**다.

보통 아래 상황에서 사용한다.

- Android Chrome 모바일 웹 디버깅
- 앱 내부 WebView 디버깅
- 모바일 전용 JS 오류 확인
- 실제 기기에서만 재현되는 레이아웃 문제 확인
- Network / Console / DOM 상태 분석

핵심은 PC Chrome에서 `chrome://inspect/#devices` 로 접속해 연결된 Android 기기의 Chrome 탭 또는 WebView를 원격으로 여는 것이다.

## 사용 전 준비사항

Chrome Inspector가 잘 안 되는 경우 대부분은 사전 준비 단계에서 막힌다.

### 1. Android 개발자 옵션 활성화
기기에서 개발자 옵션이 열려 있어야 한다.

### 2. USB 디버깅 허용
개발자 옵션 안에서 **USB 디버깅**을 켜야 한다.

### 3. PC에서 adb 사용 가능
Android SDK platform-tools가 설치되어 있어야 하고, 터미널에서 `adb` 명령이 동작해야 한다.

### 4. 기기 연결 확인
USB로 기기를 연결한 뒤 `adb devices` 에서 기기가 보여야 한다.

## 설치 및 확인

### Android platform-tools 설치
[SDK 플랫폼 도구](https://developer.android.com/studio/releases/platform-tools?hl=ko){:target="_blank"}를 설치하고 `adb`가 동작하는지 확인한다.

```bash
adb devices
```

여기서 기기가 보이지 않으면 Chrome Inspector도 사실상 못 쓴다.

## Chrome Inspector 여는 방법

1. Android 기기에서 Chrome 또는 디버깅 대상 앱의 WebView 화면을 연다.
2. 기기를 USB로 PC에 연결한다.
3. PC Chrome 주소창에 `chrome://inspect/#devices` 입력
4. 연결된 기기와 디버깅 가능한 페이지 목록을 확인한다.
5. 원하는 항목의 **inspect** 또는 **inspect fallback** 버튼을 누른다.

![Image Alt inspector](/assets/img/contents/chromeInspector/inspector.png)

정상적으로 연결되면 PC에서 모바일 페이지의 DOM, Console, Network, Sources 등을 볼 수 있다.

## 어떤 것까지 디버깅할 수 있나

Chrome Inspector로 확인 가능한 대표 항목은 다음과 같다.

- DOM 구조
- CSS 스타일 적용 상태
- JavaScript Console 로그
- Network 요청
- Storage / Cookies
- Performance 관련 일부 지표

즉 실제 모바일 기기에서 열린 페이지를 PC 개발자도구처럼 다룰 수 있다고 보면 된다.

## 모바일 Chrome 디버깅

모바일 웹사이트 자체를 확인할 때 가장 직관적이다.

예시:
- 특정 Android 기기에서만 깨지는 레이아웃 확인
- 모바일 Chrome의 캐시/네트워크 동작 확인
- 실기기 터치 후 DOM 변화를 직접 관찰

## Android WebView 디버깅

앱 내부 WebView도 조건이 맞으면 Chrome Inspector에서 볼 수 있다. 이게 특히 유용한 이유는, 앱 내부에선 재현되는데 일반 모바일 Chrome에서는 재현되지 않는 이슈를 분리해 볼 수 있기 때문이다.

다만 WebView 디버깅이 가능하려면 앱 쪽에서 디버깅이 허용되어 있어야 한다. 일반적으로는 개발 빌드에서 아래 설정을 켠다.

```java
WebView.setWebContentsDebuggingEnabled(true);
```

## 잘 안 될 때 확인할 것

### 1. `adb devices`에 기기가 안 뜬다
- USB 케이블이 충전 전용일 수 있음
- 기기에서 RSA 허용 팝업을 승인하지 않음
- USB 디버깅이 꺼져 있음
- platform-tools PATH 설정 문제

### 2. 기기는 뜨는데 페이지가 안 뜬다
- Chrome 탭이 실제로 열려 있는지 확인
- 앱 WebView에서 디버깅 허용이 켜져 있는지 확인
- 앱이 release build라 디버깅이 막혀 있을 수 있음

### 3. inspect가 안 열리거나 비어 보인다
- 네트워크가 없는 환경에서 Chrome 버전에 따라 동작이 애매할 수 있다.
- 경우에 따라 **inspect fallback** 이 더 잘 열릴 때가 있다.

### 4. 인터넷 없는 환경에서 제한된다
글을 처음 쓸 때도 느꼈지만, Chrome 버전이나 환경에 따라 온라인 연결이 없는 상태에서 Inspector가 불안정하게 느껴질 때가 있다. 이럴 땐 Edge의 유사 기능이 더 나은 경우도 있다.

## 실무 팁

### WebView 이슈는 Chrome 단독 재현과 분리해서 본다
앱 WebView 문제인지, 사이트 자체 문제인지 구분하려면 같은 URL을 모바일 Chrome에서도 열어보는 게 좋다.

### Console 로그를 먼저 본다
모바일에서만 깨지는 문제는 JavaScript 에러 하나로 끝나는 경우가 많다.

### USB 연결이 가장 중요하다
디버깅이 안 될 때 복잡한 추정보다 먼저 `adb devices`부터 다시 보는 편이 빠르다.

## 언제 유용한가

Chrome Inspector는 아래처럼 "실기기에서만 보이는 문제"에 특히 강하다.

- 특정 Android 버전에서만 깨지는 CSS
- 모바일 터치 이벤트 문제
- WebView JS 브리지 동작 점검
- 하이브리드 앱 내 쿠키/세션 문제
- 모바일 네트워크 요청 흐름 확인

## 마무리

Chrome Inspector는 Android 실기기 웹 디버깅의 기본 도구에 가깝다. 특히 WebView를 포함한 앱을 다룰 때는 재현 환경을 PC 개발자 도구처럼 볼 수 있다는 점에서 가치가 크다.

요약하면:

1. 개발자 옵션 + USB 디버깅 켜기
2. `adb devices` 확인
3. `chrome://inspect/#devices` 접속
4. 대상 탭 또는 WebView를 inspect

이 흐름만 익숙해져도 모바일 웹 디버깅 속도가 확실히 빨라진다.
