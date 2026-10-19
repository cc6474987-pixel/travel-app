// Cloudflare Worker: relays the app's AI requests to Claude so the API key never sits in the web page.
// Secrets (Settings → Variables): ANTHROPIC_API_KEY, TRIP_CODE. Optional var ALLOW_ORIGIN (e.g. https://you.github.io).
const MODELS = new Set(['claude-haiku-5-5', 'claude-sonnet-5-5']);
export default {
  async fetch(req, env) {
    const origin = env.ALLOW_ORIGIN || '*';
    const cors = { 'access-control-allow-origin': origin, 'access-control-allow-headers': 'content-type,x-trip-code', 'access-control-allow-methods': 'POST,OPTIONS' };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return new Response('POST only', { status: 405, headers: cors });
    if (req.headers.get('x-trip-code') !== env.TRIP_CODE) return new Response('forbidden', { status: 403, headers: cors });
    let body; try { body = await req.json() } catch (e) { return new Response('bad json', { status: 400, headers: cors }) }
    const model = MODELS.has(body.model) ? body.model : 'claude-haiku-5-5';
    const messages = Array.isArray(body.messages) ? body.messages.slice(-12) : [];
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
      body: JSON.stringify({ model, max_tokens: 2000, messages })
    });
    if (!r.ok) return new Response(JSON.stringify({ error: r.status }), { status: r.status === 429 ? 429 : 502, headers: { ...cors, 'content-type': 'application/json' } });
    const j = await r.json();
    const text = (j.content || []).filter(c => c.type === 'text').map(c => c.text).join('');
    return new Response(JSON.stringify({ text, truncated: j.stop_reason === 'max_tokens' }), { headers: { ...cors, 'content-type': 'application/json' } });
  }
};
