---
title:  "Safari Inspector 사용법"
excerpt: "Safari Inspector 사용법"

categories:
  - iOS
tags:
  - [Safari, Web Debugging]

toc: true
toc_sticky : true
toc_label : Safari Inspector

date: 2023-01-27
last_modified_at: 2023-01-27
---

# Safari Web Inspector
- Safari도 Web Inspector를 제공하고 있고 웹 개발시 디버깅할때 유용하다.
- 기본적으로 비활성화되어있어 설정에서 '개발자용' 메뉴를 켜야 동작한다.
- iPhone에 Mobile Safari로 Mac에 케이블로 연결해서 Web Inspector사용이 가능하다.
- Mobile Safari 디버깅시 '웹속성'이 켜져있어서 Mac에 디버깅이 가능하다.
- 하이브리드앱(WebView를 포함한 앱)도 디버깅이 가능하다. (단, 앱은 개발용으로 빌드되어있어야 한다.)

# Safari Web Inspector 활성화방법
- Mac에서 Safari를 실행시킨다.
- Safari 상단메뉴에 Safari > 설정 > 고급(탭) > '메뉴 막대에서 개발자용 메뉴 보기' 체크

| ![Image Alt Inspector1](/assets/img/contents/inspector/inspector1.png) |

- 개발용메뉴가 활성화되면 단축키 option(⌥) + command(⌘) + i 로 inspector를 열기/닫기가 가능하다.

| ![Image Alt Inspector2](/assets/img/contents/inspector/inspector2.png) |

---

# Mobile Safari 디버깅
1. Mac에서 케이블로 iPhone을 연결한다.
2. Mobile Safari로 디버깅할 웹페이지를 연다.
3. Mac Safari에 개발용 > '기기이름' > '디버깅할 웹페이지' 선택
   - 기기이름이 보이지않는다면 Mobile Safari에 웹속성이 활성화되어있는지 확인
   - 연결된 기기가 보이지않는다면 Safari Technology Preview를 설치해서 사용하기도 한다.
4. Mac에 inspector창이 열린다.

| ![Image Alt Inspector5](/assets/img/contents/inspector/inspector5.png) |

# Mobile Safari 웹속성 켜기
- '설정(앱)' > Safari > 고급 > 웹속성 활성화

| ![Image Alt Inspector3](/assets/img/contents/inspector/inspector3.png) | ![Image Alt Inspector4](/assets/img/contents/inspector/inspector4.png)

---

# 하이브리드앱 디버깅
1. Mac에서 케이블로 iPhone을 연결한다.
2. 앱을 실행시키고 WebView가 포함된 화면을 연다.
3. Mac에 Safari를 연다.
4. 상단메뉴에 개발용 > '기기이름' > 디버깅할 앱에 webview 화면 선택
5. Mac에 inspector창이 열린다.

---

# 사용기
- 모바일웹화면 디버깅할때 많이 사용한다.
- 예전과 비교해 기능이 많이 추가되어 safari inspector도 사용할만하다.
- Mac에 인터넷연결없이 사용가능해서 좋다.