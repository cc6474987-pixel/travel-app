# --- Editing members, marking a transfer paid and deleting an expense need the admin password (once per app session) ---
S = rep(S, "const getLoc=()=>", r"""const ADMIN_H='21a450ca63e673188f62d47608211457ed9f61dc8184b39c38d8fdf4b9cbaa71';
let ADMIN_OK=(()=>{try{return sessionStorage.getItem('trip-admin')===ADMIN_H}catch(e){return false}})();
const sha256=async s=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))).map(b=>b.toString(16).padStart(2,'0')).join('');
const askAdmin=(why,fn)=>{if(ADMIN_OK)return fn();const w=document.createElement('div');w.id='admin-gate';
  w.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(20,18,15,.45);display:flex;align-items:center;justify-content:center;padding:24px';
  w.innerHTML='<div style="background:#fffdf9;border-radius:18px;padding:20px;width:100%;max-width:320px;display:flex;flex-direction:column;gap:10px;font-family:\'Noto Sans TC\',sans-serif;color:#221f1a">'
   +'<div style="font-weight:700;font-size:17px">請輸入管理密碼</div><div style="font-size:13px;line-height:1.5;color:#6f685e">'+why+'</div>'
   +'<input id="adm-in" type="password" inputmode="numeric" autocomplete="off" style="height:44px;border-radius:12px;border:1.5px solid rgba(34,31,26,.2);padding:0 12px;font-size:16px;outline:none">'
   +'<div id="adm-err" style="font-size:12px;color:#b5462f;min-height:16px"></div>'
   +'<div style="display:flex;gap:8px"><button id="adm-ok" style="flex:1;height:42px;border:0;border-radius:12px;background:#221f1a;color:#fff;font-size:14px">確定</button>'
   +'<button id="adm-no" style="height:42px;padding:0 16px;border:1px solid rgba(34,31,26,.18);border-radius:12px;background:transparent;color:#221f1a;font-size:14px">取消</button></div></div>';
  document.body.appendChild(w);const inp=w.querySelector('#adm-in'),err=w.querySelector('#adm-err');setTimeout(()=>inp.focus(),50);
  const ok=async()=>{let h='';try{h=await sha256(inp.value.trim())}catch(e){}
    if(h===ADMIN_H){ADMIN_OK=true;try{sessionStorage.setItem('trip-admin',h)}catch(e){}w.remove();fn()}else{err.textContent='密碼不對，請再試一次';inp.value='';inp.focus()}};
  w.querySelector('#adm-ok').onclick=ok;inp.onkeydown=e=>{if(e.key==='Enter')ok()};w.querySelector('#adm-no').onclick=()=>w.remove();
  w.onclick=e=>{if(e.target===w)w.remove()}};
const getLoc=()=>""")
S = rep(S, "clearTimeout(this.dt);this.setState(st=>({delArm:null,exps:st.exps.filter(e=>e.id!==id)}));\n    if(this.db)this.write(()=>this.db.collection('expenses').doc(id).delete());else lsSet({exps:this.state.exps});this.flash('已刪除這筆')}",
  "clearTimeout(this.dt);this.setState({delArm:null});askAdmin('刪除記帳要先輸入管理密碼。',()=>{this.setState(st=>({exps:st.exps.filter(e=>e.id!==id)}));\n    if(this.db)this.write(()=>this.db.collection('expenses').doc(id).delete());else lsSet({exps:this.state.exps});this.flash('已刪除這筆')})}")
S = rep(S, "onPaid:()=>{this.addSettled(x);this.flash('已標記：'+NM(x.from)+' → '+NM(x.to)+' '+M(x.amt))},", "onPaid:()=>askAdmin('標記已付要先輸入管理密碼。',()=>{this.addSettled(x);this.flash('已標記：'+NM(x.from)+' → '+NM(x.to)+' '+M(x.amt))}),")
S = rep(S, "openPeople:()=>this.setState({sheet:'people'})", "openPeople:()=>askAdmin('編輯成員要先輸入管理密碼。',()=>this.setState({sheet:'people'}))")
