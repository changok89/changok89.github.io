---
title:  "iOS Developer Mode 활성화 방법"
excerpt: "Developer Mode 활성화 방법"

categories:
  - iOS
tags:
  - [iOS, Developer Mode]

toc: true
toc_sticky : true
toc_label : iOS Developer Mode

date: 2023-01-26
last_modified_at: 2023-01-26
---

# Developer Mode on/off

- 설정 > 개인정보 보호 및 보안 > 개발자 모드 on
- 개발자모드를 키면 아이폰이 재시동된다.
- 재시동이후 한번 더 사용여부를 묻고 비밀번호를 입력하면 개발자모드가 활성화된다.
- watchOS, iPadOS 모두 동일하게 설정에서 활성화시킬수 있다.
- 비활성화하려면 동일하게 설정에서 개발자모드 off

{:.text-align-center}
| ![Image Alt Developer1](/assets/img/contents/developMode/developerMode1.png) | ![Image Alt Developer2](/assets/img/contents/developMode/developerMode2.png) |
| ![Image Alt Developer3](/assets/img/contents/developMode/developerMode3.png) | ![Image Alt Developer4](/assets/img/contents/developMode/developerMode4.png) |
| ![Image Alt Developer5](/assets/img/contents/developMode/developerMode5.png) |

---

# Developer Mode가 생긴 이유

- 사용자기기에 잠재적으로 유해한 소프트웨어를 설치하지 못하도록 보호하기위해서 도입되었다.
- AppStore에서 앱을 설치하거나 TestFlight로 앱을 설치하는거에 영향이 주지않는다.
- 안드로이드폰에 개발자모드와 동일한것 같은데 왜 이제 도입되었는지 의문이다. 안드로이드처럼 빌드번호 7연타를 안해서 다행이라고 해야되나...

---

# Developer Mode에서 가능한 것

- XCode로 개발앱을 빌드하여 설치
- 자동화 Test 도구 실행 (appium, etc...)
- ipa파일을 설치 (Apple Configurator, etc...)

> XCode14에서 연결된 iPhone이 개발자모드가 비활성화되어있을때
  ![Image Alt Developer5](/assets/img/contents/developMode/disabled_developMode.png)

# 참고
[enabling developer mode on a device](https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device){:target="_blank"}


<div id="disqus_thread"></div>
<script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */
    
    var disqus_config = function () {
    this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://changok89-github-io.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>