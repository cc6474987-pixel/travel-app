# --- Search near the phone's current location ---
S = rep(S, "const getSample=async()=>", r"""const getLoc=()=>new Promise(res=>{try{if(!navigator.geolocation)return res({err:'none'});navigator.geolocation.getCurrentPosition(p=>res({lat:p.coords.latitude,lng:p.coords.longitude,acc:p.coords.accuracy}),e=>res({err:e&&e.code===1?'denied':'fail'}),{enableHighAccuracy:true,timeout:10000,maximumAge:120000})}catch(e){res({err:'none'})}});
const getSample=async()=>""")
S = rep(S, "addQ:'',sr:null,srLoading:false,srErr:''};", "addQ:'',sr:null,srLoading:false,srErr:'',nearMe:false};")
S = rep(S, "this.setState({srLoading:true,srErr:''});", r"""this.setState({srLoading:true,srErr:''});let loc=null;
    if(s.nearMe){const g=await getLoc();if(g.err){this.setState({srLoading:false,srErr:g.err==='denied'?'沒有定位權限。請在手機設定允許 Claude 使用位置，或關掉「用我現在的位置」改用當天行程區域':'讀不到目前位置，請到戶外再試，或關掉「用我現在的位置」'});return}loc=g}""")
S = rep(S, r"'\n\n只推薦真實存在、就在當天行程經過的區域附近（離某一站步行或車程約 15 分鐘內）的地點，最多 6 個，",
  r"(loc?'\n\n使用者現在的位置：緯度 '+loc.lat.toFixed(5)+'，經度 '+loc.lng.toFixed(5)+'（誤差約 '+Math.round(loc.acc)+' 公尺）。先判斷這個座標在哪一區，只推薦離這個位置步行約 10 分鐘（800 公尺）內、真實存在的地點，最多 6 個，由近到遠排，note 開頭寫大概距離（例：約 300m・），area 寫這個位置所在的區域，':'\n\n只推薦真實存在、就在當天行程經過的區域附近（離某一站步行或車程約 15 分鐘內）的地點，最多 6 個，')+'")
S = rep(S, "srHint:s.srLoading?", "nearLabel:s.nearMe?'📍 用我現在的位置 · 開':'📍 用我現在的位置 · 關',nearBg:s.nearMe?'oklch(0.5 0.11 255)':'#fffdf9',nearColor:s.nearMe?'#fff':INK,\n      toggleNear:()=>this.setState(st=>({nearMe:!st.nearMe,sr:null,srErr:''})),\n      foodNear:()=>{this.setState({sheet:'add',day:trip?TODAY:s.day,tab:'plan',addQ:s.addQ||'美食',nearMe:true,sr:null,srErr:''},()=>this.searchPlaces())},\n      srHint:s.nearMe?(s.srLoading?'正在讀取位置並請 Claude 找附近的地點…':'Claude 會找你現在位置步行約 10 分鐘內的地點'):s.srLoading?")
tpl = rep(tpl, """<div style="font:400 12px/1.6 'Noto Sans TC';color:#6f685e">{{ srHint }}</div>""",
  """<button onClick="{{ toggleNear }}" style="align-self:flex-start;height:34px;padding:0 13px;border-radius:17px;border:1px solid rgba(34,31,26,.15);background:{{ nearBg }};color:{{ nearColor }};font:500 12.5px 'Noto Sans TC';cursor:pointer">{{ nearLabel }}</button>
                <div style="font:400 12px/1.6 'Noto Sans TC';color:#6f685e">{{ srHint }}</div>""")
tpl = rep(tpl, """<div style="font:700 20px 'Noto Sans TC',sans-serif">附近美食 · 澀谷神南</div>""",
  """<div style="font:700 20px 'Noto Sans TC',sans-serif">附近美食 · 澀谷神南</div>
                <button onClick="{{ foodNear }}" style="height:46px;border:0;border-radius:14px;background:oklch(0.5 0.11 255);color:#fff;font:600 14px 'Noto Sans TC';cursor:pointer">📍 用我現在的位置找附近美食</button>""")
