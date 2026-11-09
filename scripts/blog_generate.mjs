#!/usr/bin/env node
/**
 * Blog diario de inspectorhacker.com — genera 1 artículo con IA y reconstruye el blog.
 * Copia el mecanismo de ghspecialist.com (DeepSeek → Gemini → OpenAI → Anthropic).
 *
 * Alterna idioma por día (día par = es, impar = en) salvo BLOG_LANG=es|en.
 * Tema: BLOG_TOPIC o el siguiente sin publicar de _src/blog-topics.json.
 * Escribe _src/blog/<lang>-<slug>.json, corre build_seo.py --blog y build_sitemap.py,
 * y avisa a IndexNow. Sin key de IA: sale con aviso (exit 0) para no romper el cron.
 *
 * Secrets (GitHub → Settings → Secrets and variables → Actions):
 *   DEEPSEEK_API_KEY (principal) · GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY (respaldo)
 */
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SITE = 'https://inspectorhacker.com';
const INDEXNOW_KEY = '06bce93312ef6d54ca1c53c7c15a6228';
const BLOG_DIR = path.join(ROOT, '_src', 'blog');
const TOPICS = JSON.parse(fs.readFileSync(path.join(ROOT, '_src', 'blog-topics.json'), 'utf8'));

const today = new Date(Date.now() - 6 * 3600 * 1000).toISOString().slice(0, 10); // Torreón UTC-6
const dayNum = Math.floor(Date.parse(today) / 86400000);
const lang = (process.env.BLOG_LANG || '').trim() || (dayNum % 2 === 0 ? 'es' : 'en');
const ES = lang === 'es';

const existing = fs.readdirSync(BLOG_DIR).filter((f) => f.endsWith('.json'))
  .map((f) => JSON.parse(fs.readFileSync(path.join(BLOG_DIR, f), 'utf8')));
const usedTopics = new Set(existing.map((d) => (d.topic || '').toLowerCase()));
const usedSlugs = new Set(existing.map((d) => `${d.lang}-${d.slug}`));

let topic = (process.env.BLOG_TOPIC || '').trim();
if (!topic) {
  topic = (TOPICS[lang] || []).find((t) => !usedTopics.has(t.toLowerCase()));
  if (!topic) { console.log(`::warning::No quedan temas sin publicar en _src/blog-topics.json (${lang}).`); process.exit(0); }
}

const internal = ES
  ? ['/', '/planes/', '/vigilancia-vs-pentest/', '/servicios/', '/ciudades/', '/blog/', '/servicios/monitoreo-de-ciberseguridad/', '/servicios/auditoria-de-seguridad-web/', '/servicios/seguridad-de-servidores/', '/servicios/proteccion-de-correo-y-phishing/', '/servicios/respuesta-a-incidentes/', '/ciberseguridad-torreon/', '/ciberseguridad-monterrey/', '/ciberseguridad-pymes-mexico/']
  : ['/en/', '/en/pricing/', '/en/monitoring-vs-pentest/', '/en/services/', '/en/cities/', '/en/blog/', '/en/services/cybersecurity-monitoring/', '/en/services/website-security-audit/', '/en/services/server-security/', '/en/services/email-security-phishing-protection/', '/en/services/incident-response/', '/en/cybersecurity-san-antonio-tx/', '/en/cybersecurity-bentonville-ar/', '/en/cybersecurity-for-small-business/'];
const others = existing.filter((d) => d.lang === lang).map((d) => `/${ES ? 'blog' : 'en/blog'}/${d.slug}/ — ${d.h1}`).slice(0, 25);

const prompt = ES ? `Eres editor de Inspector Hacker (inspectorhacker.com): vigilancia continua de ciberseguridad con IA para pymes en México y EE. UU., sin pentest caro. Planes: Arranque $2,000 USD una vez; Vigía $900 USD/mes; Vigía Plus $1,800 USD/mes (no cambies ni inventes precios).
Escribe UN artículo de blog en español de México (trato de "tú", directo, para dueños y gerentes de pymes) sobre: "${topic}".
Reglas duras:
- NO inventes estadísticas, porcentajes, montos, casos, clientes, testimonios ni certificaciones. Si das una cifra, debe venir de una fuente oficial o reconocida con URL real y estable (gob.mx, dof.gob.mx, ic3.gov, cisa.gov, ftc.gov, nist.gov, ibm.com, verizon.com, owasp.org, centros de ayuda oficiales). Si no estás seguro de la URL exacta, NO des la cifra.
- Pasos accionables y concretos (listas). 1,000 a 1,400 palabras. 5 a 7 secciones. 3 a 4 preguntas frecuentes.
- Enlaza 2 a 4 páginas internas SOLO de esta lista: ${internal.join(', ')}. Puedes enlazar artículos existentes: ${others.join(' | ') || 'ninguno'}.
- La última sección conecta con la vigilancia continua sin ser vendedora.
- HTML permitido en intro y secciones: p, ul, ol, li, strong, em, a, h3.
Responde SOLO con JSON válido: {"slug":"kebab-case-sin-acentos","title":"≤60 caracteres","h1":"...","description":"140-160 caracteres","category":"...","readingMinutes":6,"intro":"<p>...</p>","sections":[{"h2":"...","html":"..."}],"faq":[{"q":"...","a":"texto plano"}],"sources":[{"title":"...","url":"https://..."}]}`
  : `You are the editor of Inspector Hacker (inspectorhacker.com): continuous AI cybersecurity monitoring for small businesses in Mexico and the US, without an expensive pentest. Plans: Onboarding $2,000 USD once; Vigía $900 USD/month; Vigía Plus $1,800 USD/month (never change or invent prices).
Write ONE blog article in US English (plain, direct, for small-business owners and managers) about: "${topic}".
Hard rules:
- Do NOT invent statistics, percentages, dollar amounts, cases, clients, testimonials or certifications. Any figure must come from an official or well-known source with a real, stable URL (ftc.gov, ic3.gov, cisa.gov, nist.gov, sba.gov, fcc.gov, hhs.gov, ibm.com, verizon.com, owasp.org, official help centers). If unsure of the exact URL, leave the figure out.
- Actionable, concrete steps (lists). 1,000-1,400 words. 5-7 sections. 3-4 FAQs.
- Link 2-4 internal pages ONLY from this list: ${internal.join(', ')}. You may link existing articles: ${others.join(' | ') || 'none'}.
- The last section connects to continuous monitoring without being salesy.
- Allowed HTML in intro and sections: p, ul, ol, li, strong, em, a, h3.
Reply ONLY with valid JSON: {"slug":"kebab-case","title":"≤60 chars","h1":"...","description":"140-160 chars","category":"...","readingMinutes":6,"intro":"<p>...</p>","sections":[{"h2":"...","html":"..."}],"faq":[{"q":"...","a":"plain text"}],"sources":[{"title":"...","url":"https://..."}]}`;

async function chat(base, key, model, label) {
  const res = await fetch(base.replace(/\/$/, '') + '/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}` },
    body: JSON.stringify({ model, temperature: 0.5, max_tokens: 6000, response_format: { type: 'json_object' }, messages: [{ role: 'user', content: prompt }] }),
  });
  const raw = await res.text();
  if (!res.ok) throw new Error(`${label} ${res.status}: ${raw.slice(0, 200)}`);
  return JSON.parse(raw).choices[0].message.content;
}
async function gemini(key) {
  const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${key}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseMimeType: 'application/json', temperature: 0.5 } }),
  });
  const raw = await res.text();
  if (!res.ok) throw new Error(`Gemini ${res.status}: ${raw.slice(0, 200)}`);
  return JSON.parse(raw).candidates[0].content.parts.map((p) => p.text).join('');
}
async function anthropic(key) {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'x-api-key': key, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify({ model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-5', max_tokens: 8000, messages: [{ role: 'user', content: prompt }] }),
  });
  const raw = await res.text();
  if (!res.ok) throw new Error(`Anthropic ${res.status}: ${raw.slice(0, 200)}`);
  return JSON.parse(raw).content.map((c) => c.text || '').join('');
}

async function generate() {
  const k = (n) => (process.env[n] || '').trim();
  const tries = [];
  if (k('DEEPSEEK_API_KEY')) for (const m of (process.env.DEEPSEEK_MODEL || 'deepseek-chat,deepseek-v4-flash').split(','))
    tries.push(() => chat(process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com/v1', k('DEEPSEEK_API_KEY'), m.trim(), `DeepSeek(${m})`));
  if (k('GEMINI_API_KEY')) tries.push(() => gemini(k('GEMINI_API_KEY')));
  if (k('OPENAI_API_KEY')) tries.push(() => chat('https://api.openai.com/v1', k('OPENAI_API_KEY'), 'gpt-4o-mini', 'OpenAI'));
  if (k('ANTHROPIC_API_KEY')) tries.push(() => anthropic(k('ANTHROPIC_API_KEY')));
  if (!tries.length) {
    console.log('::warning::Falta una API key de IA. Pega DEEPSEEK_API_KEY en GitHub → inspector-hacker → Settings → Secrets and variables → Actions → New repository secret.');
    process.exit(0);
  }
  for (const t of tries) {
    try { return await t(); } catch (e) { console.warn('→', e.message); }
  }
  throw new Error('Todos los proveedores de IA fallaron');
}

const exists = (p) => fs.existsSync(path.join(ROOT, p.replace(/^\//, ''), 'index.html'));
async function urlOk(u) {
  try {
    const r = await fetch(u, { method: 'GET', redirect: 'follow', headers: { 'User-Agent': 'Mozilla/5.0 (InspectorHacker blog checker)' } });
    return r.status < 400;
  } catch { return false; }
}

const text = (await generate()).replace(/^```(?:json)?\s*|\s*```$/g, '');
const d = JSON.parse(text.slice(text.indexOf('{'), text.lastIndexOf('}') + 1));
d.slug = String(d.slug || topic).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 80);
if (usedSlugs.has(`${lang}-${d.slug}`)) d.slug += '-' + today;

// Fuentes: solo las que responden
const okSources = [];
for (const s of d.sources || []) if (s?.url?.startsWith('https://') && (await urlOk(s.url))) okSources.push({ title: s.title, url: s.url });
const dropped = new Set((d.sources || []).map((s) => s.url).filter((u) => !okSources.some((o) => o.url === u)));

// Limpia HTML: enlaces internos inexistentes o externos a fuentes caídas se convierten en texto
const clean = (html = '') => html
  .replace(/<(?!\/?(p|ul|ol|li|strong|em|a|h3)\b)[^>]*>/gi, '')
  .replace(/<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/gis, (m, href, inner) => {
    if (href.startsWith('/')) return exists(href.split('#')[0]) ? `<a href="${href}">${inner}</a>` : inner;
    if (href.startsWith('https://') && !dropped.has(href)) return `<a href="${href}" target="_blank" rel="noopener">${inner}</a>`;
    return inner;
  });
d.intro = clean(d.intro);
d.sections = (d.sections || []).filter((s) => s?.h2 && s?.html).map((s) => ({ h2: s.h2.replace(/<[^>]+>/g, ''), html: clean(s.html) }));
const all = d.intro + d.sections.map((s) => s.html).join(' ');
const words = all.replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
const hasFigures = /\d+(\.\d+)?\s?%|\$\s?\d|millones|million|billion/i.test(all);
if (words < 700 || d.sections.length < 4) throw new Error(`Artículo demasiado corto (${words} palabras, ${d.sections.length} secciones)`);
if (hasFigures && okSources.length === 0) throw new Error('El artículo trae cifras sin ninguna fuente verificable; se descarta.');

const post = {
  lang, slug: d.slug, pair: null, topic, title: d.title, h1: d.h1, description: d.description, date: today, updated: today,
  category: d.category || 'Blog', readingMinutes: Number(d.readingMinutes) || Math.max(4, Math.round(words / 220)),
  intro: d.intro, sections: d.sections, faq: (d.faq || []).filter((f) => f?.q && f?.a).map((f) => ({ q: f.q, a: String(f.a).replace(/<[^>]+>/g, '') })),
  sources: okSources, related: [], generated: true,
};
fs.writeFileSync(path.join(BLOG_DIR, `${lang}-${post.slug}.json`), JSON.stringify(post, null, 2) + '\n');
console.log(`✓ ${lang}-${post.slug}.json (${words} palabras, ${okSources.length} fuentes verificadas, ${dropped.size} descartadas)`);

execSync('python3 scripts/build_seo.py --blog && python3 scripts/build_sitemap.py', { cwd: ROOT, stdio: 'inherit' });

const url = `${SITE}/${ES ? 'blog' : 'en/blog'}/${post.slug}/`;
const urlList = [url, `${SITE}/${ES ? 'blog' : 'en/blog'}/`];
fs.writeFileSync(path.join(ROOT, '_src', 'last-indexnow.json'), JSON.stringify(urlList) + '\n');
console.log('URL nueva:', url);
