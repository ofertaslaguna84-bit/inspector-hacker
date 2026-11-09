#!/usr/bin/env python3
"""Genera las páginas locales, de planes y de comparación de inspectorhacker.com.

Uso:  python3 scripts/build_pages.py
Salida: carpetas con index.html en la raíz del repo (es) y en /en (en).
El CSS se toma del index.html raíz para que todo se vea igual.
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://inspectorhacker.com"
TODAY = datetime.date.today().isoformat()
WA = "https://wa.me/528712638082"
CAL = "https://calendar.app.google/rz32YjLinKvYWUTT9"
WA_ES = WA + "?text=Quiero%20el%20diagn%C3%B3stico%20de%2015%20minutos%20de%20Inspector%20Hacker"
WA_EN = WA + "?text=I%20want%20the%2015-minute%20Inspector%20Hacker%20assessment"

with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
    home = f.read()
CSS = re.search(r"<style>(.*?)</style>", home, re.S).group(1)
EXTRA_CSS = """
.hero.sm{padding:130px 0 60px}.hero.sm .w{grid-template-columns:1fr}
.crumbs{font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--ink3);margin-bottom:18px}.crumbs a{color:var(--ink2)}.crumbs span{margin:0 8px}
.prose{max-width:820px}.prose h2{font-size:clamp(24px,2.8vw,32px);margin:38px 0 12px}.prose h2:first-child{margin-top:0}.prose p{color:var(--ink2);font-size:16.5px;margin-bottom:16px}.prose ul{margin:0 0 18px 22px;color:var(--ink2);font-size:16px}.prose li{margin-bottom:8px}.prose a{color:var(--cy)}.prose strong{color:#fff}
.plan.cmp ul{margin-bottom:16px}.plan.cmp li{font-size:13.5px}
.cities{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.cities a{display:block;background:var(--bg3);border:1px solid var(--line);border-radius:12px;padding:16px 18px;font-size:14.5px;color:var(--ink2)}.cities a:hover{border-color:var(--cy);color:#fff}.cities a b{display:block;color:#fff;margin-bottom:3px}
.tbl.cmp td:nth-child(2),.tbl.cmp td:nth-child(3){color:var(--ink2);font-family:'Space Grotesk',system-ui,sans-serif;font-size:14px;white-space:normal}
@media(max-width:860px){.hero.sm{padding-top:110px}}
"""
GRAB = '<script src="/js/grabovoi.js" defer data-bg="linear-gradient(90deg,#06252b,#0e1218,#123640,#0e1218,#06252b)" data-num="#22d3ee" data-desc="rgba(34,211,238,.55)" data-sep="rgba(255,255,255,.25)"></script>'
WA_SVG = '<svg viewBox="0 0 24 24" fill="#fff" width="28"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.126.553 4.123 1.522 5.858L0 24l6.338-1.498A11.95 11.95 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.897 0-3.668-.508-5.194-1.396l-.371-.22-3.762.889.906-3.63-.243-.385A9.94 9.94 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>'

# ---------------------------------------------------------------- entidad global
ORG = {
    "@context": "https://schema.org",
    "@type": ["Organization", "ProfessionalService"],
    "@id": SITE + "/#org",
    "name": "Inspector Hacker",
    "alternateName": ["Inspector Hacker · Ciberseguridad con IA", "Inspector Hacker · AI Cybersecurity Monitoring"],
    "url": SITE + "/",
    "logo": SITE + "/img/logo-negro-1024.png",
    "image": SITE + "/img/og.jpg",
    "slogan": "Vigilancia continua de ciberseguridad con IA para pymes en México y EE. UU., sin pentest caro.",
    "description": "Vigilancia continua de ciberseguridad con IA para pymes en México y EE. UU., sin pentest caro. Agentes de IA revisan todos los días lo expuesto a internet, el código, los servidores y la nube; aviso en menos de 24 horas ante una vulnerabilidad crítica y reporte mensual revisado por una persona. Vigilancia, no pentest.",
    "foundingDate": "2026",
    "parentOrganization": {"@type": "Organization", "name": "GH Specialist", "url": "https://ghspecialist.com/"},
    "address": {"@type": "PostalAddress", "addressLocality": "Torreón", "addressRegion": "Coahuila", "addressCountry": "MX"},
    "areaServed": [
        {"@type": "Country", "name": "México"},
        {"@type": "Country", "name": "United States"},
        {"@type": "City", "name": "Torreón", "containedInPlace": {"@type": "State", "name": "Coahuila"}},
        {"@type": "City", "name": "Gómez Palacio", "containedInPlace": {"@type": "State", "name": "Durango"}},
        {"@type": "City", "name": "Lerdo", "containedInPlace": {"@type": "State", "name": "Durango"}},
        {"@type": "City", "name": "Monterrey", "containedInPlace": {"@type": "State", "name": "Nuevo León"}},
        {"@type": "City", "name": "Saltillo", "containedInPlace": {"@type": "State", "name": "Coahuila"}},
        {"@type": "City", "name": "Chihuahua", "containedInPlace": {"@type": "State", "name": "Chihuahua"}},
        {"@type": "City", "name": "Bentonville", "containedInPlace": {"@type": "State", "name": "Arkansas"}},
        {"@type": "City", "name": "Rogers", "containedInPlace": {"@type": "State", "name": "Arkansas"}},
        {"@type": "City", "name": "Springdale", "containedInPlace": {"@type": "State", "name": "Arkansas"}},
        {"@type": "City", "name": "Fayetteville", "containedInPlace": {"@type": "State", "name": "Arkansas"}},
        {"@type": "City", "name": "San Antonio", "containedInPlace": {"@type": "State", "name": "Texas"}},
    ],
    "knowsAbout": ["Vigilancia de seguridad con IA", "AI security monitoring", "Revisión de código", "Code review for security", "Monitoreo de servidores VPS", "VPS server monitoring", "Phishing simulado", "Simulated phishing", "Respuesta a incidentes", "Incident response", "Attack surface monitoring", "Vulnerability monitoring"],
    "knowsLanguage": ["es", "en"],
    "priceRange": "$$$",
    "currenciesAccepted": "USD, MXN",
    "telephone": "+52-871-263-8082",
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+52-871-263-8082", "availableLanguage": ["Spanish", "English"], "url": WA},
    "sameAs": ["https://ghspecialist.com/"],
}

# ---------------------------------------------------------------- textos comunes
ES = dict(
    lang="es-MX", og_locale="es_MX", home="/", home_name="Inicio",
    nav=[("/", "Inicio"), ("/planes/", "Planes"), ("/servicios/", "Servicios"), ("/ciudades/", "Ciudades"), ("/blog/", "Blog")],
    cta_btn="Diagnóstico de 15 min", wa=WA_ES, upd=f'Actualizado el <time datetime="{TODAY}">{TODAY}</time> · precios en USD · mismo precio en México y EE. UU.',
    plans_lab="Planes", plans_h2="Arranque una vez, vigilancia cada mes",
    plans_lead='Mismo precio en dólares en México y Estados Unidos. Contrato mínimo 3 meses; después mes a mes. Pago anual por adelantado: 10 % de descuento. <a href="/planes/" style="color:var(--cy)">Ver todos los planes y extras →</a>',
    plans=[
        ("Arranque · una vez", "$2,000", "USD", "Se paga antes de empezar; también se vende solo", ["Inventario de todo lo expuesto a internet", "Revisión inicial de repositorio y servidores", "Instalación de la vigilancia", "Reporte con prioridades + sesión de 1 h"], False),
        ("Vigía · mensual · más pedido", "$900", "USD / mes", "1 servidor VPS + 1 organización de GitHub + sitio web", ["Escaneo semanal de lo expuesto", "Revisión con IA de cada cambio al código", "Vigilancia de amenazas para tu tecnología", "Reporte mensual + llamada de 30 min"], True),
        ("Vigía Plus · mensual", "$1,800", "USD / mes", "Hasta 5 servidores, varias apps, nube e identidad", ["Lectura de código real en varias apps", "Nube (AWS, Azure, GCP, Vercel, DigitalOcean) y Microsoft 365 / Google Workspace", "Plan de respuesta a incidentes + simulacro anual", "Reporte Dirección + técnico; 2 llamadas al mes"], False),
    ],
    plans_foot='<b style="color:#fff">Empresa:</b> más de 5 servidores o varias razones sociales, <b style="color:var(--cy)">desde $3,500 USD al mes</b>, cotización a la medida.',
    faq_lab="Preguntas frecuentes", cities_lab="Dónde atendemos", cities_h2="Ciudades y páginas relacionadas",
    cta_h2="¿Sabes qué tienes expuesto a internet hoy?", cta_p="Diagnóstico de 15 minutos sin costo, por videollamada. Te decimos qué tienes, quién lo cuida y con qué plan arrancar.",
    cta_wa="WhatsApp", cta_cal="Agendar llamada",
    foot_a='<b style="color:#fff">Inspector Hacker</b> · Ciberseguridad con IA · Torreón, México · Bentonville y San Antonio, EE. UU.',
    foot_links=[("/planes/", "Planes"), ("/servicios/", "Servicios"), ("/ciudades/", "Ciudades"), ("/blog/", "Blog"), ("/vigilancia-vs-pentest/", "Vigilancia vs pentest"), ("/llms.txt", "llms.txt")],
    foot_b='+52 871 263 8082 · un servicio de <a href="https://ghspecialist.com/" rel="noopener">GH Specialist</a> · © 2026',
    other_lang=("en", "EN", "English version"),
)
EN = dict(
    lang="en-US", og_locale="en_US", home="/en/", home_name="Home",
    nav=[("/en/", "Home"), ("/en/pricing/", "Pricing"), ("/en/services/", "Services"), ("/en/cities/", "Cities"), ("/en/blog/", "Blog")],
    cta_btn="15-min assessment", wa=WA_EN, upd=f'Updated <time datetime="{TODAY}">{TODAY}</time> · prices in USD · same price in the US and Mexico',
    plans_lab="Plans", plans_h2="Onboarding once, monitoring every month",
    plans_lead='Same price in USD in the United States and Mexico. 3-month minimum; month to month after that. Annual prepayment: 10% off. <a href="/en/pricing/" style="color:var(--cy)">See all plans and extras →</a>',
    plans=[
        ("Onboarding · one time", "$2,000", "USD", "Paid before we start; also sold on its own", ["Inventory of everything exposed to the internet", "Initial review of repository and servers", "Monitoring setup", "Prioritized report + 1-hour session"], False),
        ("Vigía · monthly · most popular", "$900", "USD / month", "1 VPS server + 1 GitHub organization + website", ["Weekly scan of what is exposed", "AI review of every code change", "Threat monitoring for your stack", "Monthly report + 30-minute call"], True),
        ("Vigía Plus · monthly", "$1,800", "USD / month", "Up to 5 servers, several apps, cloud and identity", ["Real code reading across several apps", "Cloud (AWS, Azure, GCP, Vercel, DigitalOcean) and Microsoft 365 / Google Workspace", "Incident response plan + annual drill", "Management + technical report; 2 calls a month"], False),
    ],
    plans_foot='<b style="color:#fff">Enterprise:</b> more than 5 servers or several legal entities, <b style="color:var(--cy)">from $3,500 USD a month</b>, custom quote.',
    faq_lab="Frequently asked questions", cities_lab="Where we work", cities_h2="Cities and related pages",
    cta_h2="Do you know what you have exposed to the internet today?", cta_p="Free 15-minute assessment over a video call. We tell you what you have, who is looking after it and which plan to start with.",
    cta_wa="WhatsApp", cta_cal="Book a call",
    foot_a='<b style="color:#fff">Inspector Hacker</b> · AI Cybersecurity · Bentonville and San Antonio, USA · Torreón, Mexico',
    foot_links=[("/en/pricing/", "Pricing"), ("/en/services/", "Services"), ("/en/cities/", "Cities"), ("/en/blog/", "Blog"), ("/en/monitoring-vs-pentest/", "Monitoring vs pentest"), ("/llms.txt", "llms.txt")],
    foot_b='+52 871 263 8082 · a service of <a href="https://ghspecialist.com/" rel="noopener">GH Specialist</a> · © 2026',
    other_lang=("es", "ES", "Versión en español"),
)

ES_CITIES = [
    ("/ciberseguridad-torreon/", "Torreón", "Coahuila"),
    ("/ciberseguridad-la-laguna/", "La Laguna", "Gómez Palacio y Lerdo"),
    ("/ciberseguridad-monterrey/", "Monterrey", "Nuevo León"),
    ("/ciberseguridad-saltillo/", "Saltillo", "Coahuila"),
    ("/ciberseguridad-chihuahua/", "Chihuahua", "Chihuahua"),
    ("/ciberseguridad-pymes-mexico/", "Pymes de México", "Todo el país"),
]
EN_CITIES = [
    ("/en/cybersecurity-bentonville-ar/", "Bentonville, AR", "Benton County"),
    ("/en/cybersecurity-northwest-arkansas/", "Northwest Arkansas", "Rogers, Springdale, Fayetteville"),
    ("/en/cybersecurity-san-antonio-tx/", "San Antonio, TX", "Bexar County"),
    ("/en/cybersecurity-for-small-business/", "Small business", "United States"),
]
ES_RELATED = [("/ciudades/", "Todas las ciudades", "Servicios por ciudad en México"), ("/servicios/", "Servicios", "Monitoreo, web, servidores, correo, incidentes"), ("/blog/", "Blog", "Guías prácticas de ciberseguridad"), ("/planes/", "Planes y precios", "Arranque, Vigía, Vigía Plus, Empresa"), ("/vigilancia-vs-pentest/", "Vigilancia vs pentest", "Cuándo conviene cada una")]
EN_RELATED = [("/en/cities/", "All cities", "Services by city in the US"), ("/en/services/", "Services", "Monitoring, web, servers, email, incidents"), ("/en/blog/", "Blog", "Practical cybersecurity guides"), ("/en/pricing/", "Plans and pricing", "Onboarding, Vigía, Vigía Plus, Enterprise"), ("/en/monitoring-vs-pentest/", "Monitoring vs pentest", "When each one makes sense")]

# ---------------------------------------------------------------- páginas
PAGES = []

def page(**kw):
    PAGES.append(kw)

# ===== ES: Torreón
page(path="/ciberseguridad-torreon/", L=ES, kind="local",
     title="Ciberseguridad para empresas en Torreón, Coahuila · Inspector Hacker",
     desc="Vigilancia de ciberseguridad con IA para pymes de Torreón: lo que tienes expuesto a internet, tu código y tus servidores revisados todos los días, con reporte mensual. Desde $900 USD/mes.",
     kick="Ciberseguridad con IA · Torreón, Coahuila", h1="Ciberseguridad para empresas en <em>Torreón</em>",
     sub="Somos de Torreón. Vigilamos todos los días lo que tu empresa tiene expuesto a internet, tu código y tus servidores, y cada mes te lo explicamos en una llamada. Sin pentest, sin susto: vigilancia.",
     geo=("MX-COA", "Torreón, Coahuila, México", "25.5428, -103.4068"), city="Torreón", region="Coahuila", country="MX",
     service_name="Vigilancia de ciberseguridad con IA en Torreón",
     body=[
        ("Qué le pasa a una empresa de Torreón cuando la hackean", [
            "En Torreón la mayoría de las empresas no tiene un equipo de seguridad: tiene un proveedor de sistemas, un contador que maneja el SAT y un ERP que alguien instaló hace años. Eso funciona hasta que un día el correo de Dirección manda una factura con otra CLABE, el servidor de la nómina amanece cifrado o aparece un dominio casi igual al tuyo pidiéndole datos a tus clientes.",
            "Los casos que vemos más seguido en empresas de la región son de tres tipos: <strong>correo corporativo sin SPF, DKIM y DMARC</strong>, lo que permite que cualquiera mande correos a nombre de tu empresa; <strong>servidores con escritorio remoto, VPN o paneles abiertos a internet</strong> para que el proveedor entre desde su casa; y <strong>contraseñas repetidas</strong> entre el ERP, el correo y el banco que ya se filtraron en alguna brecha de otro servicio.",
            "Ninguno de esos problemas necesita un hacker genio. Necesita que nadie esté mirando. Y en una distribuidora, una metalmecánica, una clínica, un despacho o una constructora de la Comarca, normalmente nadie está mirando.",
        ]),
        ("Cómo funciona la vigilancia", [
            "Arrancamos con un inventario de todo lo que tu empresa tiene expuesto: dominios, IPs, puertos, certificados, correo y servicios en la nube. Luego instalamos agentes de IA que revisan cada semana ese inventario, cada cambio que entra a tu código y las amenazas nuevas que salen para la tecnología que usas. Si aparece una vulnerabilidad crítica de tu stack, te avisamos en menos de 24 horas con qué hacer.",
            "Cada mes recibes dos hojas: una para Dirección, en español llano, y una técnica para tu equipo de TI o tu proveedor. Y una llamada de 30 minutos con una persona que sí leyó el reporte. Si tu proveedor de sistemas es de aquí mismo, mejor: el reporte técnico le dice exactamente qué corregir y nosotros no competimos con él.",
            "Todos los accesos son de solo lectura, el alcance queda escrito en contrato y NDA, y tú autorizas cada escaneo. Nunca lanzamos ataques contra tus sistemas en producción.",
        ]),
        ("Por qué contratarlo desde Torreón", [
            "La operación es remota, pero la empresa está aquí: la llamada mensual puede ser en persona si estás en Torreón, Gómez Palacio o Lerdo. Si además tienes clientes o proveedores en Estados Unidos, el mismo servicio atiende en inglés en Bentonville y San Antonio con el mismo precio en dólares.",
        ]),
     ],
     faq=[
        ("¿Atienden empresas pequeñas en Torreón?", "Sí. El plan Vigía ($900 USD al mes) está pensado para una empresa con un servidor, un repositorio de código y un sitio web. Si solo tienes sitio web y correo, el Arranque de $2,000 USD una sola vez te dice cómo estás sin mensualidad."),
        ("¿Tienen oficina en Torreón?", "Inspector Hacker es un servicio de GH Specialist, con sede en Torreón, Coahuila. La vigilancia es remota; la llamada mensual puede ser presencial en la Comarca Lagunera o por videollamada."),
        ("¿Qué pasa si ya tengo proveedor de sistemas?", "Lo normal es que lo tengas y lo conserves. Nosotros vigilamos y reportamos; él corrige. El reporte técnico mensual va dirigido a él, con la lista priorizada de lo que hay que arreglar."),
        ("¿Esto sirve si solo uso WhatsApp, correo y un ERP?", "Sí. Correo y ERP son justo lo que más se ataca en una pyme: suplantación de correos para cambiar cuentas de pago y accesos remotos al ERP abiertos a internet. El inventario inicial lo detecta y la vigilancia avisa si algo cambia."),
        ("¿Cuánto tardan en arrancar?", "El diagnóstico dura 15 minutos. Después de firmar contrato y recibir los accesos de solo lectura, el Arranque termina con un reporte y una sesión de 1 hora. A partir de ahí la vigilancia corre todos los días."),
        ("¿Cobran en pesos o en dólares?", "Los precios se publican en dólares y son los mismos en México y Estados Unidos; puedes pagar en pesos al tipo de cambio del día. Vigía son $900 USD al mes, Vigía Plus $1,800 USD, Empresa desde $3,500 USD."),
     ])

# ===== ES: La Laguna
page(path="/ciberseguridad-la-laguna/", L=ES, kind="local",
     title="Ciberseguridad para empresas de La Laguna: Gómez Palacio y Lerdo · Inspector Hacker",
     desc="Vigilancia de ciberseguridad con IA para empresas de la Comarca Lagunera: Gómez Palacio, Lerdo y Torreón. Inventario de lo expuesto, revisión de código y servidores, reporte mensual. Desde $900 USD/mes.",
     kick="Ciberseguridad con IA · Comarca Lagunera", h1="Ciberseguridad para empresas de <em>La Laguna</em>: Gómez Palacio y Lerdo",
     sub="Parques industriales, agroindustria, transporte y empresas familiares de la Comarca Lagunera. Vigilancia continua con IA y una llamada al mes para explicarte qué tienes expuesto y qué corregir.",
     geo=("MX-DUR", "Gómez Palacio, Durango, México", "25.5699, -103.4959"), city="Gómez Palacio", region="Durango", country="MX",
     service_name="Vigilancia de ciberseguridad con IA en La Laguna",
     extra_cities=["Lerdo", "Torreón"],
     body=[
        ("La Laguna es una sola región con dos estados y muchas empresas familiares", [
            "Gómez Palacio y Lerdo comparten con Torreón la misma economía: parques industriales, agroindustria, lácteos, transporte y una red enorme de empresas familiares que proveen a las grandes. Lo que no comparten es un equipo de ciberseguridad. En la empresa típica de la región, sistemas lo lleva una persona o un proveedor externo que también instala cámaras, configura el router y da de alta usuarios.",
            "Eso produce un patrón que se repite: <strong>varias sucursales o naves con la misma contraseña de administrador</strong>, <strong>routers, cámaras y controles de acceso con credenciales de fábrica visibles desde internet</strong>, y <strong>respaldos guardados en el mismo servidor</strong> que se cifraría en un ataque de ransomware. Si la empresa además factura a clientes grandes, tarde o temprano le llega un cuestionario de seguridad que nadie sabe contestar.",
        ]),
        ("Qué hace la vigilancia en una empresa de Gómez Palacio o Lerdo", [
            "Primero el inventario: qué dominios, IPs, puertos, servicios y certificados tiene tu empresa expuestos, y cómo está configurado tu correo (SPF, DKIM, DMARC) para que nadie mande facturas a tu nombre. Después, agentes de IA que repiten esa revisión cada semana, leen cada cambio que entra a tu código si tienes sistemas propios, y vigilan las amenazas nuevas de la tecnología que usas: vulnerabilidades publicadas, credenciales tuyas filtradas en brechas de otros servicios y dominios parecidos al tuyo registrados para phishing.",
            "Cuando algo crítico aparece, te avisamos en menos de 24 horas. Cada mes, reporte de una hoja para Dirección, reporte técnico para quien te lleva sistemas y una llamada de 30 minutos. Todo con accesos de solo lectura y alcance escrito en contrato.",
        ]),
        ("Qué plan conviene en la región", [
            "Una empresa con un servidor, un sistema propio y un sitio web cabe en <strong>Vigía</strong> ($900 USD al mes). Una industria con varias naves, nube e identidad en Microsoft 365 o Google Workspace suele necesitar <strong>Vigía Plus</strong> ($1,800 USD al mes), que incluye un plan de respuesta a incidentes escrito y un simulacro anual. Si solo quieres saber cómo estás, el <strong>Arranque</strong> de $2,000 USD se vende solo. Los extras, como la simulación de phishing para tu personal ($4 USD por usuario al mes, mínimo 20), se cobran aparte.",
            "Estamos en Torreón, a minutos de Gómez Palacio y Lerdo: la llamada mensual puede ser presencial.",
        ]),
     ],
     faq=[
        ("¿Atienden Gómez Palacio y Lerdo igual que Torreón?", "Sí. Operamos desde Torreón y toda la Comarca Lagunera es local para nosotros: Gómez Palacio, Lerdo, Francisco I. Madero, San Pedro y Matamoros. La llamada mensual puede ser presencial."),
        ("Tengo varias naves o sucursales, ¿cuenta como un servidor?", "Depende de cuántos servidores y servicios tengas expuestos. El diagnóstico de 15 minutos lo aclara: con un servidor y un repositorio es Vigía; con varios servidores, nube e identidad es Vigía Plus; más de 5 servidores es plan Empresa."),
        ("Mi cliente grande me pidió un cuestionario de seguridad, ¿me ayudan?", "El Arranque te deja un inventario y un reporte con prioridades que responde buena parte de esas preguntas, y el reporte mensual sirve como evidencia de que alguien vigila. No emitimos certificaciones; si tu cliente exige una, te decimos qué falta."),
        ("¿Revisan cámaras, routers y equipos de la nave?", "Revisamos lo que esté expuesto a internet: si una cámara, un router o un panel de control se ve desde afuera, aparece en el inventario y en el reporte. No instalamos nada en tus equipos salvo que contrates el antivirus gestionado como extra."),
        ("¿Qué pasa si nos atacan a media noche?", "Si eres cliente con plan tienes prioridad. La respuesta a incidente se cobra aparte a $2,500 USD por día (mínimo 1 día): contención, análisis de qué pasó, recuperación y reporte. En Vigía Plus ya tienes el plan de respuesta escrito antes de que pase."),
     ])

# ===== ES: Monterrey
page(path="/ciberseguridad-monterrey/", L=ES, kind="local",
     title="Ciberseguridad para empresas en Monterrey, Nuevo León · Inspector Hacker",
     desc="Vigilancia de ciberseguridad con IA para pymes y proveedores de corporativos en Monterrey: código, servidores, nube y lo expuesto a internet, revisados todos los días. Reporte mensual. Desde $900 USD/mes.",
     kick="Ciberseguridad con IA · Monterrey, Nuevo León", h1="Ciberseguridad para empresas en <em>Monterrey</em>",
     sub="Si le vendes a un corporativo regio o a una empresa de Estados Unidos, tarde o temprano te van a preguntar quién vigila tu seguridad. Nosotros la vigilamos todos los días y te damos el reporte para contestar.",
     geo=("MX-NLE", "Monterrey, Nuevo León, México", "25.6866, -100.3161"), city="Monterrey", region="Nuevo León", country="MX",
     service_name="Vigilancia de ciberseguridad con IA en Monterrey",
     extra_cities=["San Pedro Garza García", "Apodaca", "San Nicolás de los Garza"],
     body=[
        ("El riesgo en Monterrey es ser el proveedor chico de un cliente grande", [
            "Monterrey concentra corporativos, plantas y una ola de empresas que llegaron con el nearshoring. Alrededor de cada una hay cientos de proveedores medianos y pequeños: despachos, integradores, transportistas, desarrolladores de software, agencias, maquiladoras de servicios. Esos proveedores son el camino más corto para entrar al grande, y los atacantes lo saben.",
            "Lo que vemos en empresas de la zona metropolitana: <strong>repositorios de código con llaves y contraseñas guardadas dentro</strong>, <strong>nubes en AWS, Azure o GCP configuradas rápido para salir a producción</strong> y nunca revisadas, <strong>accesos de exempleados que siguen vivos</strong> en Microsoft 365 o Google Workspace, y cuestionarios de seguridad del cliente corporativo contestados de buena fe sin que nadie haya verificado nada.",
        ]),
        ("Qué hace la vigilancia con IA", [
            "El Arranque deja un inventario de todo lo expuesto a internet y una revisión inicial de tu código, servidores y nube, con una lista de corrección por prioridad. Después, los agentes revisan cada semana ese inventario, leen cada cambio que entra al repositorio buscando secretos, dependencias vulnerables y configuraciones peligrosas, y vigilan las amenazas nuevas de tu tecnología. Ante una vulnerabilidad crítica de tu stack, aviso en menos de 24 horas.",
            "Cada mes recibes el reporte de Dirección en una hoja y el reporte técnico para tu equipo, además de una llamada. Para una empresa que desarrolla software o tiene equipo de TI, <strong>Vigía Plus</strong> ($1,800 USD al mes) cubre varias apps y repositorios con lectura de código real, nube e identidad, un plan de respuesta a incidentes escrito y simulacro anual, y dos llamadas al mes. Una startup o una agencia con un servidor y un repositorio cabe en <strong>Vigía</strong> ($900 USD al mes).",
        ]),
        ("Vigilancia, no pentest", [
            "No vendemos pruebas de penetración ni ataques autónomos contra producción. Si tu cliente te exige un pentest, lo cotizamos aparte con un socio, por día ($1,500–$2,500 USD por día de tester) y leemos el reporte contigo. Lo nuestro es lo de todos los días, con accesos de solo lectura y alcance escrito. <a href=\"/vigilancia-vs-pentest/\">Aquí explicamos la diferencia</a>.",
            "Operamos de forma remota desde Torreón, a cuatro horas de Monterrey, y en inglés para tus clientes de Texas y Arkansas al mismo precio en dólares.",
        ]),
     ],
     faq=[
        ("¿Sirve para contestar el cuestionario de seguridad de mi cliente corporativo?", "Ayuda mucho: el inventario, la lista de correcciones y el reporte mensual son evidencia de que alguien vigila y de que las fallas se corrigen. No sustituye una certificación como ISO 27001; si tu cliente la exige, el plan Empresa se cotiza con ese requisito en mente."),
        ("Desarrollamos software, ¿leen el código?", "Sí. En Vigía se revisa con IA cada cambio que entra a un repositorio (secretos, dependencias, configuraciones). En Vigía Plus se hace lectura de código real en varias aplicaciones y repositorios."),
        ("¿Trabajan con AWS, Azure o Google Cloud?", "Sí, con acceso de solo lectura. Vigía Plus incluye la revisión de configuración de AWS, Azure, GCP, Vercel y DigitalOcean, y de identidad en Microsoft 365 o Google Workspace."),
        ("¿Van a Monterrey?", "La operación es remota y la llamada mensual es por videollamada; para Arranques de plan Empresa se puede acordar una sesión presencial. Torreón está a cuatro horas por carretera."),
        ("¿Por qué el precio es en dólares si estoy en México?", "Porque el servicio es el mismo en México y en Estados Unidos y las herramientas se pagan en dólares; publicamos el mismo precio en los dos países y puedes pagar en pesos al tipo de cambio del día."),
        ("¿Pueden hacer un pentest si me lo piden?", "Lo cotizamos aparte con un socio, por día de tester ($1,500–$2,500 USD; una app típica toma de 3 a 8 días). Nosotros definimos el alcance y leemos el reporte contigo."),
     ])

# ===== ES: Saltillo
page(path="/ciberseguridad-saltillo/", L=ES, kind="local",
     title="Ciberseguridad para empresas en Saltillo, Coahuila · Inspector Hacker",
     desc="Vigilancia de ciberseguridad con IA para proveedores automotrices, transportistas y pymes de Saltillo y Ramos Arizpe. Lo expuesto a internet, código y servidores revisados cada día. Desde $900 USD/mes.",
     kick="Ciberseguridad con IA · Saltillo, Coahuila", h1="Ciberseguridad para empresas en <em>Saltillo</em>",
     sub="Proveedores de la industria automotriz, transportistas, constructoras y despachos de Saltillo y Ramos Arizpe. Te vigilamos todos los días y te damos el reporte que te piden tus clientes.",
     geo=("MX-COA", "Saltillo, Coahuila, México", "25.4232, -101.0053"), city="Saltillo", region="Coahuila", country="MX",
     service_name="Vigilancia de ciberseguridad con IA en Saltillo",
     extra_cities=["Ramos Arizpe", "Arteaga"],
     body=[
        ("En Saltillo la seguridad te la exige la cadena", [
            "Saltillo y Ramos Arizpe viven de la industria automotriz y de todo lo que gira alrededor: proveedores de segundo y tercer nivel, moldes, estampado, logística, empaques, servicios de mantenimiento. En esa cadena las plantas grandes ya tienen requisitos de seguridad de la información y los van bajando a sus proveedores. El proveedor mediano recibe un cuestionario, una auditoría o una cláusula de contrato, y descubre que nadie en su empresa sabe qué tiene expuesto a internet.",
            "Lo típico que encontramos: <strong>el ERP o el sistema de embarques accesible desde internet</strong> para que la planta consulte avances, <strong>correos de compras sin autenticación</strong>, ideales para que alguien cambie una cuenta bancaria en una orden de pago, y <strong>un proveedor de TI que administra todo con una sola cuenta</strong> compartida entre varios clientes. Nada de esto sale en una auditoría de calidad, y todo esto es lo primero que busca un atacante.",
        ]),
        ("Qué recibe una empresa de Saltillo", [
            "Un inventario de lo que tu empresa tiene expuesto: dominios, IPs, puertos, certificados, correo y servicios en la nube, con una lista de corrección por prioridad. Luego vigilancia semanal con agentes de IA, revisión de cada cambio que entra a tu código si tienes sistemas propios, y aviso en menos de 24 horas si sale una vulnerabilidad crítica de tu tecnología o aparecen credenciales tuyas en una filtración.",
            "Cada mes, una hoja para Dirección y otra técnica para tu equipo o tu proveedor, y una llamada de 30 minutos. Ese reporte mensual es el documento que puedes enseñar cuando tu cliente pregunta quién vigila tu seguridad. Para plantas con varios servidores, nube e identidad corporativa, <strong>Vigía Plus</strong> incluye además un plan de respuesta a incidentes escrito y un simulacro anual.",
        ]),
        ("Lo que no hacemos", [
            "No lanzamos ataques contra tus sistemas en producción ni paramos una línea para probar nada. Todos los accesos son de solo lectura y el alcance queda en contrato y NDA. Si tu cliente te pide un pentest formal de una aplicación, lo cotizamos con un socio por día de tester y leemos el reporte contigo. La simulación de phishing para tu personal ($4 USD por usuario al mes, mínimo 20) y la capacitación de 6 horas ($2,000 USD) se contratan aparte.",
            "Saltillo está a tres horas de Torreón: la llamada mensual es por videollamada y las sesiones de Arranque pueden ser presenciales.",
        ]),
     ],
     faq=[
        ("Soy proveedor automotriz, ¿esto cubre lo que me pide mi cliente?", "Cubre la parte de vigilancia: inventario de lo expuesto, correcciones priorizadas y reporte mensual como evidencia. No somos auditores ni emitimos certificados; si tu cliente exige una certificación específica, te decimos qué falta y el plan Empresa se arma con ese requisito."),
        ("¿Pueden interrumpir la producción con sus escaneos?", "No. Los escaneos son de lo expuesto a internet, con accesos de solo lectura, autorizados por ti y sin ataques contra producción. No tocamos redes de planta ni equipos de línea."),
        ("¿Qué plan es para una empresa de transporte con un sistema de rastreo y oficinas?", "Normalmente Vigía ($900 USD al mes): un servidor, un repositorio o sistema y el sitio web. Si el rastreo, la facturación y el correo viven en varios servidores y en la nube, es Vigía Plus ($1,800 USD al mes)."),
        ("¿Incluye capacitar a mi gente contra phishing?", "Es un extra: simulación de phishing con campañas mensuales y video corto por tema, $4 USD por usuario al mes con mínimo 20 usuarios. También hay un taller de 6 horas para hasta 15 personas por $2,000 USD más viáticos."),
        ("¿Cuánto dura el contrato?", "Mínimo 3 meses y después mes a mes. Con pago anual por adelantado hay 10 % de descuento."),
     ])

# ===== ES: Chihuahua
page(path="/ciberseguridad-chihuahua/", L=ES, kind="local",
     title="Ciberseguridad para empresas en Chihuahua · Inspector Hacker",
     desc="Vigilancia de ciberseguridad con IA para maquiladoras, agroindustria y pymes de Chihuahua y Ciudad Juárez con corporativo en Estados Unidos. Reporte mensual en español e inglés. Desde $900 USD/mes.",
     kick="Ciberseguridad con IA · Chihuahua", h1="Ciberseguridad para empresas en <em>Chihuahua</em>",
     sub="Maquiladoras con corporativo en Estados Unidos, agroindustria, mineras y empresas familiares de Chihuahua y Ciudad Juárez. Vigilancia con IA todos los días y reporte mensual en español e inglés.",
     geo=("MX-CHH", "Chihuahua, Chihuahua, México", "28.6330, -106.0691"), city="Chihuahua", region="Chihuahua", country="MX",
     service_name="Vigilancia de ciberseguridad con IA en Chihuahua",
     extra_cities=["Ciudad Juárez", "Delicias", "Cuauhtémoc"],
     body=[
        ("Chihuahua: dos idiomas, dos países y un solo correo que atacar", [
            "En Chihuahua y Ciudad Juárez conviven la maquila con corporativo en Texas, Arizona o el medio oeste de Estados Unidos, la agroindustria de Delicias y Cuauhtémoc, la minería y una base enorme de empresas familiares. Muchas de esas empresas reciben las políticas de seguridad desde el corporativo en inglés y las aplica un departamento de sistemas local con poca gente. Otras, las que son dueñas de su operación, no tienen políticas en ningún idioma.",
            "Los problemas más comunes: <strong>correo de la operación mexicana sin SPF, DKIM y DMARC</strong>, aunque el corporativo sí los tenga; <strong>servicios locales expuestos a internet</strong>, como paneles de control, accesos remotos y sistemas de nómina, que el corporativo no ve porque no están en su red; y <strong>credenciales compartidas con transportistas, agentes aduanales y proveedores</strong> que nunca se rotan.",
        ]),
        ("Un servicio que reporta en español y en inglés", [
            "La vigilancia funciona igual que en cualquier ciudad: inventario de todo lo expuesto a internet, agentes de IA que lo revisan cada semana, lectura de cada cambio al código si tienes sistemas propios, vigilancia de amenazas para tu tecnología y aviso en menos de 24 horas ante una vulnerabilidad crítica. Lo distinto en Chihuahua es que el reporte mensual lo entregamos en el idioma que necesite cada quien: <strong>la hoja de Dirección en inglés para el corporativo y la hoja técnica en español para el equipo local</strong>, o al revés.",
            "El precio es el mismo en dólares en México y en Estados Unidos, así que el corporativo puede pagarlo desde allá o la operación local desde acá, sin diferencia. <strong>Vigía</strong> cubre un servidor, un repositorio y el sitio web por $900 USD al mes; <strong>Vigía Plus</strong> cubre hasta 5 servidores, varias apps, nube e identidad por $1,800 USD al mes; <strong>Empresa</strong>, desde $3,500 USD, es para operaciones con más de 5 servidores o varias razones sociales.",
        ]),
        ("Solo lectura y alcance escrito", [
            "Pedimos accesos de solo lectura: usuario de lectura en GitHub o GitLab, llave SSH de lectura, lectura en la nube y en el DNS. El alcance queda escrito en contrato y NDA, y tú autorizas cada escaneo. No hacemos pentest ni ataques autónomos contra producción; si el corporativo exige un pentest, lo cotizamos aparte con un socio, por día.",
            "Operamos remoto desde Torreón; la distancia no cambia el servicio porque la vigilancia es sobre lo que está en internet y la llamada mensual es por videollamada.",
        ]),
     ],
     faq=[
        ("¿Pueden reportarle al corporativo en inglés y a mi equipo en español?", "Sí. El reporte de Dirección y el técnico se entregan en el idioma que necesite cada lector, y la llamada mensual puede ser en inglés o en español."),
        ("¿Atienden Ciudad Juárez además de Chihuahua capital?", "Sí. El servicio es remoto y cubre todo el estado: Chihuahua, Ciudad Juárez, Delicias, Cuauhtémoc y Parral, con el mismo precio."),
        ("El corporativo ya tiene seguridad, ¿para qué lo necesito aquí?", "Porque lo que la operación local tiene expuesto a internet (correo propio, accesos remotos, sistemas de nómina o embarques) muchas veces no está en la red del corporativo y nadie lo vigila. El inventario inicial lo hace visible para los dos."),
        ("¿Qué accesos necesitan de mi parte?", "Solo lectura: GitHub o GitLab, llave SSH de lectura, acceso de lectura a la nube y al DNS. Nada de escritura y ningún cambio sin tu aprobación."),
        ("¿Cuánto cuesta arrancar?", "El Arranque son $2,000 USD una sola vez e incluye inventario, revisión inicial, instalación de la vigilancia y reporte con prioridades. Si solo quieres el diagnóstico inicial, el Arranque se vende solo, sin mensualidad."),
        ("¿Hay contrato mínimo?", "Sí, 3 meses; después mes a mes. Pago anual por adelantado: 10 % de descuento."),
     ])

# ===== ES: Pymes México
page(path="/ciberseguridad-pymes-mexico/", L=ES, kind="local",
     title="Ciberseguridad para pymes en México: vigilancia con IA desde $900 USD/mes · Inspector Hacker",
     desc="Ciberseguridad para pequeñas y medianas empresas de México sin equipo de seguridad: agentes de IA vigilan lo expuesto a internet, código y servidores, y una persona te explica el reporte cada mes.",
     kick="Ciberseguridad con IA · Pymes de México", h1="Ciberseguridad para <em>pymes</em> en México",
     sub="Para la empresa que no tiene equipo de seguridad y no lo va a tener: vigilancia continua con IA, aviso en menos de 24 horas y una llamada al mes con alguien que te explica qué corregir, en español llano.",
     geo=("MX-COA", "Torreón, Coahuila, México", "25.5428, -103.4068"), city=None, region=None, country="MX",
     service_name="Vigilancia de ciberseguridad con IA para pymes de México",
     pair="/en/cybersecurity-for-small-business/",
     body=[
        ("Por qué atacan a las pymes si \"no tienen nada que robar\"", [
            "Una pyme sí tiene qué robar: la cuenta bancaria, la nómina, la base de clientes, las facturas y, sobre todo, la confianza de sus clientes grandes. Los ataques modernos no eligen víctimas a mano: barren internet buscando correos sin autenticación, servidores con puertos abiertos, paneles con contraseñas por defecto y credenciales que ya se filtraron en otras brechas. La pyme cae porque es la que menos vigila, no porque sea la más interesante.",
            "Los tres golpes que más vemos en empresas mexicanas de 10 a 200 personas: <strong>el fraude del cambio de cuenta</strong>, donde un correo que parece de tu proveedor o de tu director pide pagar a otra CLABE; <strong>el ransomware</strong> que cifra el servidor de facturación y los respaldos que estaban en el mismo lugar; y <strong>la cuenta de correo tomada</strong> desde la que se manda phishing a todos tus clientes con tu nombre.",
        ]),
        ("Qué es la vigilancia con IA y en qué se diferencia de un antivirus o un pentest", [
            "El antivirus cuida las computadoras desde adentro. El pentest es una prueba puntual que un especialista hace una vez al año sobre una aplicación. La vigilancia es lo de en medio y lo de todos los días: agentes de IA que revisan cada semana lo que tu empresa tiene expuesto a internet, leen cada cambio que entra a tu código, siguen las amenazas nuevas de la tecnología que usas y avisan en menos de 24 horas cuando sale algo crítico. Y una persona que cada mes te explica el reporte. <a href=\"/vigilancia-vs-pentest/\">Aquí comparamos vigilancia y pentest</a>.",
            "Arrancamos con un inventario y una revisión inicial (el <strong>Arranque</strong>, $2,000 USD una sola vez). Después, <strong>Vigía</strong> por $900 USD al mes cubre un servidor VPS, una organización de GitHub y el sitio web, con reporte mensual y llamada de 30 minutos. <strong>Vigía Plus</strong>, $1,800 USD al mes, cubre varias apps, nube e identidad, y trae un plan de respuesta a incidentes escrito. El mismo precio aplica en México y en Estados Unidos.",
        ]),
        ("Qué necesitas de tu lado", [
            "Muy poco: 15 minutos para el diagnóstico, firmar contrato y NDA, y entregar accesos de solo lectura a tu repositorio, servidor, nube y DNS. No necesitas contratar a nadie ni cambiar de proveedor de sistemas; el reporte técnico mensual le dice a tu proveedor exactamente qué corregir. Atendemos a todo México desde Torreón, Coahuila, con páginas específicas para <a href=\"/ciberseguridad-torreon/\">Torreón</a>, <a href=\"/ciberseguridad-la-laguna/\">La Laguna</a>, <a href=\"/ciberseguridad-monterrey/\">Monterrey</a>, <a href=\"/ciberseguridad-saltillo/\">Saltillo</a> y <a href=\"/ciberseguridad-chihuahua/\">Chihuahua</a>.",
        ]),
     ],
     faq=[
        ("¿Qué tamaño de empresa es el ideal para Inspector Hacker?", "Empresas de 10 a 200 personas sin equipo de seguridad propio: una pyme con un servidor, un sistema y un sitio web cabe en Vigía; una con varios sistemas, nube e identidad corporativa en Vigía Plus; más de 5 servidores o varias razones sociales es plan Empresa."),
        ("¿Es un antivirus?", "No. El antivirus protege cada computadora desde adentro; la vigilancia revisa lo que tu empresa tiene expuesto a internet, tu código y tus servidores, y te avisa de amenazas nuevas. Si lo quieres, revendemos antivirus gestionado como extra ($12 USD por equipo al mes)."),
        ("¿Cuánto cuesta la ciberseguridad para una pyme con Inspector Hacker?", "Arranque $2,000 USD una vez; Vigía $900 USD al mes; Vigía Plus $1,800 USD al mes; Empresa desde $3,500 USD al mes. Contrato mínimo 3 meses, 10 % de descuento con pago anual."),
        ("¿Necesito tener programadores o repositorio de código?", "No. Si no tienes sistemas propios, la vigilancia se concentra en lo expuesto a internet, el correo, el servidor y la nube. Si los tienes, además se revisa cada cambio al código."),
        ("¿Qué pasa si ya me hackearon?", "La respuesta a incidente se contrata aparte: $2,500 USD por día, mínimo 1 día, con contención, análisis de qué pasó, recuperación y reporte. Los clientes con plan tienen prioridad."),
        ("¿Puedo pagar en pesos?", "Sí. Los precios se publican en dólares porque son los mismos en México y Estados Unidos; el pago en pesos se calcula al tipo de cambio del día."),
     ])

# ===== ES: Planes
page(path="/planes/", L=ES, kind="pricing", pair="/en/pricing/",
     title="Planes y precios · Vigilancia de ciberseguridad con IA · Inspector Hacker",
     desc="Precios de Inspector Hacker: Arranque $2,000 USD una vez, Vigía $900 USD/mes, Vigía Plus $1,800 USD/mes, Empresa desde $3,500 USD/mes. Mismo precio en México y EE. UU. Mínimo 3 meses, anual −10 %.",
     kick="Planes y precios · USD", h1="Planes y precios de la <em>vigilancia</em>",
     sub="Precios públicos, en dólares, iguales en México y Estados Unidos. El Arranque se paga una vez; la vigilancia se paga cada mes. Contrato mínimo 3 meses; con pago anual, 10 % de descuento.",
     geo=("MX-COA", "Torreón, Coahuila, México", "25.5428, -103.4068"),
     body=[
        ("Qué incluye cada plan", [
            "<table class=\"tbl cmp\"><tr><th>Plan</th><th>Precio</th><th>Para quién</th><th>Incluye</th></tr>"
            "<tr><td>Arranque</td><td>$2,000 USD una sola vez</td><td>Toda empresa que empieza; también se vende solo</td><td>Inventario de todo lo expuesto a internet (dominios, IPs, puertos, servicios, certificados, correo), revisión inicial del repositorio y de los servidores, instalación de la vigilancia y del feed de amenazas, reporte con lista de corrección por prioridad y sesión de 1 hora.</td></tr>"
            "<tr><td>Vigía</td><td>$900 USD al mes</td><td>Pyme con 1 servidor VPS, 1 organización de GitHub y un sitio web</td><td>Escaneo semanal de lo expuesto, aviso en menos de 24 h ante una vulnerabilidad crítica, revisión con IA de cada cambio al repositorio, vigilancia de amenazas (CVE, credenciales filtradas, dominios parecidos), reporte mensual y llamada de 30 minutos.</td></tr>"
            "<tr><td>Vigía Plus</td><td>$1,800 USD al mes</td><td>Empresa con equipo de TI, varias apps o hasta 5 servidores</td><td>Todo lo de Vigía para varias aplicaciones y repositorios con lectura de código real, configuración de nube (AWS, Azure, GCP, Vercel, DigitalOcean) y de identidad (Microsoft 365, Google Workspace), plan de respuesta a incidentes escrito y simulacro anual, reporte de Dirección y técnico, 2 llamadas al mes.</td></tr>"
            "<tr><td>Empresa</td><td>desde $3,500 USD al mes</td><td>Más de 5 servidores, varias razones sociales o requisitos de un cliente corporativo</td><td>Alcance a la medida sobre la base de Vigía Plus. Se cotiza después del diagnóstico.</td></tr></table>",
            "Los montos en pesos se calculan al tipo de cambio del día; en octubre de 2026 publicamos la referencia a 18.76 (Vigía MXN 16,885; Vigía Plus MXN 33,770; Arranque MXN 37,520).",
        ]),
        ("Extras que siempre se cobran aparte", [
            "<table class=\"tbl cmp\"><tr><th>Servicio</th><th>Precio</th><th>Cómo se entrega</th></tr>"
            "<tr><td>Pentest manual de una app (web, API o móvil)</td><td>$1,500–$2,500 USD por día de tester</td><td>Con un socio; una app típica toma de 3 a 8 días. Definimos el alcance y leemos el reporte contigo. Retest incluido una vez.</td></tr>"
            "<tr><td>Evaluación puntual con IA de una app</td><td>$1,500 USD</td><td>Un solo alcance, sin mensualidad, reporte en 5 días hábiles.</td></tr>"
            "<tr><td>Respuesta a incidente</td><td>$2,500 USD por día, mínimo 1 día</td><td>Contención, análisis de qué pasó, recuperación y reporte. Clientes con plan tienen prioridad.</td></tr>"
            "<tr><td>Simulación de phishing + capacitación</td><td>$4 USD por usuario al mes, mínimo 20</td><td>Campañas mensuales, video corto por tema y reporte de quién cayó.</td></tr>"
            "<tr><td>Antivirus gestionado / EDR</td><td>$12 USD por equipo al mes</td><td>Reventa con nuestra vigilancia encima; solo si lo pides.</td></tr>"
            "<tr><td>Capacitación de ciberseguridad con IA (6 h, hasta 15 personas)</td><td>$2,000 USD + viáticos</td><td>Taller práctico, en tu empresa o en línea.</td></tr></table>",
        ]),
        ("Cómo es el onboarding", [
            "<strong>1. Diagnóstico de 15 minutos</strong>, sin costo: qué tienes (sitio, apps, servidores, nube, correo) y quién lo cuida hoy. <strong>2. Contrato, NDA y checklist de accesos de solo lectura</strong>: repositorio, servidor, nube y DNS. <strong>3. Arranque</strong>: inventario, revisión inicial, instalación de la vigilancia y reporte con prioridades en una sesión de 1 hora. <strong>4. Vigilancia mensual</strong>: los agentes corren todos los días; cada mes recibes el reporte de Dirección, el técnico y la llamada.",
        ]),
     ],
     faq=[
        ("¿Por qué los precios están en dólares?", "Porque atendemos México y Estados Unidos con el mismo equipo, las mismas herramientas y el mismo servicio, y no queremos un precio \"más barato en pesos\". Publicamos el equivalente en pesos como referencia y puedes pagar en pesos al tipo de cambio del día."),
        ("¿Qué pasa si hay un incidente?", "Si eres cliente con plan, nos avisas y tienes prioridad. La respuesta a incidente se cobra aparte: $2,500 USD por día, mínimo 1 día, e incluye contención, análisis de qué pasó, recuperación y reporte. En Vigía Plus el plan de respuesta ya está escrito y ensayado con un simulacro anual."),
        ("¿Necesitan acceso de escritura a mis sistemas?", "No. Solo lectura: usuario de solo lectura en GitHub o GitLab, llave SSH de lectura, acceso de lectura a la nube y al DNS. Todo queda escrito en el contrato, autorizas cada escaneo y nunca hacemos cambios en tus sistemas."),
        ("¿Por qué el contrato mínimo es de 3 meses?", "Porque el primer mes se va en el Arranque y en corregir lo urgente; la vigilancia muestra su valor cuando hay historial para comparar y el reporte enseña tendencia. Tres meses es lo mínimo para eso; después es mes a mes."),
        ("¿Hay descuento?", "Sí: 10 % de descuento con pago anual por adelantado, en cualquier plan."),
        ("¿El Arranque se puede comprar solo?", "Sí. Si solo quieres saber cómo estás, el Arranque de $2,000 USD se vende sin mensualidad e incluye inventario, revisión inicial y reporte con prioridades."),
        ("¿Es lo mismo que un pentest?", "No. El pentest es una prueba puntual de una aplicación hecha por un especialista; la vigilancia corre todos los días y la lee una persona cada mes. El pentest lo cotizamos aparte con un socio, por día."),
     ])

# ===== ES: Vigilancia vs pentest
page(path="/vigilancia-vs-pentest/", L=ES, kind="compare", pair="/en/monitoring-vs-pentest/",
     title="Vigilancia de seguridad vs pentest: diferencias y cuándo conviene cada una · Inspector Hacker",
     desc="Qué es un pentest, qué es la vigilancia continua de seguridad con IA, qué encuentra cada una, cuánto cuesta y cuándo conviene cada una o las dos. Explicado para dueños de pymes.",
     kick="Guía · Vigilancia vs pentest", h1="Vigilancia continua <em>vs</em> pentest: cuál necesita tu empresa",
     sub="No son competencia: son dos herramientas distintas para dos preguntas distintas. Aquí explicamos qué hace cada una, qué cuesta y cuándo conviene una, la otra o las dos.",
     geo=("MX-COA", "Torreón, Coahuila, México", "25.5428, -103.4068"),
     body=[
        ("Qué es un pentest", [
            "Un pentest (prueba de penetración) es un ejercicio puntual en el que un especialista certificado intenta vulnerar una aplicación, una red o un sistema concreto, con permiso y dentro de un alcance definido, y entrega un reporte de lo que logró y cómo. Es profundo, es manual y es una foto: describe cómo estaba ese sistema en esos días. Un pentest manual de una sola aplicación suele costar entre $3,000 y $18,000 USD, según el tamaño del alcance, y lo normal es repetirlo una vez al año o después de un cambio grande.",
            "Lo pide un cliente corporativo, un regulador o un auditor; lo necesita una aplicación que maneja dinero o datos sensibles antes de salir a producción; y lo hace bien alguien con experiencia ofensiva. Nosotros no lo hacemos con IA ni vendemos \"atacantes autónomos\": lo cotizamos aparte con un socio, por día de tester.",
        ]),
        ("Qué es la vigilancia continua", [
            "La vigilancia responde otra pregunta: no \"¿qué tan difícil es entrar a esta app hoy?\" sino \"¿qué tiene mi empresa expuesto en este momento, qué cambió desde la semana pasada y qué amenaza nueva salió para lo que uso?\". Agentes de IA revisan cada semana el inventario de lo expuesto a internet, leen cada cambio que entra al código, siguen las vulnerabilidades publicadas y las credenciales filtradas, y avisan en menos de 24 horas cuando aparece algo crítico. Una persona lee el resultado y lo explica cada mes.",
            "Es ancha, es continua y es una película, no una foto. No encuentra lo que encuentra un buen pentester en una lógica de negocio compleja, pero sí encuentra el puerto que alguien abrió el martes, la llave que quedó en el repositorio y la vulnerabilidad crítica que salió ayer para tu versión de WordPress, de Nginx o de tu librería de Node.",
        ]),
        ("Comparación directa", [
            "<table class=\"tbl cmp\"><tr><th></th><th>Pentest</th><th>Vigilancia continua</th></tr>"
            "<tr><td>Frecuencia</td><td>Una vez; se repite cada año o tras un cambio grande</td><td>Todos los días; reporte cada mes</td></tr>"
            "<tr><td>Alcance</td><td>Una aplicación o sistema definido, a profundidad</td><td>Todo lo expuesto a internet, código, servidores, nube y amenazas nuevas</td></tr>"
            "<tr><td>Quién lo hace</td><td>Un especialista certificado, de forma manual</td><td>Agentes de IA; una persona lee y explica el reporte</td></tr>"
            "<tr><td>Qué encuentra mejor</td><td>Fallas de lógica, cadenas de explotación, lo que requiere creatividad humana</td><td>Cambios, exposiciones nuevas, secretos en código, vulnerabilidades publicadas, credenciales filtradas</td></tr>"
            "<tr><td>Riesgo para producción</td><td>Controlado, pero hay pruebas activas contra el sistema</td><td>Ninguno: solo lectura, sin ataques</td></tr>"
            "<tr><td>Costo típico</td><td>$3,000–$18,000 USD por aplicación; con nuestro socio $1,500–$2,500 USD por día de tester</td><td>Vigía $900 USD al mes; Vigía Plus $1,800 USD al mes; Arranque $2,000 USD una vez</td></tr>"
            "<tr><td>Entregable</td><td>Reporte técnico detallado con pruebas de concepto</td><td>Hoja de Dirección + reporte técnico + llamada mensual; aviso en menos de 24 h ante algo crítico</td></tr></table>",
        ]),
        ("Cuándo conviene cada una", [
            "<strong>Conviene un pentest</strong> cuando vas a lanzar o rediseñar una aplicación que maneja dinero o datos sensibles, cuando un cliente, un regulador o un auditor te lo exige por escrito, o cuando ya tienes vigilancia y quieres una prueba profunda de un sistema específico.",
            "<strong>Conviene la vigilancia</strong> cuando no tienes equipo de seguridad y nadie revisa lo que tienes expuesto; cuando tu infraestructura cambia seguido (despliegues, servidores nuevos, proveedores); cuando lo que te preocupa es el ransomware, el fraude por correo y las credenciales filtradas más que una falla sofisticada; y cuando quieres un documento mensual que demuestre que alguien está mirando.",
            "<strong>Convienen las dos</strong> en la empresa que ya depende de software propio: la vigilancia todos los días y un pentest al año sobre la aplicación más crítica. Como la vigilancia ya deja limpio lo obvio, el pentester usa sus días en lo que de verdad requiere a un humano, y el retest es más corto.",
            "Lo que no conviene es confundirlas: una evaluación automática que nadie lee no es un pentest, y un pentest de hace diez meses no te dice qué tienes expuesto hoy.",
        ]),
     ],
     faq=[
        ("¿La vigilancia sustituye al pentest?", "No. Son complementarias: la vigilancia cubre lo de todos los días y lo ancho; el pentest cubre lo profundo de un sistema en una fecha. Si un cliente o regulador te exige pentest, necesitas pentest."),
        ("¿Inspector Hacker hace pentest?", "No directamente. Lo cotizamos con un socio por día de tester ($1,500–$2,500 USD; una app típica toma de 3 a 8 días), definimos el alcance y leemos el reporte contigo. Nuestro servicio es la vigilancia."),
        ("¿Una evaluación automática con IA es un pentest?", "No. Es un escaneo. Sirve para encontrar lo conocido, no para demostrar lo que un atacante creativo lograría. Ofrecemos una evaluación puntual con IA de una app por $1,500 USD, y la llamamos evaluación, no pentest."),
        ("¿Cada cuánto debería hacer un pentest una pyme?", "Si tienes una aplicación crítica, una vez al año o después de un cambio grande. Si no desarrollas software, probablemente te sirve más la vigilancia que un pentest anual."),
        ("¿La vigilancia puede tirar mis sistemas?", "No. Los accesos son de solo lectura, los escaneos son de lo expuesto a internet y nunca lanzamos ataques contra producción."),
        ("¿Qué cuesta cada una?", "Pentest manual de una app: $3,000–$18,000 USD en el mercado; con nuestro socio, por día de tester. Vigilancia: Arranque $2,000 USD una vez, Vigía $900 USD al mes, Vigía Plus $1,800 USD al mes."),
     ])

# ===== EN: Bentonville
page(path="/en/cybersecurity-bentonville-ar/", L=EN, kind="local",
     title="Cybersecurity for Small Business in Bentonville, AR · Inspector Hacker",
     desc="AI-powered security monitoring for small and mid-size businesses in Bentonville, Arkansas: what you have exposed to the internet, your code and servers reviewed every day, with a monthly report. From $900/month.",
     kick="AI Cybersecurity · Bentonville, Arkansas", h1="Cybersecurity for businesses in <em>Bentonville, AR</em>",
     sub="Suppliers, agencies, startups and professional firms in Bentonville live inside one of the most demanding vendor ecosystems in the country. We watch what you have exposed every day and hand you the monthly report your customers ask about.",
     geo=("US-AR", "Bentonville, Arkansas, USA", "36.3729, -94.2088"), city="Bentonville", region="Arkansas", country="US",
     service_name="AI cybersecurity monitoring in Bentonville, Arkansas",
     body=[
        ("Why Bentonville businesses get asked about security before they get asked about price", [
            "Bentonville is a supplier town. Hundreds of vendors, brokers, marketing agencies, data and analytics shops, logistics providers and consultants serve the large retail and consumer-goods companies headquartered here. The large companies have security teams; most of the businesses around them have an IT provider, a handful of SaaS logins and a lot of trust in their inbox.",
            "The patterns we see in companies of that size: <strong>company email without SPF, DKIM and DMARC</strong>, which lets anyone send invoices or purchase-order changes in your name; <strong>shared logins to customer portals and EDI tools</strong> that never get rotated when someone leaves; <strong>cloud environments spun up fast</strong> for a pilot and never reviewed; and <strong>credentials already leaked</strong> in breaches of other services and reused on the company's own systems. None of it needs a sophisticated attacker. It needs nobody to be watching.",
        ]),
        ("How the monitoring works", [
            "We start with an inventory of everything your business has exposed to the internet: domains, IPs, ports, services, certificates, email configuration and cloud services. Then AI agents re-check that inventory every week, review every change that lands in your code repository, and track new threats against the technology you use: published vulnerabilities, leaked credentials and look-alike domains registered for phishing. When something critical affects your stack, you hear from us within 24 hours, with what to do.",
            "Every month you get two pages: a plain-English page for the owner or leadership team and a technical page for your IT provider or in-house team. Plus a 30-minute call with a person who actually read the report. If a customer sends a vendor security questionnaire, that report is the evidence that somebody is watching and that issues get fixed.",
            "All access is read-only, the scope is written into the contract and NDA, and you authorize every scan. We never run attacks against your production systems.",
        ]),
        ("Plans for a Bentonville business", [
            "A firm with one server, one code repository and a website fits <strong>Vigía</strong> at $900 USD a month. A business with several apps, cloud accounts and Microsoft 365 or Google Workspace usually needs <strong>Vigía Plus</strong> at $1,800 USD a month, which adds a written incident response plan and an annual drill. Everything starts with <strong>Onboarding</strong>, $2,000 USD one time, which is also sold on its own if you only want to know where you stand. Same prices in the US and Mexico; monthly call in English or Spanish.",
        ]),
     ],
     faq=[
        ("Do you work with suppliers that have to answer vendor security questionnaires?", "Yes. The onboarding inventory, the prioritized fix list and the monthly report answer a good part of those questionnaires and show that someone monitors your security. We do not issue certifications; if a customer requires one, we tell you what is missing."),
        ("Are you located in Bentonville?", "Inspector Hacker operates in the United States with Bentonville, Arkansas and San Antonio, Texas as its base, and in Mexico from Torreón. Monitoring is remote; the monthly call is a video call, in English or Spanish."),
        ("We already have an IT provider. Do we need to replace them?", "No. We monitor and report; they fix. The technical report each month is written for them, with a prioritized list of what to correct."),
        ("What access do you need?", "Read-only: a read-only user on GitHub or GitLab, a read-only SSH key, read access to your cloud and DNS. No write access and no changes without your approval."),
        ("How fast can we start?", "The assessment takes 15 minutes. After the contract and read-only access, onboarding ends with a report and a 1-hour session. From there, the agents run every day."),
        ("Is there a minimum contract?", "Yes, 3 months, then month to month. Annual prepayment gets 10% off."),
     ])

# ===== EN: Northwest Arkansas
page(path="/en/cybersecurity-northwest-arkansas/", L=EN, kind="local",
     title="Cybersecurity for Businesses in Northwest Arkansas (Rogers, Springdale, Fayetteville) · Inspector Hacker",
     desc="AI security monitoring for small and mid-size businesses across Northwest Arkansas: trucking, food, construction, professional services and startups. Daily monitoring, monthly report. From $900/month.",
     kick="AI Cybersecurity · Northwest Arkansas", h1="Cybersecurity for businesses in <em>Northwest Arkansas</em>",
     sub="Rogers, Springdale, Fayetteville, Bentonville and the towns in between. Trucking, food processing, construction, healthcare practices, agencies and startups: we watch what you have exposed every day and explain it once a month.",
     geo=("US-AR", "Springdale, Arkansas, USA", "36.1867, -94.1288"), city="Springdale", region="Arkansas", country="US",
     service_name="AI cybersecurity monitoring in Northwest Arkansas",
     extra_cities=["Rogers", "Fayetteville", "Bentonville", "Siloam Springs"],
     body=[
        ("A fast-growing region with small IT teams", [
            "Northwest Arkansas grew faster than its IT departments. Trucking and logistics companies run dispatch, ELD and billing systems from the cloud; food processors and their suppliers connect plants, labs and offices; construction firms share drawings and payments through email; clinics and dental practices run patient systems that someone else hosts; and a growing crowd of startups ships code every week. In most of these businesses, security is one line item on the IT provider's invoice.",
            "What that looks like from the internet: <strong>remote desktop and VPN endpoints left open</strong> so a vendor can log in; <strong>invoices and wire instructions sent from email domains that anyone can spoof</strong>; <strong>former employees' accounts still active</strong> in Microsoft 365 or Google Workspace; and <strong>code repositories with API keys committed by accident</strong>. These are the openings that turn into ransomware, wire fraud and stolen customer lists, and they are visible to anyone who looks.",
        ]),
        ("What continuous monitoring does for a Northwest Arkansas company", [
            "Onboarding produces an inventory of everything exposed (domains, IPs, ports, services, certificates, email) and a first review of your repository, servers and cloud, with a prioritized fix list. After that, AI agents repeat the external scan weekly, review every change that lands in your code for secrets, vulnerable dependencies and risky configuration, and follow new threats to your specific stack. A critical vulnerability in something you run gets an alert within 24 hours.",
            "Each month: a one-page report for the owner or leadership, a technical report for your IT team or provider, and a 30-minute call. For trucking and food companies with several systems, cloud and identity, <strong>Vigía Plus</strong> ($1,800 USD a month) covers up to 5 servers and adds a written incident response plan with an annual drill. A smaller firm or a startup with one server and one repository fits <strong>Vigía</strong> ($900 USD a month).",
        ]),
        ("Monitoring, not pentesting", [
            "We do not sell penetration tests or autonomous attackers against production. If a customer or insurer requires a formal pentest of an application, we quote it with a partner per tester-day ($1,500 to $2,500 USD) and read the report with you. Our service is the everyday part: read-only access, written scope, no attacks. <a href=\"/en/monitoring-vs-pentest/\">Here is the difference explained</a>.",
            "Phishing simulation for your staff ($4 USD per user per month, minimum 20 users) and a 6-hour security training for up to 15 people ($2,000 USD plus travel) are available as extras.",
        ]),
     ],
     faq=[
        ("Which cities in Northwest Arkansas do you serve?", "Bentonville, Rogers, Springdale, Fayetteville, Siloam Springs, Bella Vista, Lowell and the rest of Benton and Washington counties. Monitoring is remote, so location does not change the service or the price."),
        ("We run a trucking company. Is this for us?", "Yes. Dispatch, ELD and billing systems in the cloud, plus email used for load confirmations and payments, are exactly what gets attacked. The inventory shows what is exposed and the monitoring alerts you when something changes."),
        ("Can your scans interrupt our operations?", "No. We scan what is exposed to the internet with read-only access, you authorize every scan, and we never attack production systems."),
        ("Does it help with cyber-insurance applications?", "The inventory, fix list and monthly reports document that you monitor your exposure and correct issues, which is what most applications ask about. We do not provide insurance or legal advice."),
        ("Do you train employees against phishing?", "As an extra: monthly phishing simulation campaigns with a short video per topic and a report of who clicked, $4 USD per user per month with a 20-user minimum."),
        ("How much does it cost?", "Onboarding $2,000 USD one time; Vigía $900 USD a month; Vigía Plus $1,800 USD a month; Enterprise from $3,500 USD a month. 3-month minimum, 10% off with annual prepayment."),
     ])

# ===== EN: San Antonio
page(path="/en/cybersecurity-san-antonio-tx/", L=EN, kind="local",
     title="Cybersecurity for Small Business in San Antonio, TX · Inspector Hacker",
     desc="AI-powered security monitoring for small and mid-size businesses in San Antonio, Texas: construction, healthcare practices, cross-border trade and professional services. Bilingual monthly report. From $900/month.",
     kick="AI Cybersecurity · San Antonio, Texas", h1="Cybersecurity for businesses in <em>San Antonio, TX</em>",
     sub="San Antonio has more cybersecurity talent than almost any city its size, and most of it works for the military, the big contractors and the banks. We bring daily AI monitoring to the businesses that do not have a security team: bilingual, read-only, with a monthly report.",
     geo=("US-TX", "San Antonio, Texas, USA", "29.4241, -98.4936"), city="San Antonio", region="Texas", country="US",
     service_name="AI cybersecurity monitoring in San Antonio, Texas",
     extra_cities=["New Braunfels", "Schertz", "Boerne"],
     body=[
        ("Security talent is everywhere in San Antonio, except in small businesses", [
            "San Antonio is known for cybersecurity because of its military and federal presence and the contractors around them. That talent is expensive and mostly spoken for. The city's construction companies, medical and dental practices, law and accounting firms, distributors and the thousands of businesses trading with Mexico run on an IT provider, cloud software and email, and the owner is the one who notices when something goes wrong.",
            "The problems we see most often in companies of that size: <strong>payment and wire instructions sent over email domains without SPF, DKIM and DMARC</strong>, which is how invoice fraud starts; <strong>patient, client or project systems reachable from the internet</strong> through remote desktop or a vendor's portal; <strong>bilingual teams sharing credentials across the border</strong> with suppliers and customs brokers; and <strong>cloud accounts and Microsoft 365 tenants</strong> that nobody has reviewed since they were set up.",
        ]),
        ("What you get every month", [
            "We start with an inventory of what your business exposes to the internet and a first review of your servers, code and cloud, with a prioritized fix list. Then AI agents re-scan weekly, review every change to your code, and track new vulnerabilities, leaked credentials and look-alike domains for your stack. A critical issue gets an alert within 24 hours.",
            "Each month you receive a one-page report for leadership and a technical report for your IT team or provider, and a 30-minute call with a person who read both. Because we operate in both countries, the reports and the call can be in <strong>English, Spanish or both</strong>, which matters when your office is in San Antonio and your supplier, plant or partner is in Monterrey or Torreón.",
            "Access is read-only, the scope is written into the contract and NDA, and we never run attacks against production. If a customer, insurer or regulator requires a formal penetration test, we quote it with a partner per tester-day and read the report with you.",
        ]),
        ("Which plan fits", [
            "<strong>Vigía</strong> ($900 USD a month) covers one server, one GitHub organization and your website: a practice, a firm or a distributor with one main system. <strong>Vigía Plus</strong> ($1,800 USD a month) covers up to 5 servers, several apps, cloud and identity, and includes a written incident response plan with an annual drill: a contractor or distributor with several systems and offices. <strong>Enterprise</strong>, from $3,500 USD a month, is for more than 5 servers or several legal entities. Everything begins with <strong>Onboarding</strong>, $2,000 USD one time. Same prices on both sides of the border.",
        ]),
     ],
     faq=[
        ("Do you serve businesses in the San Antonio area outside the city?", "Yes: New Braunfels, Schertz, Boerne, Seguin and the rest of the metro area. Monitoring is remote, so the service and the price are the same."),
        ("We trade with Mexico. Can you cover both sides?", "Yes. We operate in the United States and Mexico with the same team and the same price in USD, and the reports and calls can be in English, Spanish or both."),
        ("We are a medical or dental practice. Does this replace a compliance audit?", "No. We monitor what you have exposed, your systems and your cloud, and document it monthly; that supports your compliance work but does not replace a formal assessment or legal advice."),
        ("Is this a penetration test?", "No. A pentest is a one-time, in-depth test of one application by a certified specialist; we quote it separately with a partner. Our service is continuous monitoring with a human-read monthly report."),
        ("What happens if we get hacked?", "Clients with a plan get priority. Incident response is billed separately at $2,500 USD per day, minimum one day: containment, analysis of what happened, recovery and a report. Vigía Plus clients already have a written response plan."),
        ("How do we start?", "A free 15-minute assessment over a video call, then contract, NDA and a read-only access checklist. Onboarding ends with a report and a 1-hour session, and the daily monitoring starts."),
     ])

# ===== EN: Small business
page(path="/en/cybersecurity-for-small-business/", L=EN, kind="local", pair="/ciberseguridad-pymes-mexico/",
     title="Cybersecurity for Small Business: AI Monitoring from $900/month · Inspector Hacker",
     desc="Cybersecurity for small and mid-size businesses without a security team: AI agents watch what you have exposed to the internet, your code and servers every day, and a human explains the report every month.",
     kick="AI Cybersecurity · Small and mid-size business", h1="Cybersecurity for <em>small business</em>, without hiring a security team",
     sub="For the company that has an IT provider, a few cloud tools and an owner who does not want to be the one who finds out. Continuous AI monitoring, alerts within 24 hours and a monthly call in plain English.",
     geo=("US-AR", "Bentonville, Arkansas, USA", "36.3729, -94.2088"), city=None, region=None, country="US",
     service_name="AI cybersecurity monitoring for small business",
     body=[
        ("Why small businesses get hit when they \"have nothing worth stealing\"", [
            "A small business has plenty worth stealing: the bank account, payroll, the customer list, invoices and, above all, the trust of its larger customers. Modern attacks are not aimed by hand. They sweep the internet for email domains without authentication, servers with open ports, admin panels with default passwords and credentials already leaked from other breaches. Small businesses get hit because they are the least watched, not because they are the most interesting.",
            "The three hits we see most often in companies of 10 to 200 people: <strong>invoice and wire fraud</strong>, where an email that looks like your vendor or your CEO asks to pay to a new account; <strong>ransomware</strong> that encrypts the billing server and the backups stored next to it; and the <strong>hijacked mailbox</strong> that sends phishing to every customer in your name.",
        ]),
        ("What AI monitoring is, and how it differs from antivirus and from a pentest", [
            "Antivirus protects each computer from the inside. A penetration test is a one-time, in-depth exercise a specialist runs on one application, usually once a year. Monitoring is the layer in between and the everyday part: AI agents re-check what your company exposes to the internet every week, review every change to your code, follow new threats against the exact technology you use, and alert you within 24 hours when something critical appears. A person reads the results and explains them to you once a month. <a href=\"/en/monitoring-vs-pentest/\">Here is a side-by-side comparison</a>.",
            "It starts with <strong>Onboarding</strong>, $2,000 USD one time: an inventory, a first review and a prioritized fix list. Then <strong>Vigía</strong>, $900 USD a month, covers one VPS server, one GitHub organization and your website, with a monthly report and a 30-minute call. <strong>Vigía Plus</strong>, $1,800 USD a month, covers several apps, cloud and identity, and includes a written incident response plan. Prices are the same in the United States and Mexico.",
        ]),
        ("What we need from you", [
            "Very little: 15 minutes for the assessment, a signed contract and NDA, and read-only access to your repository, server, cloud and DNS. You do not need to hire anyone or change your IT provider; the monthly technical report tells your provider exactly what to fix. We serve the United States from Bentonville, Arkansas and San Antonio, Texas, with pages for <a href=\"/en/cybersecurity-bentonville-ar/\">Bentonville</a>, <a href=\"/en/cybersecurity-northwest-arkansas/\">Northwest Arkansas</a> and <a href=\"/en/cybersecurity-san-antonio-tx/\">San Antonio</a>, and Mexico from Torreón.",
        ]),
     ],
     faq=[
        ("What size of business is Inspector Hacker for?", "Companies of 10 to 200 people without their own security team. One server, one system and a website fits Vigía; several systems, cloud and corporate identity fits Vigía Plus; more than 5 servers or several legal entities is the Enterprise plan."),
        ("Is this an antivirus?", "No. Antivirus protects each computer from the inside; monitoring reviews what your company exposes to the internet, your code and servers, and alerts you to new threats. Managed antivirus/EDR is available as an extra at $12 USD per device per month."),
        ("How much does small business cybersecurity cost with Inspector Hacker?", "Onboarding $2,000 USD one time; Vigía $900 USD a month; Vigía Plus $1,800 USD a month; Enterprise from $3,500 USD a month. 3-month minimum, 10% off with annual prepayment."),
        ("Do we need developers or a code repository?", "No. Without custom software, monitoring focuses on what is exposed to the internet, email, servers and cloud. With it, every code change is reviewed as well."),
        ("What if we have already been hacked?", "Incident response is a separate service: $2,500 USD per day, minimum one day, covering containment, analysis of what happened, recovery and a report. Clients with a plan get priority."),
        ("Do you need write access to our systems?", "No. Read-only access only, written into the contract, and you authorize every scan."),
     ])

# ===== EN: Pricing
page(path="/en/pricing/", L=EN, kind="pricing", pair="/planes/",
     title="Pricing · AI Cybersecurity Monitoring Plans · Inspector Hacker",
     desc="Inspector Hacker pricing: Onboarding $2,000 USD one time, Vigía $900/month, Vigía Plus $1,800/month, Enterprise from $3,500/month. Same price in the US and Mexico. 3-month minimum, 10% off annual.",
     kick="Plans and pricing · USD", h1="Plans and pricing for <em>continuous monitoring</em>",
     sub="Public prices in US dollars, the same in the United States and Mexico. Onboarding is paid once; monitoring is paid monthly. 3-month minimum; 10% off with annual prepayment.",
     geo=("US-AR", "Bentonville, Arkansas, USA", "36.3729, -94.2088"),
     body=[
        ("What each plan includes", [
            "<table class=\"tbl cmp\"><tr><th>Plan</th><th>Price</th><th>Who it is for</th><th>Includes</th></tr>"
            "<tr><td>Onboarding</td><td>$2,000 USD one time</td><td>Every new client; also sold on its own</td><td>Inventory of everything exposed to the internet (domains, IPs, ports, services, certificates, email), initial review of the repository and servers, setup of the monitoring and the threat feed, prioritized fix list and a 1-hour session.</td></tr>"
            "<tr><td>Vigía</td><td>$900 USD a month</td><td>Small business with 1 VPS server, 1 GitHub organization and a website</td><td>Weekly scan of what is exposed, alert within 24 h on a critical vulnerability, AI review of every change to the repository, threat monitoring (CVEs, leaked credentials, look-alike domains), monthly report and a 30-minute call.</td></tr>"
            "<tr><td>Vigía Plus</td><td>$1,800 USD a month</td><td>Company with an IT team, several apps or up to 5 servers</td><td>Everything in Vigía across several applications and repositories with real code reading, cloud configuration (AWS, Azure, GCP, Vercel, DigitalOcean) and identity (Microsoft 365, Google Workspace), written incident response plan and annual drill, management and technical reports, 2 calls a month.</td></tr>"
            "<tr><td>Enterprise</td><td>from $3,500 USD a month</td><td>More than 5 servers, several legal entities or corporate-customer requirements</td><td>Custom scope built on Vigía Plus. Quoted after the assessment.</td></tr></table>",
            "Prices are identical in the United States and Mexico. Mexican clients can pay in pesos at the exchange rate of the day (reference published in October 2026: 18.76 MXN per USD).",
        ]),
        ("Extras, always billed separately", [
            "<table class=\"tbl cmp\"><tr><th>Service</th><th>Price</th><th>How it is delivered</th></tr>"
            "<tr><td>Manual pentest of one app (web, API or mobile)</td><td>$1,500–$2,500 USD per tester-day</td><td>With a partner; a typical app takes 3 to 8 days. We define the scope and read the report with you. One retest included.</td></tr>"
            "<tr><td>One-time AI assessment of one app</td><td>$1,500 USD</td><td>Single scope, no monthly fee, report in 5 business days.</td></tr>"
            "<tr><td>Incident response</td><td>$2,500 USD per day, minimum 1 day</td><td>Containment, analysis of what happened, recovery and report. Clients with a plan get priority.</td></tr>"
            "<tr><td>Phishing simulation + staff training</td><td>$4 USD per user per month, minimum 20</td><td>Monthly campaigns, a short video per topic and a report of who clicked.</td></tr>"
            "<tr><td>Managed antivirus / EDR</td><td>$12 USD per device per month</td><td>Resold with our monitoring on top; only if you ask.</td></tr>"
            "<tr><td>AI cybersecurity training (6 h, up to 15 people)</td><td>$2,000 USD + travel</td><td>Hands-on workshop, on site or online.</td></tr></table>",
        ]),
        ("How onboarding works", [
            "<strong>1. Free 15-minute assessment</strong>: what you have (website, apps, servers, cloud, email) and who looks after it today. <strong>2. Contract, NDA and read-only access checklist</strong>: repository, server, cloud and DNS. <strong>3. Onboarding</strong>: inventory, initial review, monitoring setup and a prioritized report in a 1-hour session. <strong>4. Monthly monitoring</strong>: the agents run every day; every month you get the management report, the technical report and the call.",
        ]),
     ],
     faq=[
        ("Why are prices in US dollars for both countries?", "Because we serve the United States and Mexico with the same team, the same tools and the same service, and we do not want a \"cheaper in pesos\" version. Mexican clients can pay in pesos at the exchange rate of the day."),
        ("What happens if there is an incident?", "If you are a client with a plan, you call us and you get priority. Incident response is billed separately at $2,500 USD per day, minimum one day, and covers containment, analysis of what happened, recovery and a report. Vigía Plus clients already have a written response plan rehearsed in an annual drill."),
        ("Do you need write access to our systems?", "No. Read-only only: a read-only user on GitHub or GitLab, a read-only SSH key, read access to your cloud and DNS. It is all written into the contract, you authorize every scan, and we never make changes to your systems."),
        ("Why a 3-month minimum?", "The first month goes to onboarding and fixing what is urgent; monitoring shows its value once there is history to compare and the report shows a trend. Three months is the minimum for that; after that it is month to month."),
        ("Is there a discount?", "Yes: 10% off with annual prepayment, on any plan."),
        ("Can we buy Onboarding on its own?", "Yes. If you only want to know where you stand, Onboarding ($2,000 USD) is sold without a monthly plan and includes the inventory, the initial review and the prioritized report."),
        ("Is this the same as a pentest?", "No. A pentest is a one-time test of one application by a specialist; monitoring runs every day and is read by a person every month. We quote pentests separately with a partner, per tester-day."),
     ])

# ===== EN: Monitoring vs pentest
page(path="/en/monitoring-vs-pentest/", L=EN, kind="compare", pair="/vigilancia-vs-pentest/",
     title="Security Monitoring vs Penetration Testing: Differences and When to Use Each · Inspector Hacker",
     desc="What a pentest is, what continuous AI security monitoring is, what each one finds, what each costs and when a small business needs one, the other or both. Written for business owners.",
     kick="Guide · Monitoring vs pentest", h1="Continuous monitoring <em>vs</em> penetration testing: which one your business needs",
     sub="They are not competitors. They are two different tools for two different questions. Here is what each does, what it costs and when you need one, the other or both.",
     geo=("US-AR", "Bentonville, Arkansas, USA", "36.3729, -94.2088"),
     body=[
        ("What a penetration test is", [
            "A penetration test (pentest) is a one-time exercise in which a certified specialist tries to break into a specific application, network or system, with permission and within a defined scope, and delivers a report of what they achieved and how. It is deep, it is manual and it is a snapshot: it describes how that system stood on those days. A manual pentest of a single application typically costs between $3,000 and $18,000 USD depending on scope, and it is normally repeated once a year or after a major change.",
            "A corporate customer, a regulator or an auditor asks for it; an application that handles money or sensitive data needs it before launch; and it is done well by someone with offensive experience. We do not do it with AI and we do not sell \"autonomous attackers\": we quote it separately with a partner, per tester-day.",
        ]),
        ("What continuous monitoring is", [
            "Monitoring answers a different question. Not \"how hard is it to break into this app today?\" but \"what does my company have exposed right now, what changed since last week, and what new threat came out for the things I run?\". AI agents re-check the inventory of everything exposed to the internet every week, review every change that lands in the code, follow published vulnerabilities and leaked credentials, and alert within 24 hours when something critical appears. A person reads the results and explains them every month.",
            "It is wide, it is continuous and it is a film rather than a snapshot. It will not find what a good pentester finds in complex business logic, but it will find the port someone opened on Tuesday, the key left in the repository and the critical vulnerability published yesterday for your version of WordPress, Nginx or your Node library.",
        ]),
        ("Side by side", [
            "<table class=\"tbl cmp\"><tr><th></th><th>Penetration test</th><th>Continuous monitoring</th></tr>"
            "<tr><td>Frequency</td><td>Once; repeated yearly or after a major change</td><td>Every day; report every month</td></tr>"
            "<tr><td>Scope</td><td>One defined application or system, in depth</td><td>Everything exposed to the internet, code, servers, cloud and new threats</td></tr>"
            "<tr><td>Who does it</td><td>A certified specialist, manually</td><td>AI agents; a person reads and explains the report</td></tr>"
            "<tr><td>What it finds best</td><td>Logic flaws, exploit chains, anything that needs human creativity</td><td>Changes, new exposures, secrets in code, published vulnerabilities, leaked credentials</td></tr>"
            "<tr><td>Risk to production</td><td>Controlled, but there are active tests against the system</td><td>None: read-only, no attacks</td></tr>"
            "<tr><td>Typical cost</td><td>$3,000–$18,000 USD per application; with our partner $1,500–$2,500 USD per tester-day</td><td>Vigía $900 USD a month; Vigía Plus $1,800 USD a month; Onboarding $2,000 USD one time</td></tr>"
            "<tr><td>Deliverable</td><td>Detailed technical report with proofs of concept</td><td>Management page + technical report + monthly call; alert within 24 h on anything critical</td></tr></table>",
        ]),
        ("When each one makes sense", [
            "<strong>A pentest makes sense</strong> when you are launching or redesigning an application that handles money or sensitive data, when a customer, regulator or auditor requires it in writing, or when you already have monitoring and want a deep test of one specific system.",
            "<strong>Monitoring makes sense</strong> when you have no security team and nobody reviews what you expose; when your infrastructure changes often (deployments, new servers, new vendors); when what worries you is ransomware, invoice fraud and leaked credentials more than a sophisticated flaw; and when you want a monthly document that shows someone is watching.",
            "<strong>Both make sense</strong> for a company that already depends on its own software: monitoring every day and one pentest a year on the most critical application. Because monitoring already clears the obvious, the pentester spends their days on what truly needs a human, and the retest is shorter.",
            "What does not make sense is confusing them: an automated assessment nobody reads is not a pentest, and a pentest from ten months ago does not tell you what you have exposed today.",
        ]),
     ],
     faq=[
        ("Does monitoring replace a pentest?", "No. They complement each other: monitoring covers the everyday and the wide; a pentest covers the deep view of one system on one date. If a customer or regulator requires a pentest, you need a pentest."),
        ("Does Inspector Hacker do penetration testing?", "Not directly. We quote it with a partner per tester-day ($1,500–$2,500 USD; a typical app takes 3 to 8 days), define the scope and read the report with you. Our service is monitoring."),
        ("Is an automated AI assessment a pentest?", "No. It is a scan. It finds what is known, not what a creative attacker would achieve. We offer a one-time AI assessment of one app for $1,500 USD, and we call it an assessment, not a pentest."),
        ("How often should a small business get a pentest?", "If you run a critical application, once a year or after a major change. If you do not build software, continuous monitoring is probably more useful than an annual pentest."),
        ("Can monitoring take our systems down?", "No. Access is read-only, scans target what is exposed to the internet, and we never launch attacks against production."),
        ("What does each one cost?", "Manual pentest of one app: $3,000–$18,000 USD on the market; with our partner, per tester-day. Monitoring: Onboarding $2,000 USD one time, Vigía $900 USD a month, Vigía Plus $1,800 USD a month."),
     ])

# ---------------------------------------------------------------- render
def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"

def hreflang_links(p):
    es_url = en_url = None
    if p["L"] is ES:
        es_url = SITE + p["path"]; en_url = SITE + p["pair"] if p.get("pair") else None
    else:
        en_url = SITE + p["path"]; es_url = SITE + p["pair"] if p.get("pair") else None
    out = []
    if es_url: out.append(f'<link rel="alternate" hreflang="es-MX" href="{es_url}">')
    if en_url: out.append(f'<link rel="alternate" hreflang="en-US" href="{en_url}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{es_url or en_url}">')
    return "\n".join(out)

def render(p):
    L = p["L"]; url = SITE + p["path"]; is_es = L is ES
    lang_attr = L["lang"]
    other = L["other_lang"]
    pair_url = SITE + p["pair"] if p.get("pair") else (SITE + ("/en/" if is_es else "/"))
    cities = ES_CITIES if is_es else EN_CITIES
    related = ES_RELATED if is_es else EN_RELATED

    # ---- JSON-LD
    blocks = [ORG]
    crumbs_name = strip_tags(p["h1"])
    crumbs = [(L["home_name"], L["home"])] + p.get("crumbs", []) + [(crumbs_name, p["path"])]
    blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]})
    blocks.append({"@context": "https://schema.org", "@type": "WebPage", "@id": url, "url": url, "name": p["title"],
                   "description": p["desc"], "inLanguage": lang_attr, "isPartOf": {"@type": "WebSite", "url": SITE + "/", "name": "Inspector Hacker"},
                   "about": {"@id": SITE + "/#org"}, "datePublished": p.get("published", TODAY), "dateModified": p.get("modified", TODAY)})
    blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    offers = [
        {"@type": "Offer", "name": "Arranque" if is_es else "Onboarding", "price": "2000", "priceCurrency": "USD", "url": url,
         "priceSpecification": {"@type": "PriceSpecification", "price": "2000", "priceCurrency": "USD", "valueAddedTaxIncluded": False}},
        {"@type": "Offer", "name": "Vigía", "price": "900", "priceCurrency": "USD", "url": url,
         "priceSpecification": {"@type": "UnitPriceSpecification", "price": "900", "priceCurrency": "USD", "unitCode": "MON", "billingIncrement": 1, "valueAddedTaxIncluded": False}},
        {"@type": "Offer", "name": "Vigía Plus", "price": "1800", "priceCurrency": "USD", "url": url,
         "priceSpecification": {"@type": "UnitPriceSpecification", "price": "1800", "priceCurrency": "USD", "unitCode": "MON", "billingIncrement": 1, "valueAddedTaxIncluded": False}},
        {"@type": "Offer", "name": "Empresa" if is_es else "Enterprise", "priceCurrency": "USD", "url": url,
         "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": "3500", "priceCurrency": "USD", "unitCode": "MON", "valueAddedTaxIncluded": False}},
    ]
    if p["kind"] == "local":
        if p.get("city"):
            area = [{"@type": "City", "name": p["city"], "containedInPlace": {"@type": "State", "name": p["region"]}, "address": {"@type": "PostalAddress", "addressCountry": p["country"]}}]
            for c in p.get("extra_cities", []):
                area.append({"@type": "City", "name": c, "containedInPlace": {"@type": "State", "name": p["region"]}})
        else:
            area = [{"@type": "Country", "name": "México" if is_es else "United States"}]
        blocks.append({"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": p["service_name"],
                       "serviceType": p.get("service_type") or ("Vigilancia de ciberseguridad con IA" if is_es else "AI cybersecurity monitoring"),
                       "description": p["desc"], "provider": {"@id": SITE + "/#org"}, "areaServed": area, "availableLanguage": ["es", "en"],
                       "offers": offers, "url": url})
        blocks.append({"@context": "https://schema.org", "@type": "ProfessionalService", "@id": url + "#business", "name": "Inspector Hacker",
                       "parentOrganization": {"@id": SITE + "/#org"}, "url": url, "image": SITE + "/img/og.jpg", "logo": SITE + "/img/logo-negro-1024.png",
                       "telephone": "+52-871-263-8082", "priceRange": "$$$", "currenciesAccepted": "USD, MXN",
                       "address": {"@type": "PostalAddress", "addressLocality": "Torreón", "addressRegion": "Coahuila", "addressCountry": "MX"},
                       "areaServed": area, "knowsLanguage": ["es", "en"], "makesOffer": offers})
    elif p["kind"] == "pricing":
        blocks.append({"@context": "https://schema.org", "@type": "Service", "@id": url + "#service",
                       "name": "Vigilancia de ciberseguridad con IA" if is_es else "AI cybersecurity monitoring",
                       "provider": {"@id": SITE + "/#org"}, "areaServed": [{"@type": "Country", "name": "México"}, {"@type": "Country", "name": "United States"}],
                       "offers": offers + [
                           {"@type": "Offer", "name": "Pentest manual (por día de tester)" if is_es else "Manual pentest (per tester-day)", "priceCurrency": "USD", "priceSpecification": {"@type": "PriceSpecification", "minPrice": "1500", "maxPrice": "2500", "priceCurrency": "USD"}},
                           {"@type": "Offer", "name": "Evaluación puntual con IA" if is_es else "One-time AI assessment", "price": "1500", "priceCurrency": "USD"},
                           {"@type": "Offer", "name": "Respuesta a incidente (por día)" if is_es else "Incident response (per day)", "price": "2500", "priceCurrency": "USD"},
                           {"@type": "Offer", "name": "Phishing simulado + capacitación (por usuario al mes)" if is_es else "Phishing simulation + training (per user per month)", "price": "4", "priceCurrency": "USD"},
                           {"@type": "Offer", "name": "Capacitación 6 h" if is_es else "6-hour training", "price": "2000", "priceCurrency": "USD"}],
                       "url": url})
    elif p["kind"] == "hub":
        blocks.append({"@context": "https://schema.org", "@type": "ItemList", "name": strip_tags(p["h1"]), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + h, "name": n} for i, (h, n, _s) in enumerate(p.get("grid", []))]})
    else:
        blocks.append({"@context": "https://schema.org", "@type": p.get("article_type", "Article"), "headline": strip_tags(p["h1"]), "description": p["desc"], "inLanguage": lang_attr,
                       "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "datePublished": p.get("published", TODAY), "dateModified": p.get("modified", TODAY),
                       "mainEntityOfPage": url, "image": SITE + "/img/og.jpg"})

    # ---- nav
    anchor_cities = "#ciudades" if is_es else "#cities"
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in L["nav"])
    nav += f'<a href="{pair_url}" hreflang="{other[0]}" lang="{other[0]}" title="{other[2]}">{other[1]}</a>'
    nav += f'<a class="btn btn-cy" href="{L["wa"]}" target="_blank" rel="noopener">{L["cta_btn"]}</a>'

    body_html = ""
    for h2, paras in p["body"]:
        body_html += f"<h2>{h2}</h2>\n" if h2 else ""
        for para in paras:
            body_html += para + "\n" if para.startswith(("<table", "<ul", "<ol", "<div", "<h3", "<p")) else f"<p>{para}</p>\n"

    plans_html = ""
    for name, price, unit, line, items, feat in L["plans"]:
        lis = "".join(f"<li>{i}</li>" for i in items)
        plans_html += f'<div class="plan cmp{" feat" if feat else ""}"><h3>{name}</h3><div class="price">{price} <small>{unit}</small></div><div class="mxn">{line}</div><ul>{lis}</ul><a class="btn {"btn-cy" if feat else "btn-ghost"}" href="{L["wa"]}" target="_blank" rel="noopener">{L["cta_btn"]}</a></div>'

    faq_html = "".join(f"<details{' open' if i == 0 else ''}><summary>{q}</summary><p>{a}</p></details>" for i, (q, a) in enumerate(p["faq"]))

    CUR = ' aria-current="page"'
    if not p.get("grid"):
        # páginas de ciudad existentes: enlazan a sus páginas servicio × ciudad
        from seo_data import SERVICES, CITIES_MX, CITIES_US
        lang = "es" if is_es else "en"
        local = []
        for c in (CITIES_MX if is_es else CITIES_US):
            if c.get("existing") == p["path"]:
                for k in c["services"]:
                    S = SERVICES[k][lang]
                    base = f"/servicios/{S['slug']}/" if is_es else f"/en/services/{S['slug']}/"
                    local.append((base + c["slug"] + "/", S["name"], c["name"]))
        if local:
            p = dict(p, grid=local, grid_extra=cities + related, grid_h2=("Servicios en esta zona y otras ciudades" if is_es else "Services in this area and other cities"))
    cities_html = "".join(f'<a href="{h}"{CUR if h == p["path"] else ""}><b>{n}</b>{s}</a>' for h, n, s in (p.get("grid") or []) + (p.get("grid_extra") if p.get("grid") else cities + related))

    geo_meta = ""
    if p.get("geo"):
        geo_region, geo_place, icbm = p["geo"]
        geo_meta = f'<meta name="geo.region" content="{geo_region}"><meta name="geo.placename" content="{geo_place}"><meta name="ICBM" content="{icbm}"><meta name="geo.position" content="{icbm.replace(", ", ";")}">\n'
    html = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="author" content="Inspector Hacker · GH Specialist">
<meta name="theme-color" content="#07090c">
{geo_meta}{hreflang_links(p)}
<link rel="apple-touch-icon" href="/img/logo-negro-1024.png">
<link rel="icon" href="/img/logo-negro-1024.png" type="image/png">
<meta property="og:type" content="{p.get("og_type", "website")}"><meta property="og:site_name" content="Inspector Hacker"><meta property="og:url" content="{url}"><meta property="og:title" content="{esc(p["title"])}"><meta property="og:description" content="{esc(p["desc"])}"><meta property="og:image" content="{SITE}/img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="{L["og_locale"]}"><meta property="og:locale:alternate" content="{"en_US" if is_es else "es_MX"}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(p["title"])}"><meta name="twitter:description" content="{esc(p["desc"])}"><meta name="twitter:image" content="{SITE}/img/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{chr(10).join(jsonld(b) for b in blocks)}
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<header><div class="w hdr">
  <a class="brand" href="{L["home"]}"><img src="/img/logo-blanco.png" alt="Inspector Hacker"><b>INSPECTOR <span>HACKER</span></b></a>
  <nav>{nav}</nav>
</div></header>

<section class="hero sm"><div class="w">
  <div>
    <nav class="crumbs" aria-label="breadcrumb">{"".join(f'<a href="{u}">{n}</a><span>›</span>' for n, u in crumbs[:-1])}{crumbs_name}</nav>
    <div class="kick">{p["kick"]}</div>
    <h1>{p["h1"]}</h1>
    <p class="sub">{p["sub"]}</p>
    <div class="upd">{p.get("upd") or L["upd"]}</div>
    <div class="btns"><a class="btn btn-cy" href="{L["wa"]}" target="_blank" rel="noopener">{L["cta_btn"]}</a><a class="btn btn-ghost" href="#planes">{"Ver planes" if is_es else "See plans"}</a></div>
  </div>
</div></section>

<section class="alt"><div class="w"><article class="prose">
{body_html}</article></div></section>

<section id="planes"><div class="w">
  <div class="lab">{L["plans_lab"]}</div><h2>{L["plans_h2"]}</h2>
  <p class="lead">{L["plans_lead"]}</p>
  <div class="plans">{plans_html}</div>
  <p style="margin-top:22px;color:var(--ink2);font-size:15px">{L["plans_foot"]}</p>
</div></section>

<section id="faq" class="alt"><div class="w">
  <div class="lab">{L["faq_lab"]}</div><h2>{"Preguntas y respuestas" if is_es else "Questions and answers"}</h2>
  <div style="max-width:800px;margin-top:26px">{faq_html}</div>
</div></section>

<section id="{anchor_cities[1:]}"><div class="w">
  <div class="lab">{p.get("grid_lab") or L["cities_lab"]}</div><h2>{p.get("grid_h2") or L["cities_h2"]}</h2>
  <div class="cities">{cities_html}</div>
</div></section>

<section><div class="w"><div class="cta">
  <img src="/img/logo-blanco.png" alt="" style="height:64px;width:64px;margin-bottom:16px">
  <h2>{L["cta_h2"]}</h2>
  <p>{L["cta_p"]}</p>
  <div class="btns" style="justify-content:center"><a class="btn btn-cy" href="{L["wa"]}" target="_blank" rel="noopener">{L["cta_wa"]}</a><a class="btn btn-ghost" href="{CAL}" target="_blank" rel="noopener">{L["cta_cal"]}</a></div>
</div></div></section>

<footer><div class="w">
  <div>{L["foot_a"]} · {" · ".join(f'<a href="{h}">{t}</a>' for h, t in L["foot_links"])} · <a href="{pair_url}" hreflang="{other[0]}" lang="{other[0]}">{"English" if is_es else "Español"}</a></div>
  <div>{L["foot_b"]}</div>
</div></footer>
<a class="wa" href="{L["wa"]}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
{GRAB}
</body>
</html>
"""
    return html

def main():
    for p in PAGES:
        out_dir = os.path.join(ROOT, p["path"].strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render(p))
        words = len(strip_tags(" ".join(" ".join(ps) for _, ps in p["body"])).split())
        print(f"{p['path']:45s} {words:4d} palabras cuerpo")

if __name__ == "__main__":
    main()
