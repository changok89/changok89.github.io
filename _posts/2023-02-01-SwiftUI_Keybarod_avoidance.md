---
title: SwiftUI Keyboard Avoidance
excerpt: SwiftUI에서 키보드가 올라올 때 화면이 과하게 밀리거나 WebView 스크롤이 깨질 때 정리하는 방법
categories:
- iOS
tags:
- iOS
- SwiftUI
- Keyboard
- WebView
toc: true
toc_sticky: true
toc_label: SwiftUI Keyboard Avoidance
date: 2023-02-01
last_modified_at: 2026-03-21
---

iOS 14부터 SwiftUI는 기본적으로 키보드가 올라오면 화면이 가려지지 않도록 레이아웃을 자동으로 조정합니다. 단순한 `TextField` 중심 화면에서는 이 동작이 편리하지만, 실제 프로젝트에서는 이 자동 조정이 오히려 문제를 만들 때가 많습니다.

특히 아래 같은 상황에서 자주 부딪힙니다.

- `ScrollView` 안에 입력창이 여러 개 있는 화면
- 하단 고정 버튼이 있는 폼 화면
- `WKWebView` 안의 HTML input 포커스 시점
- 키보드가 올라오면서 전체 뷰가 예상보다 크게 밀리는 화면
- 웹 콘텐츠가 스크롤되는 중에 SwiftUI와 WebView가 동시에 레이아웃을 바꾸는 화면

이 글에서는 SwiftUI의 keyboard avoidance가 언제 도움이 되고, 언제 꺼야 하는지, 그리고 `WebView`가 섞인 화면에서는 어떻게 접근하는 게 안전한지 정리한다.

## SwiftUI가 기본으로 해주는 것

SwiftUI는 키보드가 올라오면 안전 영역(safe area)과 레이아웃을 계산해서 입력창이 키보드에 가리지 않도록 화면을 밀거나 줄인다. 덕분에 단순한 폼에서는 별도 코드 없이도 꽤 자연스럽게 동작한다.

예를 들어 아래 같은 화면은 기본 동작만으로도 충분한 경우가 많다.

- 로그인 화면
- 회원가입 입력 폼
- 메모 작성 화면
- 단일 `TextEditor` 입력 화면

하지만 모든 화면이 단순 폼은 아니다. `WebView`, 커스텀 스크롤, 하단 툴바, 내부 JavaScript 포커스 이동이 섞이면 SwiftUI의 자동 조정과 앱 쪽 조정이 겹쳐 레이아웃이 과도하게 변할 수 있다.

## 문제가 자주 발생하는 패턴

### 1. WebView 내부 input 포커스

`WKWebView` 안에 있는 HTML `input`이나 `textarea`에 포커스가 가면 웹 페이지도 스크롤을 조정하고, iOS 시스템도 키보드 대응을 시도한다. 여기에 SwiftUI 상위 뷰가 keyboard avoidance까지 적용하면 아래 같은 현상이 생긴다.

- 화면이 이중으로 움직임
- 입력창 위치가 튐
- 스크롤 위치가 갑자기 맨 위나 중간으로 이동함
- 하단 영역이 비정상적으로 빈 공간처럼 보임

### 2. 하단 고정 버튼이 있는 폼

입력 화면 아래쪽에 "완료", "저장" 같은 버튼을 붙여둔 경우, 키보드 등장과 동시에 전체 레이아웃이 바뀌며 버튼 위치가 의도와 다르게 움직일 수 있다.

### 3. 커스텀 키보드 대응과 중복 적용

이미 UIKit 또는 Notification 기반으로 키보드 높이를 직접 계산하고 있는데 SwiftUI 기본 대응까지 같이 켜져 있으면 중복 이동이 발생한다.

## 언제 keyboard avoidance를 끄는 게 좋은가

아래 조건에 하나라도 해당하면 기본 동작을 비활성화하는 편이 낫다.

- WebView가 메인 콘텐츠인 화면
- 앱이 자체적으로 키보드 높이를 계산하는 화면
- 스크롤 위치를 직접 관리하는 화면
- 화면 일부만 키보드에 반응해야 하는 복합 레이아웃
- 특정 OS 버전에서 레이아웃이 깨지는 이슈를 빠르게 우회해야 하는 상황

## 해결 방법: `.ignoresSafeArea(.keyboard, edges: .bottom)`

SwiftUI에서 가장 간단한 방법은 키보드에 의한 safe area 변경을 무시하도록 설정하는 것이다.

```swift
.ignoresSafeArea(.keyboard, edges: .bottom)
```

이 modifier를 적용하면 키보드가 올라와도 SwiftUI가 하단 safe area를 기준으로 전체 화면을 다시 줄이지 않는다. 즉, 기본 keyboard avoidance를 꺼서 레이아웃 재계산을 줄이는 효과를 얻을 수 있다.

<script src="https://gist.github.com/changok89/37d8151a1e183c3b52f46c024a3b7a3a.js"></script>

## 어떤 레벨에 붙일까

이 modifier는 너무 상위에 붙이면 의도하지 않은 화면까지 영향을 줄 수 있다. 반대로 너무 내부에 붙이면 실제 문제 구간에는 적용이 안 될 수 있다.

보통은 아래 순서로 고려하면 된다.

1. 문제를 일으키는 화면 최상단 컨테이너
2. `WebView`를 포함하는 래퍼 뷰
3. 특정 섹션만 꺼야 한다면 해당 섹션 컨테이너

프로젝트 전체에 일괄 적용하기보다는 **문제가 생기는 화면 단위로 적용**하는 게 안전하다.

## 적용 전후 차이

### keyboard avoidance 적용 상태

기본 상태에서는 키보드가 올라오면서 전체 화면이 재배치된다.

![Image Alt keyboardAvoidance](/assets/img/contents/keyboardAvoidance/keyboardAvoidacne.gif)

### keyboard avoidance 비활성화 상태

safe area의 keyboard 반응을 무시하면 화면 리사이즈가 줄어들고, WebView나 자체 스크롤 로직이 더 안정적으로 유지되는 경우가 많다.

![Image Alt keyboardAvoidance_disable](/assets/img/contents/keyboardAvoidance/keyboardAvoidance_disable.gif)

## 적용할 때 주의할 점

### 입력창이 정말 가려지지 않는지 확인하기

기본 대응을 끄면, 당연히 입력창이 키보드 뒤로 숨어버릴 수도 있다. 따라서 아래를 함께 확인해야 한다.

- 실제 입력창이 보이는지
- 스크롤로 충분히 접근 가능한지
- 하단 버튼이 키보드 뒤에 완전히 가려지지 않는지
- iPhone SE처럼 화면이 작은 기기에서도 usable한지

### WebView와 네이티브 입력 화면은 분리해서 생각하기

WebView 중심 화면에서는 이 옵션이 잘 맞지만, 일반 SwiftUI 폼 화면에서는 오히려 불편해질 수 있다. 같은 앱 안에서도 화면 성격에 따라 다르게 적용하는 것이 맞다.

### iPad / 회전 / 멀티태스킹도 체크하기

iPad split view, 가로모드, 외부 키보드 연결 상태에서는 레이아웃 체감이 달라질 수 있다. 문제가 재현되는 환경에서 꼭 다시 본다.

## 실무에서 추천하는 판단 기준

내 기준으로는 아래처럼 정리하면 편하다.

- **일반 폼 화면**: 기본 keyboard avoidance 유지
- **WebView 중심 화면**: 우선 `.ignoresSafeArea(.keyboard, edges: .bottom)` 검토
- **직접 키보드 높이 제어 중인 화면**: SwiftUI 기본 동작 비활성화 고려
- **특정 OS에서만 깨지는 화면**: 문제 화면에 한정 적용

## 확인 체크리스트

적용 후에는 아래를 확인하면 된다.

- `TextField` 포커스 시 화면이 과하게 점프하지 않는가
- `WKWebView` 내부 input 포커스 시 스크롤이 안정적인가
- 하단 버튼 또는 툴바가 의도한 위치에 남아 있는가
- 작은 화면에서도 입력 완료가 가능한가
- iOS 버전 차이에서 부작용이 없는가

## 마무리

SwiftUI의 keyboard avoidance는 기본값으로는 꽤 유용하지만, `WebView`나 복합 레이아웃이 들어가면 오히려 불안정성을 만들 수 있다. 이럴 때는 키보드 safe area 반응을 끄고, 필요한 화면에서만 직접 제어하는 편이 더 예측 가능하다.

특히 **WebView 내부 input focus 때문에 스크롤이 이상하게 움직이는 문제**를 보고 있다면, 가장 먼저 확인해볼 옵션 중 하나가 `.ignoresSafeArea(.keyboard, edges: .bottom)`이다.

---

# 참고
[ios-14-swiftui-keyboard-lifts-view-automatically](https://stackoverflow.com/questions/63958912/ios-14-swiftui-keyboard-lifts-view-automatically){:target="_blank"}
