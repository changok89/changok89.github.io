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
- chrome 개발자도구는 Google 크롬 브라우저에 내장된 웹 개발자 도구모음이다.

# Chrome Inspector 사용전 준비사항
- 안드로이드폰에 개발자모드를 활성화한다. 설정에서 검색에 '빌드번호'를 검색하여 찾아 7번 터치한다.
- 개발자모드가 활성화되면 설정에서 '개발자옵션'를 검색하면 메뉴가 활성화된다.
- 개발자옵션을 들어가 'usb 디버깅'을 허용한다.
- PC에 android sdk를 설치하거나 android sdk tools를 설치하여 Path를 설정한다.
- 명령프롬프트나 터미널에 adb 명령어가 동작하는지 확인한다.
- adb 사용이 가능해야 pc에 안드로이드폰이 연결되었을때 chrome inspector에 연결된 기기가 보인다.
- 모바일 크롬에 디버깅할 웹페이지를 띄우고 안드로이드폰을 usb케이블로 PC에 연결한다. chrome inspector에 연결된 기기가 보인다.


# Chrome Inspector
- PC에서는 크롬에 개발자도구를 단축키로 열면되지만 모바일 크롬이나 웹뷰가 포함된앱에 웹 페이지를 디버깅하려면 Chrome Inspector를 사용해야한다.
- chrome 주소창에 chrome://inspect/#devices 입력하여 접속
- inspector, inspector fallback 버튼을 누르면 개발자도구를 사용할 수 있다.

![Image Alt inspector](/assets/img/contents/chromeInspector/inspector.png)

# Chrome Inspector가 안될때
- chrome에 경우 인터넷연결이되지않으면 inspector가 동작하지않는다. (버전마다 다른것 같음)
- 크롬버전에 따라 인터넷에 안되는 환경에서는 fallback을 통해서 개발자도구를 사용할 수 있다.
- ms edge도 동일한 기능을 제공하는데 인터넷이 없는 환경에서도 사용가능하다.

# Android SDK 플랫폼 도구
[SDK 플랫폼 도구](https://developer.android.com/studio/releases/platform-tools?hl=ko){:target="_blank"}