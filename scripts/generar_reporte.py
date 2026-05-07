from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
import json

PRESUPUESTO_MAX = 60000
ZONA = {
    "descripcion": "Sur-poniente CDMX",
    "colonias": [
        "Coyoacán", "Del Valle", "Narvarte", "Insurgentes Sur",
        "Pedregal de San Ángel", "Florida", "Álamos", "Portales",
        "Las Águilas", "San Jerónimo", "Copilco", "Tlalpan",
        "Jardines del Pedregal", "Santa Úrsula",
    ]
}

PESOS = {
    "jardin":    30,
    "ubicacion": 25,
    "tamanio":   20,
    "estado":    20,
    "estacion":  5,
}

def url_inmuebles24():
    base = "https://www.inmuebles24.com/casas-en-renta-en-ciudad-de-mexico.html"
    params = {"precio-desde": 0, "precio-hasta": PRESUPUESTO_MAX, "operacion": "2", "tipo-propiedad": "1"}
    return f"{base}?{urlencode(params)}"

def url_lamudi():
    base = "https://www.lamudi.com.mx/distrito-federal/casas/for-rent/"
    params = {"price[max]": PRESUPUESTO_MAX, "subdivision[]": "Coyoacan,Del+Valle,Narvarte,Pedregal"}
    return f"{base}?{urlencode(params)}"

def url_vivanuncios():
    base = "https://www.vivanuncios.com.mx/s-casas-en-renta/ciudad-de-mexico/v1c1096l1096p1"
    params = {"priceMax": PRESUPUESTO_MAX, "ad_type": "OFFER", "re_type": "residential"}
    return f"{base}?{urlencode(params)}"

def url_mercadolibre():
    base = "https://inmuebles.mercadolibre.com.mx/casas/alquiler/distrito-federal/"
    params = {"price": f"*-{PRESUPUESTO_MAX}"}
    return f"{base}?{urlencode(params)}"

def url_century21():
    base = "https://www.century21mexico.com/propiedades"
    params = {"tipo": "casas", "operacion": "renta", "estado": "ciudad-de-mexico", "precio_hasta": PRESUPUESTO_MAX}
    return f"{base}?{urlencode(params)}"

PORTALES = [
    {"nombre": "Inmuebles24",         "url": url_inmuebles24(),  "descripcion": "Mayor volumen de casas en CDMX sur",             "icono": "🏠"},
    {"nombre": "Lamudi",              "url": url_lamudi(),       "descripcion": "Buen filtro por colonia específica",              "icono": "🔍"},
    {"nombre": "Vivanuncios",         "url": url_vivanuncios(),  "descripcion": "Propiedades de particulares y agencias",          "icono": "📋"},
    {"nombre": "MercadoLibre Inmuebles", "url": url_mercadolibre(), "descripcion": "Amplio inventario, actualización frecuente",   "icono": "🛒"},
    {"nombre": "Century21",           "url": url_century21(),    "descripcion": "Agencia con presencia en Coyoacán y Del Valle",   "icono": "🏢"},
]

def generar_reporte():
    hoy = datetime.now()
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    fecha_es = f"{hoy.day} de {meses[hoy.month-1]} de {hoy.year}"
    colonias_str = " · ".join(ZONA["colonias"])

    lineas = [
        f"# Búsqueda de casa — {fecha_es}",
        "",
        f"> **Filtro duro:** Renta ≤ **${PRESUPUESTO_MAX:,} MXN/mes** con mantenimiento incluido · Casa independiente o en condominio",
        f"> **Zona:** {ZONA['descripcion']} — {colonias_str}",
        "",
        "---",
        "",
        "## 🔗 Búsquedas del día",
        "",
        "Abre cada portal con los filtros pre-aplicados:",
        "",
    ]

    for p in PORTALES:
        lineas += [f"### {p['icono']} [{p['nombre']}]({p['url']})", f"{p['descripcion']}", ""]

    lineas += [
        "---",
        "",
        "## 📊 Evaluar propiedades encontradas",
        "",
        "→ [**Abrir evaluador**](evaluador.html) — ingresa las propiedades que encuentres y calcula su rating automáticamente.",
        "",
        "---",
        "",
        "## ℹ️ Criterios de evaluación",
        "",
        "| Criterio | Peso |",
        "|---|---|",
        f"| 🌿 Jardín | {PESOS['jardin']}% |",
        f"| 📍 Ubicación y colonia | {PESOS['ubicacion']}% |",
        f"| 📐 Tamaño y distribución | {PESOS['tamanio']}% |",
        f"| 🔧 Estado del inmueble | {PESOS['estado']}% |",
        f"| 🚗 Estacionamiento | {PESOS['estacion']}% |",
        "",
        "> El precio **no forma parte del rating** — es condición de entrada (filtro duro).",
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
    historial_path = docs / "historial.json"
    historial = json.loads(historial_path.read_text()) if historial_path.exists() else []
    if hoy not in historial:
        historial.insert(0, hoy)
    historial_path.write_text(json.dumps(historial, indent=2), encoding="utf-8")
    print(f"✅ Reporte generado: docs/{hoy}.md")

if __name__ == "__main__":
    main()
