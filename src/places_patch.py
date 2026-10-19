# --- Standalone only: nearby search reads the shared food list (places.json + places the group adds) instead of AI ---
import re

HELP = r"""let PLDATA=null;
const getPlData=async()=>{if(PLDATA)return PLDATA;try{const r=await fetch('places.json',{cache:'no-cache'});PLDATA=await r.json()}catch(e){PLDATA={places:[],stops:{}}}return PLDATA};
const distM=(a,b)=>{const R=6371e3,r=Math.PI/180,dl=(b.lat-a.lat)*r,dg=(b.lng-a.lng)*r,x=Math.sin(dl/2)**2+Math.cos(a.lat*r)*Math.cos(b.lat*r)*Math.sin(dg/2)**2;return 2*R*Math.asin(Math.sqrt(x))};
const fmtDist=m=>m<30?'就在附近':m<1000?'約 '+Math.round(m/10)*10+'m':'約 '+(m/1000).toFixed(1)+'km';
const PL_SYN={'拉麵':'ラーメン 拉麺 らーめん','壽司':'寿司 鮨 すし','燒肉':'焼肉 和牛','和牛':'焼肉 燒肉 牛','咖啡':'カフェ 珈琲 喫茶 コーヒー','甜點':'スイーツ 甘味 ケーキ パフェ','鰻魚':'うなぎ 鰻','烏龍麵':'うどん','蕎麥麵':'そば 蕎麦','豬排':'とんかつ かつ','咖哩':'カレー','居酒屋':'酒場 居酒屋','海鮮':'魚 海鮮 丼','丼飯':'丼'};
const PL_ANY=/^(美食|吃的?|餐廳|食物|好吃的?|午餐|晚餐|早餐|宵夜|吃飯)?$/;
const plText=p=>[p.name,p.jp,p.cat,p.area,p.note].join(' ');
const plMatch=(p,q)=>{if(PL_ANY.test(q))return true;const t=plText(p);if(t.includes(q))return true;
  for(const k in PL_SYN){if(q.includes(k)||k.includes(q)){if(t.includes(k)||PL_SYN[k].split(' ').some(w=>t.includes(w)))return true}}return false};
const stopGeo=(it,G)=>{const g=G[it.addr]||G[it.title];return g?{lat:g[0],lng:g[1]}:null};
function findPlaces(all,G,o){const q=(o.q||'').trim(),cand=all.filter(p=>plMatch(p,q)),out=[];
  if(o.loc){cand.forEach(p=>{if(p.lat!=null)out.push({p,d:distM(o.loc,p)})});out.sort((a,b)=>a.d-b.d);
    const near=out.filter(x=>x.d<=800);return{list:(near.length?near:out.filter(x=>x.d<=3000)).slice(0,8),wide:!near.length}}
  const anchors=o.stops.map(it=>({it,g:stopGeo(it,G)})).filter(a=>a.g);
  cand.forEach(p=>{if(p.lat==null)return;let best=null;anchors.forEach(a=>{const d=distM(a.g,p);if(!best||d<best.d)best={d,after:a.it.title}});if(best)out.push({p,...best})});
  out.sort((a,b)=>a.d-b.d);let list=out.filter(x=>x.d<=1500);const wide=!list.length;if(wide)list=out.filter(x=>x.d<=6000);
  return{list:list.slice(0,8),wide}}
const gsiGeo=async addr=>{try{const r=await fetch('https://msearch.gsi.go.jp/address-search/AddressSearch?q='+encodeURIComponent(addr));const j=await r.json();const c=j&&j[0]&&j[0].geometry&&j[0].geometry.coordinates;return c?{lat:+c[1],lng:+c[0]}:null}catch(e){return null}};
const getSample=async()=>"""

SEARCH = r"""try{const P=await getPlData(),all=P.places.concat(this.state.myPlaces||[]);
      const res=findPlaces(all,P.stops||{},{q,loc,stops:sch});
      const sr=res.list.map(({p,d,after})=>({title:p.name,type:'餐飲',sub:[p.note,p.hours].filter(Boolean).join(' · '),area:p.area||'',after:after||'',
        stay:/咖啡|甜點|小吃/.test(p.cat||'')?30:60,dist:d,addr:p.addr||'',jp:p.jp||'',mine:!!p.by}));
      if(this.state.day!==di)return this.setState({srLoading:false});
      this.setState({sr,srLoading:false,srErr:sr.length?(res.wide?(loc?'步行 10 分鐘內沒有清單裡的店，以下是最近的':'當天行程附近較少，以下包含稍遠的店'):''):(q&&!PL_ANY.test(q)?'清單裡沒有「'+q+'」，換個關鍵字，或點下面把店加進清單':'清單裡這附近還沒有店，可以點下面把店加進清單')})}"""

def apply(page, rep):
    page = rep(page, "const getSample=async()=>", HELP)
    page, n = re.subn(r"try\{const sample=await getSample\(\);if\(!sample\)throw \{code:'unavailable'\};\n      const stops=.*?srErr:sr\.length\?'':'沒有找到合適的地點，換個關鍵字試試'\}\)\}", lambda m: SEARCH, page, count=1, flags=re.S)
    assert n == 1, "searchPlaces block"
    # group-added places live in Firestore collection 'places'
    page = rep(page, "collection('settled').onSnapshot(qs=>{this.setState({settled:qs.docs.map(d=>({...d.data()})).sort((a,b)=>(a.ts||0)-(b.ts||0))})},warn)}",
        "collection('settled').onSnapshot(qs=>{this.setState({settled:qs.docs.map(d=>({...d.data()})).sort((a,b)=>(a.ts||0)-(b.ts||0))})},warn);\n    db.collection('places').onSnapshot(qs=>{this.setState({myPlaces:qs.docs.map(d=>({id:d.id,...d.data()}))})},warn)}")
    page = rep(page, "addQ:'',sr:null,srLoading:false,srErr:'',nearMe:false};",
        "addQ:'',sr:null,srLoading:false,srErr:'',nearMe:false,myPlaces:[],np:null};")
    page = rep(page, "  async searchPlaces(){", r"""  async savePlace(){const np=this.state.np;if(!np||np.busy)return;const name=(np.name||'').trim();if(!name)return this.setState({np:{...np,err:'請填店名'}});
    this.setState({np:{...np,busy:true,err:''}});let g=null;
    if(np.here){const l=await getLoc();if(l.err)return this.setState({np:{...np,busy:false,err:l.err==='denied'?'沒有定位權限，請在手機設定允許瀏覽器使用位置，或改填地址':'讀不到目前位置，請改填地址'}});g={lat:l.lat,lng:l.lng}}
    else if((np.addr||'').trim())g=await gsiGeo(np.addr.trim());
    const doc={name:name.slice(0,40),jp:'',cat:'',area:'',addr:(np.addr||'').trim(),note:(np.note||'').trim().slice(0,80),hours:'',by:'旅伴',ts:Date.now(),...(g?{lat:g.lat,lng:g.lng}:{})};
    try{const db=this.db;if(!db)throw 0;await db.collection('places').add(doc);
      this.setState({np:null});this.flash(g?'已把「'+doc.name+'」加進美食清單':'已加進清單，但找不到地址位置，距離搜尋不會出現它')}
    catch(e){this.setState({np:{...np,busy:false,err:'存不進清單，請確認網路後再試'}})}}
  async searchPlaces(){""")
    page = rep(page, "this.setState({srLoading:true,srErr:''});let loc=null;", "this.setState({srLoading:true,srErr:'',np:null});let loc=null;")
    page = rep(page, "允許 Claude 使用位置", "允許瀏覽器使用位置")
    page = rep(page, "srBtn:s.srLoading?'搜尋中…':'請 Claude 找',", "srBtn:s.srLoading?'搜尋中…':'搜尋清單',")
    page = rep(page, "srHint:s.nearMe?(s.srLoading?'正在讀取位置並請 Claude 找附近的地點…':'Claude 會找你現在位置步行約 10 分鐘內的地點'):s.srLoading?'Claude 正在找 '+day.city+' 附近的地點，約需 10–30 秒':'Claude 只找 '+day.city+' 一帶、排得進當天行程的地點',",
        "srHint:s.nearMe?(s.srLoading?'正在讀取你的位置…':'從美食清單找你現在位置步行約 10 分鐘內的店'):s.srLoading?'搜尋中…':'從美食清單找當天行程附近的店，會排在最近的那一站之後',"
        "\n      npOpen:!!s.np,npClosed:!s.np,np:s.np||{},npErr:s.np&&s.np.err||'',npSave:s.np&&s.np.busy?'儲存中…':'加進清單',"
        "\n      npStart:()=>this.setState({np:{name:s.addQ&&!PL_ANY.test(s.addQ.trim())?s.addQ.trim():'',addr:'',note:'',here:false}}),npCancel:()=>this.setState({np:null}),"
        "\n      npName:e=>{const v=e.target.value;this.setState(st=>({np:{...st.np,name:v}}))},npAddr:e=>{const v=e.target.value;this.setState(st=>({np:{...st.np,addr:v}}))},npNote:e=>{const v=e.target.value;this.setState(st=>({np:{...st.np,note:v}}))},npHere:()=>this.setState(st=>({np:{...st.np,here:!st.np.here}})),"
        "\n      npHereLabel:s.np&&s.np.here?'📍 店家就在我現在的位置 · 開':'📍 店家就在我現在的位置 · 關',npHereBg:s.np&&s.np.here?'oklch(0.5 0.11 255)':'#fffdf9',npHereColor:s.np&&s.np.here?'#fff':INK,"
        "\n      saveNp:()=>this.savePlace(),myCount:(s.myPlaces||[]).length,")
    page = rep(page, "return{title:r.title,sub:r.sub,color:tc(r.type),where:(r.area?r.area+' · ':'')+(at?'會排在「'+at+'」之後':'會排在當天最後'),\n          map:'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(r.title+' '+(r.area||day.city)),\n          onClick:()=>this.addItem(s.day,{title:r.title,sub:r.sub,type:r.type,rec:r.stay?[r.stay,r.stay]:undefined},ai)}}),",
        "return{title:r.title+(r.mine?'（旅伴加的）':''),sub:r.sub,color:tc(r.type),where:(r.dist!=null?fmtDist(r.dist)+(s.nearMe?'':'（離'+(r.after||'行程')+'）')+' · ':'')+(r.area?r.area+' · ':'')+(at?'會排在「'+at+'」之後':'會排在當天最後'),\n          map:'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(r.addr?(r.jp||r.title)+' '+r.addr:r.title+' '+(r.area||day.city)),\n          onClick:()=>this.addItem(s.day,{title:r.title,sub:r.sub,type:r.type,addr:r.addr,rec:r.stay?[r.stay,r.stay]:undefined},ai)}}),")
    page = rep(page, "rating:'',addr:'',wait:0,stay:Math.round((r[0]+r[1])/2/5)*5", "rating:'',addr:src.addr||'',wait:0,stay:Math.round((r[0]+r[1])/2/5)*5")
    page = rep(page, "Claude 推薦 · 營業時間請點地圖確認", "美食清單 · 營業時間請點地圖確認")
    page = rep(page, "行程備註裡沒有符合的地點，按「請 Claude 找」查附近。", "行程備註裡沒有符合的地點，按「搜尋清單」找附近的店。")
    page = rep(page, "'翻譯失敗，請再試一次'", "'翻譯要用 AI，目前還沒開啟'")
    FORM = """                <sc-if value="{{ npClosed }}"><button onClick="{{ npStart }}" style="align-self:flex-start;border:0;background:transparent;padding:2px 0;font:500 12.5px 'Noto Sans TC';color:oklch(0.45 0.11 255);cursor:pointer">＋ 清單裡沒有？把一家店加進清單（旅伴都看得到）</button></sc-if>
                <sc-if value="{{ npOpen }}">
                  <div style="display:flex;flex-direction:column;gap:8px;padding:12px 13px;border-radius:14px;background:#fffdf9;border:1px solid rgba(34,31,26,.12)">
                    <div style="font:600 13.5px 'Noto Sans TC'">把店加進美食清單</div>
                    <input value="{{ np.name }}" onChange="{{ npName }}" placeholder="店名" style="height:42px;border-radius:12px;border:1.5px solid rgba(34,31,26,.15);background:#fff;padding:0 12px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none">
                    <button onClick="{{ npHere }}" style="align-self:flex-start;height:34px;padding:0 13px;border-radius:17px;border:1px solid rgba(34,31,26,.15);background:{{ npHereBg }};color:{{ npHereColor }};font:500 12.5px 'Noto Sans TC';cursor:pointer">{{ npHereLabel }}</button>
                    <input value="{{ np.addr }}" onChange="{{ npAddr }}" placeholder="日文地址（不在店裡時填，例：東京都台東区浅草1-29-3）" style="height:42px;border-radius:12px;border:1.5px solid rgba(34,31,26,.15);background:#fff;padding:0 12px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none">
                    <input value="{{ np.note }}" onChange="{{ npNote }}" placeholder="一句備註（招牌菜、價位）" style="height:42px;border-radius:12px;border:1.5px solid rgba(34,31,26,.15);background:#fff;padding:0 12px;font:400 16px 'Noto Sans TC';color:#221f1a;outline:none">
                    <sc-if value="{{ npErr }}"><span style="font:400 12px 'Noto Sans TC';color:oklch(0.5 0.14 30)">{{ npErr }}</span></sc-if>
                    <div style="display:flex;gap:8px">
                      <button onClick="{{ saveNp }}" style="flex:1;height:42px;border:0;border-radius:12px;background:#221f1a;color:#fff;font:500 13.5px 'Noto Sans TC';cursor:pointer">{{ npSave }}</button>
                      <button onClick="{{ npCancel }}" style="flex:none;height:42px;padding:0 14px;border:1px solid rgba(34,31,26,.15);border-radius:12px;background:transparent;font:500 13.5px 'Noto Sans TC';color:#221f1a;cursor:pointer">取消</button>
                    </div>
                  </div>
                </sc-if>
                <sc-if value="{{ hasLocal }}">"""
    page = rep(page, """                <sc-if value="{{ hasLocal }}">""", FORM)
    return page
