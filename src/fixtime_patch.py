# --- Fixed arrival times: a stop with it.fix ('HH:MM') starts at that time no matter how earlier stops change ---
# Earlier stays and moves only use up the gap before it; if they run past it, the stop is flagged as late instead of moving.
S = rep(S, "const out=d.items.map((it,i)=>{const at=t+(it.wait||0),lm=it.leg?mins(it.leg):0;t=at+it.stay+(i<n-1?lm:0);return{...it,at,dep:at+it.stay,lm}});",
  "const out=d.items.map((it,i)=>{const fx=it.fix?tm(it.fix):null,at=fx!=null?Math.max(t,fx):t+(it.wait||0),late=fx!=null&&t>fx?t-fx:0,gap=at-t,lm=it.leg?mins(it.leg):0;t=at+it.stay+(i<n-1?lm:0);return{...it,at,dep:at+it.stay,lm,late,gap}});")
# Older plans kept fixed times as a manual gap (wait); turn each such gap into a fixed time at the time it shows now.
S = rep(S, "const getLoc=()=>", r"""const pinWaits=d=>{let t=tm(d.start||'09:00');const n=d.items.length;d.items.forEach((it,i)=>{const fx=it.fix?tm(it.fix):null,at=fx!=null?Math.max(t,fx):t+(it.wait||0);
  if(!it.fix&&(it.wait||0)>4){it.fix=ft(at);it.wait=0}else if(it.fix&&it.wait)it.wait=0;t=at+it.stay+(i<n-1&&it.leg?mins(it.leg):0)})};
const getLoc=()=>""")
S = rep(S, "days.forEach(x=>this.relink(x.items));", "days.forEach(x=>{this.relink(x.items);pinWaits(x)});")
# Lateness shows the same way as the closing-time warning.
S = rep(S, "const warnOf=it=>it.close&&", "const warnOf=it=>it.late>0?{short:'比固定的 '+it.fix+' 晚 '+it.late+' 分',long:'照前面的停留和移動，會在 '+ft(it.at)+' 才到，比固定的 '+it.fix+' 晚 '+it.late+' 分。可以縮短前面的停留，或改這站的固定時間。'}:it.close&&")
S = rep(S, "fix:()=>{if(w){this.setStay(di,i,w.fix);this.flash('已調整停留為 '+w.fix+' 分')}}", "fix:()=>{if(w&&w.fix){this.setStay(di,i,w.fix);this.flash('已調整停留為 '+w.fix+' 分')}},hasFixBtn:!!(w&&w.fix)")
_k = tpl.index('<button onClick="{{ sel.fix }}"'); _e = tpl.index('</button>', _k) + 9
tpl = tpl[:_k] + '<sc-if value="{{ sel.hasFixBtn }}">' + tpl[_k:_e] + '</sc-if>' + tpl[_e:]
S = rep(S, "hasWait:!!(nxt&&nxt.wait>4),wait:nxt?nxt.wait:0,", "hasWait:!!(nxt&&nxt.gap>4),wait:nxt?nxt.gap:0,")
S = rep(S, "stayLabel:[it.rating?'★'+it.rating:'',it.stay?'停留 '+it.stay+' 分':''].filter(Boolean).join(' · ')",
  "stayLabel:[it.fix?'📌 固定 '+it.fix:'',it.rating?'★'+it.rating:'',it.stay?'停留 '+it.stay+' 分':''].filter(Boolean).join(' · ')")
S = rep(S, "selV={...it,color:tc(it.type),span:ft(it.at)+' 抵達 · '+ft(it.dep)+' 離開',stay:it.stay,",
  "selV={...it,color:tc(it.type),span:ft(it.at)+' 抵達 · '+ft(it.dep)+' 離開',stay:it.stay,\n"
  "        isFix:!!it.fix,notFix:!it.fix,fixVal:it.fix||ft(it.at),fixNote:it.fix?'固定在 '+it.fix+' 抵達，前面怎麼改都不會推動這站':'目前跟著前一站推算，設定後就固定在這個時間',\n"
  "        setFix:e=>{const v=e.target.value;if(!/^\\d\\d:\\d\\d$/.test(v))return;this.edit(di,l=>{l[i].fix=v;l[i].wait=0});this.flash('已固定在 '+v+' 抵達')},\n"
  "        pinNow:()=>{const v=ft(it.at);this.edit(di,l=>{l[i].fix=v;l[i].wait=0});this.flash('已固定在 '+v+' 抵達')},\n"
  "        clrFix:()=>{this.edit(di,l=>{delete l[i].fix;l[i].wait=0});this.flash('已取消固定，改跟著前一站推算')},")
_i = tpl.index("""<span style="font:500 12px 'Noto Sans TC';color:#6f685e">停留時間</span>""")
_j = tpl.rindex('<div style="display:flex;flex-direction:column;gap:10px;background:#fffdf9', 0, _i)
tpl = tpl[:_j] + """<div style="display:flex;flex-direction:column;gap:10px;background:#fffdf9;border:1px solid rgba(34,31,26,.1);border-radius:16px;padding:14px">
                  <span style="font:500 12px 'Noto Sans TC';color:#6f685e">抵達時間</span>
                  <div style="display:flex;align-items:center;gap:10px">
                    <input id="fix-in" type="time" value="{{ sel.fixVal }}" onChange="{{ sel.setFix }}" style="height:44px;border-radius:12px;border:1.5px solid rgba(34,31,26,.18);background:#fffdf9;padding:0 12px;font:600 17px 'JetBrains Mono',monospace;color:#221f1a;outline:none">
                    <sc-if value="{{ sel.isFix }}"><button onClick="{{ sel.clrFix }}" style="height:40px;padding:0 12px;border-radius:11px;border:1px solid rgba(34,31,26,.18);background:transparent;font:500 13px 'Noto Sans TC';color:#221f1a;cursor:pointer">取消固定</button></sc-if>
                    <sc-if value="{{ sel.notFix }}"><button onClick="{{ sel.pinNow }}" style="height:40px;padding:0 12px;border-radius:11px;border:0;background:#221f1a;font:500 13px 'Noto Sans TC';color:#fff;cursor:pointer">固定這個時間</button></sc-if>
                  </div>
                  <div style="font:400 12px/1.5 'Noto Sans TC';color:#4d473f">{{ sel.fixNote }}</div>
                </div>
                """ + tpl[_j:]

# --- 順路建議 card removed ---
S = rep(S, "aiDone:{},catTouched", "aiDone:(()=>{try{return JSON.parse(localStorage.getItem('trip-aidone')||'{}')}catch(e){return {}}})(),catTouched")
# bang (2026-11-05): the 順路建議 card is not wanted at all.
S = rep(S, "showAi:!!ai&&!s.aiDone[s.day],", "showAi:false,")

# --- After an automatic update reload, come back to the same tab and day ---
BOOT = rep(BOOT, "dcComp.componentDidMount();", "dcComp.componentDidMount();\ntry{const r=JSON.parse(sessionStorage.getItem('trip-resume')||'null');if(r){sessionStorage.removeItem('trip-resume');dcComp.setState(r)}}catch(e){}")
