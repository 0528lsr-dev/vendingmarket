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


import sys
sys.path.insert(0, ROOT)
import layout  # 공통 머리·바닥 (2026-11-17 새 디자인)


def page_head(title, desc, path, ld=None, ogtype='article'):
    return layout.head(title, desc, path, 1, ld, ogtype, extra_css='guide.css') + layout.header(1, 'guide')


def page_foot():
    return layout.cta(1, 'guide') + layout.footer(1)


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
        # 본문에 <details><summary>질문</summary><p>답</p></details> 가 있으면 FAQPage 구조화 데이터 추가 (AI 검색용, 2026-11-16)
        qa = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', p['body'], re.S)
        if qa:
            strip = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
            ld['@graph'].append({'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': strip(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip(x)}} for q, x in qa]})
        others = [q for q in posts if q is not p]
        related = (others[i:] + others[:i])[:3]
        page = page_head(p['title'] + ' | 자판기마켓', p['description'], f'guide/{p["slug"]}.html', [ld])
        page += f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumb"><a href="../">홈</a> <span>›</span> <a href="./">자판기 가이드</a> <span>›</span> {e(p["tag"])}</p>
  <span class="eyebrow">{e(p["tag"])}</span>
  <h1>{e(p["title"])}</h1>
  <p class="meta">{p["date"]} · 자판기마켓</p>
</div></section>
<section class="art-sec"><div class="wrap">
  <article class="prose">
{p["body"]}
  </article>
  <h2 class="rel-h">함께 보면 좋은 글</h2>
  <div class="ggrid">{''.join(card(q, '') for q in related)}</div>
</div></section>
</main>
'''
        page += page_foot()
        open(os.path.join(out, p['slug'] + '.html'), 'w', encoding='utf-8').write(page)

    # 목록
    desc = '자판기 설치 비용, 기종 고르기, 장소별 설치 팁, 자판기 창업 순서와 신고까지. 자판기마켓이 정리한 자판기 가이드 모음이에요.'
    page = page_head('자판기 가이드 — 설치 비용·기종·창업 정보 | 자판기마켓', desc, 'guide/', None, 'website')
    page += f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumb"><a href="../">홈</a> <span>›</span> 자판기 가이드</p>
  <span class="eyebrow">VENDING GUIDE</span>
  <h1>자판기 가이드</h1>
  <p class="lead">{e(desc)}</p>
</div></section>
<section><div class="wrap"><div class="ggrid" style="margin-top:0">{''.join(card(q, '') for q in posts)}</div></div></section>
</main>
'''
    page += page_foot()
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)

    # 사이트맵
    last = max(p['date'] for p in posts)
    urls = [(SITE + '/', last), (SITE + '/guide/', last)] + [(f'{SITE}/guide/{p["slug"]}.html', p['date']) for p in posts]
    # 홈 외 고정 페이지 (build_site.py 가 만듦): 자판기 종류·설치 장소·지역
    STATIC = '2026-11-17'
    for f in ['machines.html', 'places/index.html', 'regions/index.html'] + sorted(
            os.path.relpath(x, ROOT).replace(os.sep, '/') for x in glob.glob(os.path.join(ROOT, 'places', '*.html')) + glob.glob(os.path.join(ROOT, 'regions', '*.html'))):
        if f.endswith('/index.html') and f not in ('places/index.html', 'regions/index.html'):
            continue
        if os.path.exists(os.path.join(ROOT, f)):
            u = SITE + '/' + (f[:-10] if f.endswith('index.html') else f)
            if all(u != x for x, _ in urls):
                urls.append((u, STATIC))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)

    # RSS (네이버 서치어드바이저 'RSS 제출'용, 2026-11-13)
    import datetime, email.utils
    def rfc(d):
        return email.utils.format_datetime(datetime.datetime.strptime(d, '%Y-%m-%d').replace(hour=9, tzinfo=datetime.timezone(datetime.timedelta(hours=9))))
    items = ''.join(
        f'  <item>\n    <title>{e(p["title"])}</title>\n    <link>{SITE}/guide/{p["slug"]}.html</link>\n'
        f'    <guid>{SITE}/guide/{p["slug"]}.html</guid>\n    <description>{e(p["description"])}</description>\n'
        f'    <category>{e(p["tag"])}</category>\n    <pubDate>{rfc(p["date"])}</pubDate>\n  </item>\n' for p in posts)
    rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
           f'  <title>자판기마켓 자판기 가이드</title>\n  <link>{SITE}/</link>\n'
           '  <description>자판기 구입·렌탈·임대, 설치비, 기종 고르기, 설치 장소, 무인창업 이야기</description>\n'
           f'  <language>ko</language>\n  <lastBuildDate>{rfc(last)}</lastBuildDate>\n' + items + '</channel>\n</rss>\n')
    open(os.path.join(ROOT, 'rss.xml'), 'w', encoding='utf-8').write(rss)

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
