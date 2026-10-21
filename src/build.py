import re, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Travel App v6.dc.html")
OUT = os.path.join(HERE, "travel-app.html")
src = open(SRC, encoding="utf-8").read()

tpl = src[src.index("<div style=\"min-height:100vh"):src.index("</x-dc>")]
script = src[src.index("const MUTED="):src.rindex("</script>")]

def rep(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit("expected %d got %d for: %s" % (count, n, old[:90]))
    return text.replace(old, new)

def rrep(text, pat, new):
    m = list(re.finditer(pat, text, re.S))
    if len(m) != 1:
        sys.exit("regex %d matches: %s" % (len(m), pat[:80]))
    return text[:m[0].start()] + (m[0].expand(new) if '\\1' in new else new) + text[m[0].end():]

# ---------- template ----------
tpl = rep(tpl, '<div style="min-height:100vh;display:flex', '<div class="stage" style="min-height:100vh;display:flex')
tpl = rep(tpl, '<div style="max-width:300px;display:flex;flex-direction:column;gap:18px">', '<div class="side" style="max-width:300px;display:flex;flex-direction:column;gap:18px">')
tpl = rep(tpl, '<div style="width:390px;height:844px;', '<div class="frame" style="width:390px;height:844px;')
tpl = rep(tpl, '<div style="position:relative;width:100%;height:100%;border-radius:44px;', '<div class="screen" style="position:relative;width:100%;height:100%;border-radius:44px;')
tpl = rep(tpl, '<div style="height:50px;flex:none;display:flex;align-items:center;justify-content:space-between;', '<div class="sbar" style="height:50px;flex:none;display:flex;align-items:center;justify-content:space-between;')
tpl = rep(tpl, '<div style="height:50px;flex:none"></div>', '<div class="sbar-sp" style="height:50px;flex:none"></div>')
tpl = rep(tpl,
  """<button onClick="{{ startNav }}" style="flex:1;height:46px;border:0;border-radius:13px;background:#fff;color:#221f1a;font:700 14px 'Noto Sans TC';cursor:pointer">Google 地圖導航</button>""",
  """<a href="{{ nextNavUrl }}" target="_blank" rel="noopener" style="flex:1;height:46px;border:0;border-radius:13px;background:#fff;color:#221f1a;font:700 14px 'Noto Sans TC';cursor:pointer;display:flex;align-items:center;justify-content:center;text-decoration:none">Google 地圖導航</a>""")
tpl = rep(tpl,
  """<button onClick="{{ startNav }}" style="flex:1;height:48px;border:0;border-radius:14px;background:#221f1a;color:#fff;font:700 14px 'Noto Sans TC';cursor:pointer">Google 地圖導航</button>""",
  """<a href="{{ selNavUrl }}" target="_blank" rel="noopener" onClick="{{ afterNav }}" style="flex:1;height:48px;border:0;border-radius:14px;background:#221f1a;color:#fff;font:700 14px 'Noto Sans TC';cursor:pointer;display:flex;align-items:center;justify-content:center;text-decoration:none">Google 地圖導航</a>""")
tpl = rrep(tpl, r'<div style="height:132px;(.*?)">(\s*<span.*?當日路線</span>\s*<span.*?</span>\s*)</div>',
  r'<a href="{{ dayMapUrl }}" target="_blank" rel="noopener" style="height:132px;\1;text-decoration:none">\2</a>')
tpl = rep(tpl, '{{ dayCity }} 當日路線</span>', '{{ dayCity }} 當日路線 ↗</span>')
tpl = rep(tpl, """＋ 新增景點／餐廳</button>
            </div>""", """＋ 新增景點／餐廳</button>
            </div>
            <div class="mobsim" style="flex-direction:column;gap:8px;margin-top:10px;padding-top:14px;border-top:1px solid rgba(34,31,26,.1)">
              <div style="font:500 11px 'JetBrains Mono',monospace;color:#6f685e">模擬時間</div>
              <div style="display:flex;gap:6px;background:rgba(34,31,26,.07);padding:4px;border-radius:12px">
                <sc-for list="{{ modeBtns }}" as="m"><button onClick="{{ m.onClick }}" style="flex:1;border:0;cursor:pointer;padding:9px 4px;border-radius:9px;font:500 12px 'Noto Sans TC';background:{{ m.bg }};color:#221f1a;box-shadow:{{ m.shadow }}">{{ m.label }}</button></sc-for>
              </div>
              <div style="font:400 12px/1.6 'Noto Sans TC';color:#6f685e">{{ modeNote }}</div>
            </div>""")
tpl = rep(tpl, """<div style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-bottom:1px solid rgba(34,31,26,.07);background:{{ e.bg }};transition:background .6s">""",
  """<div onClick="{{ e.onDel }}" style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-bottom:1px solid rgba(34,31,26,.07);background:{{ e.bg }};transition:background .6s;cursor:pointer">""")
tpl = rep(tpl, """<div style="font:400 10.5px 'Noto Sans TC';color:#6f685e">{{ e.twd }}</div>
                      </div>
                    </div>
                  </sc-for>""", """<div style="font:400 10.5px 'Noto Sans TC';color:#6f685e">{{ e.twd }}</div>
                      </div>
                    </div>
                  </sc-for>
                  <sc-if value="{{ noExp }}"><div style="padding:18px 14px;font:400 12.5px/1.6 'Noto Sans TC';color:#6f685e">還沒有支出。按「＋ 記一筆」記下第一筆，會自動算出每個人該付多少。</div></sc-if>""")
tpl = rep(tpl, """<span style="font:700 16px 'Noto Sans TC'">明細</span>""", """<span style="font:700 16px 'Noto Sans TC'">明細 <span style="font:400 11px 'Noto Sans TC';color:#6f685e">點兩下可刪除</span></span>""")

# ---------- script ----------
S = script
S = rep(S, "noCtx:e=>e.preventDefault(),", "noCtx:e=>e.preventDefault(),stopClick:e=>e.stopPropagation(),")
S = rep(S, "const RATE=0.21, NOW=13*60+30, TODAY=1, BUDGET=1000000;", "const RATE=0.21, BUDGET=1000000;\nlet NOW=13*60+30, NOWSEC=NOW*60, TODAY=1;")
S = rrep(S, r"const EXPS=\[\{t:'the Moto.*?\.map\(e=>\(\{\.\.\.e,with:ALL\.slice\(\)\}\)\);", "const EXPS=[];")
S = rrep(S, r"  constructor\(p\)\{super\(p\);const m=p\.startMode\?\?'trip';.*?trErr:''\};\}",
"""  constructor(p){super(p);const C=clockOf(null,0),m=C.trip?'trip':'plan',L=lsGet();
    this.state={sim:null,mode:m,tab:m==='trip'?'today':'plan',day:m==='trip'?C.today:0,days:L.plan&&Array.isArray(L.plan.days)?L.plan.days:clone(DAYS),delay:0,elapsed:15,sheet:null,sel:null,drag:null,
      exps:L.exps||EXPS.slice(),checked:L.checked||{},cur:'JPY',
      form:{t:'',amt:'',payer:'我',cat:'餐飲',with:ALL.slice(),cur:'JPY'},errs:{},toast:'',phrase:0,ticket:0,moneyView:'list',settled:L.settled||[],aiDone:{},catTouched:false,pl:null,draft:L.plan&&L.plan.draft||false,trText:'',trRes:null,trLoading:false,trErr:'',sync:'local',delArm:null};
    this.mine=new Set();this.q=Promise.resolve();}""")
S = rrep(S, r"    this\.rt=setTimeout\(.*?elapsed:s\.elapsed\+1\}\)\)\},1000\);\n",
"""    this.iv=setInterval(()=>this.tick(),1000);this.initStore();
    this.onTouch=e=>{if(this.state.drag)e.preventDefault()};window.addEventListener('touchmove',this.onTouch,{passive:false});
""")
S = rep(S, "  flash(t){this.setState({toast:t});clearTimeout(this.tt);this.tt=setTimeout(()=>this.setState({toast:''}),2400)}",
"""  flash(t){this.setState({toast:t});clearTimeout(this.tt);this.tt=setTimeout(()=>this.setState({toast:''}),2400)}
  clockState(){const s=this.state;return clockOf(s.sim,s.elapsed)}
  tick(){const s=this.state;if(s.sim==='trip')return this.setState({elapsed:s.elapsed+1});if(s.sim)return;
    const C=clockOf(null,0),m=C.trip?'trip':'plan';
    if(m!==s.mode)this.setState({mode:m,tab:m==='trip'?'today':'plan',day:m==='trip'?C.today:0,sheet:null,delay:0});
    else if(m==='trip')this.setState({})}
  setSim(k){const C=clockOf(k,15),m=C.trip?'trip':'plan';this.setState({sim:k,mode:m,tab:m==='trip'?'today':'plan',day:m==='trip'?C.today:0,sheet:null,delay:0,elapsed:15})}
  write(fn){this.q=this.q.then(fn).catch(e=>{console.warn('sync failed',e);this.flash('同步失敗，請檢查網路後再試')})}
  savePlan(){clearTimeout(this.pt);this.pt=setTimeout(()=>{this.pt=null;const s=this.state,body={days:s.days,draft:s.draft||false};
    if(this.db){this.saving=(this.saving||0)+1;this.write(()=>this.db.doc('shared/plan').set(body).finally(()=>{this.saving--}))}else lsSet({plan:body})},600)}
  togglePack(k){const checked={...this.state.checked};if(checked[k])delete checked[k];else checked[k]=true;this.setState({checked});
    if(this.db)this.write(()=>this.db.doc('shared/pack').set({checked}));else lsSet({checked})}
  addExp(e){const x={...e,ts:Date.now()};
    if(this.db){const ref=this.db.collection('expenses').doc();this.mine.add(ref.id);this.setState(st=>({exps:[{...x,id:ref.id},...st.exps]}));this.write(()=>ref.set(x))}
    else{this.setState(st=>({exps:[{...x,id:'l'+x.ts},...st.exps]}));lsSet({exps:this.state.exps})}}
  tapExp(id){if(this.state.delArm!==id){clearTimeout(this.dt);this.setState({delArm:id});this.dt=setTimeout(()=>this.setState({delArm:null}),3000);return}
    clearTimeout(this.dt);this.setState(st=>({delArm:null,exps:st.exps.filter(e=>e.id!==id)}));
    if(this.db)this.write(()=>this.db.collection('expenses').doc(id).delete());else lsSet({exps:this.state.exps});this.flash('已刪除這筆')}
  addSettled(x){const y={from:x.from,to:x.to,amt:x.amt,ts:Date.now()};this.setState(st=>({settled:[...st.settled,y]}));
    if(this.db)this.write(()=>this.db.collection('settled').add(y));else lsSet({settled:this.state.settled})}
  remind(t){const done=()=>this.flash('已複製提醒文字，可以貼到群組');try{navigator.clipboard.writeText(t).then(done,()=>this.flash(t))}catch(e){this.flash(t)}}
  async initStore(){let db=null;try{db=window.claude&&window.claude.use?await window.claude.use('db'):null}catch(e){}
    if(!db)return;this.db=db;let first=true;const warn=e=>console.warn('db',e);
    db.doc('shared/plan').onSnapshot(snap=>{if(this.pt||this.saving||snap.metadata.hasPendingWrites)return;const d=snap.exists?snap.data():null;
      this.setState({sync:'shared',days:d&&Array.isArray(d.days)?clone(d.days):clone(DAYS),draft:d?d.draft||false:false})},warn);
    db.doc('shared/pack').onSnapshot(snap=>{const d=snap.exists?snap.data():null;this.setState({checked:d&&d.checked?{...d.checked}:{}})},warn);
    db.collection('expenses').onSnapshot(qs=>{const added=first?[]:qs.docChanges().filter(c=>c.type==='added'&&!this.mine.has(c.doc.id)).map(c=>c.doc.id);
      const exps=qs.docs.map(d=>({...d.data(),id:d.id,fresh:added.includes(d.id)})).sort((a,b)=>(b.ts||0)-(a.ts||0));
      this.setState({exps,sync:'shared'});
      if(added.length){const e=exps.find(x=>x.id===added[0]);if(e)this.flash(e.payer+' 剛記了一筆：'+e.t+' '+fJ(e.amt));clearTimeout(this.ft);this.ft=setTimeout(()=>this.setState(st=>({exps:st.exps.map(x=>({...x,fresh:false}))})),5000)}
      if(!qs.metadata.fromCache)first=false},warn);
    db.collection('settled').onSnapshot(qs=>{this.setState({settled:qs.docs.map(d=>({...d.data()})).sort((a,b)=>(a.ts||0)-(b.ts||0))})},warn)}""")
S = rep(S, "edit(di,fn,extra){this.setState(st=>{const days=clone(st.days);fn(days[di].items);return{days,...(extra||{})}})}",
           "edit(di,fn,extra){this.setState(st=>{const days=clone(st.days);fillPos(days[di].items);fn(days[di].items);return{days,...(extra||{})}});this.savePlan()}")
# Travel times follow the stops' positions on the original route: A→B 20 + B→C 20 means A→C is 40 after a reorder.
S = rep(S, "const vals=lg=>{let o;", "const vals=lg=>{if(lg.v)return{...lg.v};let o;")
S = rep(S, "const mins=lg=>", """const legV=lg=>lg.mode==='flight'||lg.orig==='flight'?{walk:lg.real,car:lg.real,train:lg.real}:vals(lg);
const addV=(a,b)=>({walk:a.walk+b.walk,car:a.car+b.car,train:a.train+b.train});
const fillPos=l=>{l.forEach((it,k)=>{if(it.p)return;const pv=l[k-1];
  if(!pv||!pv.p)it.p={walk:0,car:0,train:0};else if(pv.leg&&pv.leg.to===it.title&&!pv.pe)it.p=addV(pv.p,legV(pv.leg));else{it.p=addV(pv.p,vals(estLeg(pv,it,'train')));it.pe=true}})};
const posLeg=(a,b,dm)=>{const v={walk:Math.max(2,Math.abs(b.p.walk-a.p.walk)),car:Math.max(3,Math.abs(b.p.car-a.p.car)),train:Math.max(5,Math.abs(b.p.train-a.p.train))};
  const mode=dm==='car'?'car':v.walk<=15?'walk':'train';return{orig:mode,mode,real:v[mode],v,km:null,label:'估計',dist:'',note:'',est:true,to:b.title}};
const mins=lg=>""")
S = rep(S, "relink(l){const dm=dayModeOf(l);l.forEach((it,k)=>{", "relink(l){const dm=dayModeOf(l);fillPos(l);l.forEach((it,k)=>{")
S = rep(S, "else if(!it.leg||it.leg.to!==nx.title)it.leg=estLeg(it,nx,dm);", "else if(!it.leg||it.leg.to!==nx.title)it.leg=it.p&&nx.p&&!it.pe&&!nx.pe?posLeg(it,nx,dm):estLeg(it,nx,dm);")
S = rep(S, "try{if(!window.claude)throw new Error('no claude');\n      const txt=await window.claude.complete({max_tokens:8000,system:'你是日本旅遊行程規劃師，熟悉台灣旅客。只輸出一個 JSON 物件，不要多個版本、不要說明、不要 markdown。',messages:[{role:'user',content:prompt}]});",
           "try{const sample=await getSample();if(!sample)throw new Error('no claude');\n      const {text:txt}=await sample('你是日本旅遊行程規劃師，熟悉台灣旅客。只輸出一個 JSON 物件，不要多個版本、不要說明、不要 markdown。\\n\\n'+prompt,{modelTier:'default'});")
S = rep(S, "this.setState({days,draft:src,pl:null,mode:'plan',tab:'plan',day:0,aiDone:{0:true,1:true}});",
           "this.setState({days,draft:src,pl:null,tab:'plan',day:0,aiDone:{0:true,1:true}});this.savePlan();")
S = rep(S, """try{const txt=await window.claude.complete({max_tokens:300,system:'把使用者的中文翻成自然、禮貌、適合旅遊現場對店員說的日文。只輸出一個 JSON 物件，不要多個版本、不要說明、不要 markdown：{"jp":"日文","ro":"羅馬拼音"}',messages:[{role:'user',content:t}]});""",
           """try{const sample=await getSample();if(!sample)throw new Error('no claude');
      const {text:txt}=await sample('把下面的中文翻成自然、禮貌、適合旅遊現場對店員說的日文。只輸出一個 JSON 物件，不要多個版本、不要說明、不要 markdown：{"jp":"日文","ro":"羅馬拼音"}\\n\\n中文：'+t,{modelTier:'quick'});""")
S = rep(S, "const s=this.state, trip=s.mode==='trip', showSec=this.props.showTWD??true;",
           "const C=this.clockState();NOWSEC=C.sec;NOW=Math.floor(C.sec/60);TODAY=C.today;\n    const s=this.state, trip=s.mode==='trip', showSec=this.props.showTWD??true, shared=s.sync==='shared';")
S = rep(S, "const left=Math.max(0,(leave-NOW)*60-s.elapsed);", "const left=Math.max(0,leave*60-NOWSEC);")
S = rep(S, ".filter((it,i)=>i>nextIdx);", ".filter((it,i)=>nextIdx>=0&&i>nextIdx);")
S = rep(S, "const setMode=m=>()=>this.setState({mode:m,tab:m==='trip'?'today':'plan',day:m==='trip'?TODAY:0,sheet:null,delay:0,elapsed:15});", "const setMode=m=>()=>this.setSim(m);")
S = rep(S, "clock:trip?'13:30':'09:12',", "clock:ft(NOW),")
S = rep(S, "restoreTrip:()=>{this.setState({days:clone(DAYS),draft:false,day:0,aiDone:{}});this.flash('已還原匯入的行程')}",
           "restoreTrip:()=>{this.setState({days:clone(DAYS),draft:false,day:0,aiDone:{}});this.savePlan();this.flash('已還原匯入的行程')}")
S = rep(S, "modeBtns:[['plan','出發前 · 10/18'],['trip','旅途中 · 11/12']].map(([k,l])=>({label:l,onClick:setMode(k),bg:s.mode===k?'#fffdf9':'transparent',shadow:s.mode===k?'0 1px 3px rgba(0,0,0,.12)':'none'})),",
           "modeBtns:[[null,'實際時間'],['plan','出發前 · 10/18'],['trip','旅途中 · 11/12']].map(([k,l])=>({label:l,onClick:setMode(k),bg:s.sim===k?'#fffdf9':'transparent',shadow:s.sim===k?'0 1px 3px rgba(0,0,0,.12)':'none'})),")
S = rep(S, "modeNote:trip?'模擬 11/12 13:30 在澀谷神南：下一站倒數即時跑，可試「延後 30 分」與切換交通方式。':'出發前首頁是行程規劃；「今日」分頁尚未出現。',",
           "modeNote:s.sim==='trip'?'模擬 11/12 13:30 在澀谷神南：下一站倒數即時跑，可試「延後 30 分」與切換交通方式。':s.sim==='plan'?'模擬出發前：首頁是行程規劃，「今日」分頁尚未出現。':trip?'依東京時間，現在是旅途第 '+(TODAY+1)+' 天，首頁自動切到「今日」。':C.after?'旅程已結束，行程和帳目都還留著。':'依東京時間：出發前首頁是行程規劃，11/11 當天起自動出現「今日」分頁。',")
S = rep(S, "todayHead:'DAY 2 / 7 · '+td.date.replace(' ',' 週'),", "todayHead:'DAY '+(TODAY+1)+' / '+s.days.length+' · '+td.date.replace(' ',' 週'),")
S = rrep(S, r"startNav:\(\)=>\{let url;.*?this\.setState\(\{sheet:null\}\)\},",
           "nextNavUrl:next?this.mapUrl(next,pl):'https://www.google.com/maps',selNavUrl:(()=>{const q=s.sel;if(q&&s.days[q.di]&&s.days[q.di].items[q.i]){const ss=this.sched(q.di);return this.mapUrl(ss[q.i],ss[q.i-1]&&ss[q.i-1].leg)}return 'https://www.google.com/maps'})(),afterNav:()=>setTimeout(()=>this.setState({sheet:null}),300),")
S = rep(S, "statusLabel:trip?'旅途中':'出發倒數',statusValue:trip?'Day 2 / 7':'24 天',",
           "statusLabel:trip?'旅途中':C.after?'旅程':'出發倒數',statusValue:trip?'Day '+(TODAY+1)+' / '+s.days.length:C.after?'已結束':C.daysLeft+' 天',")
S = rep(S, "openAdd:()=>this.setState({sheet:'add'}),", "dayMapUrl:dayMapUrl(sch),openAdd:()=>this.setState({sheet:'add'}),")
S = rep(S, "balances,aiTip,online:'阿哲、Mei 在線上',", "balances,aiTip,online:shared?'與旅伴即時同步':'只存在這台裝置',")
S = rep(S, "onPaid:()=>{this.setState(st=>({settled:[...st.settled,x]}));this.flash(", "onPaid:()=>{this.addSettled(x);this.flash(")
S = rep(S, "onRemind:()=>this.flash('已傳送提醒給 '+x.from)})),", "onRemind:()=>this.remind(x.from+' 請付 '+M(x.amt)+' 給 '+x.to+'（東京河口湖旅費分帳）')})),")
S = rep(S, "expList:s.exps.map(e=>{const w=e.with||ALL;return{...e,amt:M(e.amt),twd:M2(e.amt),color:CAT[e.cat],fresh:!!e.fresh,bg:e.fresh?'oklch(0.96 0.035 165)':'transparent',meta:e.day+' · '+e.payer+' 付 · '+(w.length===ALL.length?ALL.length+' 人均分':w.join('、')+' 分')}}),",
           "noExp:!s.exps.length,expList:s.exps.map(e=>{const w=e.with||ALL,armed=s.delArm===e.id;return{...e,amt:M(e.amt),twd:M2(e.amt),color:CAT[e.cat]||MUTED,fresh:!!e.fresh,bg:armed?'oklch(0.95 0.04 30)':e.fresh?'oklch(0.96 0.035 165)':'transparent',meta:armed?'再點一次就刪除這筆':e.day+' · '+e.payer+' 付 · '+(w.length===ALL.length?ALL.length+' 人均分':w.join('、')+' 分'),onDel:()=>this.tapExp(e.id)}}),")
S = rep(S, "const allPack=s.pack.flatMap(c=>c.items), doneN=allPack.filter(p=>p.d).length;",
           "const pack=PACK.map((c,ci)=>({name:c.name,items:c.items.map(([l,w],pi)=>({l,w,d:!!s.checked[ci+'-'+pi]}))})), allPack=pack.flatMap(c=>c.items), doneN=allPack.filter(p=>p.d).length;")
S = rep(S, "packCats:s.pack.map(", "packCats:pack.map(")
S = rep(S, "onClick:()=>this.setState(st=>{const pack=st.pack.map((cc,i)=>i!==ci?cc:{...cc,items:cc.items.map((pp,j)=>j!==pi?pp:{...pp,d:!pp.d})});return{pack}})}))})),",
           "onClick:()=>this.togglePack(ci+'-'+pi)}))})),")
S = rep(S, "presence:'阿哲 正在編輯 D3 河口湖 · Mei 在線上',",
           "presence:shared?'與旅伴共用：改行程、記帳、勾清單都會即時同步':'目前只存在這台裝置，在 Claude 裡開啟才會和旅伴同步',")
S = rep(S, "this.setState(st=>({exps:[{t:f.t.trim(),amt:Math.round(amtJ),payer:f.payer,cat:f.cat,with:f.with,day:trip?'D2':'行前'},...st.exps],form:",
           "this.addExp({t:f.t.trim(),amt:Math.round(amtJ),payer:f.payer,cat:f.cat,with:f.with,day:trip?'D'+(TODAY+1):'行前'});this.setState(st=>({form:")
S = rep(S, "this.flash('已記帳，全員同步更新')", "this.flash(shared?'已記帳，旅伴那邊也會更新':'已記帳')")

# ---------- drag: touch-based long press, auto-scroll, no text selection ----------
tpl = rep(tpl, """<div style="flex:none;height:82px;border-top:1px solid rgba(34,31,26,.1);""", """<div class="navbar" style="flex:none;height:82px;border-top:1px solid rgba(34,31,26,.1);""")
tpl = rep(tpl, """onPointerDown="{{ it.down }}" """, """onPointerDown="{{ it.down }}" onTouchStart="{{ it.tdown }}" """)
tpl = rep(tpl, """touch-action:pan-y;transition:box-shadow .15s" style-hover="background:#fff">""", """touch-action:pan-y;transition:box-shadow .15s;position:relative;padding-right:40px" style-hover="background:#fff">
                      <sc-if value="{{ it.canDrag }}"><div onTouchStart="{{ it.gdown }}" onPointerDown="{{ it.gpdown }}" onClick="{{ stopClick }}" aria-label="拖曳調整順序" style="position:absolute;top:0;right:0;bottom:0;width:38px;display:flex;align-items:center;justify-content:center;touch-action:none;cursor:grab;color:rgba(34,31,26,.35);font:700 15px/1 system-ui;letter-spacing:-2px">⋮⋮</div></sc-if>""")
S = rrep(S, r"    this\.onMove=e=>\{const pr=this\.press;.*?this\.commitDrag\(d\)\};\n",
"""    this.moveTo=y=>{const d=this.state.drag;if(!d)return;this.lastY=y;const lo=d.mids[0]-d.mids[d.i],hi=d.mids[d.mids.length-1]-d.mids[d.i],dy=Math.max(lo,Math.min(hi,y-d.y0+(d.sc?d.sc.scrollTop-d.st0:0))),c=d.mids[d.i]+dy;let over=0;d.mids.forEach((m,j)=>{if(j!==d.i&&m<c)over++});if(dy!==d.dy||over!==d.over)this.setState({drag:{...d,dy,over}})};
    this.onMove=e=>{if(e.pointerType==='touch')return;const pr=this.press;if(pr&&!this.state.drag&&Math.abs(e.clientY-pr.y)>8){clearTimeout(pr.t);this.press=null}if(!this.state.drag)return;e.preventDefault();this.moveTo(e.clientY)};
    this.endPress=()=>{if(this.press){clearTimeout(this.press.t);this.press=null}const d=this.state.drag;if(!d)return;this.commitDrag(d)};
    this.onUp=e=>{if(e&&e.pointerType==='touch')return;this.endPress()};
""")
S = rep(S, "    this.onTouch=e=>{if(this.state.drag)e.preventDefault()};window.addEventListener('touchmove',this.onTouch,{passive:false});",
"""    this.onTouch=e=>{const t=e.touches[0];if(!t)return;const pr=this.press;if(pr&&!this.state.drag&&(Math.abs(t.clientY-pr.y)>8||Math.abs(t.clientX-pr.x)>8)){clearTimeout(pr.t);this.press=null}if(this.state.drag){e.preventDefault();this.moveTo(t.clientY)}};
    window.addEventListener('touchmove',this.onTouch,{passive:false});window.addEventListener('touchend',()=>this.endPress());window.addEventListener('touchcancel',()=>this.endPress());""")
S = rrep(S, r"  startDrag\(i,y\)\{.*?h:r\[i\]\.height\}\}\)\}",
"""  startDrag(i,y){this.press=null;const rows=Array.from(document.querySelectorAll('[data-row]'));if(!rows[i])return;const r=rows.map(x=>x.getBoundingClientRect()),sc=rows[i].closest('.noscroll');
    this.dragged=true;if(navigator.vibrate)navigator.vibrate(12);try{window.getSelection().removeAllRanges()}catch(e){}
    this.lastY=y;this.setState({drag:{i,y0:y,dy:0,over:i,mids:r.map(x=>x.top+x.height/2),h:r[i].height,sc,st0:sc?sc.scrollTop:0,max:sc?sc.scrollHeight-sc.clientHeight:0}});
    const loop=()=>{const d=this.state.drag;if(!d)return;if(d.sc){const b=d.sc.getBoundingClientRect(),yy=this.lastY,E=70,sp=k=>Math.max(1,Math.round(Math.min(1,k/E)**2*9));let v=0;
      if(yy<b.top+E)v=-sp(b.top+E-yy);else if(yy>b.bottom-E)v=sp(yy-(b.bottom-E));
      if(v){const before=d.sc.scrollTop,ns=Math.max(0,Math.min(d.max,before+v));if(ns!==before){d.sc.scrollTop=ns;this.moveTo(yy)}}}this.raf=requestAnimationFrame(loop)};
    cancelAnimationFrame(this.raf);this.raf=requestAnimationFrame(loop)}""")
S = rep(S, "setTimeout(()=>{this.dragged=false},60)}", "cancelAnimationFrame(this.raf);setTimeout(()=>{this.dragged=false},350)}")
S = rep(S, "down:dragList?e=>{if(e.button>0)return;const y=e.clientY;this.press={i,y,t:setTimeout(()=>this.startDrag(i,y),380)}}:null,",
"""down:dragList?e=>{if(e.pointerType==='touch'||e.button>0)return;const y=e.clientY;this.press={i,y,x:e.clientX,t:setTimeout(()=>this.startDrag(i,y),380)}}:null,
        tdown:dragList?e=>{const t=e.touches[0];if(!t)return;clearTimeout(this.press&&this.press.t);this.press={i,y:t.clientY,x:t.clientX,t:setTimeout(()=>this.startDrag(i,t.clientY),350)}}:null,
        canDrag:!!dragList,
        gdown:dragList?e=>{e.stopPropagation();const t=e.touches[0];if(!t)return;if(this.press)clearTimeout(this.press.t);this.press=null;this.startDrag(i,t.clientY)}:null,
        gpdown:dragList?e=>{e.stopPropagation();if(e.pointerType==='touch'||e.button>0)return;if(this.press)clearTimeout(this.press.t);this.press=null;e.preventDefault();this.startDrag(i,e.clientY)}:null,""")

# ---------- round 2: place search, route-aware insert, always-on 今日, no simulated time ----------
tpl = rrep(tpl, r"""<div style="display:flex;flex-direction:column;gap:8px">\s*<div style="font:500 11px 'JetBrains Mono',monospace;color:#6f685e">模擬時間</div>.*?\{\{ modeNote \}\}</div>\s*</div>""",
  """<div style="font:400 12px/1.6 'Noto Sans TC';color:#6f685e">{{ modeNote }}</div>""")
tpl = rrep(tpl, r"""\s*<div class="mobsim".*?\{\{ modeNote \}\}</div>\s*</div>""", "")
tpl = rep(tpl, """<sc-if value="{{ isToday }}" hint-placeholder-val="{{ false }}">
          <div style="padding:8px 20px 28px;display:flex;flex-direction:column;gap:16px">""", """<sc-if value="{{ isToday }}" hint-placeholder-val="{{ false }}">
          <div style="padding:8px 20px 28px;display:flex;flex-direction:column;gap:16px">
            <sc-if value="{{ isPreview }}"><div style="padding:10px 13px;border-radius:14px;background:oklch(0.97 0.02 255);border:1px solid oklch(0.85 0.05 255);font:400 12.5px/1.55 'Noto Sans TC';color:#4d473f">{{ previewNote }}</div></sc-if>""")
tpl = rep(tpl, """<span style="font:400 13px 'Noto Sans TC';opacity:.9">後該出發</span>""", """<span style="font:400 13px 'Noto Sans TC';opacity:.9">{{ cdUnit }}</span>""")
tpl = rep(tpl, """<div style="font:400 12px 'Noto Sans TC';color:#6f685e">從你行程備註裡的備案與順路點整理 · 會排在當天最後</div>""",
"""<div style="display:flex;gap:8px">
                  <input value="{{ addQ }}" onChange="{{ setAddQ }}" onKeyDown="{{ addKey }}" placeholder="想找什麼？例：拉麵、甜點、伴手禮" style="flex:1;min-width:0;height:44px;border-radius:13px;border:1.5px solid rgba(34,31,26,.15);background:#fffdf9;padding:0 13px;font:400 14.5px 'Noto Sans TC';color:#221f1a;outline:none">
                  <button onClick="{{ askClaude }}" style="flex:none;height:44px;padding:0 14px;border:0;border-radius:13px;background:oklch(0.5 0.11 255);color:#fff;font:500 13.5px 'Noto Sans TC';cursor:pointer;white-space:nowrap;opacity:{{ srOpacity }}">{{ srBtn }}</button>
                </div>
                <div style="font:400 12px/1.6 'Noto Sans TC';color:#6f685e">{{ srHint }}</div>
                <sc-if value="{{ srErr }}"><span style="font:400 12px 'Noto Sans TC';color:oklch(0.5 0.14 30)">{{ srErr }}</span></sc-if>
                <sc-if value="{{ hasSr }}">
                  <div style="font:500 12px 'Noto Sans TC';color:oklch(0.42 0.11 255)">Claude 推薦 · 營業時間請點地圖確認</div>
                  <sc-for list="{{ srList }}" as="s">
                    <div style="display:flex;align-items:center;gap:12px;padding:12px 14px;background:#fffdf9;border:1px solid oklch(0.85 0.05 255);border-radius:14px">
                      <span style="width:8px;height:8px;border-radius:50%;background:{{ s.color }};flex:none"></span>
                      <div style="flex:1;min-width:0">
                        <div style="font:500 14px 'Noto Sans TC'">{{ s.title }}</div>
                        <div style="font:400 11.5px/1.5 'Noto Sans TC';color:#6f685e">{{ s.sub }}</div>
                        <div style="display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:3px"><span style="font:400 11px 'Noto Sans TC';color:#6f685e">{{ s.where }}</span><a href="{{ s.map }}" target="_blank" rel="noopener" style="font:500 11.5px 'Noto Sans TC';color:oklch(0.45 0.11 255);text-decoration:none">地圖 ↗</a></div>
                      </div>
                      <button onClick="{{ s.onClick }}" style="flex:none;border:0;background:#221f1a;color:#fff;border-radius:10px;padding:7px 12px;font:500 12px 'Noto Sans TC';cursor:pointer">加入</button>
                    </div>
                  </sc-for>
                </sc-if>
                <sc-if value="{{ hasLocal }}"><div style="font:500 12px 'Noto Sans TC';color:#6f685e">你行程備註裡的備案與順路點</div></sc-if>
                <sc-if value="{{ noLocal }}"><div style="font:400 12px 'Noto Sans TC';color:#6f685e">行程備註裡沒有符合的地點，按「請 Claude 找」查附近。</div></sc-if>""")

S = rep(S, "sync:'local',delArm:null};", "sync:'local',delArm:null,addQ:'',sr:null,srLoading:false,srErr:''};")
S = rep(S, "openAdd:()=>this.setState({sheet:'add'}),", "openAdd:()=>this.setState({sheet:'add',addQ:'',sr:null,srErr:''}),")
S = rep(S, "this.flash('已加入 — 選擇交通方式與停留時間')}",
"""this.flash(idx>0&&list[idx-1]?'已排在「'+list[idx-1].title+'」之後，可以再調整':'已加入')}
  bestAfter(di){const l=this.state.days[di].items,n=l.length;if(!n)return null;const last=l[n-1];return (last.type==='住宿'||last.type==='機場')&&n>1?n-2:n-1}
  findAfter(di,t){const l=this.state.days[di].items;t=(t||'').trim();if(t){let i=l.findIndex(x=>x.title===t);if(i<0)i=l.findIndex(x=>x.title.includes(t)||t.includes(x.title));if(i>=0)return i===l.length-1&&l.length>1&&(l[i].type==='住宿'||l[i].type==='機場')?i-1:i}return this.bestAfter(di)}
  async searchPlaces(){const s=this.state;if(s.srLoading)return;const q=s.addQ.trim(),di=s.day,d=s.days[di],sch=this.sched(di);
    this.setState({srLoading:true,srErr:''});
    try{const sample=await getSample();if(!sample)throw {code:'unavailable'};
      const stops=sch.map((it,i)=>(i+1)+'. '+ft(it.at)+' '+it.title+(it.addr?'（'+it.addr+'）':'')).join('\\n');
      const prompt='你是熟悉日本的旅遊助理，幫 6 位台灣旅客找可以加進當天行程的地點。\\n日期：'+d.date+'，當天區域：'+d.city+'\\n當天行程：\\n'+stops+'\\n\\n想找：'+(q||'順路、值得去的景點或美食')+'\\n\\n只推薦真實存在、就在當天行程經過的區域附近（離某一站步行或車程約 15 分鐘內）的地點，最多 6 個，不要重複行程裡已有的站。每個地點指出最順路要排在哪一站之後，after 請照抄上面清單的站名。\\n只輸出 JSON：{"items":[{"title":"地點名稱","type":"景點|餐飲|購物|夜生活","note":"一句重點，含大概營業時間","area":"所在區域","after":"要排在其後的站名","stay":建議停留分鐘}]}';
      const j=await sample.json(prompt,{model:'claude-haiku-5-5',modelTier:'quick'});const arr=j&&Array.isArray(j.items)?j.items:[],TY=['景點','餐飲','購物','夜生活'];
      const sr=arr.slice(0,6).map(x=>({title:String(x.title||'').slice(0,40),type:TY.includes(x.type)?x.type:'景點',sub:String(x.note||''),area:String(x.area||''),after:String(x.after||''),stay:Math.max(0,Math.min(480,+x.stay||0))})).filter(x=>x.title);
      if(this.state.day!==di)return this.setState({srLoading:false});
      this.setState({sr,srLoading:false,srErr:sr.length?'':'沒有找到合適的地點，換個關鍵字試試'})}
    catch(e){console.warn('search failed',e);this.setState({srLoading:false,srErr:e&&e.code==='not_granted'?'需要允許這個 app 使用 Claude 才能搜尋':e&&e.code==='unavailable'?'要先登入 Claude，並在 Claude 裡打開這個連結才能搜尋':'搜尋失敗，請再試一次'})}}""")
S = rep(S, "TODAY=C.today;\n", "TODAY=C.today;const preview=!C.trip;if(preview){TODAY=C.after?this.state.days.length-1:0;NOW=tm(this.state.days[TODAY].start)-1;NOWSEC=NOW*60}\n")
S = rep(S, "const navDefs=(trip?[['today','今日']]:[]).concat(", "const navDefs=[['today','今日']].concat(")
S = rep(S, "countdown:String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0'),",
"""countdown:preview?(C.after?'—':String(C.daysLeft)):String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0'),
      cdUnit:preview?(C.after?'旅程已結束':'天後出發'):'後該出發',isPreview:preview,
      previewNote:C.after?'旅程已結束，這裡顯示最後一天的行程。':'還沒出發，這是 '+s.days[0].date.split(' ')[0]+' 第一天的預覽。出發當天起會依東京時間自動變成當天行程。',""")
S = rep(S, "delay30:()=>{this.setState(", "delay30:()=>{if(preview)return this.flash('出發當天才能延後行程');this.setState(")
S = rep(S, "const sheet=s.sheet, ai=AI[s.day];",
"""const sheet=s.sheet, ai=AI[s.day];
    const aq=s.addQ.trim(),seen={},sugPool=aq?SUGGEST.flat():(SUGGEST[s.day]||[]);
    const localSug=sugPool.filter(([t,sub])=>!seen[t]&&(seen[t]=1)&&(!aq||t.includes(aq)||sub.includes(aq))).map(([t,sub,type])=>({title:t,sub,type,color:tc(type),
      onClick:()=>this.addItem(s.day,{title:t,sub,type},this.bestAfter(s.day))}));
    const dItems=day.items;""")
S = rep(S, "suggest:(SUGGEST[s.day]||[]).map(([t,sub,type])=>({title:t,sub,type,color:tc(type),onClick:()=>this.addItem(s.day,{title:t,sub,type})})),",
"""suggest:localSug,hasLocal:localSug.length>0,noLocal:!localSug.length&&!(s.sr&&s.sr.length),
      addQ:s.addQ,setAddQ:e=>this.setState({addQ:e.target.value}),addKey:e=>{if(e.key==='Enter')this.searchPlaces()},askClaude:()=>this.searchPlaces(),
      srBtn:s.srLoading?'搜尋中…':'請 Claude 找',srOpacity:s.srLoading?.6:1,srErr:s.srErr,
      srHint:s.srLoading?'Claude 正在找 '+day.city+' 附近的地點，約需 10–30 秒':'Claude 只找 '+day.city+' 一帶、排得進當天行程的地點',
      hasSr:!!(s.sr&&s.sr.length),
      srList:(s.sr||[]).map(r=>{const ai=this.findAfter(s.day,r.after),at=ai!=null&&dItems[ai]?dItems[ai].title:'';
        return{title:r.title,sub:r.sub,color:tc(r.type),where:(r.area?r.area+' · ':'')+(at?'會排在「'+at+'」之後':'會排在當天最後'),
          map:'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(r.title+' '+(r.area||day.city)),
          onClick:()=>this.addItem(s.day,{title:r.title,sub:r.sub,type:r.type,rec:r.stay?[r.stay,r.stay]:undefined},ai)}}),""")

tpl = rrep(tpl, r"""(<div style="display:flex;gap:6px">\s*<sc-for list="\{\{ todayLegs \}\}".*?</sc-for>\s*</div>)""", r'<sc-if value="{{ hasLegs }}">\1</sc-if>')
tpl = rrep(tpl, r"""(<div style="background:rgba\(0,0,0,\.16\);border-radius:14px;.*?</sc-for>\s*</div>)""", r'<sc-if value="{{ hasRoute }}">\1</sc-if>')
S = rep(S, "todayLegs:pl&&pl.mode!=='flight'?this.legChips(TODAY,nextIdx-1,pl):[],route,", "todayLegs:pl&&pl.mode!=='flight'?this.legChips(TODAY,nextIdx-1,pl):[],route,hasLegs:!!(pl&&pl.mode!=='flight'),hasRoute:route.length>0,")

HELPERS = r"""
const TRIP0=Date.UTC(2026,10,11);
function clockOf(sim,elapsed){if(sim==='trip')return{trip:true,today:1,sec:(13*60+30)*60+elapsed};
  if(sim==='plan')return{trip:false,today:0,sec:9*3600+12*60,daysLeft:24};
  const t=new Date(Date.now()+9*3600e3),di=Math.round((Date.UTC(t.getUTCFullYear(),t.getUTCMonth(),t.getUTCDate())-TRIP0)/864e5),
    sec=t.getUTCHours()*3600+t.getUTCMinutes()*60+t.getUTCSeconds(),trip=di>=0&&di<DAYS.length;
  return{trip,today:trip?di:0,sec,daysLeft:-di,after:di>=DAYS.length}}
const dayMapUrl=sch=>{const pts=[];sch.forEach(it=>{const q=it.addr||it.title;if(q&&pts[pts.length-1]!==q)pts.push(q)});return 'https://www.google.com/maps/dir/'+pts.slice(0,10).map(encodeURIComponent).join('/')};
const LSK='travel-app-v6';
const lsGet=()=>{try{return JSON.parse(localStorage.getItem(LSK)||'{}')||{}}catch(e){return {}}};
const lsSet=o=>{try{localStorage.setItem(LSK,JSON.stringify({...lsGet(),...o}))}catch(e){}};
const getSample=async()=>{try{return window.claude&&window.claude.use?await window.claude.use('sample'):null}catch(e){return null}};
"""
S = rep(S, "class Component extends DCLogic {", HELPERS + "\nclass Component extends DCLogic {")

RUNTIME = r"""
// Small runtime for the Claude Design template: {{ path }} bindings, <sc-for>, <sc-if>, style-hover/style-active.
const {h,render:prender,Fragment}=preact;
const RE=/\{\{\s*([^}]+?)\s*\}\}/g, pseudo={};let pseudoCss='';
function pcls(kind,css){const k=kind+'|'+css;if(!pseudo[k]){const c='dcp'+Object.keys(pseudo).length;pseudo[k]=c;
  pseudoCss+='.'+c+':'+kind+'{'+css.split(';').filter(x=>x.trim()).map(d=>d+' !important').join(';')+'}'}return pseudo[k]}
function getv(p,sc){if(p==='true')return true;if(p==='false')return false;if(/^-?\d/.test(p))return Number(p);let v=sc;for(const k of p.split('.')){if(v==null)return undefined;v=v[k]}return v}
function interp(str){if(!str.includes('{{'))return()=>str;const one=str.match(/^\{\{\s*([^}]+?)\s*\}\}$/);if(one){const p=one[1];return sc=>getv(p,sc)}
  const parts=[];let last=0;str.replace(RE,(all,p,i)=>{parts.push(str.slice(last,i),{p});last=i+all.length});parts.push(str.slice(last));
  return sc=>parts.map(x=>{if(typeof x==='string')return x;const v=getv(x.p,sc);return v==null?'':String(v)}).join('')}
function kids(nodes){const fs=nodes.map(compile).filter(Boolean);return sc=>fs.map(f=>f(sc))}
function compile(n){
  if(n.nodeType===3){const t=n.nodeValue;if(!t.trim()&&t.includes('\n'))return null;const f=interp(t);return sc=>{const v=f(sc);return v==null||v===false?'':String(v)}}
  if(n.nodeType!==1)return null;const tag=n.tagName.toLowerCase();
  if(tag==='sc-for'){const lf=interp(n.getAttribute('list')),as=n.getAttribute('as'),cf=kids([...n.childNodes]);
    return sc=>(lf(sc)||[]).map(it=>{const s2=Object.create(sc);s2[as]=it;return cf(s2)})}
  if(tag==='sc-if'){const vf=interp(n.getAttribute('value')),cf=kids([...n.childNodes]);return sc=>vf(sc)?cf(sc):null}
  const attrs=[],cls=[];
  for(const a of n.attributes){let name=a.name;if(name.startsWith('hint-'))continue;
    if(name==='style-hover'){cls.push(pcls('hover',a.value));continue}
    if(name==='style-active'){cls.push(pcls('active',a.value));continue}
    if(name==='onchange')name='oninput';
    attrs.push([name,interp(a.value)])}
  const cf=kids([...n.childNodes]);
  return sc=>{const props={};for(const[k,f]of attrs)props[k]=f(sc);if(cls.length)props.class=((props.class||'')+' '+cls.join(' ')).trim();return h(tag,props,cf(sc))}}
class DCLogic{constructor(p){this.props=p||{};this.state={}}
  setState(u){const patch=typeof u==='function'?u(this.state):u;if(patch)this.state={...this.state,...patch};dcSchedule()}}
let dcComp=null,dcRoot=null,dcQueued=false;
function dcSchedule(){if(dcQueued||!dcComp)return;dcQueued=true;Promise.resolve().then(()=>{dcQueued=false;dcDraw()})}
function dcDraw(){prender(h(Fragment,null,dcRoot(dcComp.renderVals())),document.getElementById('app'))}
"""

BOOT = r"""
dcRoot=kids([...document.getElementById('tpl').content.childNodes]);
{const st=document.createElement('style');st.textContent=pseudoCss;document.head.appendChild(st)}
{const vp='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover';let m=document.querySelector('meta[name=viewport]');if(!m){m=document.createElement('meta');m.name='viewport';document.head.appendChild(m)}m.content=vp;
 ['gesturestart','gesturechange'].forEach(t=>document.addEventListener(t,e=>e.preventDefault(),{passive:false}));
 document.addEventListener('touchmove',e=>{if(e.touches.length>1)e.preventDefault()},{passive:false})}

dcComp=new Component({showTWD:true});dcDraw();dcComp.componentDidMount();
"""

exec(open(os.path.join(HERE,'people_patch.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'loc_patch.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'legfix_patch.py'),encoding='utf-8').read())

head = """<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<title>Travel App 東京河口湖</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
/* Layout: the Claude Design phone prototype; on desktop it sits in a phone frame beside the notes, on phones it fills the screen. */
:root{--ink:#221f1a;--paper:#f7f4ef;--sand:#e8e3da;--muted:#6f685e;--accent:oklch(0.52 0.14 40);color-scheme:light}
body{margin:0;background:var(--sand);font-family:'Noto Sans TC','PingFang TC','Microsoft JhengHei',system-ui,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:var(--ink)}a:hover{color:oklch(0.55 0.14 40)}
input{font-family:inherit}
@keyframes up{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
.noscroll::-webkit-scrollbar{display:none}
.mobsim{display:none}
.screen *:not(input):not(textarea){-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-tap-highlight-color:transparent}
button:focus-visible,a:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;transition-duration:.01ms!important}}
@media (max-width:640px){
  html{box-sizing:border-box;height:100%}
  body,#app{height:100%}
  body{background:var(--paper)}
  .stage{display:block!important;padding:0!important;min-height:0!important;height:100%}
  .side{display:none!important}
  .frame{width:100%!important;height:100%!important;border-radius:0!important;padding:0!important;background:transparent!important;box-shadow:none!important}
  .screen{border-radius:0!important}
  .sbar{display:none!important}
  .sbar-sp{height:8px!important}
  .mobsim{display:flex}
  :root{padding-bottom:0!important}
  html,body{overflow:hidden;overscroll-behavior:none;touch-action:pan-x pan-y}
  .noscroll{-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
  input,textarea,select{font-size:16px!important}
  .navbar{height:56px!important;padding:0 10px max(4px,calc(env(safe-area-inset-bottom,0px) - 26px))!important;box-sizing:content-box}
}
</style>
"""

preact_url = "https://cdn.jsdelivr.net/npm/preact@10.24.3/dist/preact.min.umd.js"
out = head + '<template id="tpl">\n' + tpl + '</template>\n<div id="app"></div>\n<script src="' + preact_url + '"></script>\n<script>\n' + RUNTIME + S + BOOT + '</script>\n'
open(OUT, "w", encoding="utf-8").write(out)
print("ok", len(out))
