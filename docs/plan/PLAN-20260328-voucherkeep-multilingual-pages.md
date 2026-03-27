# VoucherKeep 다국어 페이지 개선 계획

## Objective

- `voucherkeep_support.html`, `voucherkeep_privacy-policy.html`, `voucherkeep_marketting.html`에 한국어, 영어, 일본어 전환 기능을 추가한다.
- 세 페이지의 시각 언어를 통일하고 모바일/데스크톱 모두에서 읽기 쉬운 레이아웃으로 개선한다.

## Technology Stack

- 정적 HTML5
- 인라인 CSS
- 바닐라 JavaScript
- `localStorage` 기반 언어 설정 유지

## Phases and Tasks

- [✅] 현재 단일 언어 구조를 공통 문서형 레이아웃으로 재구성한다.
- [✅] 상단 언어 스위처와 페이지 내비게이션을 추가한다.
- [✅] 한국어, English, 日本語 콘텐츠를 페이지별로 분리 작성한다.
- [✅] 선택 언어를 저장하고 다른 페이지에서도 유지되는 공통 스크립트를 적용한다.
- [✅] 파이썬 HTML 파서와 브라우저 렌더 확인으로 세 HTML 파일 구조와 언어 전환을 검증한다.

## Dependencies

- 기존 파일명 유지
- 외부 빌드 도구 없이 정적 파일만으로 동작

## Risks

- 세 언어 텍스트 길이가 달라 줄바꿈과 간격이 흔들릴 수 있다.
- 정적 페이지 특성상 번역 문구 변경 시 세 언어를 함께 관리해야 한다.
