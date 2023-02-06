---
title:  "XCode Command Line tool을 이용한 Build, Archive, Export"
excerpt: "XCodeBuild 사용법"

categories:
  - Utility
tags:
  - [XCode, xcodebuild]

toc: true
toc_sticky : true
toc_label : XCodeBuild

date: 2023-02-06
last_modified_at: 2023-02-06
---

# XCode Command Line Tool
- xcode에서 앱을 Build, Archive, Test 등에 동작을 command line으로 할 수 있게 지원해주는 도구이다.
- Jenkins같은 CI/CD 도구를 이용하여 앱을 주기적으로 빌드하거나 테스트를 돌릴때 xcodebuild를 사용한다.

---

# XCode Command Line Tool 확인
- 터미널에서 xcodebuild -h 입력하여 동작하는지 확인한다.
- command not found: xcodebuild 가 발생한다면 XCode Command Line Tool 설치가 필요하다.
- xcode 설정에서도 command line tools을 아래와같이 확인할 수 있다.

> ![Image Alt xcodebuild1](/assets/img/contents/xcodebuild/xcodebuild1.png)

---

# XCode Command Line Tool 설치
- 터미널에 아래와 같이 입력하여 설치
> $ xcode-select --install 

- 또는 https://developer.apple.com 에서 dmg파일을 받아 설치한다.
> ![Image Alt xcodebuild2](/assets/img/contents/xcodebuild/xcodebuild2.png)

---

# XCode Command Line Tool 명령어 사용법

## xcodebuild 버전확인

> $ xcodebuild -version
> 
> ![Image Alt xcodebuild3](/assets/img/contents/xcodebuild/xcodebuild3.png)

## xcodebuild sdk목록 확인

> $ xcodebuild -showsdks
> 
> ![Image Alt xcodebuild4](/assets/img/contents/xcodebuild/xcodebuild4.png)

## xcodeproj clean

> ``` xcodebuild -project ${PROJECT_NAME}.xcodeproj -scheme ${TARGET_NAME} -destination 'generic/platform=iOS' clean ```

## xcworkspace clean

> ``` xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -destination 'generic/platform=iOS' clean ```

## xcodeproj build

- project : 빌드할 프로젝트파일 경로
- workspace : 빌드할 workspace 경로
- target : 빌드할 타겟이름
- sdk : iphoneos | iphonesimulator
- destination : iphone 기기명 | Generic
- configuration : Debug | Release

> device 빌드  
> 
> ``` $ xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release build ```

> simulator 빌드  
> 
> ``` $ xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${TARGET_NAME} -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -configuration Debug build ```

## xcworkspace build

> device 빌드  
> 
> ``` $ xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release build ```

> simulator 빌드  
> 
> ``` $ xcodebuild -workspace ${WORKSPACE_NAME}.xcworkspace -scheme ${TARGET_NAME} -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -configuration Debug build ```

## project archive
- archivePath : archive 파일경로 지정
 
> ``` $ xcodebuild -project ${PROJECT_NAME}.xcodeproj -scheme ${TARGET_NAME} -sdk iphoneos -destination 'generic/platform=iOS' -configuration Release -archivePath ./archive/${TARGETNAME}.xcarchive archive ```

## ipa export

> ``` $ xcodebuild -exportArchive -archivePath ./archive/${TARGET_NAME}.xcarchive -exportPath ./build/${TARGET_NAME} -exportOptionsPlist ./exportOptions.plist ``` 

> ![Image Alt xcodebuild5](/assets/img/contents/xcodebuild/xcodebuild5.png)