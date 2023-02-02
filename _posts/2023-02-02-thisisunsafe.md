---
title:  "Chrome NET::ERR_CERT_AUTHORITY_INVALID 해결방법"
excerpt: "Chrome NET::ERR_CERT_AUTHORITY_INVALID"

categories:
  - Browser
tags:
  - [self-signed certificate, Chrome]

toc: true
toc_sticky : true
toc_label : self-signed certificate

date: 2023-02-02
last_modified_at: 2023-02-02
---

# Chrome Self-Sign Certificate 오류 해결방법

- Tomcat에 Self-Sign Certificate로 설정된 SSL서버에 Chrome으로 접속시 만날수있는 오류이다.
- 이전버전에 Chrome은 무시하고 진행할 수 버튼이 있었으나 사라진걸로 보인다.
- 오류화면을 클릭하고(포커스가 크롬으로 잡혀야함) "thisisunsafe"를 입력하면 화면이 redirect되면서 해당페이지에 접속할 수 있다.

![Image Alt chrome_cert_authority_invalid](/assets/img/contents/chrome_cert_authority_invalid/chrome_cert_authority_invalid.png)

# Chrome에 ignore 옵션을 추가하여 실행
- Chrome실행시 --ignore-certificate-errors 옵션을 추가하여 실행할 수 도 있다.

## window

> 1. WIN + R 로 "실행"창을 킨다.
> 2. "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --ignore-certificate-errors 입력 후 Enter
> 3. --ignore-certificate-errors 사용중이라 경로메시지가 표시된다.
> ![Image Alt ignore_certificate_errors](/assets/img/contents/chrome_cert_authority_invalid/ignore_certificate_errors.png)

## macOS

> 1. Spotlight으로 "터미널.app" 실행
> 2. /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ignore-certificate-errors --ignore-urlfetcher-cert-requests &> /dev/null 입력 후 Enter