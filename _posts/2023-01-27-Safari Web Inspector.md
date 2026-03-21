---
title:  "Safari Inspector 사용법"
excerpt: "Mac Safari의 Web Inspector로 iPhone Safari와 앱 내 WKWebView를 디버깅하는 방법 정리"

categories:
  - iOS
tags:
  - [Safari, Web Debugging, Web Inspector, WKWebView]

toc: true
toc_sticky : true
toc_label : Safari Inspector

date: 2023-01-27
last_modified_at: 2026-03-21
---

# Safari Web Inspector

Safari에도 강력한 Web Inspector가 있다. 웹 개발자 입장에선 Chrome DevTools에 더 익숙할 수 있지만, iPhone Safari나 iOS 앱 내부의 `WKWebView`를 실기기 기준으로 디버깅할 때는 Safari Inspector가 사실상 정석에 가깝다.

특히 아래 같은 상황에서 매우 유용하다.

- iPhone Safari에서만 발생하는 CSS/JS 문제 확인
- iOS 실기기에서 터치 이벤트 문제 분석
- 앱 내부 `WKWebView` 페이지 디버깅
- Mobile Safari와 Chrome의 동작 차이 비교
- 콘솔 오류, 네트워크 요청, DOM 상태 확인

## Safari Inspector가 필요한 이유

데스크톱 Safari에서 정상인데 iPhone Safari에서만 문제가 생기는 경우는 의외로 많다. 예를 들면 다음과 같다.

- viewport 계산 차이
- iOS 키보드와 safe area 처리 문제
- touch / scroll 관련 버그
- WebView와 브라우저의 미세한 렌더링 차이

이런 문제는 실제 iOS Safari 환경을 직접 보지 않으면 파악이 어렵다. 그래서 Mac Safari의 개발자 메뉴를 활성화하고, 연결된 iPhone을 원격으로 inspect하는 흐름을 알아두면 좋다.

## 1. Mac에서 Safari 개발자 메뉴 활성화

기본적으로 Safari의 개발자 메뉴는 숨겨져 있다.

### 활성화 방법

1. Mac에서 Safari를 실행한다.
2. 상단 메뉴에서 **Safari > 설정** 으로 이동한다.
3. **고급** 탭을 연다.
4. **메뉴 막대에서 개발자용 메뉴 보기** 를 체크한다.

| ![Image Alt Inspector1](/assets/img/contents/inspector/inspector1.png) |

활성화 후에는 메뉴 막대에 **개발용** 메뉴가 나타난다.

### 단축키

Inspector 창을 열고 닫는 대표 단축키는 다음과 같다.

- `option(⌥) + command(⌘) + i`

| ![Image Alt Inspector2](/assets/img/contents/inspector/inspector2.png) |

## 2. iPhone Safari 디버깅 준비

모바일 Safari를 Mac에서 보려면 iPhone 쪽에서도 설정이 필요하다.

### iPhone에서 웹 속성 켜기

1. iPhone에서 **설정** 앱을 연다.
2. **Safari > 고급** 으로 이동한다.
3. **웹 속성(Web Inspector)** 을 활성화한다.

| ![Image Alt Inspector3](/assets/img/contents/inspector/inspector3.png) | ![Image Alt Inspector4](/assets/img/contents/inspector/inspector4.png) |

이 설정이 꺼져 있으면 Mac Safari의 개발자 메뉴에 기기가 떠도 실제 디버깅 대상 페이지가 나타나지 않을 수 있다.

## 3. Mobile Safari 디버깅 방법

1. Mac과 iPhone을 케이블로 연결한다.
2. iPhone에서 Safari로 디버깅할 웹페이지를 연다.
3. Mac에서 Safari를 열고, 상단 **개발용** 메뉴를 연다.
4. 연결된 기기 이름을 선택한다.
5. 하위 목록에서 열려 있는 웹페이지를 선택한다.
6. Inspector 창이 열린다.

| ![Image Alt Inspector5](/assets/img/contents/inspector/inspector5.png) |

이제 데스크톱 브라우저 개발자도구처럼 DOM, Console, Network, Resources 등을 확인할 수 있다.

## 4. 하이브리드 앱 WebView 디버깅

Safari Inspector는 Mobile Safari뿐 아니라 **WebView가 포함된 앱** 디버깅에도 매우 유용하다.

### 사용 방법

1. Mac과 iPhone을 케이블로 연결한다.
2. 앱을 실행하고 WebView 화면을 연다.
3. Mac에서 Safari를 연다.
4. 상단 메뉴 **개발용 > 기기 이름 > 앱의 WebView 화면** 을 선택한다.
5. Inspector 창이 열린다.

앱이 개발용 빌드로 올라가 있고 WebView 디버깅이 가능해야 정상적으로 표시된다.

## 5. Safari Inspector에서 주로 보는 항목

### Console
JavaScript 오류나 경고를 가장 빠르게 파악할 수 있다.

### Elements / DOM
실제 iPhone에서 렌더링된 DOM 구조와 스타일 적용 상태를 확인할 수 있다.

### Network
API 요청, 정적 리소스 로딩, 상태 코드, 캐시 여부를 볼 수 있다.

### Storage / Cookies
로그인 세션, 로컬 저장소, 쿠키 관련 문제 분석에 유용하다.

## 6. 잘 안 될 때 체크리스트

### 기기 이름이 안 보인다
- 케이블 연결 상태 확인
- iPhone 잠금 해제 여부 확인
- Mac을 신뢰하도록 허용했는지 확인

### 기기는 보이는데 페이지가 안 보인다
- iPhone에서 웹 속성이 켜져 있는지 확인
- Safari에서 해당 페이지가 실제로 열려 있는지 확인
- 앱 WebView가 개발용 빌드인지 확인

### 개발자 메뉴가 안 보인다
- Mac Safari 설정의 고급 탭에서 다시 체크

### 연결이 애매할 때
경우에 따라 Safari Technology Preview에서 더 잘 잡히는 경우도 있다. 특정 환경에서 기본 Safari가 불안정하면 보조 도구로 고려할 만하다.

## 7. 실무에서 자주 쓰는 상황

- iOS에서만 발생하는 CSS 깨짐 확인
- 키보드/viewport/safe area 이슈 확인
- `WKWebView` 내부 페이지 디버깅
- 실제 기기 터치와 스크롤 흐름 확인
- 하이브리드 앱의 콘솔 에러 확인

## 사용기

모바일 웹 화면 디버깅할 때 정말 자주 사용한다. 예전보다 기능도 많이 나아졌고, 무엇보다 **Mac 인터넷 연결 없이도 실기기 기준 디버깅이 가능하다**는 점이 꽤 편하다. Chrome 계열 도구가 Android에 강하다면, iOS에선 Safari Inspector를 익혀두는 게 훨씬 유리하다.

## 마무리

Safari Inspector는 iPhone Safari와 iOS WebView를 가장 정확하게 볼 수 있는 기본 도구다. iOS에서만 재현되는 웹 이슈를 자주 다루면 거의 필수라고 봐도 된다.

정리하면:

1. Mac Safari 개발자 메뉴 활성화
2. iPhone Safari의 웹 속성 켜기
3. 케이블 연결 후 개발용 메뉴에서 대상 페이지 선택
4. Mobile Safari와 앱 WebView를 실기기 기준으로 분석

Chrome Inspector가 Android 쪽 기본 도구라면, Safari Inspector는 iOS 쪽 기본 도구라고 생각하면 편하다.
