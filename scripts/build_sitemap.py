#!/usr/bin/env python3
"""Genera sitemap.xml con todas las páginas y alternates hreflang de los pares es/en."""
import os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://inspectorhacker.com"
TODAY = datetime.date.today().isoformat()
# (ruta, prioridad, par en el otro idioma o None)
PAGES = [
    ("/", "1.0", "/en/"), ("/en/", "0.9", "/"),
    ("/planes/", "0.9", "/en/pricing/"), ("/en/pricing/", "0.9", "/planes/"),
    ("/vigilancia-vs-pentest/", "0.8", "/en/monitoring-vs-pentest/"), ("/en/monitoring-vs-pentest/", "0.8", "/vigilancia-vs-pentest/"),
    ("/ciberseguridad-pymes-mexico/", "0.8", "/en/cybersecurity-for-small-business/"), ("/en/cybersecurity-for-small-business/", "0.8", "/ciberseguridad-pymes-mexico/"),
    ("/ciberseguridad-torreon/", "0.8", None), ("/ciberseguridad-la-laguna/", "0.7", None), ("/ciberseguridad-monterrey/", "0.8", None),
    ("/ciberseguridad-saltillo/", "0.7", None), ("/ciberseguridad-chihuahua/", "0.7", None),
    ("/en/cybersecurity-bentonville-ar/", "0.8", None), ("/en/cybersecurity-northwest-arkansas/", "0.7", None), ("/en/cybersecurity-san-antonio-tx/", "0.8", None),
]
def is_en(p): return p.startswith("/en/")
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for path, prio, pair in PAGES:
    assert os.path.exists(os.path.join(ROOT, path.strip("/"), "index.html")), path
    out.append("  <url>")
    out.append(f"    <loc>{SITE}{path}</loc>")
    out.append(f"    <lastmod>{TODAY}</lastmod>")
    out.append("    <changefreq>weekly</changefreq>" if path in ("/", "/en/") else "    <changefreq>monthly</changefreq>")
    out.append(f"    <priority>{prio}</priority>")
    es = pair if is_en(path) else path
    en = path if is_en(path) else pair
    if es: out.append(f'    <xhtml:link rel="alternate" hreflang="es-MX" href="{SITE}{es}"/>')
    if en: out.append(f'    <xhtml:link rel="alternate" hreflang="en-US" href="{SITE}{en}"/>')
    out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{es or en}"/>')
    out.append("  </url>")
out.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"sitemap.xml: {len(PAGES)} URLs")
