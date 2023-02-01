---
title:  "Chrome Inspector 사용법"
excerpt: "Chrome Inspector 사용법"

categories:
  - Inspector
tags:
  - [Chrome, Inspector, Web Debugging]

toc: true
toc_sticky : true
toc_label : Chrome Inspector

date: 2023-01-30
last_modified_at: 2023-01-31
---

# Chrome 개발자도구
- chrome 개발자도구는 Google 크롬 브라우저에 직접 내장 된 웹 개발자 도구모음이다.

# Chrome Inspector
- chrome 주소창에 chrome://inspect/#devices 입력하여 접속
- 안드로이드폰에 개발자모드를 활성화하고 usb 디버깅을 허용한다.
- PC에는 adb가 사용가능하게 path설정이 되어있어야한다. 명령프롬프트나 터미널에 adb 명령어가 동작하는지 확인한다.
- 모바일크롬에 디버깅할 페이지를 띄우고 usb케이블로 연결하여 PC크롬에 inspector로 개발자도구를 사용할수있다.
- chrome에 경우 인터넷연결이되지않으면 inspector가 동작하지않는다.
- 크롬버전에 따라 인터넷에 안되는 환경에서는 fallback을 통해서 개발자도구를 사용할 수 있다.
- ms edge도 동일한 기능을 제공하는데 인터넷이 없는 환경에서도 사용가능한걸로 알고있다.
