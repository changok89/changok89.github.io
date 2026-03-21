---
title:  "Safari Inspector 사용법"
excerpt: "Mac Safari에서 iPhone Safari와 WebView를 원격 디버깅하는 Web Inspector 사용법 정리"

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

모바일 웹이나 iOS 앱 내부 `WKWebView`를 디버깅할 때 가장 기본적으로 쓰는 도구가 **Safari Web Inspector**다. Mac의 Safari에서 iPhone 또는 iPad에 열려 있는 웹 페이지나 WebView를 원격으로 inspect할 수 있다.

이 기능이 특히 유용한 상황은 아래와 같다.

- iPhone Safari에서만 발생하는 레이아웃 문제 확인
- iOS WebView 안에서 실행되는 JavaScript 에러 추적
- 모바일 실기기에서의 네트워크 요청, 콘솔 로그, DOM 상태 확인
- Mac 브라우저에서는 재현되지 않는 터치/스크롤 관련 문제 점검

## Safari Inspector로 할 수 있는 것

원격 디버깅이 붙으면 아래 작업을 수행할 수 있다.

- Elements / DOM 확인
- Console 로그 및 JavaScript 실행
- Network 요청 확인
- Resource / Storage 확인
- 실제 iOS Safari 또는 앱 WebView 상태 점검

즉, Mac Safari의 개발자 도구를 이용해 **실기기 웹 콘텐츠를 직접 들여다보는 방식**이다.

## 사용 전 준비

Safari Inspector는 기본적으로 비활성화되어 있는 경우가 많다. Mac Safari와 iPhone 양쪽에서 몇 가지 설정을 먼저 확인해야 한다.

### 1. Mac Safari에서 개발자 메뉴 켜기

1. Mac에서 Safari를 실행한다.
2. 상단 메뉴에서 **Safari > 설정** 으로 이동한다.
3. **고급** 탭을 연다.
4. **메뉴 막대에서 개발자용 메뉴 보기** 를 체크한다.

| ![Image Alt Inspector1](/assets/img/contents/inspector/inspector1.png) |

개발자용 메뉴가 활성화되면 단축키 `option(⌥) + command(⌘) + i` 로 Inspector를 열고 닫을 수도 있다.

| ![Image Alt Inspector2](/assets/img/contents/inspector/inspector2.png) |

### 2. iPhone에서 웹 속성(Web Inspector) 켜기

iPhone에서도 원격 디버깅 허용이 필요하다.

- **설정 > Safari > 고급 > 웹 속성(Web Inspector)** 활성화

| ![Image Alt Inspector3](/assets/img/contents/inspector/inspector3.png) | ![Image Alt Inspector4](/assets/img/contents/inspector/inspector4.png) |

## Mobile Safari 디버깅 방법

모바일 Safari 페이지를 직접 디버깅하는 가장 기본적인 흐름이다.

1. Mac과 iPhone을 케이블로 연결한다.
2. iPhone Safari에서 디버깅할 웹페이지를 연다.
3. Mac Safari 상단 메뉴에서 **개발용 > 기기 이름 > 디버깅할 웹페이지** 를 선택한다.
4. Inspector 창이 열리면 DOM, Console, Network 등을 확인한다.

| ![Image Alt Inspector5](/assets/img/contents/inspector/inspector5.png) |

### 기기 이름이 안 보일 때
- iPhone에서 웹 속성이 켜져 있는지 확인
- 케이블 연결이 정상인지 확인
- 기기 잠금이 해제되어 있는지 확인
- Mac이 iPhone을 신뢰하고 있는지 확인

경우에 따라 Safari Technology Preview를 설치해서 시도하면 더 잘 보일 때도 있다.

## 하이브리드 앱(WebView 포함 앱) 디버깅

Safari Inspector는 Mobile Safari만이 아니라 앱 내부의 `WKWebView`도 볼 수 있다. 다만 보통은 **개발용으로 빌드된 앱**이어야 한다.

### 절차

1. Mac과 iPhone을 연결한다.
2. 앱을 실행하고 WebView가 포함된 화면을 연다.
3. Mac에서 Safari를 연다.
4. 상단 메뉴의 **개발용 > 기기 이름** 에서 해당 앱의 WebView 항목을 선택한다.
5. Inspector 창이 열리면 앱 내 웹 화면을 디버깅할 수 있다.

이 기능은 하이브리드 앱, 인증 페이지, 외부 웹 콘텐츠 포함 화면, in-app browser 디버깅에 특히 유용하다.

## 잘 안 될 때 체크리스트

### 1. 메뉴에 기기가 안 보인다
- iPhone 웹 속성 활성화 확인
- 케이블 교체 또는 허브 문제 점검
- iPhone 잠금 해제 여부 확인
- Mac과 iPhone의 신뢰 관계 확인

### 2. 기기는 보이는데 페이지가 안 보인다
- 실제로 iPhone Safari 또는 앱 WebView가 열려 있는지 확인
- WebView 화면이 foreground 상태인지 확인
- 앱이 개발용 빌드인지 확인

### 3. 특정 앱 WebView만 안 보인다
- 앱 쪽 빌드 설정이나 디버깅 허용 상태를 점검
- App Store 배포본보다 개발용 빌드에서 재시도

### 4. 인터넷 없이도 가능한가
내 경험상 Safari Inspector는 Mac이 오프라인이어도 비교적 잘 쓸 수 있는 편이라, 폐쇄망 테스트나 사내 환경 디버깅에서 꽤 편하다.

## Safari Inspector가 특히 좋은 점

- iOS 실기기 전용 문제를 바로 볼 수 있음
- WebView 디버깅까지 가능함
- Mac Safari 기본 기능이라 별도 설치 부담이 적음
- 네트워크 없는 환경에서도 활용성이 있음

## 사용하면서 느낀 점

모바일 웹을 많이 다루면 Safari Inspector는 거의 필수다. 예전에는 기능이 다소 답답하게 느껴질 때도 있었지만, 최근에는 충분히 실무에 쓸 만한 수준이라고 느낀다.

특히 iOS에서만 재현되는 문제는 결국 iOS에서 봐야 해서, Safari Inspector를 익혀두면 디버깅 시간이 꽤 줄어든다.

## 마무리

Safari Web Inspector는 iPhone Safari와 앱 내부 WebView를 Mac에서 원격 디버깅할 수 있게 해주는 기본 도구다. 핵심 준비는 단순하다.

1. Mac Safari에서 개발자 메뉴 켜기
2. iPhone Safari에서 웹 속성 켜기
3. 케이블 연결 후 개발용 메뉴에서 대상 페이지 선택

이 흐름만 익혀두면 iOS 모바일 웹 디버깅이 훨씬 수월해진다.
