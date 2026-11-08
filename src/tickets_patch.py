# --- Tickets (bang, 2026-11-08: "票券沒有可以上傳截圖的欄位"; chose 雲端共享) ---
# Tickets live in Firestore collection 'tickets' {n, s, tag, img (compressed JPEG data URL), ts}; anyone can add, edit and attach a screenshot.
# The six built-in tickets are written once under fixed ids (seed0..), so several phones seeding at once can't duplicate them.
# Deleting asks for the admin password, like every other delete. Images are also kept in localStorage so they open offline.
S = rep(S, "const clone=o=>JSON.parse(JSON.stringify(o));", r"""const clone=o=>JSON.parse(JSON.stringify(o));
const tkCache={get:id=>{try{return localStorage.getItem('tk-img-'+id)}catch(e){return null}},set:(id,v)=>{try{if(v)localStorage.setItem('tk-img-'+id,v);else localStorage.removeItem('tk-img-'+id)}catch(e){}}};
const shrinkImg=file=>new Promise((ok,bad)=>{const u=URL.createObjectURL(file),im=new Image();im.onload=()=>{URL.revokeObjectURL(u);let w=im.naturalWidth,h=im.naturalHeight,m=1600;
  for(let tries=0;tries<6;tries++){const k=Math.min(1,m/Math.max(w,h)),c=document.createElement('canvas');c.width=Math.round(w*k);c.height=Math.round(h*k);
    const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);g.drawImage(im,0,0,c.width,c.height);const q=tries<3?.8-tries*.1:.6;const d=c.toDataURL('image/jpeg',q);
    if(d.length<800000)return ok(d);m=Math.round(m*.8)}bad(new Error('too big'))};im.onerror=()=>{URL.revokeObjectURL(u);bad(new Error('not an image'))};im.src=u});""")
S = rep(S, "packX:L.packX||[],packNew:{}", "packX:L.packX||[],packNew:{},tix:null,tkEdit:null,tkZoom:false,tkBusy:false")
S = rep(S, "db.collection('packitems').onSnapshot(", r"""db.collection('tickets').onSnapshot(qs=>{if(qs.empty&&!qs.metadata.fromCache){TICKETS.forEach((t,i)=>this.write(()=>db.collection('tickets').doc('seed'+i).set({n:t.n,s:t.s,tag:t.tag,img:'',ts:i})));return}
      const tix=qs.docs.map(d=>({...d.data(),id:d.id})).sort((a,b)=>(a.ts||0)-(b.ts||0));tix.forEach(t=>{if(t.img)tkCache.set(t.id,t.img);else t.img=tkCache.get(t.id)||''});this.setState({tix})},warn);
    db.collection('packitems').onSnapshot(""")
S = rep(S, "  togglePack(k){", r"""  tkList(){return this.state.tix||TICKETS.map((t,i)=>({...t,id:'seed'+i,img:tkCache.get('seed'+i)||''}))}
  tkSave(id,o){const tix=this.tkList().map(t=>t.id===id?{...t,...o}:t);this.setState({tix});if(o.img!==undefined)tkCache.set(id,o.img);
    if(this.db){const t=tix.find(x=>x.id===id);this.write(()=>this.db.collection('tickets').doc(id).set({n:t.n,s:t.s||'',tag:t.tag||'',img:t.img||'',ts:t.ts!=null?t.ts:Date.now()}))}}
  tkAdd(){const id='t'+Date.now().toString(36),t={id,n:'新票券',s:'',tag:'其他',img:'',ts:Date.now()};this.setState(st=>({tix:[...this.tkList(),t],ticket:this.tkList().length,tkEdit:{n:'',s:''}}));
    if(this.db)this.write(()=>this.db.collection('tickets').doc(id).set({n:t.n,s:'',tag:t.tag,img:'',ts:t.ts}))}
  async tkPick(e,id){const f=e.target.files&&e.target.files[0];e.target.value='';if(!f)return;this.setState({tkBusy:true});
    try{const d=await shrinkImg(f);this.tkSave(id,{img:d});this.flash('截圖已存好，大家都看得到')}catch(err){this.flash('這張圖存不了，換一張試試')}this.setState({tkBusy:false})}
  tkDel(id,n){askAdmin('刪除票券「'+n+'」要先輸入管理密碼。',()=>{const tix=this.tkList().filter(t=>t.id!==id);tkCache.set(id,null);this.setState({tix,ticket:0,tkEdit:null});
    if(this.db)this.write(()=>this.db.collection('tickets').doc(id).delete());this.flash('已刪除「'+n+'」')},true)}
  togglePack(k){""")
S = rep(S, "ticket:TICKETS[s.ticket],tickets:TICKETS.map((t,i)=>({...t,onClick:()=>this.setState({ticket:i}),border:i===s.ticket?INK:'rgba(34,31,26,.1)'})),",
r"""ticket:(()=>{const L=this.tkList(),t=L[Math.min(s.ticket,L.length-1)];if(!t)return{none:true};const ed=s.tkEdit;
        return{...t,has:true,hasImg:!!t.img,noImg:!t.img,imgStyle:s.tkZoom?'width:100%;height:auto;display:block':'width:100%;max-height:52vh;object-fit:contain;display:block',
          zoomLabel:s.tkZoom?'縮小':'放大',zoom:()=>this.setState(st=>({tkZoom:!st.tkZoom})),
          pickLabel:s.tkBusy?'處理中…':t.img?'換截圖':'＋ 上傳截圖',pick:e=>this.tkPick(e,t.id),
          editing:!!ed,notEditing:!ed,edN:ed?ed.n:'',edS:ed?ed.s:'',
          startEdit:()=>this.setState({tkEdit:{n:t.n,s:t.s||''}}),setN:e=>{const v=e.target.value;this.setState(st=>({tkEdit:{...st.tkEdit,n:v}}))},setS:e=>{const v=e.target.value;this.setState(st=>({tkEdit:{...st.tkEdit,s:v}}))},
          saveEdit:()=>{const n=(s.tkEdit.n||'').trim()||'未命名票券';this.tkSave(t.id,{n,s:(s.tkEdit.s||'').trim()});this.setState({tkEdit:null});this.flash('已儲存')},
          cancelEdit:()=>this.setState({tkEdit:null}),del:()=>this.tkDel(t.id,t.n)}})(),
      addTicket:()=>this.tkAdd(),
      tickets:this.tkList().map((t,i)=>({...t,clip:t.img?'📎 ':'',onClick:()=>this.setState({ticket:i,tkEdit:null,tkZoom:false}),border:i===s.ticket?INK:'rgba(34,31,26,.1)'})),""")
_k = tpl.index('<sc-if value="{{ sh.ticket }}">'); _e = tpl.index('</sc-if>', tpl.index('</sc-for>', _k)) + 8
BTN = "height:44px;padding:0 14px;border-radius:12px;border:1px solid rgba(34,31,26,.18);background:transparent;font:500 14px 'Noto Sans TC';color:#221f1a;cursor:pointer"
INP = "height:46px;border-radius:12px;border:1.5px solid rgba(34,31,26,.18);background:#fffdf9;padding:0 12px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none;width:100%;box-sizing:border-box"
tpl = tpl[:_k] + """<sc-if value="{{ sh.ticket }}">
              <div style="display:flex;flex-direction:column;gap:12px">
                <div style="display:flex;align-items:center;justify-content:space-between">
                  <div style="font:700 20px 'Noto Sans TC',sans-serif">票券</div>
                  <button onClick="{{ addTicket }}" style="height:38px;padding:0 14px;border:0;border-radius:11px;background:#221f1a;color:#fff;font:500 13px 'Noto Sans TC';cursor:pointer">＋ 新增票券</button>
                </div>
                <sc-if value="{{ ticket.has }}">
                <div style="background:#fffdf9;border:1px solid rgba(34,31,26,.12);border-radius:18px;padding:14px;display:flex;flex-direction:column;gap:12px">
                  <sc-if value="{{ ticket.hasImg }}"><img onClick="{{ ticket.zoom }}" src="{{ ticket.img }}" alt="票券截圖" style="{{ ticket.imgStyle }};border-radius:10px;background:#fff;cursor:zoom-in"></sc-if>
                  <sc-if value="{{ ticket.noImg }}"><div style="height:120px;border-radius:12px;border:1.5px dashed rgba(34,31,26,.25);display:flex;align-items:center;justify-content:center;font:400 13px 'Noto Sans TC';color:#5c554c;text-align:center;padding:0 16px">還沒有截圖。按下面「上傳截圖」，選訂單畫面或 QR code 的截圖</div></sc-if>
                  <sc-if value="{{ ticket.notEditing }}">
                    <div style="font:700 17px/1.35 'Noto Sans TC'">{{ ticket.n }}</div>
                    <div style="font:400 13px/1.6 'Noto Sans TC';color:#4d473f;white-space:pre-wrap">{{ ticket.s }}</div>
                  </sc-if>
                  <sc-if value="{{ ticket.editing }}">
                    <input value="{{ ticket.edN }}" onChange="{{ ticket.setN }}" placeholder="名稱，例如 SHIBUYA SKY" style=\"""" + INP + """\">
                    <textarea value="{{ ticket.edS }}" onChange="{{ ticket.setS }}" placeholder="日期、訂單編號、注意事項" style=\"""" + INP + """;height:96px;padding:10px 12px;line-height:1.5;resize:vertical"></textarea>
                    <div style="display:flex;gap:8px"><button onClick="{{ ticket.saveEdit }}" style="flex:1;height:44px;border:0;border-radius:12px;background:#221f1a;color:#fff;font:500 14px 'Noto Sans TC';cursor:pointer">儲存</button><button onClick="{{ ticket.cancelEdit }}" style=\"""" + BTN + """\">取消</button></div>
                  </sc-if>
                  <div style="display:flex;gap:8px;flex-wrap:wrap">
                    <label style=\"""" + BTN + """;display:inline-flex;align-items:center;background:#221f1a;color:#fff;border-color:#221f1a">{{ ticket.pickLabel }}<input type="file" accept="image/*" onChange="{{ ticket.pick }}" style="display:none"></label>
                    <sc-if value="{{ ticket.hasImg }}"><button onClick="{{ ticket.zoom }}" style=\"""" + BTN + """\">{{ ticket.zoomLabel }}</button></sc-if>
                    <sc-if value="{{ ticket.notEditing }}"><button onClick="{{ ticket.startEdit }}" style=\"""" + BTN + """\">編輯文字</button></sc-if>
                    <button onClick="{{ ticket.del }}" style=\"""" + BTN + """;color:oklch(0.5 0.15 30);margin-left:auto">刪除</button>
                  </div>
                </div>
                </sc-if>
                <sc-for list="{{ tickets }}" as="t" hint-placeholder-count="3">
                  <div onClick="{{ t.onClick }}" style="display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 14px;border-radius:14px;border:1.5px solid {{ t.border }};background:#fffdf9;cursor:pointer">
                    <span style="font:500 14px 'Noto Sans TC';min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ t.clip }}{{ t.n }}</span>
                    <span style="flex:none;font:400 12px 'Noto Sans TC';color:#5c554c">{{ t.tag }}</span>
                  </div>
                </sc-for>
              </div>
            </sc-if>""" + tpl[_e:]
