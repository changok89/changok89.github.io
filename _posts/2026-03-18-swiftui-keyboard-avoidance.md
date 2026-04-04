---
title: SwiftUI Keyboard Avoidance
excerpt: SwiftUI는 기본 keyboard avoidance를 제공하지만, 실제 프로젝트에서는 ScrollView, safe area,
  WebView, 하단 고정 버튼이 섞이면서 오히려 더 미묘한 버그가 나온다. 실무 관점에서 정리한다.
categories:
- iOS
tags:
- SwiftUI
- Keyboard
- iOS
- Layout
- WebView
toc: true
toc_sticky: true
toc_label: SwiftUI Keyboard Avoidance
date: 2026-03-18
last_modified_at: 2026-03-21
---

SwiftUI로 폼 화면을 만들다 보면 키보드가 올라올 때 화면이 자동으로 밀리거나, 반대로 예상보다 과하게 레이아웃이 변하는 상황을 자주 만난다. 기본 제공 동작이 있으니 편할 것 같지만, 실제 프로젝트에서는 `ScrollView`, `sheet`, `safe area`, `WebView`가 섞이면서 꽤 미묘한 버그가 나온다.

특히 iOS 14 이후 SwiftUI가 기본적으로 keyboard avoidance를 제공하면서, 예전 UIKit처럼 직접 키보드 높이를 계산하지 않아도 되는 장점은 생겼다. 그런데 동시에 **원하지 않는 자동 이동**도 생겼다. 그래서 중요한 것은 기능이 있느냐보다 **언제 기본 동작을 믿고, 언제 제어해야 하는가**다.

## SwiftUI의 기본 동작 이해하기

SwiftUI는 키보드가 올라오면 가려질 수 있는 입력 필드를 보이도록 레이아웃을 조정한다. 간단한 로그인 화면에서는 꽤 편하다. `TextField`에 포커스가 들어가면 뷰 전체가 적절히 올라오거나, 스크롤 가능한 영역이 조정된다.

문제는 화면 구조가 단순하지 않을 때다.

- `VStack` 기반 고정 레이아웃
- `ScrollView` 안의 다수 입력 필드
- 하단 고정 버튼
- `UIViewRepresentable`로 감싼 `WKWebView`
- 커스텀 sheet나 popup

이런 조건이 겹치면 기본 동작이 오히려 UX를 망가뜨릴 수 있다.

## 대표적인 문제 시나리오

### 화면 전체가 과하게 리사이즈된다

입력 필드 하나에 포커스가 갔을 뿐인데 상단 헤더, 중간 콘텐츠, 하단 버튼이 전부 흔들리는 경우가 있다. 특히 fixed layout처럼 설계한 화면에서는 더 어색하다.

### WebView 안의 input 포커스에서 이상 동작한다

이건 꽤 자주 헷갈린다. SwiftUI 외부 뷰라고 생각한 `WKWebView` 안의 HTML input에도 키보드 이벤트가 연결되면서, 상위 SwiftUI 레이아웃이 불필요하게 반응할 수 있다. 그러면 스크롤 위치가 튀거나 콘텐츠가 겹쳐 보인다.

## 기본 회피를 끄고 싶을 때

상황에 따라 아래 modifier가 도움이 된다.

```swift
.ignoresSafeArea(.keyboard, edges: .bottom)
```

이 설정은 키보드에 의해 하단 safe area가 조정되는 동작을 무시하게 해 준다. 즉, 기본 keyboard avoidance를 부분적으로 꺼서 레이아웃 리사이즈를 막는 데 유용하다.

예를 들면 아래처럼 쓸 수 있다.

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            Spacer()
            TextField("메시지 입력", text: .constant(""))
                .textFieldStyle(.roundedBorder)
        }
        .padding()
        .ignoresSafeArea(.keyboard, edges: .bottom)
    }
}
```

하지만 이것을 만능 해결책처럼 쓰면 또 다른 문제가 생긴다. 키보드가 올라와도 입력 필드가 실제로 가려질 수 있기 때문이다.

## 그래서 어떻게 판단할까

내 기준은 아래와 같다.

### 기본 동작을 그대로 두는 편이 좋은 경우

- 로그인이나 회원가입처럼 입력 필드 중심 화면
- `ScrollView` 기반 폼
- 키보드가 올라와도 자연스럽게 스크롤 가능한 구조

### 제어가 필요한 경우

- 하단 고정 CTA가 중요한 화면
- WebView와 SwiftUI가 섞인 화면
- 커스텀 애니메이션이나 오버레이가 있는 화면
- 기획상 레이아웃 흔들림이 명확히 거슬리는 화면

즉, 무조건 끈다가 아니라 **화면 성격에 따라 다르게 본다**가 맞다.

## 실전 대응 패턴

### ScrollView로 구조를 바꾸기

단순 `VStack` 대신 `ScrollView`와 `safeAreaInset` 조합으로 바꾸면 기본 동작과 더 잘 맞는 경우가 많다. 특히 긴 폼 입력은 억지로 avoidance를 끄기보다 스크롤 가능하게 두는 편이 UX가 좋다.

### 하단 입력 바는 별도 처리

채팅 입력창처럼 하단 고정 UI가 중요하면 keyboard safe area와 inset 전략을 별도로 설계하는 편이 낫다. SwiftUI 기본 동작만 믿으면 기기별 차이가 드러난다.

### WebView는 독립적으로 생각하기

웹 입력과 네이티브 레이아웃이 서로 간섭하면 상위 SwiftUI만 조정해서는 해결이 안 된다. HTML과 CSS의 viewport 처리, 웹 내부 스크롤 정책까지 같이 봐야 한다.

## 자주 겪는 실패 사례

### `.ignoresSafeArea(.keyboard...)`를 넣었더니 입력창이 가려진다

당연한 결과다. 자동 회피를 껐기 때문이다. 이 경우는 회피를 끄는 대신 스크롤 구조를 바꾸거나, 하단 inset을 직접 설계해야 한다.

### 시뮬레이터에서는 괜찮은데 실기기에서만 튄다

실기기 키보드 높이, 예측 입력 바, 다국어 키보드, safe area 차이 때문에 그렇다. 키보드 이슈는 실기기 검증이 거의 필수다.

### sheet 안에서만 이상하다

presentation 방식에 따라 safe area 계산이 달라질 수 있다. `fullScreenCover`와 `sheet`는 체감이 다를 수 있어 분리해서 확인하는 편이 좋다.

## 같이 보면 좋은 주제

이 주제는 아래 글과 같이 보면 더 이해가 쉽다.

- `iOS 화면 미러링`
- `iOS Developer Mode 활성화 방법`

실기기에서 키보드 동작을 실제로 보여 주고 검증하려면 주변 환경 세팅도 같이 필요하기 때문이다.

## 빠른 체크리스트

- [ ] 현재 화면이 폼 중심인지, 고정 레이아웃 중심인지 먼저 구분했다
- [ ] 실기기에서 키보드 동작을 확인했다
- [ ] WebView가 섞여 있다면 별도 원인으로 분리해 봤다
- [ ] 회피를 끄는 대신 ScrollView 구조가 더 적합한지 검토했다
- [ ] 하단 고정 버튼이나 입력창은 safe area 전략을 따로 설계했다

## 마무리

SwiftUI의 keyboard avoidance는 기본 제공 기능이라 편하지만, 실무에서는 자동이라서 끝이 아니라 **자동이라서 더 의식적으로 제어해야 하는 영역**이기도 하다. 단순 폼은 기본 동작을 믿고, 복잡한 레이아웃이나 WebView 혼합 화면은 명시적으로 다루는 편이 낫다. 결국 중요한 것은 modifier 하나보다 **화면 구조와 입력 흐름을 어떤 방식으로 설계했는가**다.
