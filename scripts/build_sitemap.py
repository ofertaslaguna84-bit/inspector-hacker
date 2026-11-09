#!/usr/bin/env python3
"""Genera sitemap.xml escaneando todos los index.html del sitio.

Toma de cada página su canonical, sus alternates hreflang (es-MX / en-US / x-default)
y su dateModified del JSON-LD (si no hay, la fecha de hoy). Así cualquier página nueva
(blog diario incluido) entra sola al sitemap con su par de idioma.
"""
import glob, os, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://inspectorhacker.com"
TODAY = datetime.date.today().isoformat()

def prio(path):
    if path in ("/", "/en/"): return "1.0"
    if path in ("/planes/", "/en/pricing/", "/servicios/", "/en/services/", "/ciudades/", "/en/cities/", "/blog/", "/en/blog/"): return "0.9"
    if path.count("/") <= 3 and not path.startswith(("/blog/", "/en/blog/")): return "0.8"
    return "0.7"

entries = []
for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(("_", ".", "scripts")) or "/_" in rel: continue
    s = open(f, encoding="utf-8").read()
    if re.search(r'<meta name="robots" content="[^"]*noindex', s): continue
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not m or not m.group(1).startswith(SITE): continue
    loc = m.group(1); path = loc[len(SITE):]
    alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s)
    mods = re.findall(r'"dateModified":"(\d{4}-\d{2}-\d{2})', s)
    entries.append((path, loc, alts, max(mods) if mods else TODAY))

def order(e):
    p = e[0]; return (0 if p in ("/", "/en/") else 1, p.startswith("/en/"), p)
entries.sort(key=order)
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for path, loc, alts, mod in entries:
    out += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{mod}</lastmod>",
            "    <changefreq>weekly</changefreq>" if path in ("/", "/en/", "/blog/", "/en/blog/") else "    <changefreq>monthly</changefreq>",
            f"    <priority>{prio(path)}</priority>"]
    for hl, href in alts:
        out.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>')
    out.append("  </url>")
out.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"sitemap.xml: {len(entries)} URLs")
