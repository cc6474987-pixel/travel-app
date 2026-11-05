# Builds the standalone web app (GitHub Pages + Firebase) from the Claude-artifact build.
# Usage: python3 build_standalone.py <travel-app.html> <seed plan.json or -> <out dir>
import json, re, sys, os
src, seed, out = sys.argv[1], sys.argv[2], sys.argv[3]
page = open(src, encoding="utf-8").read()

def rep(t, old, new, n=1):
    assert t.count(old) == n, (old[:60], t.count(old))
    return t.replace(old, new)

# Start from the plan the group already edited in the Claude version.
if seed != "-":
    days = json.load(open(seed, encoding="utf-8"))["days"]
    page = re.sub(r"^const DAYS=\[.*?\];$", lambda m: "const DAYS=" + json.dumps(days, ensure_ascii=False) + ";", page, count=1, flags=re.M)

page = rep(page, "目前只存在這台裝置，在 Claude 裡開啟才會和旅伴同步", "目前只存在這台裝置，連上網路後會和旅伴同步")
page = rep(page, "'要先登入 Claude，並在 Claude 裡打開這個連結才能搜尋'", "'AI 搜尋還沒設定好，請先用地圖連結'")
page = rep(page, "'需要允許這個 app 使用 Claude 才能搜尋'", "'AI 搜尋暫時無法使用，請稍後再試'")
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "places_patch.py"), encoding="utf-8").read())
page = apply(page, rep)

head_extra = """<meta charset="utf-8">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="旅遊 App">
<meta name="theme-color" content="#f7f4ef">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
<script src="config.js?v=__V__"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
<script src="shim.js?v=__V__"></script>
<script>window.APP_V='__V__';
// Pages that stay open pick up a new version on their own: check every minute and whenever the app comes back to the screen.
(function(){let busy=false;const check=()=>{if(busy||document.hidden)return;busy=true;
  fetch('version.json?ts='+Date.now(),{cache:'no-store'}).then(r=>r.json()).then(j=>{if(j&&j.v&&j.v!==window.APP_V){pend=j.v;tryGo()}}).catch(()=>{}).finally(()=>{busy=false})};
  // A new version waits until nobody is touching the app (2 minutes idle, or the app is switched away and back), then reloads on the same tab and day.
  let pend=null,last=Date.now();['pointerdown','keydown','scroll','touchstart'].forEach(t=>window.addEventListener(t,()=>{last=Date.now()},{passive:true,capture:true}));
  const go=()=>{try{const s=dcComp&&dcComp.state;if(s)sessionStorage.setItem('trip-resume',JSON.stringify({tab:s.tab,day:s.day,mode:s.mode}))}catch(e){}location.replace(location.pathname+'?v='+pend)};
  const tryGo=()=>{if(!pend)return;let open=false;try{open=!!(dcComp&&dcComp.state&&(dcComp.state.sheet||dcComp.state.drag))||!!document.getElementById('admin-gate')}catch(e){}if(!open&&(document.hidden||Date.now()-last>120000))go()};
  setInterval(()=>{check();tryGo()},60000);document.addEventListener('visibilitychange',()=>{if(document.hidden)tryGo();else check()});window.addEventListener('focus',check)})();
// Offline: a service worker keeps the app's files so it still opens with no signal (trip data comes from Firestore's own offline cache).
if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>
"""
out_html = "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n" + head_extra + page.replace("<template id=\"tpl\">", "</head>\n<body>\n<template id=\"tpl\">", 1) + "</body>\n</html>\n"
import hashlib
ver = hashlib.sha1(out_html.encode("utf-8")).hexdigest()[:10]
out_html = out_html.replace("__V__", ver)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "version.json"), "w").write(json.dumps({"v": ver}) + "\n")
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(out_html)
# Same-origin files: network first (so updates arrive), cache when offline. Scripts and fonts from CDNs: cache first.
SW = r"""const C='trip-__V__';
const CORE=['./','index.html','config.js','shim.js','places.json','manifest.webmanifest','icon-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(CORE.map(u=>c.add(new Request(u,{cache:'reload'})).catch(()=>{}))))).then(()=>self.skipWaiting())});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
const CDN=/^https:\/\/(www\.gstatic\.com\/firebasejs|cdn\.jsdelivr\.net|fonts\.googleapis\.com|fonts\.gstatic\.com)\//;
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(u.origin===location.origin){if(u.pathname.endsWith('version.json'))return;
    e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(C).then(c=>c.put(r.mode==='navigate'?'index.html':u.pathname.replace(/^.*\//,''),cp))}return res})
      .catch(()=>caches.match(r.mode==='navigate'?'index.html':r,{ignoreSearch:true}).then(x=>x||caches.match(u.pathname.replace(/^.*\//,''),{ignoreSearch:true}))));return}
  if(CDN.test(r.url))e.respondWith(caches.match(r).then(x=>x||fetch(r).then(res=>{if(res.ok||res.type==='opaque'){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res})))});
"""
open(os.path.join(out, "sw.js"), "w", encoding="utf-8").write(SW.replace("__V__", ver))
print("ok", len(out_html))
