# --- Today screen while travelling (bang, 2026-11-05: fix everything found in the trip simulation) ---
# D1 stops up to the outbound flight are in Taiwan time (one hour behind Tokyo).
# The phone's location, when it is near one of today's stops, decides which stop counts as "here".
# Running late shows how late and offers to push the rest of the day back; a flight counts down to takeoff.
S = rep(S, """const nextIdx=tsch.findIndex(it=>it.at>NOW);
    const next=tsch[nextIdx], prevT=nextIdx>0?tsch[nextIdx-1]:null, pl=prevT&&prevT.leg;
    const leave=next?next.at-(prevT?prevT.lm:0):0;
    const left=Math.max(0,leave*60-NOWSEC);""",
"""const fi=TODAY===0?tsch.findIndex(x=>x.leg&&x.leg.mode==='flight'):-1,off=i=>fi>=0&&i<=fi?60:0;
    const hr=s.here,here=!preview&&hr&&hr.day===TODAY&&Date.now()-hr.ts<15*60e3&&tsch[hr.i]?hr.i:-1;
    let nextIdx=tsch.findIndex((it,i)=>it.at>NOW-off(i));if(here>=0&&(nextIdx<0||nextIdx<=here))nextIdx=here+1<tsch.length?here+1:-1;
    const next=tsch[nextIdx], prevT=nextIdx>0?tsch[nextIdx-1]:null, pl=prevT&&prevT.leg;
    const isFl=!!next&&/起飛/.test(next.title),nOff=next?off(nextIdx):0;
    const leave=next?(isFl?next.at:next.at-(prevT?prevT.lm:0)):0;
    const left=Math.max(0,(leave+nOff)*60-NOWSEC),lateM=next&&!preview&&!isFl?Math.max(0,NOW-nOff-leave):0;
    const fmtM=m=>m>=60?Math.floor(m/60)+'小時'+(m%60?(m%60)+'分':''):m+'分';""")
S = rep(S, "countdown:preview?(C.after?'—':String(C.daysLeft)):String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0'),",
  "countdown:preview?(C.after?'—':String(C.daysLeft)):!next?'—':lateM>0?'晚 '+fmtM(lateM):fmtM(Math.ceil(left/60)),")
S = rep(S, "cdUnit:preview?(C.after?'旅程已結束':'天後出發'):'後該出發',",
  "cdUnit:preview?(C.after?'旅程已結束':'天後出發'):!next?'':isFl?'後起飛':lateM>0?'該出發了':'後該出發',\n"
  "      leaveLabel:isFl?'起飛 '+ft(next.at):'建議出發 '+(next?ft(leave):'--:--')+(nOff?'（台灣時間）':''),\n"
  "      hasHere:here>=0,hereLabel:here>=0?'📍 你在「'+tsch[here].title+'」附近':'',\n"
  "      hasNote:!next||!!next.sub,\n"
  "      delayOpts:(preview?[]:[...(lateM>4?[lateM]:[]),10,30]).map(m=>({label:(m===lateM?'順延 ':'+')+m+' 分',onClick:()=>{this.setState(st=>({delay:st.delay+m}));this.flash('之後的行程都延後 '+m+' 分鐘')}})),")
S = rep(S, "nextNote:next?(next.sub||'沒有備註'):'今天的行程都完成了',", "nextNote:next?(next.sub||''):'今天的行程都完成了',")
# Translation needs AI, which this app does not have.
S = rep(S, "quick:[['翻','翻譯卡','translate',tc('交通')],", "quick:[")
tpl = rep(tpl, "grid-template-columns:repeat(4,minmax(0,1fr));gap:10px\">\n              <sc-for list=\"{{ quick }}\"", "grid-template-columns:repeat(3,minmax(0,1fr));gap:10px\">\n              <sc-for list=\"{{ quick }}\"")
tpl = rep(tpl, "建議出發 {{ leaveTime }}", "{{ leaveLabel }}")
tpl = rep(tpl, """<div style="font:700 24px/1.25 'Noto Sans TC',sans-serif">{{ nextTitle }}</div>""",
  """<div style="font:700 24px/1.25 'Noto Sans TC',sans-serif">{{ nextTitle }}</div>
              <sc-if value="{{ hasHere }}"><div style="font:500 12px 'Noto Sans TC';opacity:.92;margin-top:-8px">{{ hereLabel }}</div></sc-if>""")
_k = tpl.index('<button onClick="{{ delay30 }}"'); _e = tpl.index('</button>', _k) + 9
tpl = tpl[:_k] + """<sc-for list="{{ delayOpts }}" as="o" hint-placeholder-count="2"><button onClick="{{ o.onClick }}" style="flex:none;height:46px;padding:0 11px;border:1px solid rgba(255,255,255,.5);border-radius:13px;background:transparent;color:#fff;font:500 13px 'Noto Sans TC';cursor:pointer;white-space:nowrap">{{ o.label }}</button></sc-for>""" + tpl[_e:]
_k = tpl.index("""<div style="border:1px solid oklch(0.62 0.12 85);background:oklch(0.97 0.025 85);border-radius:14px;padding:12px 14px;display:flex;gap:10px">"""); _e = tpl.index('</div>', _k) + 6
tpl = tpl[:_k] + '<sc-if value="{{ hasNote }}">' + tpl[_k:_e] + '</sc-if>' + tpl[_e:]
# Where are we: check the phone's location when the app opens, comes back to the screen, and every 3 minutes during the trip.
S = rep(S, "  componentDidMount(){\n    this.iv=setInterval(()=>this.tick(),1000);",
"""  async whereAmI(){if(this.state.mode!=='trip'||this.state.sim||typeof getPlData!=='function')return;const g=await getLoc();if(g.err)return;
    const P=await getPlData(),G=P.stops||{},C=clockOf(null,0),sch=this.sched(C.today);let best=null;
    sch.forEach((it,i)=>{const p=typeof stopGeo==='function'?stopGeo(it,G):null;if(!p)return;const d=distM(g,p);if(d<=Math.max(350,g.acc||0)&&(!best||d<best.d))best={i,d}});
    this.setState({here:best?{day:C.today,i:best.i,ts:Date.now()}:null})}
  componentDidMount(){
    this.iv=setInterval(()=>this.tick(),1000);setTimeout(()=>this.whereAmI(),1500);this.geoIv=setInterval(()=>this.whereAmI(),180000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)this.whereAmI()});""")

# The first snapshot can come from the phone's offline cache and be out of date; only write load-time repairs back when the data came from the server,
# otherwise an old cached copy overwrites everyone's newer plan.
S = rep(S, "if(d&&JSON.stringify(days)!==before)this.savePlan()},warn);", "if(d&&!snap.metadata.fromCache&&JSON.stringify(days)!==before)this.savePlan()},warn);")
