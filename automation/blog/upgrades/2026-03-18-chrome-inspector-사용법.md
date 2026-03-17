---
title: "Chrome Inspector 사용법"
source_post: "_posts/2023-01-30-Chrome_Inspector.md"
source_title: "Chrome Inspector 사용법"
category: Inspector
tags: [Chrome, Inspector, Web Debugging, Android]
status: needs_review
upgrade_note: "모바일 크롬/웹뷰 디버깅 기준으로 확장"
---

# Chrome Inspector 사용법

모바일 웹이나 하이브리드 앱을 디버깅할 때 가장 답답한 순간은 “PC 브라우저에서는 잘 되는데, 폰에서만 깨진다”는 상황이다. 레이아웃이 밀리거나, 특정 이벤트가 안 먹거나, 웹뷰 안에서만 네트워크 요청이 다르게 나가면 스크린샷만 보고는 해결이 어렵다. 이럴 때 필요한 도구가 **Chrome Inspector**다.

PC 브라우저 개발자 도구는 다들 익숙하지만, 모바일 기기에서 열린 크롬 탭이나 웹뷰를 원격으로 붙여서 보는 흐름은 처음 해보면 생각보다 막힌다. ADB가 필요하고, USB 디버깅도 켜야 하고, 네트워크가 불안정하면 inspector 창이 안 뜨기도 한다.

## Chrome Inspector가 필요한 상황

다음 상황이라면 거의 바로 써볼 가치가 있다.

- Android Chrome에서만 발생하는 CSS/JS 문제
- 앱 내 WebView에서 특정 스크립트가 실패하는 문제
- 모바일 터치 이벤트, viewport, user agent 확인
- 콘솔 에러나 네트워크 요청을 실기기 기준으로 보고 싶을 때

특히 하이브리드 앱에서는 “웹 문제인지 앱 래퍼 문제인지” 경계가 흐려서, Inspector로 실제 DOM과 콘솔을 보는 것만으로도 절반은 정리된다.

## 준비물

Chrome Inspector를 쓰려면 최소한 아래가 준비되어야 한다.

- Android 기기에서 **개발자 옵션 활성화**
- **USB 디버깅** 허용
- PC에 `adb` 사용 가능 환경
- 기기와 PC를 연결할 수 있는 데이터 케이블
- 기기에서 디버깅 대상 페이지 또는 웹뷰가 열린 상태

즉, 이 글은 사실상 `Android USB Debugging 활성화`와 한 세트다. ADB가 안 되면 inspector도 안 된다고 생각하면 편하다.

## 연결 순서

1. Android 기기에서 USB 디버깅을 켠다.
2. PC에 연결한 뒤 기기에서 RSA 디버깅 허용 팝업을 승인한다.
3. 터미널에서 아래 명령으로 기기가 보이는지 확인한다.

```bash
adb devices
```

4. 모바일 크롬에서 디버깅할 페이지를 연다.
5. PC 크롬 주소창에 아래 주소를 입력한다.

```text
chrome://inspect/#devices
```

6. 연결된 기기와 탭 목록이 보이면 `inspect` 버튼을 눌러 개발자 도구를 연다.

이후에는 익숙한 Chrome DevTools처럼 Elements, Console, Network, Sources 탭을 사용할 수 있다.

## 웹뷰 디버깅에서 중요한 점

모바일 크롬 탭은 비교적 잘 붙지만, 앱 내부 WebView는 별도 설정이 필요할 수 있다. 안드로이드 앱 코드에서 디버깅 가능 상태를 켜지 않으면 inspector에 안 보인다.

예를 들면 보통 아래 설정이 필요하다.

```kotlin
if (BuildConfig.DEBUG) {
    WebView.setWebContentsDebuggingEnabled(true)
}
```

이 설정이 없으면 크롬 탭은 보여도 정작 앱 웹뷰는 목록에 안 뜬다. 팀에서 자주 겪는 오해가 바로 이 부분이다.

## Inspector로 먼저 보는 것들

실무에서는 아래 순서가 효율적이다.

1. **Console**: 에러가 있는지 확인
2. **Network**: 요청이 실제로 나가는지 확인
3. **Elements**: 레이아웃/스타일 깨짐 확인
4. **Application/Storage**: 로컬 스토리지나 쿠키 확인

특히 모바일에서만 발생하는 이슈는 PC 크롬 에뮬레이터로는 재현이 안 되는 경우가 많다. 키보드, safe area, 실제 viewport 계산, OEM 브라우저 차이 등이 섞이면 실기기 inspector가 훨씬 정확하다.

## 자주 겪는 문제와 해결

### 기기는 연결됐는데 탭이 안 보인다

대부분 아래 원인이다.

- 모바일 크롬 탭이 실제로 열려 있지 않음
- 웹뷰 디버깅 설정이 꺼져 있음
- ADB 세션이 꼬였음

이럴 때는 `adb kill-server && adb start-server`로 다시 붙여 보고, 기기 화면이 잠겨 있지 않은지도 확인한다.

### inspect 버튼을 눌렀는데 창이 이상하다

회사망, 오프라인 환경, 크롬 버전 차이 때문에 UI가 다르게 보일 수 있다. 예전 글에도 적었듯 인터넷 연결이 약할 때 fallback 경로가 필요한 경우가 있었는데, 지금도 네트워크 상태와 브라우저 버전 영향을 받는 편이다.

### 웹뷰가 아예 목록에 안 뜬다

앱이 디버그 빌드인지, `setWebContentsDebuggingEnabled(true)`가 적용되었는지 먼저 봐야 한다. 릴리스 빌드에서는 막아두는 것이 맞다.

## 언제 유용하고 언제 한계가 있는가

Chrome Inspector는 프론트엔드 문제를 보는 데는 정말 강력하지만, 네트워크 복호화나 인증서 문제까지 깊게 보려면 `Charles Web Proxy`가 더 적합하다. 반대로 DOM 구조나 이벤트 전파, 콘솔 에러를 보려면 Charles로는 부족하다.

그래서 보통은 이렇게 구분한다.

- UI/JS/CSS 문제: Chrome Inspector
- API 헤더/응답 비교: Charles
- 연결 자체가 안 됨: USB 디버깅/ADB 점검

## 빠른 체크리스트

- [ ] Android 기기에서 USB 디버깅을 켰다
- [ ] `adb devices`에서 기기가 `device` 상태다
- [ ] 모바일 크롬 또는 웹뷰가 실제로 열려 있다
- [ ] 웹뷰라면 디버깅 설정을 코드에서 켰다
- [ ] `chrome://inspect/#devices`에서 inspect 버튼이 보인다

## 마무리

Chrome Inspector는 모바일 웹과 하이브리드 앱 문제를 푸는 가장 직접적인 도구다. 핵심은 “기기를 연결했다”가 아니라 **ADB 연결, 웹뷰 디버깅 설정, 실제 탭 상태**까지 한 세트로 확인하는 것이다. 한 번 연결 흐름을 익혀 두면, 실기기에서만 보이는 프론트 문제를 훨씬 덜 감으로 디버깅하게 된다.
## 팀 온보딩 문서에 꼭 넣을 문장

모바일 웹/웹뷰 디버깅 문서에는 단순히 `chrome://inspect` 주소만 적지 말고, 최소한 아래 문장을 같이 넣는 편이 좋다.

- USB 디버깅과 ADB 연결이 먼저 되어야 한다
- 웹뷰는 앱 코드에서 디버깅 허용 설정이 필요할 수 있다
- 실기기 화면이 잠겨 있으면 연결이 불안정할 수 있다

이 세 줄만 있어도 신입 개발자가 "인스펙터가 고장난 것 같다"며 시간을 쓰는 일을 꽤 줄일 수 있다.


status: needs_review
