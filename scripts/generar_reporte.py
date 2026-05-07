from datetime import datetime
from pathlib import Path
import json

PRESUPUESTO_MAX = 60000

PESOS = {
    "jardin":    30,
    "ubicacion": 25,
    "tamanio":   20,
    "estado":    20,
    "estacion":   5,
}

COLONIAS = [
    {"nombre": "Del Valle Sur",             "alcaldia": "Benito Juárez",       "cp": "03200", "slug_lamudi": "benito-juarez/del-valle-sur",                    "slug_i24": "del-valle-sur-ciudad-de-mexico"},
    {"nombre": "La Florida",                "alcaldia": "Álvaro Obregón",      "cp": "01030", "slug_lamudi": "alvaro-obregon/la-florida",                      "slug_i24": "florida-ciudad-de-mexico"},
    {"nombre": "Del Carmen Coyoacán",       "alcaldia": "Coyoacán",            "cp": "04100", "slug_lamudi": "coyoacan/del-carmen",                            "slug_i24": "del-carmen-ciudad-de-mexico"},
    {"nombre": "Romero de Terreros",        "alcaldia": "Coyoacán",            "cp": "04310", "slug_lamudi": "coyoacan/romero-de-terreros",                    "slug_i24": "romero-de-terreros-ciudad-de-mexico"},
    {"nombre": "Narvarte Poniente",         "alcaldia": "Benito Juárez",       "cp": "03020", "slug_lamudi": "benito-juarez/narvarte-poniente",                "slug_i24": "narvarte-poniente-ciudad-de-mexico"},
    {"nombre": "Pedregal de San Francisco", "alcaldia": "Coyoacán",            "cp": "04320", "slug_lamudi": "coyoacan/pedregal-de-san-francisco",             "slug_i24": "pedregal-de-san-francisco-ciudad-de-mexico"},
    {"nombre": "Acacias",                   "alcaldia": "Benito Juárez",       "cp": "03240", "slug_lamudi": "benito-juarez/acacias-1",                        "slug_i24": "acacias-ciudad-de-mexico"},
    {"nombre": "San Ángel Inn",             "alcaldia": "Álvaro Obregón",      "cp": "01060", "slug_lamudi": "alvaro-obregon/san-angel-inn",                   "slug_i24": "san-angel-inn-ciudad-de-mexico"},
    {"nombre": "Las Águilas",               "alcaldia": "Álvaro Obregón",      "cp": "01710", "slug_lamudi": "alvaro-obregon/las-aguilas",                     "slug_i24": "las-aguilas-ciudad-de-mexico"},
    {"nombre": "San Jerónimo Lídice",       "alcaldia": "Magdalena Contreras", "cp": "10200", "slug_lamudi": "la-magdalena-contreras/san-jeronimo-lidice",     "slug_i24": "san-jeronimo-lidice-ciudad-de-mexico"},
    {"nombre": "Pedregal de San Ángel",     "alcaldia": "Álvaro Obregón",      "cp": "01900", "slug_lamudi": "alvaro-obregon/jardines-del-pedregal",           "slug_i24": "jardines-del-pedregal-ciudad-de-mexico"},
    {"nombre": "San Ángel",                 "alcaldia": "Álvaro Obregón",      "cp": "01000", "slug_lamudi": "alvaro-obregon/san-angel",                       "slug_i24": "san-angel-ciudad-de-mexico"},
]

BASE_LAMUDI   = "https://www.lamudi.com.mx/distrito-federal"
BASE_I24      = "https://www.inmuebles24.com/casas-en-renta-en"
BASE_I24_COND = "https://www.inmuebles24.com/casa-en-condominio-en-renta-en"

def url_lamudi(c):      return f"{BASE_LAMUDI}/{c['slug_lamudi']}/casa/for-rent/price:0-{PRESUPUESTO_MAX}/"
def url_lamudi_j(c):    return f"{BASE_LAMUDI}/{c['slug_lamudi']}/casa/for-rent/price:0-{PRESUPUESTO_MAX}/garden/"
def url_i24(c):         return f"{BASE_I24}-{c['slug_i24']}-hasta-{PRESUPUESTO_MAX}-pesos.html"
def url_i24_cond(c):    return f"{BASE_I24_COND}-{c['slug_i24']}-hasta-{PRESUPUESTO_MAX}-pesos.html"

PORTALES_FIJOS = [
    {
        "nombre": "MercadoLibre Inmuebles", "icono": "🛒",
        "descripcion": "Filtrar zona manualmente al abrir",
        "instrucciones": "Al abrir: en el mapa escribe cada colonia y filtra precio hasta $60,000",
        "urls": [{"zona": "Casas renta CDMX hasta $60k", "url": "https://inmuebles.mercadolibre.com.mx/casas/alquiler/distrito-federal/_PriceRange_0MXN-60000MXN"}],
    },
    {
        "nombre": "Vivanuncios", "icono": "📋",
        "descripcion": "Filtrar al abrir: Tipo → Casa · Precio máx → $60,000",
        "instrucciones": "Al abrir: Tipo → Casa, Precio máx → $60,000, busca cada colonia",
        "urls": [{"zona": "Casas renta sur CDMX", "url": "https://www.vivanuncios.com.mx/s-casas-en-renta/ciudad-de-mexico/v1c1096l1096p1"}],
    },
    {
        "nombre": "Century21", "icono": "🏢",
        "descripcion": "Filtrar manualmente: Renta · Casa · CDMX · hasta $60k",
        "instrucciones": "Al abrir: Operación → Renta, Tipo → Casa, Estado → CDMX, Precio máx → $60,000",
        "urls": [{"zona": "Buscador Century21 México", "url": "https://www.century21mexico.com/propiedades"}],
    },
]


def generar_reporte():
    hoy = datetime.now()
    meses = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    fecha_es = f"{hoy.day} de {meses[hoy.month-1]} de {hoy.year}"
    nombres = " · ".join(c["nombre"] for c in COLONIAS)

    lineas = [
        f"# Búsqueda de casa — {fecha_es}",
        "",
        f"> **Filtro duro:** Renta ≤ **$60,000 MXN/mes** con mantenimiento · Casa independiente o en condominio",
        f"> **Colonias:** {nombres}",
        "",
        "---",
        "",
        "## 🏠 Inmuebles24",
        "*Mayor volumen — una URL por colonia con precio en la ruta*",
        "",
    ]
    for col in COLONIAS:
        lineas.append(f"- [{col['nombre']} — casas]({url_i24(col)}) · [condominios]({url_i24_cond(col)}) *(CP {col['cp']} · {col['alcaldia']})*")
    lineas.append("")

    lineas += [
        "---",
        "",
        "## 🔍 Lamudi",
        "*URLs verificadas por colonia · incluye filtro de jardín*",
        "",
    ]
    for col in COLONIAS:
        lineas.append(f"- [{col['nombre']}]({url_lamudi(col)}) · [con jardín]({url_lamudi_j(col)}) *(CP {col['cp']} · {col['alcaldia']})*")
    lineas.append("")

    for portal in PORTALES_FIJOS:
        lineas += [
            "---",
            "",
            f"## {portal['icono']} {portal['nombre']}",
            f"*{portal['descripcion']}*",
            f"> ⚙️ {portal['instrucciones']}",
            "",
        ]
        for item in portal["urls"]:
            lineas.append(f"- [{item['zona']}]({item['url']})")
        lineas.append("")

    lineas += [
        "---",
        "",
        "## 📮 Colonias objetivo",
        "",
        "| # | Colonia | CP | Alcaldía |",
        "|---|---|---|---|",
    ]
    for i, col in enumerate(COLONIAS, 1):
        lineas.append(f"| {i} | {col['nombre']} | {col['cp']} | {col['alcaldia']} |")

    lineas += [
        "",
        "---",
        "",
        "## 📊 Evaluar propiedades encontradas",
        "",
        "→ [**Abrir evaluador**](evaluador.html)",
        "",
        "| Criterio | Peso |",
        "|---|---|",
        f"| 🌿 Jardín | {PESOS['jardin']}% |",
        f"| 📍 Ubicación | {PESOS['ubicacion']}% |",
        f"| 📐 Tamaño | {PESOS['tamanio']}% |",
        f"| 🔧 Estado | {PESOS['estado']}% |",
        f"| 🚗 Estacionamiento | {PESOS['estacion']}% |",
        "",
        "> Precio = filtro duro, no criterio de rating.",
        "",
        "---",
        "",
        f"*Generado automáticamente · {hoy.strftime('%Y-%m-%d %H:%M')} UTC*",
    ]
    return "\n".join(lineas)


def main():
    docs = Path("docs")
    docs.mkdir(exist_ok=True)
    reporte = generar_reporte()
    hoy = datetime.now().strftime("%Y-%m-%d")
    (docs / f"{hoy}.md").write_text(reporte, encoding="utf-8")
    (docs / "index.md").write_text(reporte, encoding="utf-8")
    (docs / "colonias.json").write_text(
        json.dumps(COLONIAS, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    historial_path = docs / "historial.json"
    historial = json.loads(historial_path.read_text()) if historial_path.exists() else []
    if hoy not in historial:
        historial.insert(0, hoy)
    historial_path.write_text(json.dumps(historial, indent=2), encoding="utf-8")
    print(f"✅ Reporte generado: docs/{hoy}.md")
    print(f"   {len(COLONIAS)} colonias · {len(COLONIAS)*4} URLs de Inmuebles24+Lamudi")

if __name__ == "__main__":
    main()
