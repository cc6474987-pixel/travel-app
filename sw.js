const C='trip-f4e7b6606b';
const CORE=['./','index.html','config.js','shim.js','places.json','manifest.webmanifest','icon-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(CORE.map(u=>c.add(new Request(u,{cache:'reload'})).catch(()=>{}))))).then(()=>self.skipWaiting())});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
const CDN=/^https:\/\/(www\.gstatic\.com\/firebasejs|cdn\.jsdelivr\.net|fonts\.googleapis\.com|fonts\.gstatic\.com)\//;
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(u.origin===location.origin){if(u.pathname.endsWith('version.json'))return;
    e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(C).then(c=>c.put(r.mode==='navigate'?'index.html':u.pathname.replace(/^.*\//,''),cp))}return res})
      .catch(()=>caches.match(r.mode==='navigate'?'index.html':r,{ignoreSearch:true}).then(x=>x||caches.match(u.pathname.replace(/^.*\//,''),{ignoreSearch:true}))));return}
  if(CDN.test(r.url))e.respondWith(caches.match(r).then(x=>x||fetch(r).then(res=>{if(res.ok||res.type==='opaque'){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res})))});
