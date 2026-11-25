# -*- coding: utf-8 -*-
"""네트워크관리사 2급 교재 지원 페이지 생성기(2026-11-23).

사용자 지시(2026-11-23): 「교재 지원 페이지 신설」(뒷표지 QR 목적지).
사무자동화 교재 지원 페이지(13_사무자동화산업기사/90_자산/지원페이지, sumilee-phd.github.io/OA)와 같은 구조이고,
실습 파일·영상 쪽은 없다(이 책은 실습 파일이 없고 영상은 미정). 색은 앞표지 v4(A 연두)와 같다.

python tools/build_site.py
  1) data/config·apps·errata·faq.json 으로 5개 쪽을 만든다.
  2) 표지 축소판, 홈 QR, 인쇄용 QR(qr/qr_print_300dpi.png), 연습 웹앱별 QR을 assets/ 에 둔다.
쪽 주소는 뒷표지 QR 이 가리키므로 바꾸지 않는다: / · /apps/ · /errata/ · /faq/ · /report/
"""
import html
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET = os.path.dirname(SITE)                                   # 90_자산
COVERS = os.path.join(ASSET, "표지", "v4_권별_20261118")

CFG = json.load(io.open(os.path.join(SITE, "data", "config.json"), encoding="utf-8"))
APPS = json.load(io.open(os.path.join(SITE, "data", "apps.json"), encoding="utf-8"))["items"]
BASE = CFG["base_url"].rstrip("/") + "/"
E = html.escape
NAV = [("", "홈"), ("apps/", "연습 웹앱"), ("errata/", "정오표"), ("faq/", "자주 묻는 질문"), ("report/", "오류 제보")]
FONT = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" crossorigin>'
TITLE = "네트워크관리사 2급"


def page(rel, title, body, desc):
    up = "../" * rel.count("/")
    nav = "".join(f'<a href="{up}{href}"{" aria-current=\"page\"" if href == rel else ""}>{E(name)}</a>' for href, name in NAV)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{FONT}
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}">{TITLE} <span class="tag">교재 지원</span></a>
<nav class="nav" aria-label="교재 지원 메뉴">{nav}</nav>
</div></header>
{body}
<footer class="foot"><div class="wrap">
<img src="{up}assets/qr_home.png" alt="교재 지원 페이지 QR 코드">
<div><b>『2027 네트워크관리사 2급』 교재 지원 페이지</b><br>이수미 지음 · 1권 필기 · 2권 실기<br>
주소 <span class="num">{E(BASE)}</span><br>
시험 문항 복원 자료는 제공하지 않습니다.</div>
</div></footer>
</body>
</html>
"""


def band(chip, title, right=""):
    r = f"<p>{E(right)}</p>" if right else ""
    return f'<div class="band"><span class="chip">{E(chip)}</span><h1>{E(title)}</h1>{r}</div>'


def para(text):
    """faq 답 문자열: '- ' 로 시작하는 줄 묶음은 목록, 나머지는 문단."""
    lines = text.split("\n")
    if all(l.startswith("- ") for l in lines):
        return "<ul>" + "".join(f"<li>{E(l[2:])}</li>" for l in lines) + "</ul>"
    return "<p>" + E(text) + "</p>"


# ---------------------------------------------------------------- 연습 웹앱
def apps_page():
    cards = []
    for a in APPS:
        cards.append(f'''<div class="app {E(a["color"])}">
<div class="app-h"><span class="k">실기 {E(a["item"])}</span><h3>{E(a["name"])}</h3></div>
<div class="app-b">
<img src="../assets/qr_app_{E(a["id"])}.png" alt="{E(a["name"])} QR 코드" width="112" height="112">
<dl><dt>구성</dt><dd>{E(a["parts"])}</dd><dt>교재</dt><dd>{E(a["book"])}</dd>
<dt>주소</dt><dd><a href="{E(a["url"])}">{E(a["url"].replace("https://", "").rstrip("/"))}</a></dd></dl>
</div></div>''')
    body = f"""<main><div class="wrap">
{band("APPS", "연습 웹앱", "실기 문항 번호별 4종")}
<div class="page-intro">회원 가입·설치 없음 · 웹 브라우저 · 무료</div>
<section class="sec">
<div class="sec-h"><span class="no">01</span><h2>웹앱 4종</h2><span class="sub">교재 QR과 같은 주소</span></div>
<div class="apps">{"".join(cards)}</div>
</section>
<section class="sec">
<div class="sec-h"><span class="no">02</span><h2>사용 기준</h2></div>
<div class="box key"><span class="lab">PC 화면</span><p>윈도우 서버 설정 연습기는 PC 화면(가로 1000px 이상) 기준입니다.</p></div>
<div class="box key"><span class="lab">라우터 해석 기준</span><p>시험 대비 연습은 「시험 프로그램 방식」으로 합니다. 「Packet Tracer 방식」과의 차이는 2권 18.3절에 있습니다.</p></div>
<div class="box warn"><span class="lab">채점</span><p>연습 웹앱의 채점은 이 책의 연습 기준입니다. 협회는 채점 기준을 공개하지 않습니다. 시험 전 마지막 연습은 협회 연습 프로그램으로 합니다(2권 13.3절).</p></div>
</section>
</div></main>"""
    return page("apps/", f"연습 웹앱 · {TITLE} 교재 지원", body, "케이블링 트레이너, 윈도우 서버 설정 연습기, 단답형 타자 연습기, 라우터 타자 연습기")


# ---------------------------------------------------------------- 정오표
def errata_page():
    data = json.load(io.open(os.path.join(SITE, "data", "errata.json"), encoding="utf-8"))
    secs = []
    for i, vol in enumerate(data["volumes"], 1):
        items = vol.get("items", [])
        if items:
            trs = "".join(f'<tr><td class="num">{E(it["page"])}</td><td>{E(it["where"])}</td><td>{E(it["wrong"])}</td><td>{E(it["right"])}</td><td class="num">{E(it["date"])}</td></tr>' for it in items)
            inner = f'<div class="tbl-wrap"><table><thead><tr><th>쪽</th><th>위치</th><th>잘못</th><th>바름</th><th>반영일</th></tr></thead><tbody>{trs}</tbody></table></div>'
        else:
            inner = '<div class="empty">등록된 정오 사항 없음</div>'
        secs.append(f'<section class="sec"><div class="sec-h"><span class="no">{i:02d}</span><h2>{E(vol["title"])}</h2><span class="sub">{E(vol["edition"])}</span></div>{inner}</section>')
    body = f"""<main><div class="wrap">
{band("ERRATA", "정오표", "기준일 " + data["updated"])}
<div class="page-intro">교재 본문과 연습 웹앱 4종의 정오 사항 · 판·쇄별 · 반영일 표기. 오류 제보는 <a href="../report/">오류 제보</a> 쪽으로 받습니다.</div>
{"".join(secs)}
</div></main>"""
    return page("errata/", f"정오표 · {TITLE} 교재 지원", body, "1권 필기·2권 실기·연습 웹앱 정오표")


# ---------------------------------------------------------------- FAQ
def faq_page():
    data = json.load(io.open(os.path.join(SITE, "data", "faq.json"), encoding="utf-8"))
    out, n = [], 0
    for ci, cat in enumerate(data["categories"], 1):
        qs = []
        for it in cat["items"]:
            n += 1
            ans = "".join(para(a) for a in it["a"])
            qs.append(f'<details class="q" id="q{n}"><summary><span class="qn">Q{n}</span><span>{E(it["q"])}</span></summary>'
                      f'<div class="a">{ans}<span class="ref">근거 {E(it["ref"])}</span></div></details>')
        out.append(f'<section class="sec faq-cat"><div class="sec-h"><span class="no">{ci:02d}</span><h2>{E(cat["title"])}</h2><span class="sub">{len(cat["items"])}문항</span></div>{"".join(qs)}</section>')
    body = f"""<main><div class="wrap">
{band("FAQ", "자주 묻는 질문", f"{n}문항")}
<div class="page-intro">시험 형식 · 응시 방식과 출제기준 · 실기 연습. 답마다 근거 절 번호 표기. 협회 공고가 바뀌면 공고를 따릅니다.</div>
{"".join(out)}
</div></main>"""
    return page("faq/", f"자주 묻는 질문 · {TITLE} 교재 지원", body, "네트워크관리사 2급 시험 형식·응시 방식·출제기준·실기 연습 FAQ"), n


# ---------------------------------------------------------------- 오류 제보
def report_page():
    url = CFG["report_url"]
    body = f"""<main><div class="wrap">
{band("REPORT", "오류 제보", "교재 · 연습 웹앱 4종")}
<div class="page-intro">교재 본문과 연습 웹앱 4종의 오류 제보 · 반영 내용은 <a href="../errata/">정오표</a>에 게시합니다.</div>
<section class="sec">
<div class="sec-h"><span class="no">01</span><h2>제보 양식</h2></div>
<p><a class="btn" href="{E(url)}" rel="noopener">오류 제보하기 <span class="meta">{E(CFG["report_label"])}</span></a></p>
<div class="box key"><span class="lab">적을 항목</span><ol>
<li>권(1권 필기·2권 실기) 또는 웹앱 이름</li>
<li>쪽 번호와 위치(절 번호, 표·그림 번호, 문항 번호, 단계 번호)</li>
<li>잘못된 내용과 바른 내용, 근거</li>
</ol></div>
<div class="box warn"><span class="lab">주의</span><ul>
<li>이름·연락처·수험번호 같은 개인정보는 적지 않습니다.</li>
<li>시험 문항의 원문·보기를 옮겨 적지 않습니다.</li>
<li>다른 출판사 교재의 쪽을 촬영해 올리지 않습니다.</li>
</ul></div>
</section>
</div></main>"""
    return page("report/", f"오류 제보 · {TITLE} 교재 지원", body, "교재·연습 웹앱 오류 제보")


# ---------------------------------------------------------------- 홈
def home_page(n_faq):
    pills = "".join(f'<a class="pill {E(a["color"])}" href="{E(a["url"])}"><span class="k">{E(a["item"])}</span>{E(a["name"])}</a>' for a in APPS)
    body = f"""<section class="hero"><div class="wrap">
<div>
<p class="eyebrow">Network Administrator Level 2 · 2027</p>
<h1>{TITLE}</h1>
<span class="vol">교재 지원</span><br>
<span class="slogan"><span>1권 필기 · 2권 실기 · Windows Server 2022 출제기준</span></span>
<div class="pills">{pills}</div>
</div>
<div class="covers">
<img src="assets/cover_vol1.png" alt="2027 네트워크관리사 2급 1권 필기 앞표지" width="420" height="588">
<img src="assets/cover_vol2.png" alt="2027 네트워크관리사 2급 2권 실기 앞표지" width="420" height="588">
</div>
</div></section>
<main><div class="wrap">
<section class="sec">
<div class="sec-h"><span class="no">01</span><h2>바로 가기</h2></div>
<div class="cards four">
<a class="card" href="apps/"><span class="chip">APPS</span><h3>연습 웹앱 4종</h3><p>케이블 · 윈도우 서버 · 단답 · 라우터, 실기 문항 번호별 연습</p></a>
<a class="card" href="errata/"><span class="chip">ERRATA</span><h3>정오표</h3><p>1권 · 2권 · 연습 웹앱의 정오 사항</p></a>
<a class="card" href="faq/"><span class="chip">FAQ</span><h3>자주 묻는 질문 {n_faq}문항</h3><p>합격 기준, 실기 시간 배분, 라우터 저장, 정기검정과 단체검정</p></a>
<a class="card" href="report/"><span class="chip">REPORT</span><h3>오류 제보</h3><p>쪽 번호 · 위치 · 바른 내용</p></a>
</div>
</section>
<section class="sec">
<div class="sec-h"><span class="no">02</span><h2>이 페이지의 원칙</h2></div>
<div class="box warn"><span class="lab">제공하지 않는 것</span><p>시험 문항을 복원한 자료는 제공하지 않습니다.</p></div>
<div class="box key"><span class="lab">주소</span><p>이 페이지의 주소 <span class="num">{E(BASE)}</span>는 교재 뒷표지 QR의 고정 주소입니다. 하위 쪽 주소(/apps/, /errata/, /faq/, /report/)도 바꾸지 않습니다.</p></div>
</section>
</div></main>"""
    return page("", f"{TITLE} 교재 지원", body, "2027 네트워크관리사 2급 1권 필기·2권 실기 교재 지원: 연습 웹앱 4종, 정오표, 자주 묻는 질문, 오류 제보")


def qr_img(data, box, border):
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def assets():
    from PIL import Image
    a = os.path.join(SITE, "assets")
    os.makedirs(a, exist_ok=True)
    for vol, src in ((1, "네트워크관리사2급_1권필기_앞표지_preview.png"), (2, "네트워크관리사2급_2권실기_앞표지_preview.png")):
        im = Image.open(os.path.join(COVERS, src)).convert("RGB")
        im = im.resize((420, round(im.height * 420 / im.width)), Image.Resampling.LANCZOS)
        im.save(os.path.join(a, f"cover_vol{vol}.png"), optimize=True)
    qr_img(BASE, 6, 2).save(os.path.join(a, "qr_home.png"))
    os.makedirs(os.path.join(SITE, "qr"), exist_ok=True)
    qr_img(BASE, 20, 4).save(os.path.join(SITE, "qr", "qr_print_300dpi.png"), dpi=(300, 300))
    for app in APPS:
        qr_img(app["url"], 6, 2).save(os.path.join(a, f"qr_app_{app['id']}.png"))
    print("표지 축소판·QR 생성:", BASE)


def main():
    assets()
    faq_html, n_faq = faq_page()
    pages = {"": home_page(n_faq), "apps/": apps_page(), "errata/": errata_page(), "faq/": faq_html, "report/": report_page()}
    for rel, text in pages.items():
        d = os.path.join(SITE, rel)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(text)
    print("쪽", len(pages), "개 생성 · FAQ", n_faq, "문항")


if __name__ == "__main__":
    main()
