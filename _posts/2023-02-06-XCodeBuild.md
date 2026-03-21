---
title:  "XCode Command Line tool을 이용한 Build, Archive, Export"
excerpt: "xcodebuild로 iOS 프로젝트를 clean, build, archive, export 하는 기본 흐름 정리"

categories:
  - Utility
tags:
  - [XCode, xcodebuild, iOS, CI]

toc: true
toc_sticky : true
toc_label : XCodeBuild

date: 2023-02-06
last_modified_at: 2026-03-21
---

# Xcode Command Line Tool과 xcodebuild

`xcodebuild`는 Xcode 프로젝트를 터미널에서 빌드, 테스트, 아카이브, 내보내기 할 수 있게 해주는 기본 도구다. 로컬 자동화 스크립트, Jenkins 같은 CI, 배포 파이프라인에서 거의 빠지지 않는다.

실무에서 자주 쓰는 작업은 아래와 같다.

- clean
- build
- archive
- export
- sdk 목록 확인
- Xcode 버전/환경 확인

즉 Xcode GUI에서 하던 작업을 커맨드라인으로 재현한다고 생각하면 된다.

## 1. 먼저 확인할 것

터미널에서 아래 명령이 동작하는지 확인한다.

```bash
xcodebuild -h
```

`command not found: xcodebuild` 가 나오면 Xcode 또는 Command Line Tools 설정을 확인해야 한다.

### Xcode 설정에서 확인
Xcode의 설정에서 Command Line Tools가 어떤 버전으로 잡혀 있는지 확인할 수 있다.

> ![Image Alt xcodebuild1](/assets/img/contents/xcodebuild/xcodebuild1.png)

## 2. Command Line Tools 설치

### 터미널에서 설치

```bash
xcode-select --install
```

### 또는 Apple Developer 사이트에서 설치
직접 DMG를 받아 설치하는 방법도 있다.

> ![Image Alt xcodebuild2](/assets/img/contents/xcodebuild/xcodebuild2.png)

## 3. 자주 쓰는 확인 명령

### Xcode 버전 확인

```bash
xcodebuild -version
```

> ![Image Alt xcodebuild3](/assets/img/contents/xcodebuild/xcodebuild3.png)

### 사용 가능한 SDK 목록 확인

```bash
xcodebuild -showsdks
```

> ![Image Alt xcodebuild4](/assets/img/contents/xcodebuild/xcodebuild4.png)

이 두 명령은 CI 환경이 꼬였을 때도 매우 자주 확인한다.

## 4. clean

빌드 찌꺼기를 정리하고 새로 시작할 때 사용한다.

### xcodeproj clean

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -scheme ${TARGET_NAME} -destination 'generic/platform=iOS' clean
```

### xcworkspace clean

```bash
xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -destination 'generic/platform=iOS' clean
```

CocoaPods나 여러 프로젝트 구성이 있으면 `workspace` 기준으로 작업하는 경우가 많다.

## 5. build

### 빌드 시 자주 쓰는 옵션

- `-project` : `.xcodeproj` 경로
- `-workspace` : `.xcworkspace` 경로
- `-scheme` 또는 `-target`
- `-sdk` : `iphoneos`, `iphonesimulator`
- `-destination`
- `-configuration` : `Debug`, `Release`

### xcodeproj build

#### device build

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release build
```

#### simulator build

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${TARGET_NAME} -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -configuration Debug build
```

### xcworkspace build

#### device build

```bash
xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release build
```

#### simulator build

```bash
xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -configuration Debug build
```

## 6. archive

배포 가능한 산출물 기준으로 묶는 단계다. 보통 Release 구성에서 `archive`를 수행한다.

```bash
xcodebuild -project ${PROJECT_NAME}.xcodeproj -scheme ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release -archivePath ./archive/${TARGET_NAME}.xcarchive archive
```

### archivePath를 쓰는 이유
결과 산출물 위치를 고정해두면 이후 export 단계나 CI 파이프라인에서 다루기 편하다.

## 7. IPA export

archive 이후 IPA를 꺼내려면 `-exportArchive` 를 사용한다.

```bash
xcodebuild -exportArchive -archivePath ./archive/${TARGET_NAME}.xcarchive -exportPath ./build/${TARGET_NAME} -exportOptionsPlist ./exportOptions.plist
```

> ![Image Alt xcodebuild5](/assets/img/contents/xcodebuild/xcodebuild5.png)

여기서 핵심은 `exportOptions.plist`다. 배포 방식(App Store, Ad Hoc, Enterprise 등)에 따라 설정이 달라진다.

## 8. 언제 project를 쓰고, 언제 workspace를 쓰나

- 순수 Xcode 프로젝트만 쓰는 경우 → `-project`
- CocoaPods 등으로 workspace가 생긴 경우 → `-workspace`

실제론 workspace 기반 프로젝트가 많아서 `-workspace -scheme` 조합에 익숙해지는 편이 좋다.

## 9. CI에서 자주 하는 흐름

보통은 아래 순서로 자동화한다.

1. `xcodebuild -version` 으로 환경 확인
2. clean
3. build
4. archive
5. export
6. 아티팩트 업로드

즉 xcodebuild는 단일 명령 하나보다 **빌드 파이프라인의 중심 축**에 가깝다.

## 10. 자주 막히는 문제

### scheme 이름이 틀렸다
터미널에선 GUI와 달리 정확한 scheme 이름이 중요하다.

### signing / provisioning 오류
빌드는 되는데 archive/export에서 막히는 경우가 많다. 이건 xcodebuild 명령보다 서명 설정을 먼저 봐야 한다.

### 올바른 Xcode 버전이 선택되지 않았다
여러 Xcode가 설치돼 있으면 `xcode-select -p` 와 `xcodebuild -version`을 같이 확인하는 편이 좋다.

## 마무리

xcodebuild는 iOS 빌드 자동화의 기본 도구다. 처음엔 옵션이 많아 보여도 clean, build, archive, export 흐름만 익히면 대부분의 배포 작업을 스크립트화할 수 있다.

핵심만 정리하면:

- 환경 확인 → `xcodebuild -version`, `-showsdks`
- 빌드 정리 → `clean`
- 산출물 생성 → `build`
- 배포용 묶기 → `archive`
- IPA 꺼내기 → `exportArchive`

로컬에서 한 번 정확히 정리해두면 CI/CD 환경으로 옮길 때도 훨씬 수월하다.
