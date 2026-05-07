from datetime import datetime
from pathlib import Path
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

PORTALES = [
    {
        "nombre": "Inmuebles24",
        "icono": "🏠",
        "descripcion": "Mayor volumen de casas en CDMX sur",
        "urls": [
            {"zona": "Coyoacán",              "url": "https://www.inmuebles24.com/casas-en-renta-en-coyoacan-ciudad-de-mexico.html?precio-hasta=60000"},
            {"zona": "Del Valle",             "url": "https://www.inmuebles24.com/casas-en-renta-en-del-valle-ciudad-de-mexico.html?precio-hasta=60000"},
            {"zona": "Narvarte / Álamos",     "url": "https://www.inmuebles24.com/casas-en-renta-en-narvarte-ciudad-de-mexico.html?precio-hasta=60000"},
            {"zona": "Pedregal / San Jerónimo","url": "https://www.inmuebles24.com/casas-en-renta-en-pedregal-de-san-angel-ciudad-de-mexico.html?precio-hasta=60000"},
        ]
    },
    {
        "nombre": "Lamudi",
        "icono": "🔍",
        "descripcion": "Buen filtro por colonia específica y precio",
        "urls": [
            {"zona": "Coyoacán hasta $60k",                    "url": "https://www.lamudi.com.mx/distrito-federal/coyoacan/casa/for-rent/price:0-60000/"},
            {"zona": "Del Valle hasta $60k",                   "url": "https://www.lamudi.com.mx/distrito-federal/benito-juarez/del-valle/casa/for-rent/price:0-60000/"},
            {"zona": "Álvaro Obregón (Águilas/Pedregal) $60k", "url": "https://www.lamudi.com.mx/distrito-federal/alvaro-obregon/casa/for-rent/price:0-60000/"},
        ]
    },
    {
        "nombre": "Vivanuncios",
        "icono": "📋",
        "descripcion": "Propiedades de particulares y agencias",
        "urls": [
            {"zona": "Casas renta sur CDMX hasta $60k", "url": "https://www.vivanuncios.com.mx/s-casas-en-renta/ciudad-de-mexico/v1c1096l1096p1?ad_type=OFFER&re_type=residential&priceMax=60000&re_subtype=house"},
        ]
    },
    {
        "nombre": "MercadoLibre Inmuebles",
        "icono": "🛒",
        "descripcion": "Amplio inventario, actualización frecuente",
        "urls": [
            {"zona": "Casas renta CDMX hasta $60k", "url": "https://inmuebles.mercadolibre.com.mx/casas/alquiler/distrito-federal/_PriceRange_0MXN-60000MXN"},
        ]
    },
    {
        "nombre": "Century21",
        "icono": "🏢",
        "descripcion": "Agencia con presencia en Coyoacán y Del Valle",
        "urls": [
            {"zona": "Casas renta CDMX", "url": "https://www.century21mexico.com/busqueda?tipoOperacion=2&tipoPropiedad=2&estado=9&precioMax=60000"},
        ]
    },
]


def generar_reporte():
    hoy = datetime.now()
    meses = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    fecha_es = f"{hoy.day} de {meses[hoy.month-1]} de {hoy.year}"
    colonias_str = " · ".join(ZONA["colonias"])

    lineas = [
        f"# Búsqueda de casa — {fecha_es}",
        "",
        f"> **Filtro duro:** Renta ≤ **${PRESUPUESTO_MAX:,} MXN/mes** con mantenimiento · Casa independiente o en condominio",
        f"> **Zona:** {ZONA['descripcion']} — {colonias_str}",
        "",
        "---",
        "",
        "## 🔗 Búsquedas del día",
        "",
    ]

    for portal in PORTALES:
        lineas.append(f"### {portal['icono']} {portal['nombre']}")
        lineas.append(f"*{portal['descripcion']}*")
        lineas.append("")
        for item in portal["urls"]:
            lineas.append(f"- [{item['zona']}]({item['url']})")
        lineas.append("")

    lineas += [
        "---",
        "",
        "## 📊 Evaluar propiedades encontradas",
        "",
        "→ [**Abrir evaluador**](evaluador.html) — califica cada propiedad y obtén su rating ponderado automáticamente.",
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
