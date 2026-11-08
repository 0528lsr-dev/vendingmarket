// 방문 알림 → 텔레그램 "방문알림" 방 (티쳐포유·국제학교튜터와 같은 Apps Script 웹 앱. 코드: Desktop/국제학교사이트_복제키트/텔레그램_방문알림_코드.gs)
//   내 방문 빼기: 주소 끝에 ?novisit 붙여 한 번 열면 그 브라우저는 알림 안 감 (?visit 로 되돌림)
//   첫 방문 1번 + 60초 이상 머물거나 3페이지 이상 보면 🔥관심 높음
(function () {
  var HOOK = "https://script.google.com/macros/s/AKfycbzpQIZERcfJP0aKF15sZFpIo0-HPvARnnyhlaORN0PCk1bf8j5F0Q5fHRZZ7rkABi5E/exec", SITE = "자판기마켓", SKIP = ["121.128.108.11"];
  var ls = {}, ss = {};
  try { ls = localStorage; ss = sessionStorage; } catch (e) {}
  try { if (/[?&]novisit/.test(location.search)) ls.setItem('novisit', '1'); if (/[?&]visit(&|$)/.test(location.search)) ls.removeItem('novisit'); } catch (e) {}
  try { if (ls.getItem && ls.getItem('novisit')) return; } catch (e) {}
  var ua = navigator.userAgent || '';
  if (navigator.webdriver || /bot|crawl|spider|slurp|yeti|daum|lighthouse|headless|preview/i.test(ua)) return;
  if (!/^https?:$/.test(location.protocol) || /^(localhost|127[.])/.test(location.hostname)) return;
  function get(k) { try { return ss.getItem('vt_' + k); } catch (e) { return null; } }
  function set(k, v) { try { ss.setItem('vt_' + k, v); } catch (e) {} }
  function source() {
    var q = location.search, m = /[?&]utm_source=([^&]+)/.exec(q);
    var r = document.referrer || '', h = '';
    try { h = r ? new URL(r).hostname : ''; } catch (e) {}
    if (h && h.indexOf(location.hostname) >= 0) h = '';
    var u = m ? decodeURIComponent(m[1]) : '';
    var map = [['search.naver', '네이버 검색'], ['m.search.naver', '네이버 검색'], ['blog.naver', '네이버 블로그'], ['cafe.naver', '네이버 카페'], ['naver', '네이버'],
      ['google', '구글 검색'], ['daum', '다음 검색'], ['bing', '빙 검색'], ['chatgpt', 'chatgpt.com'], ['openai', 'chatgpt.com'], ['perplexity', 'perplexity'], ['claude.ai', 'claude.ai'],
      ['instagram', '인스타그램'], ['facebook', '페이스북'], ['kakao', '카카오톡'], ['youtube', '유튜브'], ['threads', '스레드'],
      ['fmkorea', '커뮤니티(fmkorea)'], ['theqoo', '커뮤니티(더쿠)'], ['dcinside', '커뮤니티(디시)'], ['clien', '커뮤니티(클리앙)'], ['ppomppu', '커뮤니티(뽐뿌)'], ['82cook', '커뮤니티(82쿡)'], ['mom', '맘카페']];
    var key = (h + ' ' + u).toLowerCase();
    for (var i = 0; i < map.length; i++) if (key.indexOf(map[i][0]) >= 0) return map[i][1];
    if (u) return u;
    return h || '직접 방문';
  }
  function device() {
    if (/iPhone|iPod/.test(ua)) return '모바일(아이폰)';
    if (/iPad/.test(ua)) return '태블릿(아이패드)';
    if (/Android/.test(ua)) return /Mobile/.test(ua) ? '모바일(안드로이드)' : '태블릿(안드로이드)';
    if (/Windows/.test(ua)) return 'PC(윈도우)';
    if (/Mac/.test(ua)) return 'PC(맥)';
    return 'PC';
  }
  var KR = { 'Seoul': '서울', 'Busan': '부산', 'Incheon': '인천', 'Daegu': '대구', 'Daejeon': '대전', 'Gwangju': '광주', 'Ulsan': '울산', 'Sejong': '세종', 'Gyeonggi': '경기', 'Gangwon': '강원',
    'North Chungcheong': '충북', 'South Chungcheong': '충남', 'North Jeolla': '전북', 'South Jeolla': '전남', 'North Gyeongsang': '경북', 'South Gyeongsang': '경남', 'Jeju': '제주' };
  function region(d) {
    if (!d || !d.country_code) return '';
    if (d.country_code !== 'KR') return [d.country_name, d.city].filter(Boolean).join(' ');
    var r = d.region || '', k = '';
    for (var n in KR) if (r.indexOf(n) >= 0) { k = KR[n]; break; }
    return k && d.city && d.city.indexOf(r.split(' ')[0]) < 0 && k !== '서울' ? k + ' ' + d.city : (k || d.city || '');
  }
  function post(data, beacon) {
    var b = new URLSearchParams(data);
    if (beacon && navigator.sendBeacon) { try { if (navigator.sendBeacon(HOOK, b)) return; } catch (e) {} }
    try { fetch(HOOK, { method: 'POST', mode: 'no-cors', body: b, keepalive: true }); } catch (e) {}
  }
  var title = (document.title || '').split(' | ')[0], path = location.pathname.replace(/index[.]html$/, '');
  set('pages', String(+(get('pages') || 0) + 1));
  if (!get('start')) {
    set('start', String(Date.now()));
    var info = { site: SITE, kind: 'visit', title: title, path: path, ref: source(), dev: device(), geo: '' };
    set('ref', info.ref);
    var done = false;
    var go = function (geo) {
      if (done) return; done = true;
      /* 위치를 못 얻었는데 브라우저 언어가 한국어가 아니면(검색 로봇은 보통 en-US) 보내지 않는다 — 2026-11-05 */
      if (!geo && !/^ko/i.test(navigator.language || '')) { set('bot', '1'); return; }
      info.geo = geo || ''; set('geo', info.geo); post(info);
    };
    /* 2026-11-05: 구글·아마존 같은 서버 회사(검색 로봇이 브라우저처럼 들어옴, 예: 미국 Mountain View) 는 알림 안 보냄 */
    var DC = /google|amazon|aws|microsoft|azure|digitalocean|linode|akamai|ovh|hetzner|cloudflare|oracle|alibaba|tencent|facebook|meta platforms|apple|yandex|baidu|naver cloud|kakao enterprise/i;
    setTimeout(function () { go(''); }, 6000);
    try { fetch('https://ipapi.co/json/').then(function (r) { return r.json(); }).then(function (d) {
      if (d && SKIP.indexOf(d.ip) >= 0) { done = true; try { ls.setItem('novisit', '1'); } catch (e) {} return; }
      if (d && DC.test((d.org || '') + ' ' + (d.asn_org || ''))) { done = true; set('bot', '1'); return; }
      /* 2026-11-08: 해외 IP 인데 브라우저 언어도 한국어가 아니면 로봇으로 보고 알림 안 보냄 (해외의 한국 손님은 보통 ko 설정이라 그대로 알림) */
      if (d && d.country_code && d.country_code !== 'KR' && !/^ko/i.test(navigator.language || '')) { done = true; set('bot', '1'); return; }
      go(region(d)); }, function () { go(''); }); } catch (e) { go(''); }
  }
  function hot() {
    if (get('hot') || get('bot')) return;
    try { if (ls.getItem && ls.getItem('novisit')) return; } catch (e) {}
    var sec = Math.round((Date.now() - +(get('start') || Date.now())) / 1000), pages = +(get('pages') || 1);
    if (sec < 60 && pages < 3) return;
    set('hot', '1');
    post({ site: SITE, kind: 'hot', title: title, path: path, ref: get('ref') || source(), dev: device(), geo: get('geo') || '',
      dur: Math.floor(sec / 60) + '분 ' + (sec % 60) + '초', pages: String(pages) }, true);
  }
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') hot(); });
  window.addEventListener('pagehide', hot);
  setTimeout(hot, 180000);
})();
