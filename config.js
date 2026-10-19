// Fill these in once (see 設定步驟.md). None of these are secret except that the trip password itself is never stored here.
window.TRIP_CONFIG = {
  // Firebase console → Project settings → Your apps → Web app → firebaseConfig
  firebase: { apiKey: "", authDomain: "", projectId: "", appId: "" },
  // SHA-256 of the trip password (Claude computes this for you)
  tripHash: "",
  // Cloudflare Worker address for Claude search, e.g. https://travel-ai.<you>.workers.dev
  workerUrl: ""
};
