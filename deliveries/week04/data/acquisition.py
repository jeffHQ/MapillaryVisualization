import json
import requests

# 1. Tus 4 PUNTOS EN LIMA (Latitud, Longitud)
uno = (-12.09216904553763, -77.06329743577919)
dos = (-12.092982079994037, -77.06200997545204)
tres = (-12.094293420682783, -77.06233720495186)
cuatro = (-12.093066005990726, -77.06395725919684)

ACCESS_TOKEN = ""  # Reemplaza con tu token "MLY|..."

# 2. CÁLCULO DEL BOUNDING BOX AUTOMÁTICO
puntos = [uno, dos, tres, cuatro]
lats = [p[0] for p in puntos]
lons = [p[1] for p in puntos]
BBOX = f"{min(lons)},{min(lats)},{max(lons)},{max(lats)}"

# 3. CAMPOS A SOLICITAR (Incluyendo la relación 'detections')
# Nota cómo 'detections.value' solicita el tipo de objeto detectado en la foto
fields = (
    "id,"
    "geometry,"
    "computed_geometry,"
    "captured_at,"
    "compass_angle,"
    "sequence,"
    "thumb_1024_url,"
    "camera_type,"
    "make,"
    "model,"
    "is_pano,"
    "quality_score,"
    "detections.value"
)

url = f"https://graph.mapillary.com/images?fields={fields}&bbox={BBOX}&limit=10"
headers = {"Authorization": f"OAuth {ACCESS_TOKEN}"}

all_features = []
next_url = url

print("Consultando imágenes y sus detecciones internas...")

while next_url:
    response = requests.get(next_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        features = data.get("data", [])
        all_features.extend(features)

        paging = data.get("paging", {})
        next_url = paging.get("next")
    else:
        print(f"Error {response.status_code}: {response.text}")
        break

# 4. CONSTRUIR GEOJSON COMPLETO CON METADATOS Y OBJETOS DETECTADOS
geojson_data = {"type": "FeatureCollection", "features": []}

for item in all_features:
    # Extraer las etiquetas de las detecciones de la imagen
    detections_raw = item.get("detections", {}).get("data", [])
    objetos_detectados = [d.get("value") for d in detections_raw if "value" in d]

    # Usar 'computed_geometry' si existe por ser más precisa, o 'geometry' por defecto
    geometria = item.get("computed_geometry") or item.get("geometry")

    feature = {
        "type": "Feature",
        "geometry": geometria,
        "properties": {
            "id_imagen": item.get("id"),
            "fecha_captura_timestamp": item.get("captured_at"),
            "angulo_camara": item.get("compass_angle"),
            "id_secuencia": item.get("sequence"),
            "url_miniatura": item.get("thumb_1024_url"),
            "tipo_camara": item.get("camera_type"),
            "marca": item.get("make"),
            "modelo": item.get("model"),
            "es_panoramica": item.get("is_pano"),
            "calidad": item.get("quality_score"),
            "cantidad_objetos_detectados": len(objetos_detectados),
            "objetos_detectados": objetos_detectados,  # Arreglo con la lista de objetos (ej: ["regulatory--stop"])
        },
    }
    geojson_data["features"].append(feature)

# 5. GUARDAR ARCHIVO
output_file = "Magdalena.geojson"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, indent=2)

print(
    f"¡Éxito! Se procesaron {len(all_features)} imágenes con sus detecciones en '{output_file}'."
)