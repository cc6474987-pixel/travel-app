// Fill these in once (see 設定步驟.md). None of these are secret except that the trip password itself is never stored here.
window.TRIP_CONFIG = {
  // Firebase console → Project settings → Your apps → Web app → firebaseConfig
  firebase: {
    apiKey: "AIzaSyB67b2edn1QCgbKc18K5rD5cUaAFMUoKMs",
    authDomain: "travel-app-a20ad.firebaseapp.com",
    projectId: "travel-app-a20ad",
    appId: "1:47951169561:web:85b62d11928dce8e30c288"
  },
  // SHA-256 of the trip password (Claude computes this for you)
  tripHash: "bdbfdaabb8082709644595ffb386028dedaceba8a1f08307ceeb137aaa6b0d92",
  // Cloudflare Worker address for Claude search, e.g. https://travel-ai.<you>.workers.dev
  workerUrl: ""
};
