#!/usr/bin/env python3
"""Verifica que todo href/src interno de los HTML del repo exista como archivo."""
import os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)]
bad = 0; total = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    for attr, link in re.findall(r'(href|src)="([^"]+)"', s):
        if link.startswith(("http", "mailto:", "tel:", "#", "data:")) and not link.startswith("https://inspectorhacker.com"):
            continue
        link = link.replace("https://inspectorhacker.com", "")
        link = link.split("#")[0].split("?")[0]
        if not link: continue
        total += 1
        target = os.path.join(ROOT, link.lstrip("/")) if link.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(f), link))
        if os.path.isdir(target): target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            bad += 1; print(f"ROTO  {os.path.relpath(f, ROOT)} -> {link}")
print(f"{total} enlaces internos revisados en {len(files)} archivos, {bad} rotos")
sys.exit(1 if bad else 0)
