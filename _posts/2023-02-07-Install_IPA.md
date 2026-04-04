---
title: IPA 파일 설치
excerpt: Xcode, Apple Configurator, OTA 링크를 이용해 IPA 파일을 iPhone에 설치하는 대표 방법 정리
categories:
- iOS
tags:
- IPA
- iOS
- Xcode
- Apple Configurator
toc: true
toc_sticky: true
toc_label: IPA 파일 설치 방법
date: 2023-02-07
last_modified_at: 2026-03-21
---

일반 사용자는 App Store를 통해 앱을 설치하지만, 개발/테스트 환경에서는 App Store를 거치지 않고 IPA 파일을 직접 설치해야 하는 경우가 있다.

예를 들면 아래와 같다.

- 개발용 빌드 테스트
- 사내 배포 앱 설치
- 엔터프라이즈 배포 앱 설치
- TestFlight 외 별도 배포 경로 검토
- 특정 버전 IPA를 직접 확인해야 하는 상황

다만 IPA 설치는 단순히 파일만 있으면 끝나는 문제가 아니다. **서명 방식, 프로비저닝, 기기 등록 여부, 배포 방식**에 따라 성공 여부가 달라진다. 이 글에서는 실제로 많이 쓰는 설치 방법 3가지를 정리한다.

## 먼저 알아둘 점

아래 조건이 맞지 않으면 설치가 실패할 수 있다.

- IPA가 해당 기기에서 실행 가능한 서명인지
- 개발용 provisioning profile에 기기 UDID가 포함되어 있는지
- 엔터프라이즈/Ad Hoc 배포 규칙이 맞는지
- 설치 대상 iOS 버전이 앱 최소 지원 버전 이상인지

즉 설치 도구만 맞아도 끝나는 게 아니라, **IPA 자체가 설치 가능한 상태인지**를 같이 봐야 한다.

## 1. Xcode를 이용하여 설치

프로젝트는 없지만 IPA 파일만 있고, Mac + Xcode 환경이 있는 경우 가장 먼저 시도하기 쉬운 방법이다.

### 사용 방법

1. iPhone을 Mac에 연결한다.
2. Xcode를 실행한다.
3. 상단 메뉴에서 **Window > Devices and Simulators** 를 연다.
4. 연결된 기기를 선택한다.
5. Installed Apps 영역에 IPA 파일을 drag & drop 하거나 `+` 버튼으로 선택한다.

![Image Alt ipa1](/assets/img/contents/ipa/ipa1.png)

### 장점

- 개발자에게 가장 익숙한 방식
- 실기기 연결 상태를 같이 확인하기 좋음
- 설치 실패 시 디바이스 상태를 같이 볼 수 있음

### 단점

- Mac과 Xcode가 필요함
- 프로비저닝/서명 문제가 있으면 결국 IPA 자체를 다시 확인해야 함

## 2. Apple Configurator를 이용하여 설치

Apple Configurator는 다수 기기 관리나 수동 설치 작업에서 편하다. 사내 테스트 기기, 전시 기기, 데모폰처럼 여러 대를 다루는 환경에서도 꽤 유용하다.

### 사용 방법

1. Apple Configurator를 실행한다.
2. 연결된 iPhone을 선택한다.
3. 좌측 메뉴에서 **앱**을 선택한다.
4. 설치할 IPA를 드래그 앤 드롭하거나 앱 목록에 추가한다.

![Image Alt ipa2](/assets/img/contents/ipa/ipa2.png)

### 장점

- 기기 관리 도구로서 UI가 비교적 직관적
- 여러 기기 작업에 적합
- Mac 환경에서 반복 설치 시 편함

### 단점

- 여전히 Mac이 필요함
- IPA 서명 문제는 별도로 해결되지 않음

## 3. 링크(OTA)로 설치

사용자에게 설치 링크를 전달해야 하거나, 브라우저를 통해 설치 흐름을 만들고 싶다면 OTA(Over-the-Air) 방식이 필요하다.

이 방식은 단순히 IPA 파일만 올리는 것이 아니라, **manifest.plist**까지 같이 준비해야 한다.

### 필요한 것

- HTTPS가 설정된 웹서버
- 설치할 IPA 파일
- OTA용 `manifest.plist`
- 사용자가 Safari 등으로 열 수 있는 설치 링크

### 링크 예시

```html
<a href="itms-services://?action=download-manifest&url=https://domain.com/app/iOS/manifest.plist">app install</a>
```

![Image Alt ipa3](/assets/img/contents/ipa/ipa3.png)

### OTA 방식이 잘 맞는 경우

- 소수 사용자에게 테스트 빌드를 배포할 때
- Ad Hoc / Enterprise 방식의 사내 배포
- 설치 페이지를 별도 웹으로 운영할 때

### 주의할 점

- 반드시 HTTPS여야 한다.
- manifest.plist의 IPA URL, bundle identifier, version 정보가 정확해야 한다.
- iOS 정책과 배포 서명이 맞지 않으면 링크는 떠도 설치가 안 된다.
- 일반 App Store 앱 배포를 대신하는 방식으로 생각하면 안 된다.

## 설치가 안 될 때 먼저 확인할 것

### 1. 기기 UDID 등록 여부
개발용 또는 Ad Hoc 배포라면 대상 기기 UDID가 provisioning profile에 포함되어 있어야 한다.

### 2. 서명 방식
- Development
- Ad Hoc
- Enterprise
- App Store

이 중 어떤 서명인지에 따라 설치 가능한 경로가 달라진다.

### 3. 최소 iOS 버전
오래된 기기나 구버전 iOS에서는 설치 자체가 막히거나 설치 후 실행이 안 될 수 있다.

### 4. 신뢰 설정
엔터프라이즈 배포 앱은 기기에서 개발자 신뢰 설정을 별도로 요구할 수 있다.

## 어떤 방법을 선택하면 좋나

내 기준으로는 이렇게 정리한다.

- **개발자가 Mac에서 직접 설치** → Xcode
- **여러 대 기기 관리 또는 수동 설치 편의성** → Apple Configurator
- **링크 배포가 필요** → OTA + manifest.plist

## 실무 팁

### 설치보다 서명 문제가 더 자주 원인이다
도구를 바꿔도 계속 실패하면 설치 방식보다 IPA 생성 과정부터 다시 보는 게 빠르다.

### 테스트 기기 목록을 관리해두면 좋다
Ad Hoc 배포를 자주 한다면 UDID 목록과 배포 대상 기기 버전을 정리해두는 것이 편하다.

### TestFlight와 역할을 나눠 생각하기
내부 테스트가 넓게 퍼져야 하면 TestFlight가 더 편하고, 특정 버전 IPA를 강하게 통제해야 하면 직접 설치 방식이 더 맞을 수 있다.

## 마무리

IPA 파일 설치는 방법 자체는 여러 가지지만, 결국 핵심은 **설치 도구보다 서명과 배포 방식이 맞는지**다. Xcode, Apple Configurator, OTA 링크는 각각 잘 맞는 상황이 다르므로 목적에 맞게 선택하는 것이 좋다.

빠르게 정리하면:

- 직접 설치: Xcode
- 기기 관리형 설치: Apple Configurator
- 링크 배포: OTA

그리고 설치가 안 되면 도구 탓보다 먼저 **서명과 provisioning**을 확인하는 편이 맞다.
