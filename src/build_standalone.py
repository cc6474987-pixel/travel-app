# Builds the standalone web app (GitHub Pages + Firebase) from the Claude-artifact build.
# Usage: python3 build_standalone.py <travel-app.html> <seed plan.json or -> <out dir>
import json, re, sys, os
src, seed, out = sys.argv[1], sys.argv[2], sys.argv[3]
page = open(src, encoding="utf-8").read()

def rep(t, old, new, n=1):
    assert t.count(old) == n, (old[:60], t.count(old))
    return t.replace(old, new)

# Start from the plan the group already edited in the Claude version.
if seed != "-":
    days = json.load(open(seed, encoding="utf-8"))["days"]
    page = re.sub(r"^const DAYS=\[.*?\];$", lambda m: "const DAYS=" + json.dumps(days, ensure_ascii=False) + ";", page, count=1, flags=re.M)

page = rep(page, "目前只存在這台裝置，在 Claude 裡開啟才會和旅伴同步", "目前只存在這台裝置，連上網路後會和旅伴同步")
page = rep(page, "'要先登入 Claude，並在 Claude 裡打開這個連結才能搜尋'", "'AI 搜尋還沒設定好，請先用地圖連結'")
page = rep(page, "'需要允許這個 app 使用 Claude 才能搜尋'", "'AI 搜尋暫時無法使用，請稍後再試'")
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "places_patch.py"), encoding="utf-8").read())
page = apply(page, rep)

head_extra = """<meta charset="utf-8">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="旅遊 App">
<meta name="theme-color" content="#f7f4ef">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
<script src="config.js?v=__V__"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
<script src="shim.js?v=__V__"></script>
<script>window.APP_V='__V__';
// Pages that stay open pick up a new version on their own: check every minute and whenever the app comes back to the screen.
(function(){let busy=false;const check=()=>{if(busy||document.hidden)return;busy=true;
  fetch('version.json?ts='+Date.now(),{cache:'no-store'}).then(r=>r.json()).then(j=>{if(j&&j.v&&j.v!==window.APP_V)location.replace(location.pathname+'?v='+j.v)}).catch(()=>{}).finally(()=>{busy=false})};
  setInterval(check,60000);document.addEventListener('visibilitychange',check);window.addEventListener('focus',check)})();</script>
"""
out_html = "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n" + head_extra + page.replace("<template id=\"tpl\">", "</head>\n<body>\n<template id=\"tpl\">", 1) + "</body>\n</html>\n"
import hashlib
ver = hashlib.sha1(out_html.encode("utf-8")).hexdigest()[:10]
out_html = out_html.replace("__V__", ver)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "version.json"), "w").write(json.dumps({"v": ver}) + "\n")
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(out_html)
print("ok", len(out_html))
