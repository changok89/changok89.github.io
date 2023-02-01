---
title:  "SwiftUi Keyboard Avoidance"
excerpt: "SwiftUi Keyboard Avoidance"

categories:
  - iOS
tags:
  - [iOS, SwiftUI]

toc: true
toc_sticky : true
toc_label : SwiftUi Keyboard Avoidance

date: 2023-02-01
last_modified_at: 2023-02-01
---

# SwiftUI Keyboard avoidance
- iOS14부터 SwiftUI가 자동으로 keyboard avoidance 기능을 제공하고 있다.
- 덕분에 textfield에 focus시 전체화면이 resize된다.
- webview에 input에 focus시에도 적용된다. scroll이 있는 화면에 input에 focus시 키보드가 올라오면서 webview를 resize하여 scroll이 이상동작한다.
- .ignoresSafeArea(.keyboard, edges: .bottom)를 적용하면 화면이 resize되지않는다.

``` Swift
struct ContentView: View {
    @State private var text: String = ""
    var body: some View {
        VStack {
            Spacer()
            Text("Hello, World")
            TextField("입력하세요!", text: $text)
                .textFieldStyle(RoundedBorderTextFieldStyle())
        }
        .padding()
        .ignoresSafeArea(.keyboard, edges: .bottom)
    }
}
```

# keyboard avoidance 예

![Image Alt keyboardAvoidance](/assets/img/contents/keyboardAvoidance/keyboardAvoidacne.gif)

# keyboard avoidance ignore 예

![Image Alt keyboardAvoidance_ignore](/assets/img/contents/keyboardAvoidance/keyboardAvoidance_ignore.gif)

---

# 참고
[ios-14-swiftui-keyboard-lifts-view-automatically](https://stackoverflow.com/questions/63958912/ios-14-swiftui-keyboard-lifts-view-automatically){:target="_blank"}
