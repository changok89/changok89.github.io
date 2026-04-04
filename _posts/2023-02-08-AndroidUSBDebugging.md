---
title: Android USB Debugging 활성화
excerpt: Android에서 개발자 옵션을 열고 USB 디버깅과 무선 디버깅을 활성화하는 방법 정리
categories:
- Android
tags:
- usb debugging
- Android
- adb
- wireless debugging
toc: true
toc_sticky: true
toc_label: Android USB Debugging 활성화
date: 2023-02-08
last_modified_at: 2026-03-21
---

Android 기기를 개발이나 디버깅 용도로 사용하려면 가장 먼저 필요한 설정 중 하나가 **USB 디버깅(USB debugging)** 이다. `adb` 명령, Android Studio 디버깅, 로그 확인, APK 설치, WebView 디버깅 같은 작업은 대부분 이 기능이 활성화되어 있어야 한다.

실제로는 아래 작업 전에 거의 항상 확인한다.

- Android Studio에서 실기기 실행
- `adb devices` 확인
- APK 직접 설치
- logcat 수집
- Chrome DevTools / WebView 디버깅
- scrcpy 화면 미러링

## USB 디버깅을 켜기 전에 필요한 것

Android에서는 기본적으로 개발자 옵션 메뉴가 숨겨져 있다. 따라서 먼저 **개발자 옵션**을 활성화해야 한다.

## 1. Android 개발자 옵션 활성화

기기 제조사마다 메뉴 이름은 조금 다르지만 흐름은 거의 비슷하다.

### 일반적인 방법

1. **설정** 앱을 연다.
2. **휴대전화 정보** 또는 **기기 정보**로 이동한다.
3. **빌드 번호**를 찾는다.
4. 빌드 번호를 7번 정도 연속으로 탭한다.
5. 잠금 해제 비밀번호 입력 후 개발자 옵션이 활성화된다.

설정 검색에서 "빌드 번호"를 직접 찾아 들어가는 방식도 편하다.

| ![Image Alt debug1](/assets/img/contents/usb/debug1.png) | ![Image Alt debug2](/assets/img/contents/usb/debug2.png) |

### 잘 안 보일 때

삼성, 샤오미, 픽셀 등 제조사마다 메뉴 위치가 약간 다를 수 있다. 이럴 땐 설정 상단 검색창에 아래 키워드를 넣는 게 빠르다.

- 빌드 번호
- 개발자 옵션
- developer options

## 2. USB Debugging 활성화

개발자 옵션이 열리면 이제 USB 디버깅을 켤 수 있다.

### 일반적인 경로

1. **설정 > 시스템 > 개발자 옵션** 으로 이동한다.
2. **USB 디버깅** 항목을 찾는다.
3. 스위치를 켠다.
4. 경고 팝업이 나오면 허용한다.

설정 검색에서 "개발자 옵션"을 찾은 뒤 들어가도 된다.

![Image Alt usb1](/assets/img/contents/usb/usb1.png)

## 3. 기기를 PC에 연결한 뒤 확인할 것

USB 디버깅을 켠 뒤에도 바로 끝나는 건 아니다. 실제 연결 시 아래 확인이 필요하다.

### RSA 디버깅 허용 팝업
처음 연결하면 기기에 "이 컴퓨터의 RSA 키를 허용할까요?" 비슷한 팝업이 뜬다. 여기서 허용하지 않으면 `adb devices`에 unauthorized로 보일 수 있다.

### 케이블 품질
충전 전용 케이블은 데이터 통신이 안 될 수 있다. 의외로 가장 흔한 원인 중 하나다.

### USB 모드
기기 연결 후 알림창에서 파일 전송/데이터 전송 모드가 필요한 경우도 있다. 제조사별로 미묘하게 다르므로 연결이 안 되면 이것도 확인한다.

## 4. 무선 디버깅 활성화

최근 Android 버전에서는 USB 없이도 **무선 디버깅(Wireless debugging)** 을 통해 ADB 연결을 할 수 있다. 같은 네트워크에서 테스트 장비를 자주 붙였다 떼는 환경이라면 매우 편하다.

### 경로

1. **설정 > 개발자 옵션** 으로 이동한다.
2. **무선 디버깅** 을 켠다.
3. 같은 네트워크의 개발 PC와 pairing을 진행한다.

![Image Alt remote1](/assets/img/contents/usb/remote1.png)

### 무선 디버깅이 유용한 경우

- USB 포트가 부족할 때
- 여러 기기를 번갈아 테스트할 때
- 케이블 연결 없이 간단히 로그를 보고 싶을 때
- scrcpy나 adb 연결을 더 유연하게 유지하고 싶을 때

### 주의할 점

- 같은 Wi-Fi 환경이 필요하다.
- 네트워크가 바뀌면 다시 pairing이 필요할 수 있다.
- 보안상 공용 네트워크에서 장시간 열어두는 것은 주의가 필요하다.

## 연결이 안 될 때 체크리스트

### `adb devices`에 아무 것도 안 뜬다
- 케이블 문제인지 확인
- 개발자 옵션/USB 디버깅이 켜져 있는지 확인
- PC에 adb가 정상 설치됐는지 확인
- 제조사 드라이버 이슈(Windows) 여부 확인

### `unauthorized` 로 보인다
- 기기 화면 잠금 해제
- RSA 허용 팝업 재확인
- 필요하면 `adb kill-server && adb start-server` 재시도

### 무선 디버깅이 안 붙는다
- 같은 네트워크인지 확인
- pairing code / pairing port 재확인
- 방화벽이나 보안 솔루션이 막는지 확인

## 실무에서 자주 같이 쓰는 도구

USB 디버깅을 켠 뒤에는 보통 아래 작업으로 이어진다.

- `adb devices`
- `adb install`
- `adb logcat`
- Chrome WebView inspect
- `scrcpy`
- Android Studio Run / Debug

즉 USB 디버깅은 그 자체가 목적이 아니라 **실기기 개발 작업의 출발점**이다.

## 마무리

Android USB 디버깅 활성화는 절차 자체는 간단하지만, 실제로 막히는 지점은 주로 개발자 옵션 위치, 케이블, RSA 허용, 무선 디버깅 페어링 쪽이다.

정리하면:

1. 빌드 번호 7번 → 개발자 옵션 활성화
2. USB 디버깅 ON
3. 연결 후 RSA 허용
4. 필요하면 무선 디버깅까지 사용

이 흐름만 익숙해지면 실기기 테스트 준비 시간이 훨씬 줄어든다.
