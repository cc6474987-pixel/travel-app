# 旅遊 App 東京河口湖

六人東京河口湖行程 app（2026/11/11–17），手機打開就能用：行程、今日、記帳分帳、行李清單，旅伴之間即時同步。

- 網址（開好 GitHub Pages 後）：`https://cc6474987-pixel.github.io/travel-app/`
- 第一次打開要輸入旅行密碼，之後會記住。
- iPhone：Safari 打開 → 分享 →「加入主畫面」。
- 設定 Firebase、旅行密碼、AI 搜尋：見 [設定步驟.md](設定步驟.md)。

## 檔案
- `index.html`：app 本體（由 `src/build.sh` 產生，不要手改）
- `config.js`：Firebase 設定、旅行密碼雜湊、AI 轉接網址
- `shim.js`：同步（Firebase）、密碼頁、AI 搜尋轉接
- `worker.js`：放到 Cloudflare Workers 的 AI 轉接程式
- `firestore.rules`：貼到 Firebase 的資料庫規則
- `src/`：設計稿與產生 app 的程式；改完執行 `src/build.sh`
