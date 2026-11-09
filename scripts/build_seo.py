#!/usr/bin/env python3
"""Genera páginas servicio × ciudad, hubs (Servicios, Ciudades, Blog) y artículos del blog.

Uso:
  python3 scripts/build_seo.py          # todo (servicios, ciudades, hubs y blog)
  python3 scripts/build_seo.py --blog   # solo blog (lo usa el workflow diario)

Los artículos viven en _src/blog/<lang>-<slug>.json (Jekyll no publica carpetas con _).
Reutiliza render() de build_pages.py para que todo comparta diseño y schema.
"""
import glob, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp
from seo_data import SERVICES, SERVICE_ORDER, IND_ES, IND_EN, CITIES_MX, CITIES_US, PUBLISHED, POSITIONING_ES, POSITIONING_EN

ROOT, SITE, TODAY = bp.ROOT, bp.SITE, bp.TODAY
ES, EN = bp.ES, bp.EN
GENERATED = []  # rutas escritas en esta corrida

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
def fecha_es(iso):
    d = datetime.date.fromisoformat(iso); return f"{d.day} de {MESES[d.month-1]} de {d.year}"
def fecha_en(iso):
    d = datetime.date.fromisoformat(iso); return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")

def write(p):
    out_dir = os.path.join(ROOT, p["path"].strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(bp.render(p))
    GENERATED.append(p["path"])

def lc(t):
    return t[0].lower() + t[1:]

def spath(lang, skey, city=None):
    S = SERVICES[skey][lang]
    base = f"/servicios/{S['slug']}/" if lang == "es" else f"/en/services/{S['slug']}/"
    return base + (city["slug"] + "/" if city else "")

# ------------------------------------------------------------------ blog
def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "_src", "blog", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        d["path"] = ("/blog/" if d["lang"] == "es" else "/en/blog/") + d["slug"] + "/"
        posts.append(d)
    posts.sort(key=lambda d: (d["date"], d["slug"]), reverse=True)
    return posts

POSTS = load_posts()
POST_BY = {(d["lang"], d["slug"]): d for d in POSTS}

BLOG_FOR_SERVICE = {
    "es": {"monitoreo": "costo-de-un-incidente-de-ciberseguridad-pyme", "auditoria": "checklist-seguridad-tienda-en-linea-shopify-woocommerce",
           "servidores": "como-saber-si-tu-servidor-esta-expuesto", "correo": "whatsapp-business-hackeado-que-revisar", "incidentes": "ransomware-pymes-mexico"},
    "en": {"monitoreo": "ftc-safeguards-rule-small-business", "auditoria": "shopify-woocommerce-security-checklist",
           "servidores": "when-do-you-need-a-pentest", "correo": "whatsapp-business-meta-account-hacked", "incidentes": "cost-of-a-cybersecurity-incident-small-business"},
}
def blog_link(lang, skey):
    d = POST_BY.get((lang, BLOG_FOR_SERVICE[lang][skey]))
    if not d: return ""
    if lang == "es":
        return f' Si quieres profundizar, lee nuestra guía: <a href="{d["path"]}">{d["h1"]}</a>.'
    return f' For more detail, read our guide: <a href="{d["path"]}">{d["h1"]}</a>.'

def build_blog():
    for d in POSTS:
        es = d["lang"] == "es"; L = ES if es else EN
        pair = POST_BY.get(("en" if es else "es", d.get("pair") or ""))
        body = [("", [d["intro"]])] + [(s["h2"], [s["html"]]) for s in d["sections"]]
        if d.get("sources"):
            lis = "".join(f'<li><a href="{bp.esc(s["url"])}" target="_blank" rel="noopener">{s["title"]}</a></li>' for s in d["sources"])
            body.append(("Fuentes" if es else "Sources", [f"<ul>{lis}</ul>"]))
        same = [x for x in POSTS if x["lang"] == d["lang"] and x["slug"] != d["slug"]][:6]
        grid = [(x["path"], x["h1"], x.get("category", "")) for x in same]
        upd = (f'Publicado el <time datetime="{d["date"]}">{fecha_es(d["date"])}</time> · actualizado el <time datetime="{d["updated"]}">{fecha_es(d["updated"])}</time> · {d.get("readingMinutes", 6)} min de lectura'
               if es else f'Published <time datetime="{d["date"]}">{fecha_en(d["date"])}</time> · updated <time datetime="{d["updated"]}">{fecha_en(d["updated"])}</time> · {d.get("readingMinutes", 6)} min read')
        write(dict(path=d["path"], L=L, kind="article", article_type="BlogPosting", og_type="article",
                   title=d["title"] + " · Inspector Hacker", desc=d["description"], kick=d.get("category", "Blog"), h1=d["h1"], sub=d["description"],
                   published=d["date"], modified=d["updated"], upd=upd, pair=pair["path"] if pair else None,
                   crumbs=[("Blog", "/blog/" if es else "/en/blog/")], body=body, faq=[(f["q"], f["a"]) for f in d.get("faq", [])],
                   grid=grid, grid_lab="Blog", grid_h2="Más artículos" if es else "More articles",
                   grid_extra=(bp.ES_RELATED if es else bp.EN_RELATED)))
    for lang in ("es", "en"):
        es = lang == "es"; L = ES if es else EN
        mine = [x for x in POSTS if x["lang"] == lang]
        items = "".join(f'<li><a href="{x["path"]}"><strong>{x["h1"]}</strong></a> · <time datetime="{x["date"]}">{fecha_es(x["date"]) if es else fecha_en(x["date"])}</time><br>{x["description"]}</li>' for x in mine)
        if es:
            body = [("Guías de ciberseguridad para pymes", [
                "Artículos prácticos para dueños y gerentes de pymes en México: qué revisar, qué hacer cuando ya pasó algo y cómo decidir en qué invertir. Sin tecnicismos innecesarios y con fuentes cuando damos cifras. Publicamos un artículo nuevo casi todos los días, en español e inglés.",
                f"<ul>{items}</ul>"])]
            faq = [("¿Cada cuándo publican?", "Casi todos los días, alternando español e inglés. Los artículos en inglés están en la sección /en/blog/."),
                   ("¿Puedo pedir un tema?", "Sí. Escríbenos por WhatsApp al +52 871 263 8082 con la duda que tienes y la convertimos en guía.")]
        else:
            body = [("Cybersecurity guides for small businesses", [
                "Practical articles for small-business owners and managers in the US: what to check, what to do when something already happened and how to decide where to invest. No unnecessary jargon, and sources whenever we give numbers. We publish a new article almost every day, in English and Spanish.",
                f"<ul>{items}</ul>"])]
            faq = [("How often do you publish?", "Almost every day, alternating English and Spanish. Spanish articles live at /blog/."),
                   ("Can I request a topic?", "Yes. Message us on WhatsApp at +52 871 263 8082 with your question and we will turn it into a guide.")]
        write(dict(path="/blog/" if es else "/en/blog/", L=L, kind="hub", published=PUBLISHED,
                   title=("Blog de ciberseguridad para pymes · Inspector Hacker" if es else "Small business cybersecurity blog · Inspector Hacker"),
                   desc=("Guías prácticas de ciberseguridad para pymes de México: WhatsApp hackeado, ransomware, servidores expuestos, tiendas en línea y protección de datos." if es else
                         "Practical cybersecurity guides for US small businesses: hacked WhatsApp and Meta accounts, online store security, FTC Safeguards Rule, incident costs."),
                   kick="Blog", h1=("Blog de <em>ciberseguridad</em> para pymes" if es else "Small business <em>cybersecurity</em> blog"),
                   sub=(POSITIONING_ES + " Aquí publicamos lo que vemos en el día a día." if es else POSITIONING_EN + " Here we publish what we see every day."),
                   pair="/en/blog/" if es else "/blog/", body=body, faq=faq,
                   grid=[(x["path"], x["h1"], x.get("category", "")) for x in mine], grid_lab="Blog", grid_h2=("Todos los artículos" if es else "All articles"),
                   grid_extra=(bp.ES_RELATED if es else bp.EN_RELATED)))

# ------------------------------------------------------------------ servicio × ciudad
def city_service(lang, c, skey):
    es = lang == "es"; L = ES if es else EN
    S = SERVICES[skey][lang]; IND = IND_ES if es else IND_EN
    i0, i1, i2 = [IND[k] for k in c["ind"]]
    path = spath(lang, skey, c)
    others_here = [k for k in c["services"] if k != skey]
    cities = CITIES_MX if es else CITIES_US
    same_elsewhere = [x for x in cities if skey in x["services"] and x["key"] != c["key"]]
    other_links = ", ".join(f'<a href="{spath(lang, k, c)}">{lc(SERVICES[k][lang]["name"])}</a>' for k in others_here)
    if es:
        title = f"{S['name']} en {c['name']}, {c['region']} · Inspector Hacker"
        if len(title) > 75: title = f"{S['name']} en {c['name']} · Inspector Hacker"
        desc = f"{S['name']} para empresas de {c['name']}, {c['region']}: {lc(S['short'])}. Precios en USD, accesos de solo lectura, sin pentest caro."
        body = [
            (f"Por qué {S['art']} {S['noun']} importa en {c['name']}", [c["context"],
                f"En <strong>{i0['name']}</strong>, {i0['risk']}. {i0['s'][skey]}",
                f"En <strong>{i1['name']}</strong> el patrón se repite con otra cara: {i1['s'][skey][0].lower() + i1['s'][skey][1:]}"]),
            (f"Qué incluye el servicio en {c['name']}", [S["what"], "<ul>" + "".join(f"<li>{x}</li>" for x in S["includes"]) + "</ul>"]),
            (f"Lo que vemos en {i2['name']}", [f"En {i2['name']}, {i2['risk']}. {i2['s'][skey]}" + blog_link(lang, skey)]),
            ("Cómo trabajamos", [c["local"],
                'Todos los accesos son de solo lectura, el alcance queda escrito en contrato y NDA, y tú autorizas cada escaneo. No lanzamos ataques contra tus sistemas: es <a href="/vigilancia-vs-pentest/">vigilancia, no pentest</a>.'
                + (f' Más contexto de la ciudad en <a href="{c["existing"]}">ciberseguridad en {c["name"] if c["key"] != "gomez" else "La Laguna"}</a>.' if c.get("existing") else "")
                + (f" En {c['name']} también ofrecemos {other_links}." if others_here else "")]),
            ("Cuánto cuesta", [S["plan"] + " Mismo precio en dólares en México y Estados Unidos; contrato mínimo de 3 meses en planes mensuales."]),
        ]
        faq = [(f"¿Cuánto cuesta {S['art']} {S['noun']} para una empresa de {c['name']}?", bp.strip_tags(S["plan"])),
               (f"¿Atienden en {c['name']} de forma presencial?", c["local"])] + list(S["faq"])
        kick = f"{S['short']} · {c['name']}, {c['region']}"
        h1 = f"{S['name']} en <em>{c['name']}</em>"
        sub = f"{S['name']} para empresas de {c['name']}, con foco en {i0['name']} y {i1['name']}. {POSITIONING_ES}"
        crumbs = [("Servicios", "/servicios/"), (S["name"], spath(lang, skey))]
        grid_h2 = f"{S['name']} en otras ciudades y más servicios en {c['name']}"
        grid = [(spath(lang, skey, x), x["name"], S["name"]) for x in same_elsewhere] + [(spath(lang, k, c), SERVICES[k][lang]["name"], c["name"]) for k in others_here]
        extra = [("/ciudades/", "Todas las ciudades", "Servicios por ciudad"), (spath(lang, skey), S["name"], "Página del servicio"), ("/planes/", "Planes y precios", "Arranque, Vigía, Vigía Plus"), ("/blog/", "Blog", "Guías prácticas")]
    else:
        title = f"{S['name']} in {c['name']}, {c['region']} · Inspector Hacker"
        if len(title) > 75: title = f"{S['name']} in {c['name']} · Inspector Hacker"
        desc = f"{S['name']} for {c['name']}, {c['region']} businesses: {lc(S['short'])}. USD pricing, read-only access, no expensive pentest."
        body = [
            (f"Why {S['noun']} matters in {c['name']}", [c["context"],
                f"For <strong>{i0['name']}</strong>, {i0['risk']}. {i0['s'][skey]}",
                f"For <strong>{i1['name']}</strong> the pattern looks different but rhymes: {i1['s'][skey][0].lower() + i1['s'][skey][1:]}"]),
            (f"What the service includes in {c['name']}", [S["what"], "<ul>" + "".join(f"<li>{x}</li>" for x in S["includes"]) + "</ul>"]),
            (f"What we see in {i2['name']}", [f"In {i2['name']}, {i2['risk']}. {i2['s'][skey]}" + blog_link(lang, skey)]),
            ("How we work", [c["local"],
                'All access is read-only, the scope is written into a contract and NDA, and you authorize every scan. We never attack your systems: it is <a href="/en/monitoring-vs-pentest/">monitoring, not pentesting</a>.'
                + (f' More local context on our <a href="{c["existing"]}">{c["name"] if c["key"] in ("sanantonio", "bentonville") else "Northwest Arkansas"} cybersecurity page</a>.' if c.get("existing") else "")
                + (f" In {c['name']} we also offer {other_links}." if others_here else "")]),
            ("Pricing", [S["plan"] + " Same USD price in the US and Mexico; 3-month minimum on monthly plans."]),
        ]
        faq = [(f"How much does {S['noun']} cost for a {c['name']} business?", bp.strip_tags(S["plan"])),
               (f"Do you work on site in {c['name']}?", c["local"])] + list(S["faq"])
        kick = f"{S['short']} · {c['name']}, {c['region']}"
        h1 = f"{S['name']} in <em>{c['name']}</em>"
        sub = f"{S['name']} for {c['name']} businesses, with a focus on {i0['name']} and {i1['name']}. {POSITIONING_EN}"
        crumbs = [("Services", "/en/services/"), (S["name"], spath(lang, skey))]
        grid_h2 = f"{S['name']} in other cities and more services in {c['name']}"
        grid = [(spath(lang, skey, x), x["name"] + ", " + x["region"], S["name"]) for x in same_elsewhere] + [(spath(lang, k, c), SERVICES[k][lang]["name"], c["name"]) for k in others_here]
        extra = [("/en/cities/", "All cities", "Services by city"), (spath(lang, skey), S["name"], "Service page"), ("/en/pricing/", "Plans and pricing", "Onboarding, Vigía, Vigía Plus"), ("/en/blog/", "Blog", "Practical guides")]
    write(dict(path=path, L=L, kind="local", published=PUBLISHED, title=title, desc=desc, kick=kick, h1=h1, sub=sub,
               geo=c["geo"], city=c["name"], region=c["region"], country="MX" if es else "US", service_name=f"{S['name']} {'en' if es else 'in'} {c['name']}",
               service_type=S["stype"], crumbs=crumbs, body=body, faq=faq, grid=grid, grid_extra=extra,
               grid_lab=("Ciudades y servicios" if es else "Cities and services"), grid_h2=grid_h2))

def service_hub(lang, skey):
    es = lang == "es"; L = ES if es else EN
    S = SERVICES[skey][lang]; other = SERVICES[skey]["en" if es else "es"]
    cities = [c for c in (CITIES_MX if es else CITIES_US) if skey in c["services"]]
    city_lis = "".join(f'<li><a href="{spath(lang, skey, c)}">{S["name"]} {"en" if es else "in"} {c["name"]}</a> · {c["region"]}</li>' for c in cities)
    if es:
        body = [(f"Qué es {S['art']} {S['noun']}", [S["what"]]),
                ("Qué incluye", ["<ul>" + "".join(f"<li>{x}</li>" for x in S["includes"]) + "</ul>"]),
                ("Cómo se contrata", [S["plan"], 'Accesos de solo lectura, alcance por escrito, NDA y sin ataques contra producción: <a href="/vigilancia-vs-pentest/">vigilancia, no pentest</a>.' + blog_link(lang, skey)]),
                ("Dónde lo ofrecemos", ["Operamos desde Torreón para todo México y desde Bentonville y San Antonio para Estados Unidos. Páginas por ciudad:", f"<ul>{city_lis}</ul>",
                                        f'In English: <a href="{spath("en", skey)}" hreflang="en" lang="en">{other["name"]}</a>.'])]
        faq = list(S["faq"]) + [(f"¿En qué ciudades ofrecen {S['noun']}?", "En todo México de forma remota, con páginas para " + ", ".join(c["name"] for c in cities) + ". En Estados Unidos atendemos en inglés desde Bentonville y San Antonio."),
                                (f"¿Cuánto cuesta {S['art']} {S['noun']}?", bp.strip_tags(S["plan"]))]
        title = f"{S['name']} para pymes en México · Inspector Hacker"
        desc = f"{S['name']} para pymes de México: {S['short'].lower()}. Accesos de solo lectura, reporte mensual y precios en USD. Vigilancia, no pentest."
        crumbs = [("Servicios", "/servicios/")]; grid_h2 = f"{S['name']} por ciudad"
        sub = f"{S['short']}. {POSITIONING_ES}"
        grid = [(spath(lang, skey, c), c["name"], c["region"]) for c in cities]
        extra = [("/servicios/", "Todos los servicios", "Monitoreo, web, servidores, correo, incidentes"), ("/ciudades/", "Todas las ciudades", "Servicios por ciudad"), ("/planes/", "Planes y precios", "Arranque, Vigía, Vigía Plus")]
    else:
        body = [(f"What {S['noun']} is", [S["what"]]),
                ("What's included", ["<ul>" + "".join(f"<li>{x}</li>" for x in S["includes"]) + "</ul>"]),
                ("How it's sold", [S["plan"], 'Read-only access, written scope, NDA and no attacks against production: <a href="/en/monitoring-vs-pentest/">monitoring, not pentesting</a>.' + blog_link(lang, skey)]),
                ("Where we offer it", ["We work from Bentonville and San Antonio for the United States and from Torreón for Mexico. City pages:", f"<ul>{city_lis}</ul>",
                                       f'En español: <a href="{spath("es", skey)}" hreflang="es" lang="es">{other["name"]}</a>.'])]
        faq = list(S["faq"]) + [(f"Which cities do you offer {S['noun']} in?", "Anywhere in the US remotely, with city pages for " + ", ".join(c["name"] for c in cities) + ". In Mexico we work in Spanish from Torreón."),
                                (f"How much does {S['noun']} cost?", bp.strip_tags(S["plan"]))]
        title = f"{S['name']} for small businesses · Inspector Hacker"
        desc = f"{S['name']} for US small businesses: {S['short'].lower()}. Read-only access, monthly report, USD pricing. Monitoring, not pentesting."
        crumbs = [("Services", "/en/services/")]; grid_h2 = f"{S['name']} by city"
        sub = f"{S['short']}. {POSITIONING_EN}"
        grid = [(spath(lang, skey, c), c["name"] + ", " + c["region"], S["name"]) for c in cities]
        extra = [("/en/services/", "All services", "Monitoring, web, servers, email, incidents"), ("/en/cities/", "All cities", "Services by city"), ("/en/pricing/", "Plans and pricing", "Onboarding, Vigía, Vigía Plus")]
    write(dict(path=spath(lang, skey), L=L, kind="local", published=PUBLISHED, title=title, desc=desc, kick=S["short"], h1=S["name"], sub=sub,
               geo=None, service_name=S["name"], service_type=S["stype"], pair=spath("en" if es else "es", skey), crumbs=crumbs,
               body=body, faq=faq, grid=grid, grid_extra=extra, grid_lab=("Ciudades" if es else "Cities"), grid_h2=grid_h2))

def services_index(lang):
    es = lang == "es"; L = ES if es else EN
    lis = "".join(f'<li><a href="{spath(lang, k)}"><strong>{SERVICES[k][lang]["name"]}</strong></a>: {SERVICES[k][lang]["short"].lower()}.</li>' for k in SERVICE_ORDER)
    if es:
        body = [("Cinco servicios, una sola vigilancia", [POSITIONING_ES + " Todo arranca con un inventario de lo que tu empresa tiene expuesto a internet y sigue con agentes de IA que lo revisan cada semana. Estos son los servicios, que puedes contratar juntos dentro de un plan o por separado:", f"<ul>{lis}</ul>",
                 'Si no sabes por dónde empezar, el <a href="/planes/">Arranque de $2,000 USD</a> te da el inventario y un reporte con prioridades. Y si te piden un pentest, primero lee <a href="/vigilancia-vs-pentest/">vigilancia vs pentest</a>.'])]
        faq = [("¿Puedo contratar un solo servicio?", "Sí. La auditoría web y la respuesta a incidentes se venden por separado; el monitoreo, servidores y correo se contratan dentro de los planes Vigía o Vigía Plus."),
               ("¿Hacen pentest?", "No como servicio principal. Somos vigilancia continua. Si un cliente o aseguradora te exige un pentest manual, lo cotizamos aparte con un socio certificado.")]
    else:
        body = [("Five services, one monitoring program", [POSITIONING_EN + " Everything starts with an inventory of what your business exposes to the internet, followed by AI agents that review it every week. These are the services, available together in a plan or separately:", f"<ul>{lis}</ul>",
                 'If you are not sure where to start, <a href="/en/pricing/">Onboarding at $2,000 USD</a> gives you the inventory and a prioritized report. If someone asked you for a pentest, read <a href="/en/monitoring-vs-pentest/">monitoring vs pentest</a> first.'])]
        faq = [("Can I buy a single service?", "Yes. The website audit and incident response are sold separately; monitoring, server and email security are delivered within the Vigía or Vigía Plus plans."),
               ("Do you do pentests?", "Not as our core service. We do continuous monitoring. If a customer or insurer requires a manual pentest, we quote it separately with a certified partner.")]
    write(dict(path="/servicios/" if es else "/en/services/", L=L, kind="hub", published=PUBLISHED,
               title=("Servicios de ciberseguridad para pymes · Inspector Hacker" if es else "Small business cybersecurity services · Inspector Hacker"),
               desc=("Monitoreo de ciberseguridad, auditoría web, seguridad de servidores, protección de correo y respuesta a incidentes para pymes de México y EE. UU." if es else
                     "Cybersecurity monitoring, website audits, server security, email protection and incident response for small businesses in the US and Mexico."),
               kick=("Servicios" if es else "Services"), h1=("Servicios de <em>ciberseguridad</em>" if es else "Cybersecurity <em>services</em>"),
               sub=(POSITIONING_ES if es else POSITIONING_EN), pair="/en/services/" if es else "/servicios/", body=body, faq=faq,
               grid=[(spath(lang, k), SERVICES[k][lang]["name"], SERVICES[k][lang]["short"]) for k in SERVICE_ORDER],
               grid_extra=(bp.ES_RELATED if es else bp.EN_RELATED), grid_lab=("Servicios" if es else "Services"), grid_h2=("Elige un servicio" if es else "Pick a service")))

def cities_hub(lang):
    es = lang == "es"; L = ES if es else EN
    cities = CITIES_MX if es else CITIES_US
    blocks = []
    for c in cities:
        links = " · ".join(f'<a href="{spath(lang, k, c)}">{SERVICES[k][lang]["name"]}</a>' for k in c["services"])
        main = f' · <a href="{c["existing"]}">{"página de la ciudad" if es else "city page"}</a>' if c.get("existing") else ""
        blocks.append(f"<h3>{c['name']}, {c['region']}</h3><p>{links}{main}</p>")
    if es:
        body = [("Ciberseguridad para pymes por ciudad", ["Operamos desde Torreón para todo México. La vigilancia es remota y funciona igual en cualquier ciudad; estas páginas explican qué cambia en cada zona según sus industrias. Para Estados Unidos, ve la página en inglés: <a href=\"/en/cities/\" hreflang=\"en\" lang=\"en\">Cities</a>."] + blocks
                 + ['Otras páginas: <a href="/ciberseguridad-la-laguna/">La Laguna</a> · <a href="/ciberseguridad-pymes-mexico/">pymes de México</a>.'])]
        faq = [("¿Atienden en mi ciudad si no aparece aquí?", "Sí. La vigilancia es remota y atendemos todo México y Estados Unidos. Estas páginas son las ciudades donde más trabajamos o donde más nos buscan."),
               ("¿Las reuniones pueden ser presenciales?", "En la Comarca Lagunera (Torreón, Gómez Palacio y Lerdo), sí. En el resto del país la llamada mensual es por videollamada y, para el Arranque o un incidente, podemos viajar.")]
        grid = [(c.get("existing") or spath(lang, c["services"][0], c), c["name"], c["region"]) for c in cities]
    else:
        body = [("Small business cybersecurity by city", ["We work from Bentonville and San Antonio for the United States. Monitoring is remote and works the same anywhere; these pages explain what changes in each area based on its industries. For Mexico, see the Spanish page: <a href=\"/ciudades/\" hreflang=\"es\" lang=\"es\">Ciudades</a>."] + blocks
                 + ['More pages: <a href="/en/cybersecurity-northwest-arkansas/">Northwest Arkansas</a> · <a href="/en/cybersecurity-for-small-business/">small business</a>.'])]
        faq = [("Do you work in my city if it isn't listed?", "Yes. Monitoring is remote and we serve the whole United States and Mexico. These are the cities where we work most or get the most requests."),
               ("Can meetings be in person?", "In Northwest Arkansas and San Antonio, yes. Elsewhere the monthly call is by video, and we can travel for onboarding or an incident.")]
        grid = [(c.get("existing") or spath(lang, c["services"][0], c), c["name"] + ", " + c["region"], ", ".join(SERVICES[k][lang]["name"] for k in c["services"][:2])) for c in cities]
    write(dict(path="/ciudades/" if es else "/en/cities/", L=L, kind="hub", published=PUBLISHED,
               title=("Ciberseguridad por ciudad en México · Inspector Hacker" if es else "Cybersecurity by city in the US · Inspector Hacker"),
               desc=("Servicios de ciberseguridad para pymes en Torreón, Gómez Palacio, Saltillo, Monterrey, Chihuahua, Durango, CDMX, Guadalajara, Querétaro y Ramos Arizpe." if es else
                     "Cybersecurity services for small businesses in San Antonio, Bentonville, Rogers, Fayetteville, Austin and Dallas. Monitoring, not pentesting."),
               kick=("Ciudades" if es else "Cities"), h1=("Ciberseguridad por <em>ciudad</em>" if es else "Cybersecurity by <em>city</em>"),
               sub=(POSITIONING_ES if es else POSITIONING_EN), pair="/en/cities/" if es else "/ciudades/", body=body, faq=faq,
               grid=grid, grid_extra=(bp.ES_RELATED if es else bp.EN_RELATED)[1:], grid_lab=("Ciudades" if es else "Cities"), grid_h2=("Elige tu ciudad" if es else "Pick your city")))

def main():
    blog_only = "--blog" in sys.argv
    if not blog_only:
        for lang, cities in (("es", CITIES_MX), ("en", CITIES_US)):
            for c in cities:
                for k in c["services"]:
                    city_service(lang, c, k)
            for k in SERVICE_ORDER:
                service_hub(lang, k)
            services_index(lang)
            cities_hub(lang)
    build_blog()
    print(f"build_seo: {len(GENERATED)} páginas ({len(POSTS)} artículos)")

if __name__ == "__main__":
    main()
