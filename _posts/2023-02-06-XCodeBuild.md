---
title: XCode Command Line tool을 이용한 Build, Archive, Export
excerpt: xcodebuild로 iOS 프로젝트를 clean, build, archive, export 할 때 자주 쓰는 명령 정리
categories:
- Utility
tags:
- XCode
- xcodebuild
- iOS
- CI
toc: true
toc_sticky: true
toc_label: XCodeBuild
date: 2023-02-06
last_modified_at: 2026-03-21
---

`xcodebuild`는 Xcode 프로젝트를 명령줄에서 빌드, 테스트, 아카이브, 내보내기 할 수 있게 해주는 기본 도구다. CI/CD 환경에서는 사실상 필수고, 로컬에서도 GUI를 열지 않고 빌드 상태를 빠르게 확인할 때 유용하다.

특히 아래 상황에서 자주 쓴다.

- Jenkins, GitHub Actions 등 CI에서 iOS 빌드 자동화
- Xcode GUI 없이 clean/build/archive 수행
- Release 빌드 결과 확인
- xcarchive 생성 후 IPA export
- workspace / scheme 조합을 명령줄로 통제

## xcodebuild를 왜 익혀두면 좋나

- 반복 작업을 스크립트로 자동화할 수 있다.
- 빌드 로그를 텍스트로 남기기 쉽다.
- GUI 상태와 무관하게 CI 환경을 재현하기 좋다.
- 팀 내 배포 스크립트나 nightly build 파이프라인에 바로 연결된다.

## 먼저 확인할 것

터미널에서 아래 명령이 동작하는지 본다.

```bash
xcodebuild -h
```

`command not found: xcodebuild` 같은 오류가 나면 Command Line Tools 설치 또는 Xcode 선택 상태를 확인해야 한다.

## Xcode Command Line Tools 확인

- Xcode 설정에서도 Command Line Tools가 올바르게 선택돼 있는지 볼 수 있다.

> ![Image Alt xcodebuild1](/assets/img/contents/xcodebuild/xcodebuild1.png)

## 설치 방법

### 1. 터미널에서 설치

```bash
xcode-select --install
```

### 2. Apple Developer에서 직접 설치
필요하면 Apple Developer 사이트에서 관련 패키지를 내려받아 설치할 수도 있다.

> ![Image Alt xcodebuild2](/assets/img/contents/xcodebuild/xcodebuild2.png)

## 자주 쓰는 기본 명령

### 버전 확인

```bash
xcodebuild -version
```

> ![Image Alt xcodebuild3](/assets/img/contents/xcodebuild/xcodebuild3.png)

이 명령으로 현재 사용 중인 Xcode 및 Build version을 확인할 수 있다.

### 사용 가능한 SDK 확인

```bash
xcodebuild -showsdks
```

> ![Image Alt xcodebuild4](/assets/img/contents/xcodebuild/xcodebuild4.png)

## clean

### xcodeproj clean

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -scheme ${TARGET_NAME} -destination 'generic/platform=iOS' clean
```

### xcworkspace clean

```bash
xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -destination 'generic/platform=iOS' clean
```

빌드 캐시 상태를 초기화하고 다시 시작할 때 주로 쓴다.

## build

빌드할 때 자주 쓰는 주요 옵션은 아래다.

- `-project` : 빌드할 `.xcodeproj`
- `-workspace` : 빌드할 `.xcworkspace`
- `-scheme` 또는 `-target`
- `-sdk` : `iphoneos`, `iphonesimulator`
- `-destination`
- `-configuration` : `Debug`, `Release`

### xcodeproj build

#### device 빌드

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release build
```

#### simulator 빌드

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${TARGET_NAME} -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -configuration Debug build
```

### xcworkspace build

#### device 빌드

```bash
xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release build
```

#### simulator 빌드

```bash
xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -configuration Debug build
```

## archive

배포용 산출물을 만들려면 보통 archive 단계가 필요하다.

- `archivePath` 옵션으로 결과 저장 위치를 지정할 수 있다.

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -scheme ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release -archivePath ./archive/${TARGETNAME}.xcarchive archive
```

archive는 단순 build보다 배포 준비에 더 가까운 단계라고 생각하면 된다.

## IPA export

xcarchive를 만든 뒤 IPA를 export 하려면 아래처럼 사용한다.

```bash
xcodebuild -exportArchive -archivePath ./archive/${TARGET_NAME}.xcarchive -exportPath ./build/${TARGET_NAME} -exportOptionsPlist ./exportOptions.plist
```

> ![Image Alt xcodebuild5](/assets/img/contents/xcodebuild/xcodebuild5.png)

여기서 `exportOptions.plist`는 배포 방식(App Store, Ad Hoc, Development, Enterprise 등)에 맞게 준비돼 있어야 한다.

## project와 workspace 중 무엇을 써야 하나

- CocoaPods, Swift Package, 여러 타겟 구성 때문에 `.xcworkspace`를 쓰는 프로젝트가 많다.
- 순수 단일 프로젝트 구조라면 `.xcodeproj`로도 충분할 수 있다.

헷갈릴 때는 실제로 Xcode에서 무엇을 열고 작업하는지 보면 빠르다. 평소 `.xcworkspace`를 열고 있다면 CLI에서도 workspace 기준으로 맞추는 편이 안전하다.

## CI에서 자주 보는 흐름

대표적인 자동화 흐름은 아래와 비슷하다.

1. clean
2. build
3. archive
4. exportArchive
5. 산출물 업로드 또는 배포

즉 `xcodebuild`는 단일 명령이라기보다 **iOS 빌드 파이프라인의 중심 명령**에 가깝다.

## 자주 막히는 문제

### scheme 이름이 틀림
workspace나 project 안의 scheme 이름이 정확하지 않으면 바로 실패한다. 공백이나 대소문자까지 확인하는 편이 좋다.

### signing 문제
로컬에서는 되는데 CI에서 안 되는 경우 대부분 서명, 인증서, provisioning profile, keychain 접근 문제와 연결된다.

### destination 지정 오류
시뮬레이터용과 디바이스용 destination을 혼동하면 오류가 발생한다. 특히 `generic/platform=iOS` 와 `generic/platform=iOS Simulator` 차이를 주의해야 한다.

## 마무리

`xcodebuild`는 iOS 프로젝트를 자동화하고, 배포 파이프라인을 만들고, GUI 없이 빌드 흐름을 통제할 수 있게 해주는 핵심 도구다.

우선 아래 흐름만 익혀도 충분히 실무에 도움이 된다.

- `xcodebuild -version`
- `xcodebuild -showsdks`
- `clean`
- `build`
- `archive`
- `exportArchive`

CI/CD를 붙일 계획이라면 결국 다시 돌아오게 되는 도구라서, 초반에 기본 패턴을 익혀두면 많이 편해진다.
