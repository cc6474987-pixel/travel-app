// Stands in for the Claude artifact runtime: trip-code gate, Firebase for shared data, Cloudflare Worker for Claude search.
(function(){
  const C = window.TRIP_CONFIG || {};
  const KEY = 'trip-code';
  const sha = async s => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))).map(b => b.toString(16).padStart(2, '0')).join('');
  let codeResolve; const codeReady = new Promise(r => codeResolve = r);
  let tripCode = null;

  async function tryCode(c){ c = (c || '').trim(); if (!c) return false; if (await sha(c) !== C.tripHash) return false;
    tripCode = c; try { localStorage.setItem(KEY, c) } catch(e) {} codeResolve(c); return true }

  function gate(){
    const d = document.createElement('div');
    d.id = 'trip-gate';
    d.innerHTML = '<div class="g-card"><div class="g-t">輸入旅行密碼</div><div class="g-s">第一次打開要輸入一次，之後就不用再輸入。</div>'
      + '<input id="g-in" type="password" autocomplete="current-password" placeholder="旅行密碼"><div id="g-err"></div><button id="g-go">進入</button></div>';
    const st = document.createElement('style');
    st.textContent = '#trip-gate{position:fixed;inset:0;z-index:9999;background:#f7f4ef;display:flex;align-items:center;justify-content:center;padding:24px;font-family:"Noto Sans TC",system-ui,sans-serif;color:#221f1a}'
      + '.g-card{width:100%;max-width:340px;display:flex;flex-direction:column;gap:12px}.g-t{font:700 24px "Noto Sans TC",sans-serif}.g-s{font:400 13.5px/1.6 "Noto Sans TC";color:#6f685e}'
      + '#g-in{height:50px;border-radius:14px;border:1.5px solid rgba(34,31,26,.2);background:#fffdf9;padding:0 14px;font-size:16px;outline:none}'
      + '#g-err{min-height:18px;font:400 12.5px "Noto Sans TC";color:oklch(0.5 0.14 30)}#g-go{height:50px;border:0;border-radius:14px;background:#221f1a;color:#fff;font:700 15px "Noto Sans TC"}';
    document.head.appendChild(st); document.body.appendChild(d);
    const go = async () => { if (await tryCode(document.getElementById('g-in').value)) d.remove(); else document.getElementById('g-err').textContent = '密碼不對，再試一次'; };
    document.getElementById('g-go').onclick = go;
    document.getElementById('g-in').onkeydown = e => { if (e.key === 'Enter') go(); };
  }

  async function start(){
    const fromUrl = new URLSearchParams(location.search).get('t');
    let saved = null; try { saved = localStorage.getItem(KEY) } catch(e) {}
    if (fromUrl && await tryCode(fromUrl)) { history.replaceState(null, '', location.pathname); return }
    if (saved && await tryCode(saved)) return;
    if (!C.tripHash) { console.warn('config.js has no tripHash'); return }
    if (document.body) gate(); else document.addEventListener('DOMContentLoaded', gate);
  }
  start();

  let dbP = null;
  function getDb(){
    if (dbP) return dbP;
    dbP = codeReady.then(async code => {
      if (!window.firebase || !C.firebase || !C.firebase.projectId) return null;
      const app = firebase.apps.length ? firebase.app() : firebase.initializeApp(C.firebase);
      const fs = app.firestore();
      try { await fs.enablePersistence({ synchronizeTabs: true }) } catch(e) {}
      const root = 'trips/' + code + '/';
      return { doc: p => fs.doc(root + p), collection: p => fs.collection(root + p) };
    }).catch(e => { console.warn('firebase', e); return null });
    return dbP;
  }

  const TIER = { quick: 'claude-haiku-5-5', default: 'claude-sonnet-5-5', complex: 'claude-sonnet-5-5' };
  async function ask(input, o){
    o = o || {};
    if (!C.workerUrl) throw { code: 'unavailable' };
    const code = await codeReady;
    const messages = typeof input === 'string' ? [{ role: 'user', content: input }] : input;
    const r = await fetch(C.workerUrl, { method: 'POST', headers: { 'content-type': 'application/json', 'x-trip-code': code },
      body: JSON.stringify({ model: o.model || TIER[o.modelTier || 'default'], messages }) });
    if (r.status === 429) throw { code: 'rate_limited' };
    if (!r.ok) throw { code: 'error', message: 'worker ' + r.status };
    const j = await r.json();
    return { text: j.text || '', truncated: !!j.truncated };
  }
  const sample = (input, o) => ask(input, o);
  sample.json = async (input, o) => { const { text } = await ask(input, o);
    const m = text.match(/[\[{][\s\S]*[\]}]/); if (!m) throw { code: 'bad_json' }; return JSON.parse(m[0]) };

  window.claude = { use: async name => name === 'db' ? getDb() : name === 'sample' ? (C.workerUrl ? sample : null) : null };
})();
