# --- Edit times by tapping them (bang, 2026-11-08: "我想要改幾點出發幾點離開都做不到"; chose 點時間直接改) ---
# Tapping the time on a timeline card opens a small sheet with arrival and departure, as 24-hour hour/minute pickers.
# Arrival pins the stop (fix); on the first stop of a day it changes the day's start instead. Departure sets the stay length.
_H=''.join(f'<option value="{h:02d}">{h:02d}</option>' for h in range(24))
_M=''.join(f'<option value="{m:02d}">{m:02d}</option>' for m in range(60))
_SEL="height:52px;border-radius:12px;border:1.5px solid rgba(34,31,26,.18);background:#fffdf9;padding:0 10px;font:600 22px 'JetBrains Mono',monospace;color:#221f1a;outline:none;-webkit-appearance:none;appearance:none;text-align:center;min-width:70px"
def picker(k):
    return ('<div style="display:flex;align-items:center;gap:6px"><select value="{{ tv.'+k+'H }}" onChange="{{ tv.'+k+'SetH }}" style="'+_SEL+'">'+_H+'</select>'
      '<span style="font:700 22px \'JetBrains Mono\',monospace">:</span><select value="{{ tv.'+k+'M }}" onChange="{{ tv.'+k+'SetM }}" style="'+_SEL+'">'+_M+'</select></div>')
S = rep(S, "return{...it,time:ft(it.at),", "return{...it,time:ft(it.at),openTime:e=>{e.stopPropagation();this.setState({sheet:'time',tsel:{di,i}})},")
S = rep(S, "people:sheet==='people'},", "people:sheet==='people',time:sheet==='time'&&!!timeV},")
S = rep(S, "      sel:selV,\n", r"""      sel:selV,tv:timeV||{},
""")
S = rep(S, "    const d=s.drag;\n", r"""    const d=s.drag;
    let timeV=null;if(s.sheet==='time'&&s.tsel&&s.days[s.tsel.di]){const{di:tdi,i:ti}=s.tsel,tsc=this.sched(tdi),it=tsc[ti];
      if(it){const first=ti===0,last=ti===tsc.length-1,a=ft(it.at),dp=ft(it.dep),nx=tsc[ti+1];
        const setA=v=>{if(first){this.setState(st=>{const days=clone(st.days);days[tdi].start=v;return{days}});this.savePlan();this.flash('這天改成 '+v+' 出發')}
          else{this.edit(tdi,l=>{l[ti].fix=v;l[ti].wait=0});this.flash('固定在 '+v+' 抵達')}};
        const setD=v=>{const n=tm(v)-it.at;if(n<0)return this.flash('離開不能早於抵達 '+a);this.setStay(tdi,ti,n);this.flash(v+' 離開，停留 '+n+' 分')};
        timeV={title:it.title,first,notFirst:!first,showDep:!last,arrLabel:first?'出發時間（這天的第一站）':'抵達時間',
          aH:a.slice(0,2),aM:a.slice(3),dH:dp.slice(0,2),dM:dp.slice(3),
          aSetH:e=>setA(e.target.value+':'+a.slice(3)),aSetM:e=>setA(a.slice(0,2)+':'+e.target.value),
          dSetH:e=>setD(e.target.value+':'+dp.slice(3)),dSetM:e=>setD(dp.slice(0,2)+':'+e.target.value),
          isFix:!first&&!!it.fix,clr:()=>{this.edit(tdi,l=>{delete l[ti].fix;l[ti].wait=0});this.flash('已取消固定，改跟著前一站推算')},
          note:first?'改了之後，這天後面的時間會一起往前或往後移':it.fix?'📌 已固定在 '+it.fix+' 抵達，前面怎麼改都不會推動這站':'改抵達時間會把這站固定在那個時間；前面的行程改了也不會推動它',
          stayTxt:'停留 '+it.stay+' 分',nextTxt:nx?'下一站「'+nx.title+'」'+ft(nx.at)+' 抵達':'這天的最後一站',
          lateTxt:it.late>0?'照前面的安排會晚 '+it.late+' 分才到':'',hasLate:it.late>0,
          openStop:()=>this.setState({sheet:'stop',sel:{di:tdi,i:ti}})}}}
""")
tpl = rep(tpl, """<div style="width:44px;flex:none;padding-top:15px;font:600 13px 'JetBrains Mono',monospace;opacity:{{ it.opacity }}">{{ it.time }}</div>""",
  """<div onClick="{{ it.openTime }}" style="width:48px;flex:none;padding-top:13px;cursor:pointer;opacity:{{ it.opacity }}"><span style="display:inline-block;font:700 14px 'JetBrains Mono',monospace;color:#221f1a;border-bottom:1.5px dashed rgba(34,31,26,.35);padding-bottom:1px">{{ it.time }}</span></div>""")
tpl = rep(tpl, """            <sc-if value="{{ sh.people }}">""", """            <sc-if value="{{ sh.time }}">
              <div style="display:flex;flex-direction:column;gap:14px">
                <div style="font:700 20px/1.3 'Noto Sans TC',sans-serif">{{ tv.title }}</div>
                <div style="display:flex;flex-direction:column;gap:8px">
                  <span style="font:600 13px 'Noto Sans TC';color:#4d473f">{{ tv.arrLabel }}</span>
                  <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">""" + picker('a') + """
                    <sc-if value="{{ tv.isFix }}"><button onClick="{{ tv.clr }}" style="height:44px;padding:0 12px;border-radius:11px;border:1px solid rgba(34,31,26,.18);background:transparent;font:500 13px 'Noto Sans TC';color:#221f1a;cursor:pointer">取消固定</button></sc-if>
                  </div>
                  <sc-if value="{{ tv.hasLate }}"><div style="font:600 12.5px 'Noto Sans TC';color:oklch(0.48 0.14 35)">! {{ tv.lateTxt }}</div></sc-if>
                </div>
                <sc-if value="{{ tv.showDep }}">
                  <div style="display:flex;flex-direction:column;gap:8px">
                    <span style="font:600 13px 'Noto Sans TC';color:#4d473f">離開時間 · {{ tv.stayTxt }}</span>
                    """ + picker('d') + """
                  </div>
                </sc-if>
                <div style="font:400 12.5px/1.6 'Noto Sans TC';color:#4d473f;background:#fffdf9;border:1px solid rgba(34,31,26,.1);border-radius:12px;padding:10px 12px">{{ tv.note }}<br>{{ tv.nextTxt }}</div>
                <button onClick="{{ tv.openStop }}" style="height:46px;border-radius:13px;border:1px solid rgba(34,31,26,.18);background:transparent;font:500 14px 'Noto Sans TC';color:#221f1a;cursor:pointer">看這站的詳細資料</button>
              </div>
            </sc-if>

            <sc-if value="{{ sh.people }}">""")
# The stop sheet's 12-hour time input becomes a button into the same picker.
tpl = rep(tpl, """<input id="fix-in" type="time" value="{{ sel.fixVal }}" onChange="{{ sel.setFix }}" style="height:44px;border-radius:12px;border:1.5px solid rgba(34,31,26,.18);background:#fffdf9;padding:0 12px;font:600 17px 'JetBrains Mono',monospace;color:#221f1a;outline:none">""",
  """<button id="fix-in" onClick="{{ sel.openTime }}" style="height:44px;border-radius:12px;border:1.5px solid rgba(34,31,26,.18);background:#fffdf9;padding:0 14px;font:600 17px 'JetBrains Mono',monospace;color:#221f1a;cursor:pointer">{{ sel.fixVal }} ✎</button>""")
S = rep(S, "isFix:!!it.fix,notFix:!it.fix,fixVal:it.fix||ft(it.at),", "isFix:!!it.fix,notFix:!it.fix,fixVal:it.fix||ft(it.at),openTime:()=>this.setState({sheet:'time',tsel:{di,i}}),")

# --- Clean-up (bang chose 全部拿掉): no AI planner button, no placeholder map or photo, countdown as one line, notes one line ---
_k = tpl.index('<button onClick="{{ openPlanner }}"'); _e = tpl.index('</button>', _k) + 9; tpl = tpl[:_k] + tpl[_e:]
tpl = rep(tpl, """<div style="display:flex;align-items:center;justify-content:space-between;background:#221f1a;color:#f7f4ef;border-radius:16px;padding:14px 16px">
              <span style="font:500 13px 'Noto Sans TC'">{{ statusLabel }}</span>
              <span style="font:600 18px 'JetBrains Mono',monospace">{{ statusValue }}</span>
            </div>""", """<div style="font:600 13px 'Noto Sans TC';color:#4d473f;margin-top:-8px">{{ statusLabel }} <b style="font:700 14px 'JetBrains Mono',monospace;color:oklch(0.52 0.14 40)">{{ statusValue }}</b></div>""")
_k = tpl.index('<a href="{{ dayMapUrl }}"'); _e = tpl.index('</a>', _k) + 4
tpl = tpl[:_k] + """<a href="{{ dayMapUrl }}" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:11px 14px;border-radius:14px;border:1px solid rgba(34,31,26,.12);background:#fffdf9;text-decoration:none;color:#221f1a">
              <span style="font:600 14px 'Noto Sans TC';flex:none">🗺 當日路線</span>
              <span style="flex:1;min-width:0;font:400 12px 'Noto Sans TC';color:#4d473f;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ dayStats }}</span>
              <span style="flex:none;color:#6f685e">↗</span>
            </a>""" + tpl[_e:]
tpl = rep(tpl, "長按卡片拖曳排序 · 放開後時間自動重排", "點左邊的時間可以改抵達／離開 · 按住 ⋮⋮ 拖曳排序")
_k = tpl.index("""<div style="height:110px;border-radius:16px;background:repeating-linear-gradient(135deg,#efe9df 0 10px,#e8e1d5 10px 20px);display:flex;align-items:center;justify-content:center;font:500 11px 'JetBrains Mono',monospace;color:#6f685e">照片：{{ sel.title }}</div>"""); _e = tpl.index('</div>', _k) + 6
tpl = tpl[:_k] + tpl[_e:]
tpl = rep(tpl, """<div style="font:400 12px/1.5 'Noto Sans TC';color:#6f685e;margin-top:1px;display:-webkit-box;-webkit-line-clamp:2;""", """<div style="font:400 12.5px/1.5 'Noto Sans TC';color:#5c554c;margin-top:2px;display:-webkit-box;-webkit-line-clamp:1;""")

# --- Small style pass (bang chose 小幅調整): bigger titles, darker secondary text ---
tpl = rep(tpl, """<div style="font:600 15px/1.35 'Noto Sans TC';margin-top:3px">{{ it.title }}</div>""", """<div style="font:700 16px/1.35 'Noto Sans TC';margin-top:3px;color:#221f1a">{{ it.title }}</div>""")
tpl = rep(tpl, """<span style="font:500 11px 'Noto Sans TC';color:{{ it.color }};white-space:nowrap">{{ it.type }}</span>""", """<span style="font:600 11.5px 'Noto Sans TC';color:{{ it.color }};white-space:nowrap">{{ it.type }}</span>""")
tpl = rep(tpl, """<span style="margin-left:auto;font:500 11px 'JetBrains Mono',monospace;color:#6f685e;white-space:nowrap">{{ it.stayLabel }}</span>""", """<span style="margin-left:auto;font:500 11.5px 'Noto Sans TC';color:#4d473f;white-space:nowrap">{{ it.stayLabel }}</span>""")
