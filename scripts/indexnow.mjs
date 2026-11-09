#!/usr/bin/env node
/**
 * Avisa a IndexNow (Bing, Yandex, Seznam, Naver…) de URLs nuevas o actualizadas.
 * Uso: node scripts/indexnow.mjs https://inspectorhacker.com/a/ https://inspectorhacker.com/b/
 *      node scripts/indexnow.mjs --file _src/last-indexnow.json   (arreglo JSON de URLs)
 */
import fs from 'node:fs';
const HOST = 'inspectorhacker.com';
const KEY = '06bce93312ef6d54ca1c53c7c15a6228';
const args = process.argv.slice(2);
let urls = args[0] === '--file' ? JSON.parse(fs.readFileSync(args[1], 'utf8')) : args;
urls = urls.filter((u) => u.startsWith(`https://${HOST}/`));
if (!urls.length) { console.log('[indexnow] sin URLs'); process.exit(0); }
for (let i = 0; i < urls.length; i += 10000) {
  const res = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList: urls.slice(i, i + 10000) }),
  });
  console.log('[indexnow] api.indexnow.org', res.status, `(${Math.min(10000, urls.length - i)} URLs)`);
}
