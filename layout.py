"""자판기마켓 공통 머리·바닥 (2026-11-17)
build_site.py(홈·자판기 종류·설치 장소·지역 페이지)와 build_guide.py(가이드 글)가 같이 쓴다.
depth: 사이트 루트에서 몇 단계 아래 폴더인지 (0=루트, 1=guide/ places/ regions/)
"""
import html, json

SITE = 'https://mooinstore.kr'
TEL = '010-5577-3067'
TEL_LINK = 'tel:01055773067'
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='10' y='4' width='44' height='56' rx='6' fill='%231f2b38'/%3E"
        "%3Crect x='16' y='10' width='22' height='34' rx='2' fill='%23c8a06a'/%3E%3Crect x='42' y='14' width='6' height='10' rx='1' fill='%23fff'/%3E%3Crect x='16' y='48' width='32' height='6' rx='2' fill='%23fff'/%3E%3C/svg%3E")

# 지역 17곳 (파일명, 짧은 이름, 정식 이름)
REGIONS = [
    ('seoul', '서울', '서울특별시'), ('gyeonggi', '경기', '경기도'), ('incheon', '인천', '인천광역시'),
    ('busan', '부산', '부산광역시'), ('daegu', '대구', '대구광역시'), ('daejeon', '대전', '대전광역시'),
    ('gwangju', '광주', '광주광역시'), ('ulsan', '울산', '울산광역시'), ('sejong', '세종', '세종특별자치시'),
    ('gangwon', '강원', '강원특별자치도'), ('chungbuk', '충북', '충청북도'), ('chungnam', '충남', '충청남도'),
    ('jeonbuk', '전북', '전북특별자치도'), ('jeonnam', '전남', '전라남도'), ('gyeongbuk', '경북', '경상북도'),
    ('gyeongnam', '경남', '경상남도'), ('jeju', '제주', '제주특별자치도'),
]
# 설치 장소 12곳 (파일명, 이름)
PLACES = [
    ('office', '사무실 · 오피스'), ('factory', '공장 · 물류센터'), ('gym', '헬스장 · 필라테스'),
    ('study-cafe', '스터디카페 · 독서실 · 학원'), ('apartment', '아파트 · 오피스텔'), ('hospital', '병원 · 약국'),
    ('camping', '캠핑장 · 펜션 · 낚시터'), ('school', '학교 · 관공서'), ('sauna', '사우나 · 찜질방'),
    ('pc-room', 'PC방 · 노래방 · 당구장'), ('car-wash', '셀프세차장 · 빨래방'), ('hotel', '호텔 · 숙박시설'),
]


def e(s):
    return html.escape(str(s), quote=True)


def up(depth):
    return '../' * depth


def head(title, desc, path, depth=0, ld=None, ogtype='website', extra_css=''):
    """path: 루트 기준 주소 (예: '' / 'machines.html' / 'regions/seoul.html')"""
    r = up(depth)
    url = SITE + '/' + path
    lds = ''
    for x in (ld or []):
        lds += '<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>\n'
    css = f'<link rel="stylesheet" href="{r}site.css">' + (f'\n<link rel="stylesheet" href="{extra_css}">' if extra_css else '')
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="자판기마켓 자판기 가이드" href="{SITE}/rss.xml">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:site_name" content="자판기마켓">
<meta property="og:locale" content="ko_KR">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@500;600;700&display=swap" rel="stylesheet">
{css}
{lds}</head>
<body>
'''


def header(depth=0, active=''):
    r = up(depth)
    items = [('machines', '자판기 종류', f'{r}machines.html'), ('places', '설치 장소', f'{r}places/'),
             ('regions', '지역별 설치', f'{r}regions/'), ('guide', '자판기 가이드', f'{r}guide/')]
    on = ' class="on"'
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, on if k == active else '', t) for k, t, h in items)
    return f'''<header class="top"><div class="wrap hd">
  <a href="{r or './'}" class="logo">자판기마켓<small>무인 자판기 설치 · 구입</small></a>
  <nav id="nav">{nav}</nav>
  <div class="hd-r"><a class="tel" href="{TEL_LINK}">{TEL}</a><a class="btn btn-dark sm" href="{r}#apply">설치 상담</a>
  <button class="menu-btn" aria-label="메뉴" onclick="document.getElementById('nav').classList.toggle('open')">☰</button></div>
</div></header>
'''


def footer(depth=0):
    r = up(depth)
    regs = ' · '.join(f'<a href="{r}regions/{k}.html">{n} 자판기</a>' for k, n, _ in REGIONS)
    pls = ' · '.join(f'<a href="{r}places/{k}.html">{n.split(" · ")[0]} 자판기</a>' for k, n in PLACES)
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <div>
        <div class="logo light">자판기마켓<small>무인 자판기 설치 · 구입</small></div>
        <p>대표번호 <a href="{TEL_LINK}">{TEL}</a></p>
        <p>자판기 구입 · 할부 · 렌탈 · 설치 · 운영 상담 · 전국 17개 시·도</p>
      </div>
      <div class="ft-menu">
        <a href="{r}machines.html">자판기 종류</a><a href="{r}places/">설치 장소</a><a href="{r}regions/">지역별 설치</a><a href="{r}guide/">자판기 가이드</a><a href="{r}#faq">자주 묻는 질문</a><a href="{r}#apply">상담 신청</a>
      </div>
    </div>
    <p class="ft-links"><b>지역별</b> {regs}</p>
    <p class="ft-links"><b>장소별</b> {pls}</p>
    <p class="copy">© 2026 자판기마켓. All rights reserved.</p>
  </div>
</footer>
<div class="bar"><div class="wrap"><span class="msg"><b>우리 공간엔 어떤 자판기가 맞을까?</b> 무료로 상담받아 보세요</span><a class="t" href="{TEL_LINK}">전화</a><a class="btn btn-dark" href="{r}#apply">무료 상담</a></div></div>
<script>document.querySelectorAll('#nav a').forEach(a=>a.addEventListener('click',()=>document.getElementById('nav').classList.remove('open')));</script>
<script src="{r}visit.js" defer></script>
</body>
</html>
'''


def cta(depth=0, src='page'):
    r = up(depth)
    return f'''<section class="cta-band"><div class="wrap cta-in">
  <div><span class="eyebrow light">FREE CONSULTING</span><h2>우리 공간에 맞는 자판기,<br>무료로 상담받으세요</h2>
  <p>설치할 장소를 알려 주시면 기종·품목과 일시불·할부·렌탈 견적을 함께 안내해 드려요. 설치비는 0원이에요.</p></div>
  <div class="btns"><a class="btn btn-light" href="{r}?utm_source={src}#apply">무료 상담 신청 →</a><a class="btn btn-ghost" href="{TEL_LINK}">{TEL} 전화 상담</a></div>
</div></section>
'''


def crumb(depth, items):
    """items: [(이름, 주소 또는 None)]"""
    r = up(depth)
    parts = [f'<a href="{r or "./"}">홈</a>'] + [(f'<a href="{h}">{e(n)}</a>' if h else e(n)) for n, h in items]
    return '<p class="crumb">' + ' <span>›</span> '.join(parts) + '</p>'


def breadcrumb_ld(items):
    """items: [(이름, 절대주소)]"""
    lst = [('홈', SITE + '/')] + items
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(lst)]}
