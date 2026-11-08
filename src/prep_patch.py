# --- Pre-departure to-do list (bang, 2026-11-08): a 出國前要辦 group in the 清單 tab, shown first ---
# Appended to PACK so the checked-state keys of the existing groups (index-index) don't shift; only the display order puts it on top.
S = rep(S, "['大購物袋（Outlet）','我']]}];", "['大購物袋（Outlet）','我']]},{name:'出國前要辦',items:["
  "['確認 11/17 08:00 送機有有效訂單','舊單 SAR427709 已取消'],"
  "['訂 SHIBUYA SKY 11/12 16:20 ×6','Klook／KKday'],"
  "['訂 63 ANGEL 11/12 晚場 ×6','Klook・限 20 歲'],"
  "['訂 Gyu Star 11/11 午餐 ×6','☎ 03-3834-2215'],"
  "['訂 湖波 11/13 18:00 ×6','☎ 0555-72-0349'],"
  "['訂 牛たんの檸檬 11/15 19:45 ×6','TableCheck 中文'],"
  "['訂 GOKU 淺草寺店 11/16 11:40 ×6','TableCheck 中文'],"
  "['訂 伊豆榮本店 11/16 17:30 ×6','☎ 03-3831-0954'],"
  "['訂 Maidreamin 11/16 六人位','官網'],"
  "['酷航 TR866 線上報到','起飛前 48 小時開放'],"
  "['確認去回程託運行李額度','酷航／樂桃'],"
  "['11/11 清晨去桃園機場','04:40 前到'],"
  "['網路：eSIM 或 Wi-Fi 分享器','各自'],"
  "['旅平險／不便險','各自'],"
  "['手機把這個 App 加到主畫面並打開一次','離線也能用'],"
  "['Google 地圖下載離線區域','東京・河口湖・鎌倉']]}];")
S = rep(S, "onClick:()=>this.togglePack(p.k)}))})),", "onClick:()=>this.togglePack(p.k)}))})).map((c,i,a)=>a[(i+a.length-1)%a.length]),")
