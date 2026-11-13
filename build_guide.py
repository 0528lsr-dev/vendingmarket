"""자판기 가이드 글 만들기 (2026-11-13)
글 원본: guide/_posts/<주소>.html  (머리말 title/description/date/tag, '---' 아래 본문 HTML)
실행: python build_guide.py  →  guide/<주소>.html, guide/index.html, sitemap.xml, 홈(index.html) 가이드 칸을 새로 만든다.
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://mooinstore.kr'
TEL = '010-5577-3067'


def load():
    posts = []
    for p in glob.glob(os.path.join(ROOT, 'guide', '_posts', '*.html')):
        raw = open(p, encoding='utf-8').read()
        head, body = raw.split('\n---\n', 1)
        meta = dict(l.split(':', 1) for l in head.strip().splitlines())
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        meta['slug'] = os.path.basename(p)[:-5]
        meta['body'] = body.strip()
        posts.append(meta)
    posts.sort(key=lambda m: (m['date'], m['slug']), reverse=True)
    return posts


HEAD = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="자판기마켓">
<meta property="og:locale" content="ko_KR">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='10' y='4' width='44' height='56' rx='6' fill='%230f2a4a'/%3E%3Crect x='16' y='10' width='22' height='34' rx='2' fill='%23ffb020'/%3E%3Crect x='42' y='14' width='6' height='10' rx='1' fill='%23fff'/%3E%3Crect x='16' y='48' width='32' height='6' rx='2' fill='%23fff'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{ld}
</head>
<body>
<header><div class="wrap hd">
  <a href="{home}" class="logo"><svg width="28" height="28" viewBox="0 0 64 64" aria-hidden="true"><rect x="10" y="4" width="44" height="56" rx="6" fill="#0f2a4a"/><rect x="16" y="10" width="22" height="34" rx="2" fill="#ffb020"/><rect x="42" y="14" width="6" height="10" rx="1" fill="#fff"/><rect x="16" y="48" width="32" height="6" rx="2" fill="#fff"/></svg>자판기<b>마켓</b></a>
  <nav><a href="{home}">홈</a><a href="{guide}">자판기 가이드</a><a class="cta" href="{home}#apply">무료 상담</a></nav>
</div></header>
'''

FOOT = '''<footer><div class="wrap">
  <p><b>자판기마켓</b> · 자판기 구매 · 렌탈 · 설치 · 운영 상담 · 대표번호 <a href="tel:01055773067">{tel}</a></p>
  <p><a href="{home}">홈</a> · <a href="{guide}">자판기 가이드</a> · <a href="{home}#apply">상담 신청</a></p>
  <p>© 2026 자판기마켓. All rights reserved.</p>
</div></footer>
<div class="bar"><div class="wrap"><span class="msg"><b>우리 공간엔 어떤 자판기가 맞을까?</b> 무료로 상담받아 보세요</span><a class="t" href="tel:01055773067">📞 전화</a><a class="btn" href="{home}#apply">무료 상담</a></div></div>
<script src="{visit}" defer></script>
</body>
</html>
'''


def e(s):
    return html.escape(s, quote=True)


def card(p, prefix):
    return (f'<a class="gcard" href="{prefix}{p["slug"]}.html"><span class="gtag">{e(p["tag"])}</span>'
            f'<h3>{e(p["title"])}</h3><p>{e(p["description"])}</p><span class="more">읽어 보기 →</span></a>')


def build():
    posts = load()
    out = os.path.join(ROOT, 'guide')
    for i, p in enumerate(posts):
        url = f'{SITE}/guide/{p["slug"]}.html'
        ld = {'@context': 'https://schema.org', '@graph': [
            {'@type': 'Article', 'headline': p['title'], 'description': p['description'], 'datePublished': p['date'],
             'dateModified': p['date'], 'mainEntityOfPage': url, 'inLanguage': 'ko',
             'author': {'@type': 'Organization', 'name': '자판기마켓', 'url': SITE + '/'},
             'publisher': {'@type': 'Organization', 'name': '자판기마켓', 'url': SITE + '/'}},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': '홈', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': '자판기 가이드', 'item': SITE + '/guide/'},
                {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]}]}
        others = [q for q in posts if q is not p]
        related = (others[i:] + others[:i])[:3]
        page = HEAD.format(title=e(p['title']) + ' | 자판기마켓', desc=e(p['description']), url=url, ogtype='article',
                           css='guide.css', home='../', guide='./',
                           ld='<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')
        page += f'''<main class="wrap art">
  <p class="crumb"><a href="../">홈</a> › <a href="./">자판기 가이드</a> › {e(p["tag"])}</p>
  <h1>{e(p["title"])}</h1>
  <p class="meta">{e(p["tag"])} · {p["date"]} · 자판기마켓</p>
  <article>
{p["body"]}
  </article>
  <div class="cta-box">
    <h2>우리 공간에 맞는 자판기, 무료로 상담받으세요</h2>
    <p>설치할 장소와 원하는 점을 남겨 주시면 기종·품목·구매/렌탈 견적을 비교해 드려요.</p>
    <div class="btns"><a class="btn" href="../?utm_source=guide#apply">무료 상담 신청 →</a><a class="btn line" href="tel:01055773067">📞 {TEL}</a></div>
  </div>
  <h2 class="rel-h">함께 보면 좋은 글</h2>
  <div class="ggrid">{''.join(card(q, '') for q in related)}</div>
</main>
'''
        page += FOOT.format(tel=TEL, home='../', guide='./', visit='../visit.js')
        open(os.path.join(out, p['slug'] + '.html'), 'w', encoding='utf-8').write(page)

    # 목록
    desc = '자판기 설치 비용, 기종 고르기, 장소별 설치 팁, 자판기 창업 순서와 신고까지. 자판기마켓이 정리한 자판기 가이드 모음이에요.'
    page = HEAD.format(title='자판기 가이드 — 설치 비용·기종·창업 정보 | 자판기마켓', desc=desc, url=SITE + '/guide/', ogtype='website',
                       css='guide.css', home='../', guide='./', ld='')
    page += f'''<main class="wrap art">
  <p class="crumb"><a href="../">홈</a> › 자판기 가이드</p>
  <h1>자판기 가이드</h1>
  <p class="meta">{e(desc)}</p>
  <div class="ggrid">{''.join(card(q, '') for q in posts)}</div>
</main>
'''
    page += FOOT.format(tel=TEL, home='../', guide='./', visit='../visit.js')
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)

    # 사이트맵
    last = max(p['date'] for p in posts)
    urls = [(SITE + '/', last), (SITE + '/guide/', last)] + [(f'{SITE}/guide/{p["slug"]}.html', p['date']) for p in posts]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)

    # 홈 가이드 칸 (최근 6편)
    idx = os.path.join(ROOT, 'index.html')
    s = open(idx, encoding='utf-8').read()
    block = '<!--GUIDE-START-->\n    <div class="ggrid">' + ''.join(card(q, 'guide/') for q in posts[:6]) + '</div>\n    <!--GUIDE-END-->'
    s, n = re.subn(r'<!--GUIDE-START-->.*?<!--GUIDE-END-->', lambda m: block, s, flags=re.S)
    if n != 1:
        raise SystemExit('index.html 에 GUIDE 표시가 없음')
    open(idx, 'w', encoding='utf-8').write(s)
    print('가이드', len(posts), '편 만듦')


if __name__ == '__main__':
    build()
