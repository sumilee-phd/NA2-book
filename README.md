# 네트워크관리사 2급 교재 지원 페이지

공개 주소: https://sumilee-phd.github.io/NA2-book/ · 저장소: https://github.com/sumilee-phd/NA2-book (2026-11-23 첫 공개)

『2027 네트워크관리사 2급』(이수미 지음, 1권 필기·2권 실기)의 교재 지원 페이지입니다. 교재 뒷표지 QR 코드가 이 주소를 가리키므로 쪽 주소를 바꾸지 않습니다.

| 쪽 | 주소 | 내용 |
|---|---|---|
| 홈 | `/` | 표지, 연습 웹앱 바로 가기, 원칙 |
| 연습 웹앱 | `/apps/` | 케이블링 트레이너·윈도우 서버 설정 연습기·단답형 타자 연습기·라우터 타자 연습기, 웹앱별 QR |
| 정오표 | `/errata/` | 1권·2권·연습 웹앱 정오 사항 |
| 자주 묻는 질문 | `/faq/` | 13문항, 답마다 근거 절 번호 |
| 오류 제보 | `/report/` | GitHub 이슈 양식으로 연결 |

## 고치는 법

- 정오 사항: `data/errata.json`의 `items`에 `{page, where, wrong, right, date}`를 추가합니다.
- FAQ: `data/faq.json`. 답은 교재 원고의 사실만 쓰고 `ref`에 근거 절을 적습니다.
- 연습 웹앱: `data/apps.json`.
- 제보 버튼 목적지: `data/config.json`의 `report_url`·`report_label`.

고친 뒤 `python tools/build_site.py`를 실행하고 커밋·푸시합니다.

## 디자인과 글꼴

- 사무자동화산업기사 교재 지원 페이지(https://sumilee-phd.github.io/OA/)와 같은 구조입니다. 홈은 교재 앞표지(연두·먹·원색 알약), 하위 쪽은 내지(버건디 절 번호·꼬리표 상자) 형식입니다.
- 글꼴: Pretendard(SIL OFL 1.1), jsDelivr 고정 버전 v1.3.9. 불러오지 못하면 맑은 고딕으로 표시합니다.

## 인쇄용 QR

`qr/qr_print_300dpi.png`는 교재 인쇄용 QR(오류 정정 M, 300dpi)입니다. 뒷표지 생성기 `90_자산/표지/gen_back_network_v4.py`도 같은 주소로 QR을 그립니다.
