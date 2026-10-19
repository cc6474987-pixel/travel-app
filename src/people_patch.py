# --- Editable members (ids stay stable; names can change) ---
S = rrep(S, r"const PEOPLE=\[\['我',40\].*?;\nconst ALL=PEOPLE\.map\(p=>p\.n\);", """const HUES=[40,165,255,85,300,340,200,20,120,280];
const mkPeople=l=>l.map((p,k)=>({id:p.id,n:p.n,bg:'oklch(0.5 0.12 '+(p.hu!=null?p.hu:HUES[k%HUES.length])+')'}));
const PEOPLE0=[['我',40],['阿哲',165],['小安',255],['Mei',85],['阿凱',300],['Ken',340]].map(([n,hu])=>({id:n,n,hu}));
let PEOPLE=mkPeople(PEOPLE0),ALL=PEOPLE.map(p=>p.id);
const NM=id=>{const p=PEOPLE.find(x=>x.id===id);return p?(p.n||'?'):String(id||'?')};
const setPeopleG=l=>{PEOPLE=mkPeople(l);ALL=PEOPLE.map(p=>p.id)};""")
S = rep(S, "L=lsGet();\n    this.state={sim:null,", "L=lsGet();if(Array.isArray(L.people)&&L.people.length)setPeopleG(L.people);\n    this.state={people:Array.isArray(L.people)&&L.people.length?L.people:PEOPLE0,newName:'',sim:null,")
S = S.replace("payer:'我'", "payer:ALL[0]")
S = rep(S, "  addSettled(x){", """  applyPeople(l){setPeopleG(l);this.setState(st=>{const wasAll=st.people.every(p=>st.form.with.includes(p.id));const w=wasAll?ALL.slice():st.form.with.filter(id=>ALL.includes(id));
    return{people:l,form:{...st.form,with:w,payer:ALL.includes(st.form.payer)?st.form.payer:ALL[0]}}})}
  setPeople(l){this.applyPeople(l);this.pplBusy=true;clearTimeout(this.pplT);
    this.pplT=setTimeout(()=>{if(this.db)this.write(()=>this.db.doc('shared/people').set({list:l}).finally(()=>{this.pplBusy=false}));else{lsSet({people:l});this.pplBusy=false}},500)}
  addSettled(x){""")
S = rep(S, "    db.collection('settled').onSnapshot(", """    db.doc('shared/people').onSnapshot(snap=>{if(this.pplBusy||snap.metadata.hasPendingWrites)return;const d=snap.exists?snap.data():null;if(d&&Array.isArray(d.list)&&d.list.length)this.applyPeople(d.list)},warn);
    db.collection('settled').onSnapshot(""")
S = rep(S, "this.flash(e.payer+' 剛記了一筆", "this.flash(NM(e.payer)+' 剛記了一筆")
S = rep(S, "const balances=PEOPLE.map(p=>{const v=net[p.n],z=Math.abs(v)<1;return{name:p.n,", "const balances=PEOPLE.map(p=>{const v=net[p.id]||0,z=Math.abs(v)<1;return{id:p.id,name:p.n||'?',")
S = rep(S, "i:p.n.slice(0,1),bg:p.bg,v,net:", "i:(p.n||'?').slice(0,1),bg:p.bg,v,net:")
S = rep(S, "balances.filter(b=>b.v>1).map(b=>({n:b.name,v:b.v}))", "balances.filter(b=>b.v>1).map(b=>({n:b.id,v:b.v}))")
S = rep(S, "balances.filter(b=>b.v<-1).map(b=>({n:b.name,v:-b.v}))", "balances.filter(b=>b.v<-1).map(b=>({n:b.id,v:-b.v}))")
S = rep(S, "s.exps.forEach(e=>{const w=e.with&&e.with.length?e.with:ALL;net[e.payer]+=e.amt;w.forEach(n=>net[n]-=e.amt/w.length)});",
           "s.exps.forEach(e=>{const w=e.with&&e.with.length?e.with:ALL;net[e.payer]=(net[e.payer]||0)+e.amt;w.forEach(n=>net[n]=(net[n]||0)-e.amt/w.length)});")
S = rep(S, "s.settled.forEach(x=>{net[x.from]+=x.amt;net[x.to]-=x.amt});", "s.settled.forEach(x=>{net[x.from]=(net[x.from]||0)+x.amt;net[x.to]=(net[x.to]||0)-x.amt});")
S = rep(S, "const bgOf=n=>PEOPLE.find(p=>p.n===n).bg;", "const bgOf=n=>(PEOPLE.find(p=>p.id===n)||{bg:'oklch(0.6 0 0)'}).bg;")
S = rep(S, "avatars:PEOPLE.map(p=>({i:p.n.slice(0,1),bg:p.bg})),", "avatars:PEOPLE.map(p=>({i:(p.n||'?').slice(0,1),bg:p.bg})),")
S = rep(S, "transfers:tr.map(x=>({...x,fromI:x.from.slice(0,1),toI:x.to.slice(0,1),", "transfers:tr.map(x=>({...x,from:NM(x.from),to:NM(x.to),fromI:NM(x.from).slice(0,1),toI:NM(x.to).slice(0,1),")
S = rep(S, "this.flash('已標記：'+x.from+' → '+x.to+' '+M(x.amt))", "this.flash('已標記：'+NM(x.from)+' → '+NM(x.to)+' '+M(x.amt))")
S = rep(S, "this.remind(x.from+' 請付 '+M(x.amt)+' 給 '+x.to+", "this.remind(NM(x.from)+' 請付 '+M(x.amt)+' 給 '+NM(x.to)+")
S = rep(S, "settledList:s.settled.map(x=>({...x,amt:M(x.amt)}))", "settledList:s.settled.map(x=>({...x,from:NM(x.from),to:NM(x.to),amt:M(x.amt)}))")
S = rep(S, "就能讓 6 人打平", "就能讓 '+ALL.length+' 人打平")
S = rep(S, "e.payer+' 付 · '+(w.length===ALL.length?ALL.length+' 人均分':w.join('、')+' 分')", "NM(e.payer)+' 付 · '+(w.length===ALL.length&&ALL.every(id=>w.includes(id))?ALL.length+' 人均分':w.map(NM).join('、')+' 分')")
S = rep(S, "payerChips:PEOPLE.map(p=>chip(f.payer,p.n,'payer')),", "payerChips:PEOPLE.map(p=>({...chip(f.payer,p.id,'payer'),label:p.n||'?'})),")
S = rep(S, "withChips:PEOPLE.map(p=>{const on=f.with.includes(p.n);return{label:p.n,",
  "withChips:[(()=>{const on=f.with.length===ALL.length;return{label:'全部',bg:on?INK:'#fffdf9',color:on?'#fff':INK,border:on?INK:'rgba(34,31,26,.15)',onClick:()=>this.setState(st=>({form:{...st.form,with:st.form.with.length===ALL.length?[]:ALL.slice()},errs:{...st.errs,with:''}}))}})()].concat(PEOPLE.map(p=>{const on=f.with.includes(p.id);return{label:p.n||'?',")
S = rep(S, "st.form.with.includes(p.n)?st.form.with.filter(x=>x!==p.n):ALL.filter(x=>x===p.n||st.form.with.includes(x));return{form:{...st.form,with:w},errs:{...st.errs,with:''}}})}}),",
           "st.form.with.includes(p.id)?st.form.with.filter(x=>x!==p.id):ALL.filter(x=>x===p.id||st.form.with.includes(x));return{form:{...st.form,with:w},errs:{...st.errs,with:''}}})}})),")
S = rep(S, "幫 6 位台灣旅客", "幫 '+ALL.length+' 位台灣旅客")
S = rep(S, "exp:sheet==='exp'}", "exp:sheet==='exp',people:sheet==='people'}")
S = rep(S, "stopClick:e=>e.stopPropagation(),", """stopClick:e=>e.stopPropagation(),nPeople:ALL.length,openPeople:()=>this.setState({sheet:'people'}),
      peopleRows:s.people.map((p,k)=>{const used=s.exps.some(e=>e.payer===p.id||(e.with||[]).includes(p.id))||s.settled.some(x=>x.from===p.id||x.to===p.id);
        return{n:p.n,bg:PEOPLE[k]?PEOPLE[k].bg:'#999',delLabel:used?'有帳目':'刪除',delOp:used||s.people.length<=1?.35:1,
          onName:e=>{const v=e.target.value.slice(0,12);this.setPeople(this.state.people.map(x=>x.id===p.id?{...x,n:v}:x))},
          onDel:()=>{if(used)return this.flash((p.n||'這位')+' 還有帳目，先刪掉相關帳目才能移除');if(this.state.people.length<=1)return;this.setPeople(this.state.people.filter(x=>x.id!==p.id));this.flash('已移除 '+(p.n||''))}}}),
      setNewName:e=>this.setState({newName:e.target.value.slice(0,12)}),
      addPerson:()=>{const n=(this.state.newName||'').trim();if(!n)return;const l=this.state.people,used=l.map(x=>x.hu),hu=HUES.find(h=>!used.includes(h));
        this.setPeople([...l,{id:'p'+Date.now().toString(36),n,hu:hu!=null?hu:(l.length*47)%360}]);this.setState({newName:''});this.flash('已新增 '+n)},
      newKey:e=>{if(e.key==='Enter')e.target.blur()},""")
# templates
tpl = rep(tpl, "2026.11.11 – 11.17 · 6 人</div>", "2026.11.11 – 11.17 · {{ nPeople }} 人</div>")
tpl = rep(tpl, """<div style="display:flex;flex:none;padding:4px 0 0 10px">""", """<div onClick="{{ openPeople }}" title="編輯成員" style="display:flex;flex:none;padding:4px 0 0 10px;cursor:pointer">""")
tpl = rep(tpl, "共同支出 · 6 人</span>", """共同支出 · {{ nPeople }} 人 <button onClick="{{ openPeople }}" style="border:0;background:transparent;padding:0 0 0 4px;font:500 12px 'Noto Sans TC';color:oklch(0.52 0.14 40);cursor:pointer;text-decoration:underline">編輯成員</button></span>""")
for key in ("payerChips", "withChips"):
    tpl = rep(tpl, '<div style="display:flex;gap:8px">\n                    <sc-for list="{{ %s }}" as="c" hint-placeholder-count="4">\n                      <button onClick="{{ c.onClick }}" style="flex:1;height:40px;' % key,
                   '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px">\n                    <sc-for list="{{ %s }}" as="c" hint-placeholder-count="4">\n                      <button onClick="{{ c.onClick }}" style="flex:1 0 62px;height:40px;' % key)
tpl = rep(tpl, '            <sc-if value="{{ sh.exp }}">', """            <sc-if value="{{ sh.people }}">
              <div style="display:flex;flex-direction:column;gap:12px">
                <div style="font:700 20px 'Noto Sans TC',sans-serif">成員 · {{ nPeople }} 人</div>
                <sc-for list="{{ peopleRows }}" as="r" hint-placeholder-count="3">
                  <div style="display:flex;align-items:center;gap:10px">
                    <span style="width:14px;height:14px;border-radius:50%;background:{{ r.bg }};flex:none"></span>
                    <input value="{{ r.n }}" onChange="{{ r.onName }}" onKeyDown="{{ newKey }}" placeholder="名字" style="flex:1;min-width:0;height:44px;border-radius:12px;border:1.5px solid rgba(34,31,26,.15);background:#fffdf9;padding:0 12px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none">
                    <button onClick="{{ r.onDel }}" style="flex:none;height:44px;padding:0 12px;border:1px solid rgba(34,31,26,.15);border-radius:12px;background:transparent;color:#221f1a;font:500 13px 'Noto Sans TC';cursor:pointer;opacity:{{ r.delOp }}">{{ r.delLabel }}</button>
                  </div>
                </sc-for>
                <div style="display:flex;gap:8px">
                  <input value="{{ newName }}" onChange="{{ setNewName }}" placeholder="新成員名字" style="flex:1;min-width:0;height:44px;border-radius:12px;border:1.5px dashed rgba(34,31,26,.25);background:#fffdf9;padding:0 12px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none">
                  <button onClick="{{ addPerson }}" style="flex:none;height:44px;padding:0 16px;border:0;border-radius:12px;background:#221f1a;color:#fff;font:600 14px 'Noto Sans TC';cursor:pointer">＋ 新增</button>
                </div>
                <span style="font:400 12px/1.6 'Noto Sans TC';color:#6f685e">改名會套用到所有帳目，大家看到的名字會一起更新。有帳目的人要先刪掉相關帳目才能移除。</span>
              </div>
            </sc-if>
            <sc-if value="{{ sh.exp }}">""")
