---
title:  "Charles Web Proxy 사용법"
excerpt: "Charles Web Proxy 사용법"

categories:
  - Proxy
tags:
  - [Charles, Proxy]

toc: true
toc_sticky : true
toc_label : Charles Proxy

date: 2023-01-29
last_modified_at: 2023-01-29
---

# Charles Web Proxy 란?
- Charles Web Debugging Proxy는 Java로 작성된 크로스 플랫폼 HTTP 디버깅 프록시 프로그램이다.
- 브라우저나 앱에서 발생하는 http(s)통신을 모니터링할때 사용한다.

# Charles Web Proxy 설치

- window, mac, linux를 지원하며 플랫폼에 맞는 설치프로그램을 다운로드받아서 설치한다. 
- 라이센스를 구매하지않았다면 30일 트라이얼버전으로 사용할 수 있다. 30분 사용제한이 있다.
- [다운로드](https://www.charlesproxy.com/download/latest-release/){:target="_blank"}

# Charles Web Proxy 사용법

## MacOS

- Charles를 실행시킨다. 실행하자마다 Recording 상태라 http통신이 발생하면 좌측바에 표시된다.
![Image Alt charles1](/assets/img/contents/charles/charles1.png)

- Proxy > Proxy Settings 에서 port를 확인한다. 8888이 기본으로 잡혀있다.
![Image Alt charles2](/assets/img/contents/charles/charles3.png)

- Proxy > SSL Proxy Settings에서 SSL Proxying 탭에 Enable Proxying이 체크되어있는지 확인한다.
![Image Alt charles4](/assets/img/contents/charles/charles4.png)

- Help > SSL Proxying > Install Charles Root Certificate를 눌러 인증서 설치
![Image Alt charles4](/assets/img/contents/charles/charles6.png)

- 키체인 접근에 설치된 Charles Proxy CA 인증서를 항상신뢰로 변경한다.
![Image Alt charles4](/assets/img/contents/charles/charles5.png)

## iOS 설정

- iPhone에 "설정(앱)" > Wi-Fi > HTTP 프록시 > 프록시 구성 "수동"으로 변경
    - 수동으로 변경하여 연결할 mac에 서버주소와 charles에 설정된 8888 포트를 입력한다.

- Safari 브라우저에서 https://charlesproxy.com/getssl 에 접속한다.
![Image Alt charles9](/assets/img/contents/charles/charles9.png)

- 설정 > 일반 > VPN 및 기기관리 (프로파일 및 기기관리) > 다운로드한 인증서 설치
![Image Alt charles9](/assets/img/contents/charles/charles7.png)

- 설정 > 일반 > 정보 > 인증서 신뢰 설정 > 루트 인증서 전체 신뢰 활성화 on
![Image Alt charles9](/assets/img/contents/charles/charles8.png)

## 모바일 proxy 연결 

- iOS 설정이 완료되면 mac에 charles를 킨 상태에서 iphone에서 http통신을 발생시킨다.
- mac에 charles에 연결알림창에서 확인하면 그때 부터 iphone에서 발생하는 모든 통신을 mac에서 charles로 확인가능하다.
