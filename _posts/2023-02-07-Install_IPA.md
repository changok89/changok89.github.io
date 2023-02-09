---
title:  "IPA 파일 설치"
excerpt: "IPA 파일 설치"

categories:
  - iOS
tags:
  - [IPA]

toc: true
toc_sticky : true
toc_label : IPA 파일 설치 방법

date: 2023-02-07
last_modified_at: 2023-02-07
---

# IPA파일 설치방법

- 개발용앱 또는 엔터프라이즈 인증서로 빌드된 앱 등 AppStore를 통하지않고 IPA파일로 앱을 설치할 수 있다.

## XCode로 이용하여 설치

- 일반적이라면 기기를 연결하여 프로젝트를 빌드하면되지만 프로젝트가 없고 IPA파일만 있을 때 사용한다.
- XCode를 실행하고 상단메뉴에 Window > Device and Simulators 실행
- Installed App 영역에 IPA파일을 drag&drop 하거나 + 버튼을 클릭하여 IPA파일을 선택.

> ![Image Alt ipa1](/assets/img/contents/ipa/ipa1.png)

## Apple Configurator를 이용하여 설치

- Apple Configurator를 실행하고 연결되있는 iPhone을 선택한다.
- 좌측메뉴에 '앱'을 선택하고 설치할 IPA파일을 우측 앱목록에 drag&drop한다.

> ![Image Alt ipa2](/assets/img/contents/ipa/ipa2.png)

## 링크를 이용하여 설치

- SSL(https)이 구성된 웹서버가 필요하다.
- html파일에 a tag로 링크를 만들어 ipa파일을 설치할 수 있다.
- 링크를 생성하려면 ipa파일뿐만아니라 OTA(over the air)용 manifest.plist파일을 만들어야 한다.
- mainfest.plist파일을 만들고 html파일에 다음과 같이 주소를 입력한다.  

``` <a href="itms-services://?action=download-manifest&url=https://domain.com/app/iOS/manifest.plist">app install</a> ```

> ![Image Alt ipa3](/assets/img/contents/ipa/ipa3.png)