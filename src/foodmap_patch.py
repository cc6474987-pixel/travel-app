# --- Nearby food as a map (bang, 2026-11-08: chose App 內建地圖 + 附近 1 公里全部) ---
# The 附近美食 sheet shows an OpenStreetMap map (Leaflet, no key) centred on the phone's location, with every place in places.json
# within 1 km as a coloured dot, category chips, and a distance-sorted list underneath. Tapping a dot or a row shows hours/notes and a
# Google Maps navigation link. Away from Japan (or without location) it centres on today's next stop instead and says so.
def apply_map(page, rep):
    page = rep(page, "let PLDATA=null;", r"""let PLDATA=null;
const FM_GROUPS=[['all','全部'],['meal','正餐'],['sweet','甜點'],['cafe','咖啡・麵包']];
const fmGroup=c=>/甜點|和菓子|冰淇淋|甘味|聖代/.test(c||'')?'sweet':/咖啡|麵包|喫茶/.test(c||'')?'cafe':'meal';
const FM_COL={meal:'#c2410c',sweet:'#be185d',cafe:'#7c5a2a'};
const fmEsc=t=>String(t||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmNav=p=>p.src&&/google\.com\/maps/.test(p.src)?p.src:'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((p.jp||p.name)+' '+(p.addr||''));
let FM_LL=null;const loadLeaflet=()=>FM_LL||(FM_LL=new Promise((ok,bad)=>{if(window.L)return ok();const c=document.createElement('link');c.rel='stylesheet';c.href='https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css';document.head.appendChild(c);
  const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js';s.onload=()=>ok();s.onerror=()=>{FM_LL=null;bad(new Error('leaflet'))};document.head.appendChild(s)}));""")
    page = rep(page, "nearMe:false,myPlaces:[],np:null};", "nearMe:false,myPlaces:[],np:null,fm:{cat:'all',center:null,src:'',loading:false,err:'',sel:null}};")
    page = rep(page, "  togglePack(k){", r"""  openFood(){this.setState(st=>({sheet:'food',fm:{...st.fm,loading:true,err:'',sel:null}}));this.fmStart()}
  async fmStart(){let err='';try{await loadLeaflet()}catch(e){err='地圖載入失敗，請確認網路後再開一次'}
    const P=await getPlData(),g=await getLoc();let c=null,src='me';
    if(!g.err){c={lat:g.lat,lng:g.lng};if(!P.places.some(p=>distM(c,p)<30000))c=null}
    if(!c){src='trip';const C=clockOf(null,0),di=this.state.mode==='trip'?C.today:this.state.day,sc=this.sched(di),G=P.stops||{};
      const nx=sc.findIndex(it=>it.at>NOW),order=nx>=0?[...sc.slice(nx),...sc.slice(0,nx)]:sc;for(const it of order){const q=stopGeo(it,G);if(q){c=q;src='trip:'+it.title;break}}}
    if(!c){c={lat:35.7101,lng:139.7777};src='trip:上野'}
    this.setState(st=>({fm:{...st.fm,center:c,src,acc:g.acc||0,loading:false,err}}));setTimeout(()=>this.fmDraw(true),60)}
  fmItems(){const f=this.state.fm;if(!PLDATA||!f.center)return[];const all=PLDATA.places.concat((this.state.myPlaces||[]).filter(p=>p.lat));
    return all.map(p=>({...p,d:distM(f.center,p),g:fmGroup(p.cat)})).filter(p=>p.d<=1000&&(f.cat==='all'||p.g===f.cat)).sort((a,b)=>a.d-b.d)}
  fmDraw(recenter){const el=document.getElementById('fmap'),f=this.state.fm;if(!el||!window.L||!f.center)return;
    if(this.fmMap&&this.fmMap.getContainer()!==el){this.fmMap.remove();this.fmMap=null}
    if(!this.fmMap){this.fmMap=L.map(el,{zoomControl:false,preferCanvas:true});L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap'}).addTo(this.fmMap);this.fmLayer=L.layerGroup().addTo(this.fmMap);recenter=true}
    if(recenter)this.fmMap.setView([f.center.lat,f.center.lng],15);this.fmLayer.clearLayers();this.fmDots={};
    L.circle([f.center.lat,f.center.lng],{radius:1000,color:'#2563eb',weight:1,fill:false,dashArray:'4 6'}).addTo(this.fmLayer);
    if(f.src==='me')L.circleMarker([f.center.lat,f.center.lng],{radius:8,color:'#fff',weight:3,fillColor:'#2563eb',fillOpacity:1}).addTo(this.fmLayer);
    else L.circleMarker([f.center.lat,f.center.lng],{radius:7,color:'#221f1a',weight:2,fillColor:'#fff',fillOpacity:1}).addTo(this.fmLayer);
    this.fmItems().forEach((p,i)=>{const m=L.circleMarker([p.lat,p.lng],{radius:7,color:'#fff',weight:1.5,fillColor:FM_COL[p.g],fillOpacity:.95}).addTo(this.fmLayer);
      m.bindPopup('<b>'+fmEsc(p.name)+'</b><br><span style="color:#5c554c">'+fmEsc(p.cat)+' · '+Math.round(p.d)+' m</span>'+(p.hours?'<br>'+fmEsc(p.hours):'')+(p.note?'<br><span style="color:#5c554c">'+fmEsc(p.note)+'</span>':'')+'<br><a href="'+fmEsc(fmNav(p))+'" target="_blank" rel="noopener">Google 地圖導航 ↗</a>',{maxWidth:240});
      this.fmDots[p.name+'|'+p.lat]=m});setTimeout(()=>this.fmMap&&this.fmMap.invalidateSize(),80)}
  fmFocus(p){if(!this.fmMap)return;const m=this.fmDots&&this.fmDots[p.name+'|'+p.lat];this.fmMap.setView([p.lat,p.lng],17);if(m)m.openPopup();const el=document.getElementById('fmap');if(el)el.scrollIntoView({behavior:'smooth',block:'center'})}
  togglePack(k){""")
    page = rep(page, "onClick:()=>this.setState({sheet:k,errs:{}})}))", "onClick:()=>k==='food'?this.openFood():this.setState({sheet:k,errs:{}})}))")
    page = rep(page, "      addTicket:()=>this.tkAdd(),", r"""      addTicket:()=>this.tkAdd(),
      fmChips:FM_GROUPS.map(([k,l])=>{const on=s.fm.cat===k;return{label:l,bg:on?INK:'#fffdf9',color:on?'#fff':INK,border:on?INK:'rgba(34,31,26,.18)',onClick:()=>{this.setState(st=>({fm:{...st.fm,cat:k}}));setTimeout(()=>this.fmDraw(false),30)}}}),
      fmLoading:!!s.fm.loading,fmErr:s.fm.err||'',hasFmErr:!!s.fm.err,
      fmNote:s.fm.loading?'正在讀取你的位置…':!s.fm.center?'':s.fm.src==='me'?'藍點是你，虛線圈是 1 公里':'你現在不在日本或沒開定位，先顯示「'+s.fm.src.slice(5)+'」附近 1 公里',
      fmRecenter:()=>this.openFood(),
      fmList:(s.sheet==='food'?this.fmItems():[]).slice(0,40).map(p=>({n:p.name,tag:[p.cat,Math.round(p.d)+' m',p.area].filter(Boolean).join(' · '),hours:p.hours||'',note:p.note||'',hasHours:!!p.hours,dot:FM_COL[p.g],nav:fmNav(p),focus:()=>this.fmFocus(p)})),
      fmCount:s.sheet==='food'&&s.fm.center?this.fmItems().length+' 間在 1 公里內':'',""")
    i = page.index('<sc-if value="{{ sh.food }}">'); j = page.index('</sc-for>', i); j = page.index('</sc-if>', j) + 8
    while page[i:j].count('<sc-if') > page[i:j].count('</sc-if>'):
        j = page.index('</sc-if>', j) + 8
    page = page[:i] + """<sc-if value="{{ sh.food }}">
              <div style="display:flex;flex-direction:column;gap:10px">
                <div style="display:flex;align-items:center;justify-content:space-between">
                  <div style="font:700 20px 'Noto Sans TC',sans-serif">附近美食</div>
                  <button onClick="{{ fmRecenter }}" style="height:36px;padding:0 12px;border:1px solid rgba(34,31,26,.18);border-radius:11px;background:#fffdf9;font:500 13px 'Noto Sans TC';color:#221f1a;cursor:pointer">📍 重新定位</button>
                </div>
                <div style="display:flex;gap:6px;overflow-x:auto;scrollbar-width:none">
                  <sc-for list="{{ fmChips }}" as="c" hint-placeholder-count="4"><button onClick="{{ c.onClick }}" style="flex:none;height:34px;padding:0 13px;border-radius:17px;border:1px solid {{ c.border }};background:{{ c.bg }};color:{{ c.color }};font:500 13px 'Noto Sans TC';cursor:pointer">{{ c.label }}</button></sc-for>
                </div>
                <div id="fmap" style="height:46vh;min-height:260px;border-radius:16px;overflow:hidden;border:1px solid rgba(34,31,26,.12);background:#e8e1d5"></div>
                <div style="display:flex;justify-content:space-between;gap:8px;font:400 12px 'Noto Sans TC';color:#4d473f"><span>{{ fmNote }}</span><span style="flex:none">{{ fmCount }}</span></div>
                <sc-if value="{{ hasFmErr }}"><div style="font:600 12.5px 'Noto Sans TC';color:oklch(0.48 0.14 35)">{{ fmErr }}</div></sc-if>
                <sc-for list="{{ fmList }}" as="f" hint-placeholder-count="5">
                  <div onClick="{{ f.focus }}" style="display:flex;gap:10px;align-items:flex-start;padding:11px 13px;background:#fffdf9;border:1px solid rgba(34,31,26,.1);border-radius:14px;cursor:pointer">
                    <span style="width:10px;height:10px;border-radius:50%;background:{{ f.dot }};flex:none;margin-top:6px"></span>
                    <div style="flex:1;min-width:0">
                      <div style="font:600 14.5px 'Noto Sans TC'">{{ f.n }}</div>
                      <div style="font:400 12px 'Noto Sans TC';color:#4d473f;margin-top:1px">{{ f.tag }}</div>
                      <sc-if value="{{ f.hasHours }}"><div style="font:400 12px 'Noto Sans TC';color:#4d473f">{{ f.hours }}</div></sc-if>
                      <div style="font:400 12px/1.5 'Noto Sans TC';color:#5c554c;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden">{{ f.note }}</div>
                    </div>
                    <a href="{{ f.nav }}" target="_blank" rel="noopener" onClick="{{ stopClick }}" style="flex:none;align-self:center;padding:7px 10px;border-radius:10px;background:#221f1a;color:#fff;font:500 12px 'Noto Sans TC';text-decoration:none">導航</a>
                  </div>
                </sc-for>
              </div>
            </sc-if>""" + page[j:]
    return page
page = apply_map(page, rep)
