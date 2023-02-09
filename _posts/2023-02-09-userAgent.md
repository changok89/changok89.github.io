---
title:  "WKWebView userAgent"
excerpt: "WKWebView userAgent"

categories:
  - iOS
tags:
  - [WKWebView, userAgent]

toc: true
toc_sticky : true
toc_label : WKWebView userAgent

date: 2023-02-09
last_modified_at: 2023-02-09
---

# UserAgent
- HTTP요청시 디바이스와 브라우저(WebView) 등 사용자 식별정보를 담고 있는 header이다.
- userAgent는 Mozilla 버전(정보) + OS정보 + 렌더링 엔진 정보 + 브라우저이름 형태로 구성된다.
- 브라우저나 WebView console창에 navigator.userAgent 호출시 아래와같이 형태로 출력된다.

> navigator.userAgent
> 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'  

# WKWebView UserAgent에 값 추가
- userAgent값에 특정한 문자열 추가해보자.
- 보통 하이브리드앱와 모바일브라우저를 구분하거나 앱인지 웹인지 구분하기위해서 사용된다.
- Swift에서 WKWebView생성시 Configuration에 applicationNameForUserAgent에 값을 추가한다.

``` Swift
  let configuration = WKWebViewConfiguration()
  configuration.applicationNameForUserAgent = "changok89"
  let webView = WKWebView(frame: .zero, configuration: configuration)
```

- 사파리 인스펙터로 확인
![Image Alt userAgent1](/assets/img/contents/userAgent/userAgent1.png)

# WKWebView UserAgent 변경
- userAgent값을 기존값을 제거하거 현재 입력된 string으로 대체한다.
- 이렇게 userAgent를 변경하면 userAgent값을 보고 동작하는 javascript library에 영향을 줄 수 있다.

``` Swift
  let configuration = WKWebViewConfiguration()
  let webView = WKWebView(frame: .zero, configuration: configuration)
  webView.customUserAgent = "changok89"
```

- 사파리 인스펙터로 확인  
![Image Alt userAgent2](/assets/img/contents/userAgent/userAgent2.png)

# WKWebView에 userAgent 값 가져오기

``` Swift
  let configuration = WKWebViewConfiguration()
  configuration.applicationNameForUserAgent = "changok89"
  let webView = WKWebView(frame: .zero, configuration: configuration)

  if let userAgent = webView.value(forKey: "userAgent") {
    print("\(userAgent)")
  }
```

- 로그확인
![Image Alt userAgent3](/assets/img/contents/userAgent/userAgent3.png)