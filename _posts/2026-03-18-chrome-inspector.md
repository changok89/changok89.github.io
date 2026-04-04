---
title: Chrome Inspector 사용법
excerpt: 안드로이드 실기기나 WebView에서만 보이는 문제는 PC 브라우저만으로 잡기 어렵다. ADB 연결부터 chrome://inspect,
  WebView 디버깅 설정까지 실무 기준으로 정리한다.
categories:
- Inspector
tags:
- Chrome
- Inspector
- Android
- WebView
- Debugging
toc: true
toc_sticky: true
toc_label: Chrome Inspector 사용법
date: 2026-03-18
last_modified_at: 2026-03-21
---

모바일 웹이나 하이브리드 앱을 디버깅하다 보면 꼭 한 번은 "PC 브라우저에서는 잘 되는데 폰에서만 깨진다"는 상황을 만난다. 레이아웃이 밀리거나, 특정 이벤트가 안 먹거나, 앱 안 WebView에서만 콘솔 에러가 나는 문제는 스크린샷 몇 장으로는 해결이 잘 안 된다. 이럴 때 가장 직접적으로 도움이 되는 도구가 **Chrome Inspector**다.

데스크톱 Chrome DevTools는 익숙해도, Android 기기에서 열린 크롬 탭이나 WebView를 PC에서 원격으로 붙여 보는 흐름은 처음 하면 꽤 자주 막힌다. ADB 연결, USB 디버깅, WebView 디버깅 설정이 한 세트로 맞아야 하기 때문이다. 이 글에서는 단순히 주소 한 줄만 적는 대신, 실제로 연결이 안 될 때 어디를 봐야 하는지까지 포함해서 정리한다.

## Chrome Inspector가 필요한 상황

아래 같은 상황이라면 거의 바로 써볼 가치가 있다.

- Android Chrome에서만 발생하는 CSS/JS 문제
- 앱 내부 WebView에서 특정 스크립트가 실패하는 문제
- 모바일 터치 이벤트, viewport, user agent 확인
- 실기기 기준 콘솔 에러와 네트워크 요청을 보고 싶을 때

특히 하이브리드 앱에서는 문제가 웹 코드인지, 네이티브 래퍼인지, 특정 단말 환경인지 경계가 흐려진다. 이럴 때 Inspector로 실제 DOM과 Console, Network를 확인하면 추측보다 훨씬 빠르게 범위를 좁힐 수 있다.

## 준비물

Chrome Inspector를 쓰려면 최소한 아래 조건이 갖춰져야 한다.

- Android 기기에서 **개발자 옵션 활성화**
- **USB 디버깅** 허용
- PC에서 `adb` 사용 가능
- 데이터 전송 가능한 USB 케이블
- 기기에서 디버깅 대상 페이지 또는 WebView가 열린 상태

즉, 이 글은 사실상 `Android USB Debugging 활성화`와 같이 봐야 한다. ADB 연결이 안 되면 Inspector도 안 된다고 생각하는 편이 이해가 쉽다.

## 연결 순서

기본 흐름은 아래와 같다.

1. Android 기기에서 USB 디버깅을 켠다.
2. PC와 기기를 연결한다.
3. 기기 화면에 뜨는 RSA 디버깅 허용 팝업을 승인한다.
4. 터미널에서 아래 명령으로 기기 연결 상태를 확인한다.

```bash
adb devices
```

정상이면 대체로 아래처럼 보인다.

```text
List of devices attached
R3CN30XXXX    device
```

5. 기기에서 Chrome 또는 디버깅 대상 앱의 WebView를 연다.
6. PC Chrome 주소창에 아래 주소를 입력한다.

```text
chrome://inspect/#devices
```

7. 연결된 기기와 탭 목록이 보이면 `inspect` 버튼을 눌러 개발자 도구를 연다.

이후에는 데스크톱 Chrome DevTools와 비슷하게 Elements, Console, Network, Sources 탭을 사용할 수 있다.

## WebView 디버깅에서 중요한 점

모바일 Chrome 탭은 비교적 잘 붙지만, 앱 내부 WebView는 별도 설정이 필요할 수 있다. Android 앱 코드에서 WebView 디버깅을 켜지 않으면 `chrome://inspect`에 안 보일 수 있다.

보통은 디버그 빌드에서 아래 설정을 사용한다.

```kotlin
if (BuildConfig.DEBUG) {
    WebView.setWebContentsDebuggingEnabled(true)
}
```

이 설정이 없으면 Chrome 탭은 보여도 정작 앱 WebView는 목록에 안 뜬다. 실무에서 많이 헷갈리는 지점이 바로 여기다.

## Inspector로 먼저 볼 것들

실무에서는 아래 순서로 보는 편이 효율적이다.

1. **Console**: 에러가 있는지 확인
2. **Network**: 요청이 실제로 나가는지 확인
3. **Elements**: 레이아웃이나 스타일 깨짐 확인
4. **Application/Storage**: 로컬 스토리지, 쿠키, 캐시 확인

모바일에서만 발생하는 문제는 데스크톱 에뮬레이션으로는 재현이 안 되는 경우가 많다. 키보드, 실제 viewport, OEM 브라우저 차이, 단말 성능 차이 같은 요소는 결국 실기기 Inspector가 가장 정확하다.

## 자주 겪는 문제와 해결

### 기기는 연결됐는데 탭이 안 보인다

대부분 아래 원인이다.

- 모바일 Chrome 탭이 실제로 열려 있지 않음
- WebView 디버깅 설정이 꺼져 있음
- ADB 세션이 꼬였음
- 기기 화면이 잠겨 있거나 권한 팝업을 놓침

이럴 때는 아래처럼 ADB를 재시작해 보는 것이 빠르다.

```bash
adb kill-server
adb start-server
adb devices
```

### `inspect` 버튼을 눌렀는데 창이 이상하다

Chrome 버전 차이, 네트워크 상태, 사내망 정책 때문에 UI가 어색하거나 일부 기능이 제대로 안 뜰 수 있다. 이때는 기기와 PC의 Chrome 버전 차이도 같이 보는 편이 좋다.

### WebView가 아예 목록에 안 뜬다

앱이 디버그 빌드인지, `setWebContentsDebuggingEnabled(true)`가 실제로 적용됐는지 먼저 확인해야 한다. 릴리스 빌드에서 막아두는 것이 일반적이므로, 릴리스 환경에서 안 보이는 것이 오히려 정상일 수 있다.

## 언제 유용하고 언제 한계가 있는가

Chrome Inspector는 DOM, CSS, JavaScript, 콘솔 에러를 보는 데는 매우 강력하다. 반면 네트워크를 복호화해서 상세 비교하거나 헤더 차이를 집중적으로 보고 싶다면 `Charles Web Proxy`가 더 적합하다.

나는 보통 아래처럼 나눈다.

- UI, JS, CSS 문제: Chrome Inspector
- API 헤더, 응답, HTTPS 요청 확인: Charles
- 연결 자체가 안 됨: USB 디버깅과 ADB 점검

## 빠른 체크리스트

- [ ] Android 기기에서 USB 디버깅을 켰다
- [ ] `adb devices`에서 기기가 `device` 상태로 보인다
- [ ] 모바일 Chrome 또는 WebView가 실제로 열려 있다
- [ ] WebView라면 앱 코드에서 디버깅을 켰다
- [ ] `chrome://inspect/#devices`에서 `inspect` 버튼이 보인다

## 마무리

Chrome Inspector는 모바일 웹과 하이브리드 앱 문제를 푸는 가장 직접적인 도구 중 하나다. 핵심은 단순히 기기를 연결하는 것이 아니라, **ADB 연결, WebView 디버깅 설정, 실제 탭 상태**까지 한 세트로 맞추는 것이다. 이 흐름만 익혀 두면 실기기에서만 보이는 프론트엔드 문제를 훨씬 덜 감으로 디버깅하게 된다.
