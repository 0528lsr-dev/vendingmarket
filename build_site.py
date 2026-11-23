"""자판기마켓 사이트 페이지 만들기 (2026-11-17)
실행: python build_site.py
 → index.html(홈), machines.html, places/(12곳), regions/(17곳)을 만들고, 마지막에 build_guide.py 로 가이드·사이트맵·RSS까지 갱신.
내용은 site_data.py, 머리·바닥은 layout.py, 디자인은 site.css.
※ 매일 가이드 루틴은 build_guide.py 만 실행한다(홈의 GUIDE 칸만 바뀜).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import (SITE, TEL, TEL_LINK, REGIONS, PLACES, e, head, header, footer, cta, crumb, breadcrumb_ld)
from site_data import REGION_INFO, PLACE_INFO, MACHINES, MIX

ROOT = os.path.dirname(os.path.abspath(__file__))
BIZ = {'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': '자판기마켓', 'url': SITE + '/',
       'description': '자판기·무인키오스크 구입, 할부, 렌탈, 설치, 운영 상담', 'telephone': '+82-10-5577-3067',
       'areaServed': 'KR', 'priceRange': '상담 후 견적', 'image': SITE + '/img/og.jpg'}

PROCESS = [('상담 접수', '전화나 신청서로 설치할 곳과 원하는 점을 알려 주세요. 상담은 무료예요.'),
           ('현장 확인 · 자리 분석', '공간 크기, 전기 위치, 사람 흐름을 보고 맞는 기종인지 판단해요.'),
           ('기종 · 품목 · 견적 제안', '기종과 첫 품목 구성, 일시불·할부·렌탈 견적을 함께 안내해요.'),
           ('설치 · 세팅', '반입·설치, 카드 결제 등록, 상품 진열까지 마치고 바로 팔 수 있게 넘겨드려요.'),
           ('운영 · 사후 관리', '매출·재고 확인 방법을 알려 드리고, 고장 대응·이전 설치까지 이어서 도와드려요.')]


def w(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)


def steps_html():
    return '<ol class="steps">' + ''.join(
        f'<li><span class="n">{i:02d}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(PROCESS, 1)) + '</ol>'


def plans_html():
    return '''<div class="cards c3">
      <div class="plan"><h3>일시불 구입</h3><p class="for">한 번에 정리하고 깔끔하게 시작하고 싶다면</p>
        <dl><dt>내는 방법</dt><dd>기계 값을 한 번에</dd><dt>매달 비용</dt><dd>없음</dd><dt>소유</dt><dd>바로 내 자판기</dd></dl></div>
      <div class="plan hot"><span class="badge">가장 많이 선택</span><h3>할부 구입</h3><p class="for">목돈 없이 매달 나눠서 시작하고 싶다면</p>
        <dl><dt>내는 방법</dt><dd>기계 값을 매달 나눠서</dd><dt>매달 비용</dt><dd>할부금 (기간에 따라 다름)</dd><dt>소유</dt><dd>할부가 끝나면 내 자판기</dd></dl></div>
      <div class="plan"><h3>렌탈</h3><p class="for">정해진 금액으로 매달 이용하고 싶다면</p>
        <dl><dt>내는 방법</dt><dd>매달 렌탈료</dd><dt>매달 비용</dt><dd>렌탈료 (기간에 따라 다름)</dd><dt>계약</dt><dd>기간·조건은 상담 때 안내</dd></dl></div>
    </div>
    <p class="note">※ 어떤 방법이든 설치비는 0원이에요. 기종·대수·기간에 따라 금액이 달라져서 정확한 견적은 상담 때 안내해 드립니다.</p>'''


# ───────────── 홈
FAQ = [
 ('자판기 한 대 놓는 데 자리가 얼마나 필요한가요?', '기종마다 달라요. 일반적인 스탠드형은 폭 1m 안팎의 자리와 콘센트 하나면 설치할 수 있어요. 들어가는 길(문 폭·엘리베이터)도 함께 확인해 드려요.'),
 ('설치비가 따로 드나요?', '설치비는 무료예요. 기계는 일시불·할부·렌탈 중에 고르시면 되고, 금액은 기종과 대수, 설치 조건에 따라 달라져서 현장을 확인한 뒤 견적을 드려요. 상담과 자리 분석도 무료입니다.'),
 ('상품은 누가 채워 넣나요?', '직접 채우셔도 되고, 상품 보충까지 맡기는 위탁운영도 가능해요. 처음 채울 품목 구성과 가격은 함께 정해 드려요.'),
 ('카드·간편결제가 되나요?', '네. 신용·체크카드와 삼성페이·카카오페이·네이버페이 같은 간편결제, QR 결제를 기종에 맞춰 연결해 드려요. 매출은 휴대폰으로 확인할 수 있어요.'),
 ('고장이 나면 어떻게 하나요?', '전화로 접수해 주시면 증상을 확인하고 수리를 연결해 드려요. 설치 후에도 고장 대응과 기기 이전 설치를 도와드려요.'),
 ('자판기 사업에 허가나 신고가 필요한가요?', '파는 상품에 따라 다릅니다. 포장된 음료·과자만 판다면 비교적 간단하고, 커피처럼 그 자리에서 만드는 자판기는 영업 신고가 필요할 수 있어요. 상담 때 필요한 절차를 안내해 드려요.'),
 ('전국 어디든 설치되나요?', '네, 전국 17개 시·도 어디든 방문 상담 후 설치해요. 섬이나 일부 산간 지역은 일정이 조금 더 걸릴 수 있어요.'),
 ('쓰던 자판기가 있는데 바꿀 수 있나요?', '네. 현금만 되던 오래된 자판기를 카드 되는 기종으로 바꾸거나, 다른 자리로 옮겨 설치하거나, 한 대 더 늘리는 것도 상담해 드려요.'),
 ('어디에 놓으면 잘 팔리나요?', '사람이 오래 머물고 주변에 편의점이 먼 곳일수록 좋아요. 자리를 보고 잘 안 될 것 같으면 설치 전에 솔직하게 먼저 말씀드려요.'),
]

FORM_SCRIPT = r'''<script>
  // 기종 고르기 버튼 → 신청서 관심 기종 미리 고르기
  document.querySelectorAll('[data-machine]').forEach(a => a.addEventListener('click', () => {
    var s = document.querySelector('#applyForm select[name="machine"]'); if (s) s.value = a.dataset.machine;
  }));
  // 신청 폼 → 티쳐포유 구글 시트(같은 Apps Script, "자판기마켓" 탭) + 메일 알림
  // 티쳐포유 스크립트는 영문 키(name·phone·memo 등)만 읽으므로 한글 키와 같이 보낸다
  var SHEET_ENDPOINT = 'https://script.google.com/macros/s/AKfycbx7cFmG03i-dpfj7IWynETu5Z2af_dla1qaA-Kt8KbFF28H-4Re684VpmO7vBSeaILU/exec';
  var SITE_NAME = '자판기마켓';
  document.getElementById('applyForm').addEventListener('submit', async e => {
    e.preventDefault();
    var f = e.target, v = n => (f.elements[n].value || '').trim();
    var memo = '[' + SITE_NAME + '] 지역: ' + v('region') + ' / 장소: ' + v('place') + ' / 기종: ' + v('machine') + ' / 방식: ' + v('type') + (v('memo') ? ' / ' + v('memo') : '');
    var payload = {
      sheet: '자판기마켓', _form: SITE_NAME, _time: new Date().toLocaleString('ko-KR'),
      사이트: SITE_NAME, 이름: v('name'), 연락처: v('phone'), 설치지역: v('region'), 설치장소: v('place'),
      관심기종: v('machine'), 원하는방식: v('type'), 문의내용: v('memo'), 신청페이지: location.href,
      name: '[' + SITE_NAME + '] ' + v('name'), phone: v('phone'), subject: v('machine'), grade: v('place'), memo: memo
    };
    var btn = f.querySelector('button[type="submit"]');
    btn.disabled = true; btn.textContent = '접수 중…';
    try {
      await fetch(SHEET_ENDPOINT, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }, body: new URLSearchParams(payload).toString() });
    } catch (_) {}
    document.getElementById('done').style.display = 'block';
    btn.textContent = '신청 완료 ✓';
    f.reset();
  });
</script>
'''


def home():
    old = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read() if os.path.exists(os.path.join(ROOT, 'index.html')) else ''
    import re
    m = re.search(r'<!--GUIDE-START-->.*?<!--GUIDE-END-->', old, re.S)
    guide_block = m.group(0) if m else '<!--GUIDE-START--><!--GUIDE-END-->'
    verify = ('<meta name="naver-site-verification" content="ad0c32b153affffc4c2415fab25f0c68dd69ee64" />\n'
              '<meta name="google-site-verification" content="cUo4ZzAgD52azNM2htVvWJ59VUhHQ5ghyeZK6kNiSxI" />\n')
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    h = head('자판기 설치·구입 상담 | 자판기마켓 — 설치비 0원, 전국 17개 시·도',
             '음료·커피·스낵·아이스크림 자판기와 무인키오스크 설치·구입 상담. 설치비 0원, 일시불·할부·렌탈, 카드·간편결제, 전국 17개 시·도 방문 설치. 상담 010-5577-3067',
             '', 0, [BIZ, faq_ld])
    h = h.replace('<link rel="canonical"', verify + '<meta name="keywords" content="자판기, 자판기 설치, 자판기 구매, 자판기 할부, 자판기 렌탈, 음료자판기, 커피자판기, 스낵자판기, 아이스크림자판기, 무인자판기, 스마트자판기, 무인키오스크, 무인창업">\n<link rel="canonical"', 1)
    places6 = ['office', 'factory', 'gym', 'study-cafe', 'apartment', 'hotel']
    pn = dict(PLACES)
    place_cards = ''.join(
        f'<a class="card" href="places/{k}.html"><span class="no">{i:02d}</span><h3>{pn[k]}</h3><p>{PLACE_INFO[k]["users"][0]}</p><span class="go">자세히 보기 →</span></a>'
        for i, k in enumerate(places6, 1))
    chips = ''.join(f'<a href="regions/{k}.html">{n}</a>' for k, n, _ in REGIONS)
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    place_opts = ''.join(f'<option>{n.replace(" · ", "·")}</option>' for _, n in PLACES) + '<option>무인매장 창업</option><option>기타</option>'
    mach_opts = '<option>아직 모르겠어요</option>' + ''.join(f'<option>{t}</option>' for _, t, _, _ in MACHINES)
    body = f'''{header(0)}
<main id="top">
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">NATIONWIDE INSTALLATION</span>
    <h1>남는 자리 한 칸이,<br><em>24시간 매장</em>이 됩니다.</h1>
    <p class="sub">음료·커피, 스낵, 아이스크림·냉동, 생활용품, 복합 자판기부터 무인키오스크까지. 설치할 자리를 먼저 보고 잘 팔릴 기종과 품목을 골라 전국에 설치해 드립니다. 설치비는 무료이고, 일시불·할부·렌탈로 편하게 시작할 수 있어요.</p>
    <div class="btns"><a class="btn btn-dark" href="#apply">무료 설치 상담 →</a><a class="btn btn-line" href="machines.html">자판기 종류 보기</a></div>
    <div class="stats">
      <div><b>24시간</b><span>무인 운영</span></div><div><b>설치비 0원</b><span>일시불·할부·렌탈</span></div>
      <div><b>전국 17개</b><span>시·도 설치</span></div><div><b>간편결제</b><span>카드·페이·QR</span></div>
    </div>
  </div>
  <div class="stage"><img src="img/product.webp" width="483" height="758" alt="키오스크 결합형 스마트 자판기" fetchpriority="high"><div class="tag">24시간 · 365일<b>무인으로 팔아요</b></div></div>
</div></section>

<section class="ivory" id="why"><div class="wrap">
  <span class="eyebrow">WHY UNMANNED</span>
  <h2>직원 없이도 파는 가게가<br>하나 더 생깁니다</h2>
  <p class="lead">자판기가 하는 일은 단순해요. 문 닫은 시간에도 팔고, 사람 손을 덜 쓰고, 매출은 휴대폰으로 확인돼요.</p>
  <div class="cards c3">
    <div class="card"><span class="no">01</span><h3>24시간 무인 운영</h3><p>영업시간 제약이 없어요. 매장이 문을 닫은 밤·새벽·주말에도 자판기는 계속 팔아요.</p></div>
    <div class="card"><span class="no">02</span><h3>인건비 없는 소자본 시작</h3><p>추가 인력 없이 운영돼요. 할부를 이용하면 초기 부담을 매달 나눠서 시작할 수 있어요.</p></div>
    <div class="card"><span class="no">03</span><h3>카드·간편결제 전부 지원</h3><p>신용·체크카드는 물론 삼성페이·카카오페이·네이버페이·QR까지 한 대로 받아요.</p></div>
    <div class="card"><span class="no">04</span><h3>매출·재고 원격 관리</h3><p>어떤 품목이 잘 나가는지, 무엇을 채워야 하는지 현장에 가지 않고 확인해요.</p></div>
    <div class="card"><span class="no">05</span><h3>자투리 공간 활용</h3><p>복도, 휴게실, 엘리베이터 홀처럼 비어 있던 한 평이 그대로 매대가 돼요.</p></div>
    <a class="card dark" href="#apply"><span class="no">NEXT</span><h3>우리 자리엔 뭐가 맞을까요?</h3><p>자리와 유동 인원을 먼저 보고 기종·품목을 제안해 드려요. 상담은 무료예요.</p><span class="go">무료 상담 신청 →</span></a>
  </div>
</div></section>

<section id="places"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">PLACEMENT</span><h2>이런 장소에 많이 설치합니다</h2>
  <p class="lead">자리마다 잘 나가는 품목이 달라요. 장소를 누르면 맞는 기종·품목·놓을 위치를 자세히 볼 수 있어요.</p></div>
  <a class="more-link" href="places/">설치 장소 12곳 전체 보기 →</a></div>
  <div class="cards c3">{place_cards}</div>
</div></section>

<section class="ivory" id="cases"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">RECENT</span><h2>설치된 모습</h2></div></div>
  <div class="photos">
    <figure><img src="img/case-cafe-sokcho.jpg" loading="lazy" width="602" height="602" alt="카페에 나란히 설치된 스마트 자판기"><figcaption>카페 · 강원 속초</figcaption></figure>
    <figure><img src="img/case-hotel-jeju.jpg" loading="lazy" width="602" height="602" alt="호텔 로비에 설치된 스마트 자판기"><figcaption>호텔 로비 · 제주</figcaption></figure>
    <figure><img src="img/case-school.jpg" loading="lazy" width="602" height="602" alt="학교 휴게 공간에 설치된 스마트 자판기"><figcaption>학교 휴게 공간</figcaption></figure>
    <figure><img src="img/case-cafe.jpg" loading="lazy" width="602" height="602" alt="커피 매장 입구에 설치된 스마트 자판기"><figcaption>커피 매장 입구</figcaption></figure>
  </div>
</div></section>

<section id="plans"><div class="wrap">
  <span class="eyebrow">HOW TO START</span>
  <h2>일시불·할부·렌탈,<br>편한 방법으로 시작하세요</h2>
  <p class="lead">어떤 방법이든 설치비는 무료예요. 예산과 운영 계획을 들어 보고 맞는 방법을 함께 정해 드려요.</p>
  {plans_html()}
</div></section>

<section class="ivory" id="regions"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">FIND YOUR AREA</span><h2>우리 지역, 어디까지 설치되나요</h2>
  <p class="lead">시·도를 누르면 그 지역에서 많이 찾는 설치 장소와 시·군·구를 볼 수 있어요. 전국 어디든 방문 상담 후 설치합니다.</p></div>
  <a class="more-link" href="regions/">지역별 설치 전체 보기 →</a></div>
  <div class="chips">{chips}</div>
</div></section>

<section id="process"><div class="wrap">
  <div style="max-width:880px;margin:0 auto"><span class="eyebrow">PROCESS</span><h2>설치는 이렇게 진행됩니다</h2></div>
  {steps_html()}
</div></section>

<section class="ivory" id="guide"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">VENDING GUIDE</span><h2>시작 전에 알아 두면 좋은 이야기</h2></div>
  <a class="more-link" href="guide/">자판기 가이드 전체 보기 →</a></div>
    {guide_block}
</div></section>

<section id="faq"><div class="wrap">
  <div style="max-width:880px;margin:0 auto"><span class="eyebrow">FAQ</span><h2>자주 묻는 질문</h2></div>
  <div class="faq-list">{faq}</div>
</div></section>

<section class="apply" id="apply"><div class="wrap apply-grid">
  <div>
    <span class="eyebrow light">FREE CONSULTING</span>
    <h2>내 공간에 맞는 자판기,<br>무료로 상담받으세요</h2>
    <p class="lead">신청서를 남겨 주시면 확인하는 대로 바로 연락드려요. 급하시면 전화 주세요.</p>
    <a class="big-tel" href="{TEL_LINK}">{TEL}</a>
    <ul class="points"><li>상담·견적·자리 분석 무료</li><li>설치비 0원 · 일시불·할부·렌탈 견적 비교</li><li>설치 장소에 맞는 기종·품목 추천</li></ul>
  </div>
  <form id="applyForm">
    <div class="row">
      <div><label>이름 <i>*</i></label><input name="name" required placeholder="홍길동"></div>
      <div><label>연락처 <i>*</i></label><input name="phone" type="tel" required placeholder="010-0000-0000"></div>
    </div>
    <div class="row">
      <div><label>설치 지역 <i>*</i></label><input name="region" required placeholder="예: 경기 수원시"></div>
      <div><label>설치 장소</label><select name="place">{place_opts}</select></div>
    </div>
    <div class="row">
      <div><label>관심 기종</label><select name="machine">{mach_opts}</select></div>
      <div><label>원하는 방식</label><select name="type"><option>상담 후 결정</option><option>일시불 구입</option><option>할부 구입</option><option>렌탈</option></select></div>
    </div>
    <label>문의 내용</label>
    <textarea name="memo" placeholder="예: 직원 30명 사무실 휴게실에 음료 자판기 1대 놓고 싶어요"></textarea>
    <label class="agree"><input type="checkbox" required> 개인정보(이름·연락처·지역)를 상담 목적으로 수집·이용하는 데 동의합니다.</label>
    <button class="btn btn-dark" type="submit">무료 상담 신청하기 →</button>
    <div id="done">신청이 접수됐어요! 곧 연락드릴게요.</div>
    <p class="safe">남겨 주신 정보는 상담에만 쓰고, 상담이 끝나면 지웁니다.</p>
  </form>
</div></section>
</main>
'''
    page = h + body + footer(0)
    page = page.replace('<script src="visit.js" defer></script>', FORM_SCRIPT + '<script src="visit.js" defer></script>')
    w('index.html', page)


# ───────────── 자판기 종류
def machines():
    url = SITE + '/machines.html'
    h = head('자판기 종류 — 음료·커피·스낵·아이스크림·복합·스마트 자판기 | 자판기마켓',
             '음료자판기, 커피자판기, 스낵자판기, 아이스크림·냉동자판기, 복합자판기, 키오스크형 스마트자판기, 생활용품·문구 자판기, 무인키오스크까지. 장소별 품목 구성표와 결제·관리 시스템을 정리했어요.',
             'machines.html', 0, [BIZ, breadcrumb_ld([('자판기 종류', url)])])
    cards = ''.join(
        f'<div class="card" id="m{i}"><span class="lb">{lb}</span><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in tags)}</ul>'
        f'<a class="go" href="./#apply" data-machine="{t}">이 기종 상담하기 →</a></div>'
        for i, (lb, t, d, tags) in enumerate(MACHINES, 1))
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in MIX)
    body = f'''{header(0, 'machines')}
<main>
<section class="page-hero"><div class="wrap">
  {crumb(0, [('자판기 종류', None)])}
  <span class="eyebrow">MACHINES</span>
  <h1>공간과 손님에 맞춰 고르는<br><em>자판기 종류</em></h1>
  <p class="lead">같은 자판기라도 놓는 곳에 따라 잘 팔리는 품목이 달라요. 기종별 특징과 장소별 품목 구성을 정리했어요. 기종에 따라 사양이 다를 수 있어서 정확한 사양은 상담 때 안내해 드려요.</p>
</div></section>
<section><div class="wrap">
  <span class="eyebrow">LINE UP</span><h2>자판기마켓에서 상담하는 기종</h2>
  <div class="cards c3">{cards}</div>
</div></section>
<section class="ivory"><div class="wrap">
  <span class="eyebrow">PRODUCT MIX</span><h2>장소별로 이렇게 구성해요</h2>
  <p class="lead">처음 채울 품목은 장소에 맞춰 함께 정해요. 운영하면서 잘 나가는 품목 위주로 바꿔 나가면 돼요.</p>
  <table class="mix"><thead><tr><th>장소</th><th>추천 기종</th><th>많이 나가는 품목</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
<section id="payment"><div class="wrap">
  <span class="eyebrow">PAYMENT &amp; SYSTEM</span><h2>현금 없어도 OK,<br>멀리서도 관리해요</h2>
  <div class="cards c4">
    <div class="card"><span class="lb">CARD</span><h3>카드 결제</h3><p>신용·체크카드, 교통카드</p></div>
    <div class="card"><span class="lb">PAY</span><h3>간편결제</h3><p>삼성페이·카카오페이·네이버페이·토스페이</p></div>
    <div class="card"><span class="lb">QR</span><h3>QR 결제</h3><p>휴대폰으로 찍어서 결제</p></div>
    <div class="card"><span class="lb">REMOTE</span><h3>원격 관리</h3><p>매출·재고를 휴대폰으로 확인</p></div>
  </div>
  <p class="note">※ 결제 수단과 원격 관리 기능은 기종에 따라 달라요.</p>
</div></section>
</main>
{cta(0, 'machines')}'''
    w('machines.html', h + body + footer(0))


# ───────────── 설치 장소
def places():
    pn = dict(PLACES)
    idx_url = SITE + '/places/'
    cards = ''.join(f'<a class="card" href="{k}.html"><span class="no">{i:02d}</span><h3>{n} 자판기</h3><p>{PLACE_INFO[k]["users"][0]}</p><span class="go">자세히 보기 →</span></a>'
                    for i, (k, n) in enumerate(PLACES, 1))
    h = head('설치 장소별 자판기 — 사무실·공장·헬스장·아파트·호텔 등 12곳 | 자판기마켓',
             '사무실, 공장·물류센터, 헬스장, 스터디카페, 아파트, 병원, 캠핑장, 학교, 사우나, PC방, 셀프세차장, 호텔까지. 장소별로 맞는 자판기 기종·품목·놓을 위치를 정리했어요.',
             'places/', 1, [BIZ, breadcrumb_ld([('설치 장소', idx_url)])])
    body = f'''{header(1, 'places')}
<main>
<section class="page-hero"><div class="wrap">
  {crumb(1, [('설치 장소', None)])}
  <span class="eyebrow">PLACEMENT</span>
  <h1>설치 장소별 자판기</h1>
  <p class="lead">사람이 오래 머무는 곳이면 어디든 설치할 수 있어요. 장소마다 이용하는 사람, 잘 팔리는 품목, 놓을 위치가 달라서 따로 정리했어요.</p>
</div></section>
<section><div class="wrap"><div class="cards c3" style="margin-top:0">{cards}</div></div></section>
</main>
{cta(1, 'places')}'''
    w('places/index.html', h + body + footer(1))

    for i, (k, n) in enumerate(PLACES):
        d = PLACE_INFO[k]
        short = n.split(' · ')[0]
        url = f'{SITE}/places/{k}.html'
        title = f'{short} 자판기 설치 — 맞는 기종·품목·위치 | 자판기마켓'
        desc = f'{n} 자판기 설치 안내. 이용자 특징, 잘 맞는 기종, 추천 품목, 놓을 위치와 주의할 점을 정리했어요. 설치비 0원, 전국 상담 {TEL}.'
        ul = lambda xs: '<ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
        others = [PLACES[(i + j) % len(PLACES)] for j in (1, 2, 3)]
        rel = ''.join(f'<a class="card" href="{ok}.html"><h3>{on} 자판기</h3><p>{PLACE_INFO[ok]["users"][0]}</p><span class="go">보기 →</span></a>' for ok, on in others)
        guide = (f'<div class="box">더 자세한 이야기는 가이드 글 <a href="../guide/{d["guide"]}.html"><b>{short} 자판기 가이드</b></a>에서 볼 수 있어요.</div>' if d['guide'] else '')
        ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': f'{short} 자판기 설치', 'serviceType': '자판기 설치·구입 상담',
               'provider': {'@type': 'LocalBusiness', 'name': '자판기마켓', 'telephone': '+82-10-5577-3067', 'url': SITE + '/'}, 'areaServed': 'KR', 'url': url},
              breadcrumb_ld([('설치 장소', SITE + '/places/'), (f'{short} 자판기', url)])]
        h = head(title, desc, f'places/{k}.html', 1, ld)
        body = f'''{header(1, 'places')}
<main>
<section class="page-hero"><div class="wrap">
  {crumb(1, [('설치 장소', './'), (f'{short} 자판기', None)])}
  <span class="eyebrow">PLACEMENT</span>
  <h1>{n}<br><em>자판기 설치</em></h1>
  <p class="lead">{d["intro"]}</p>
</div></section>
<section><div class="wrap prose">
  <h2>이용하는 사람의 특징</h2>{ul(d["users"])}
  <h2>잘 맞는 자판기 기종</h2>{ul(d["machines"])}
  <h2>처음 채우기 좋은 품목</h2>{ul(d["items"])}
  <p>처음엔 위 품목으로 시작하고, 2~3주 판매 기록을 보고 잘 나가는 품목 위주로 바꿔 나가면 돼요.</p>
  <h2>어디에 놓으면 좋을까</h2>{ul(d["spot"])}
  <h2>설치 전에 확인할 점</h2>{ul(d["care"])}
  {guide}
  <h2>시작하는 방법</h2>
  <p>설치비는 0원이고, 기계는 <b>일시불·할부·렌탈</b> 중 편한 방법으로 시작할 수 있어요. {short} 공간의 크기와 이용 인원을 알려 주시면 맞는 기종과 첫 품목 구성을 함께 정해 드려요.</p>
</div></section>
<section class="ivory"><div class="wrap"><span class="eyebrow">MORE PLACES</span><h2>다른 장소도 보기</h2><div class="cards c3">{rel}</div></div></section>
</main>
{cta(1, 'place-' + k)}'''
        w(f'places/{k}.html', h + body + footer(1))


# ───────────── 지역
def regions():
    idx_url = SITE + '/regions/'
    chips = ''.join(f'<a href="{k}.html">{n}</a>' for k, n, _ in REGIONS)
    cards = ''.join(f'<a class="card" href="{k}.html"><h3>{full}</h3><p>{REGION_INFO[k]["items"]}</p><span class="go">{n} 자판기 보기 →</span></a>' for k, n, full in REGIONS)
    h = head('지역별 자판기 설치 — 전국 17개 시·도 | 자판기마켓',
             '서울, 경기, 인천, 부산, 대구, 대전, 광주, 울산, 세종, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주까지. 전국 17개 시·도 자판기 설치·구입 상담. 지역별로 많이 찾는 설치 장소를 정리했어요.',
             'regions/', 1, [BIZ, breadcrumb_ld([('지역별 설치', idx_url)])])
    body = f'''{header(1, 'regions')}
<main>
<section class="page-hero"><div class="wrap">
  {crumb(1, [('지역별 설치', None)])}
  <span class="eyebrow">FIND YOUR AREA</span>
  <h1>지역별 자판기 설치</h1>
  <p class="lead">전국 17개 시·도 어디든 방문 상담 후 설치해요. 지역마다 산업단지, 대학가, 관광지처럼 성격이 달라서 많이 찾는 장소와 기종도 달라요.</p>
  <div class="chips">{chips}</div>
</div></section>
<section><div class="wrap"><div class="cards c3" style="margin-top:0">{cards}</div></div></section>
</main>
{cta(1, 'regions')}'''
    w('regions/index.html', h + body + footer(1))

    for i, (k, n, full) in enumerate(REGIONS):
        d = REGION_INFO[k]
        url = f'{SITE}/regions/{k}.html'
        subs = d['subs'].split()
        title = f'{n} 자판기 설치·구입 상담 — {full} 전 지역 | 자판기마켓'
        desc = f'{full} 자판기 설치 안내. {n}에서 많이 찾는 설치 장소와 기종, 시·군·구별 방문 상담. 설치비 0원, 일시불·할부·렌탈. 상담 {TEL}.'
        spots = ''.join(f'<div class="card"><span class="no">{j:02d}</span><h3>{s}</h3><p>{why}</p></div>' for j, (s, why) in enumerate(d['spots'], 1))
        sub_html = ''.join(f'<span>{x} 자판기</span>' for x in subs) if k != 'sejong' else '<span>세종 자판기</span><span>세종시 전역</span>'
        near = [REGIONS[(i + j) % len(REGIONS)] for j in (1, 2, 3, 4)]
        near_html = ''.join(f'<a href="{nk}.html">{nn} 자판기</a>' for nk, nn, _ in near)
        ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': f'{n} 자판기 설치', 'serviceType': '자판기 설치·구입 상담',
               'provider': {'@type': 'LocalBusiness', 'name': '자판기마켓', 'telephone': '+82-10-5577-3067', 'url': SITE + '/'},
               'areaServed': {'@type': 'AdministrativeArea', 'name': full}, 'url': url},
              breadcrumb_ld([('지역별 설치', SITE + '/regions/'), (f'{n} 자판기', url)])]
        h = head(title, desc, f'regions/{k}.html', 1, ld)
        body = f'''{header(1, 'regions')}
<main>
<section class="page-hero"><div class="wrap">
  {crumb(1, [('지역별 설치', './'), (f'{n} 자판기', None)])}
  <span class="eyebrow">{k.upper()}</span>
  <h1>{n} 자판기<br><em>설치 · 구입 상담</em></h1>
  <p class="lead">{d["intro"]}</p>
  <div class="btns" style="margin-top:30px"><a class="btn btn-dark" href="../?utm_source=region-{k}#apply">{n} 설치 상담 신청 →</a><a class="btn btn-line" href="{TEL_LINK}">{TEL}</a></div>
</div></section>
<section><div class="wrap">
  <span class="eyebrow">POPULAR SPOTS</span><h2>{n}에서 많이 찾는 설치 장소</h2>
  <div class="cards c3">{spots}</div>
  <div class="box" style="margin-top:30px"><b>{n}에서 많이 상담하는 구성</b><br>{d["items"]}</div>
</div></section>
<section class="ivory"><div class="wrap">
  <span class="eyebrow">AREA</span><h2>{full} 설치 가능 지역</h2>
  <p class="lead">아래 시·군·구 모두 방문 상담 후 설치해요. 섬이나 일부 산간 지역은 일정이 조금 더 걸릴 수 있어요.</p>
  <div class="subchips">{sub_html}</div>
</div></section>
<section><div class="wrap">
  <span class="eyebrow">HOW TO START</span><h2>{n} 자판기, 이렇게 시작해요</h2>
  {plans_html()}
  {steps_html()}
</div></section>
<section class="ivory" style="padding:60px 0"><div class="wrap"><span class="eyebrow">NEARBY</span><div class="chips" style="grid-template-columns:repeat(4,1fr);margin-top:10px">{near_html}</div></div></section>
</main>
{cta(1, 'region-' + k)}'''
        w(f'regions/{k}.html', h + body + footer(1))


if __name__ == '__main__':
    home(); machines(); places(); regions()
    import build_guide
    build_guide.build()
    print('홈·자판기 종류·장소 %d·지역 %d 페이지 만듦' % (len(PLACES), len(REGIONS)))
