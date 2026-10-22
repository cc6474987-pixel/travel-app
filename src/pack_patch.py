# --- Packing list: anyone can add their own items to a category (collection 'packitems'); deleting one asks for the admin password every time ---
S = rep(S, "checked:L.checked||{}", "checked:L.checked||{},packX:L.packX||[],packNew:{}")
S = rep(S, "db.doc('shared/pack').onSnapshot(", "db.collection('packitems').onSnapshot(qs=>{this.setState({packX:qs.docs.map(d=>({...d.data(),id:d.id})).sort((a,b)=>(a.ts||0)-(b.ts||0))})},warn);\n    db.doc('shared/pack').onSnapshot(")
S = rep(S, "  togglePack(k){", r"""  addPackItem(ci,v){const l=(v!=null?v:((this.state.packNew||{})[ci]||'')).trim().slice(0,40);if(!l)return;const x={cat:PACK[ci].name,l,w:'',ts:Date.now()};
    this.setState(st=>({packNew:{...st.packNew,[ci]:''}}));
    if(this.db){const ref=this.db.collection('packitems').doc();this.setState(st=>({packX:[...st.packX,{...x,id:ref.id}]}));this.write(()=>ref.set(x))}
    else{const px=[...this.state.packX,{...x,id:'l'+x.ts}];this.setState({packX:px});lsSet({packX:px})}this.flash('已新增「'+l+'」')}
  delPackItem(id,l){askAdmin('刪除清單項目「'+l+'」要先輸入管理密碼。',()=>{const checked={...this.state.checked};delete checked['x-'+id];
    this.setState(st=>({packX:st.packX.filter(x=>x.id!==id),checked}));
    if(this.db){this.write(()=>this.db.collection('packitems').doc(id).delete());this.write(()=>this.db.doc('shared/pack').set({checked}))}else lsSet({packX:this.state.packX.filter(x=>x.id!==id),checked});this.flash('已刪除「'+l+'」')},true)}
  togglePack(k){""")
S = rep(S, "const pack=PACK.map((c,ci)=>({name:c.name,items:c.items.map(([l,w],pi)=>({l,w,d:!!s.checked[ci+'-'+pi]}))})),",
  "const pack=PACK.map((c,ci)=>({name:c.name,items:c.items.map(([l,w],pi)=>({l,w,k:ci+'-'+pi,d:!!s.checked[ci+'-'+pi]})).concat((s.packX||[]).filter(x=>x.cat===c.name).map(x=>({l:x.l,w:x.w||'',k:'x-'+x.id,d:!!s.checked['x-'+x.id],xid:x.id})))})),")
S = rep(S, "packCats:pack.map((c,ci)=>({name:c.name,items:c.items.map((p,pi)=>({label:p.l,who:p.w,",
  "packCats:pack.map((c,ci)=>({name:c.name,newVal:(s.packNew||{})[ci]||'',setNew:e=>{const v=e.target.value;this.setState(st=>({packNew:{...st.packNew,[ci]:v}}))},newKey:e=>{if(e.key==='Enter')this.addPackItem(ci,e.target.value)},add:()=>this.addPackItem(ci),\n        items:c.items.map((p,pi)=>({label:p.l,who:p.w,isX:!!p.xid,onDel:e=>{e.stopPropagation();this.delPackItem(p.xid,p.l)},")
S = rep(S, "onClick:()=>this.togglePack(ci+'-'+pi)}))})),", "onClick:()=>this.togglePack(p.k)}))})),")
tpl = rep(tpl, """                      <span style="font:400 11px 'Noto Sans TC';color:#6f685e">{{ p.who }}</span>
                    </div>
                  </sc-for>""", """                      <span style="font:400 11px 'Noto Sans TC';color:#6f685e">{{ p.who }}</span>
                      <sc-if value="{{ p.isX }}"><button onClick="{{ p.onDel }}" style="flex:none;border:0;background:transparent;padding:2px 2px 2px 6px;font:500 12px 'Noto Sans TC';color:#9a8f82;cursor:pointer">刪除</button></sc-if>
                    </div>
                  </sc-for>
                  <div style="display:flex;gap:8px;padding:8px 10px 10px 14px">
                    <input value="{{ c.newVal }}" onChange="{{ c.setNew }}" onKeyDown="{{ c.newKey }}" placeholder="＋ 新增項目" style="flex:1;min-width:0;height:38px;border-radius:10px;border:1.5px dashed rgba(34,31,26,.22);background:transparent;padding:0 10px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none">
                    <button onClick="{{ c.add }}" style="flex:none;height:38px;padding:0 12px;border:0;border-radius:10px;background:#221f1a;color:#fff;font:500 13px 'Noto Sans TC';cursor:pointer">新增</button>
                  </div>""")
