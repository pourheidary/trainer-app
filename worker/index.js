// Cloudflare Worker: share links for assigned programs.
// Routes
//   POST   /api/links          body {data, exp?}      -> {id, token}   (open: no key needed)
//   PUT    /api/links/:id      header x-edit-token, body {data, exp?}  -> {ok:true}
//   DELETE /api/links/:id      header x-edit-token                      -> {ok:true}
//   GET    /api/links/:id      (public)                        -> {data, exp}  | 404 | 410 (expired)
//   GET    /p/:id              (public)                        -> the student page (p.html)
// KV binding: LINKS. Each link gets a random edit token when created; only the app that created it can change or delete it.
const MAX_BODY = 3 * 1024 * 1024;
const J = (o, status = 200, extra = {}) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra } });
const ID_RE = /^[A-Za-z0-9_-]{20,40}$/;

function randomId() {
  const b = new Uint8Array(16); crypto.getRandomValues(b);
  let s = ''; for (const x of b) s += String.fromCharCode(x);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function safeEqual(a, b) {
  a = String(a || ''); b = String(b || '');
  let d = a.length ^ b.length;
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) d |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return d === 0;
}
const tokenOk = (req, rec) => !!rec.token && safeEqual(req.headers.get('x-edit-token') || '', rec.token);
async function readBody(req) {
  const len = +req.headers.get('content-length') || 0;
  if (len > MAX_BODY) return { err: J({ error: 'too_large' }, 413) };
  const txt = await req.text();
  if (txt.length > MAX_BODY) return { err: J({ error: 'too_large' }, 413) };
  let b; try { b = JSON.parse(txt); } catch (_) { return { err: J({ error: 'bad_json' }, 400) }; }
  if (!b || typeof b !== 'object' || !b.data || typeof b.data !== 'object') return { err: J({ error: 'bad_request' }, 400) };
  let exp = null;
  if (b.exp !== null && b.exp !== undefined) {
    exp = Number(b.exp);
    if (!Number.isFinite(exp) || exp <= 0) return { err: J({ error: 'bad_exp' }, 400) };
  }
  return { data: b.data, exp };
}
// KV needs a TTL of at least 60 s; keep the record one day past expiry so a late visitor still sees "expired".
function ttlFor(exp) {
  if (exp === null) return undefined;
  const s = Math.ceil((exp - Date.now()) / 1000) + 86400;
  return Math.max(60, s);
}
async function put(env, id, data, exp, created, token) {
  const rec = { v: 2, created: created || Date.now(), updated: Date.now(), exp, token, data };
  const opts = {}; const t = ttlFor(exp); if (t) opts.expirationTtl = t;
  await env.LINKS.put('l:' + id, JSON.stringify(rec), opts);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), path = url.pathname;

    if (path === '/api/links' && req.method === 'POST') {
      const r = await readBody(req); if (r.err) return r.err;
      const id = randomId(), token = randomId() + randomId(); await put(env, id, r.data, r.exp, null, token);
      return J({ id, token }, 201);
    }

    const m = /^\/api\/links\/([^/]+)$/.exec(path);
    if (m) {
      const id = m[1]; if (!ID_RE.test(id)) return J({ error: 'not_found' }, 404);
      if (req.method === 'GET') {
        const raw = await env.LINKS.get('l:' + id);
        if (!raw) return J({ error: 'not_found' }, 404);
        const rec = JSON.parse(raw);
        if (rec.exp !== null && rec.exp !== undefined && Date.now() >= rec.exp) return J({ error: 'expired', exp: rec.exp }, 410);
        return J({ data: rec.data, exp: rec.exp ?? null });
      }
      if (req.method !== 'PUT' && req.method !== 'DELETE') return J({ error: 'method_not_allowed' }, 405);
      const raw = await env.LINKS.get('l:' + id);
      if (!raw) return J({ error: 'not_found' }, 404);
      const rec = JSON.parse(raw);
      if (!tokenOk(req, rec)) return J({ error: 'unauthorized' }, 401);
      if (req.method === 'PUT') {
        const r = await readBody(req); if (r.err) return r.err;
        await put(env, id, r.data, r.exp, rec.created, rec.token);
        return J({ ok: true });
      }
      await env.LINKS.delete('l:' + id); return J({ ok: true });
      return J({ error: 'method_not_allowed' }, 405);
    }

    if (/^\/p\/[^/]+\/?$/.test(path)) {
      let r = await env.ASSETS.fetch(new Request(new URL('/p.html', url.origin), { headers: req.headers }));
      for (let i = 0; i < 3 && r.status >= 300 && r.status < 400 && r.headers.get('location'); i++) r = await env.ASSETS.fetch(new Request(new URL(r.headers.get('location'), url.origin), { headers: req.headers }));
      const h = new Headers(r.headers); h.set('cache-control', 'no-store'); h.set('x-robots-tag', 'noindex, nofollow'); h.set('referrer-policy', 'no-referrer');
      return new Response(r.body, { status: r.status, headers: h });
    }

    return env.ASSETS.fetch(req);
  }
};
