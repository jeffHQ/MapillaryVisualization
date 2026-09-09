"""Convert a Mapillary GeoJSON FeatureCollection into analysis-ready CSV tables."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IMAGE_COLUMNS = [
    "id_imagen", "longitud", "latitud", "fecha_captura_timestamp", "fecha_captura_utc",
    "distrito", "angulo_camara", "id_secuencia", "url_miniatura", "tipo_camara", "marca", "modelo",
    "es_panoramica", "calidad", "cantidad_objetos_detectados",
]


def as_utc(timestamp: Any) -> str:
    if timestamp in (None, ""):
        return ""
    return datetime.fromtimestamp(int(timestamp) / 1000, timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--images", required=True, type=Path)
    parser.add_argument("--detections", required=True, type=Path)
    args = parser.parse_args()

    collection = json.loads(args.input.read_text(encoding="utf-8"))
    features = collection.get("features", [])
    args.images.parent.mkdir(parents=True, exist_ok=True)
    args.detections.parent.mkdir(parents=True, exist_ok=True)
    with args.images.open("w", newline="", encoding="utf-8") as image_file, args.detections.open("w", newline="", encoding="utf-8") as detection_file:
        image_writer = csv.DictWriter(image_file, fieldnames=IMAGE_COLUMNS)
        detection_writer = csv.DictWriter(detection_file, fieldnames=["id_imagen", "objeto_detectado", "conteo_objeto"])
        image_writer.writeheader()
        detection_writer.writeheader()
        for feature in features:
            properties = feature.get("properties", {})
            coordinates = feature.get("geometry", {}).get("coordinates", [None, None])
            timestamp = properties.get("fecha_captura_timestamp")
            image_writer.writerow({
                "id_imagen": properties.get("id_imagen"), "longitud": coordinates[0], "latitud": coordinates[1],
                "fecha_captura_timestamp": timestamp, "fecha_captura_utc": as_utc(timestamp),
                "distrito": properties.get("distrito"), "angulo_camara": properties.get("angulo_camara"), "id_secuencia": properties.get("id_secuencia"),
                "url_miniatura": properties.get("url_miniatura"), "tipo_camara": properties.get("tipo_camara"),
                "marca": properties.get("marca"), "modelo": properties.get("modelo"),
                "es_panoramica": properties.get("es_panoramica"), "calidad": properties.get("calidad"),
                "cantidad_objetos_detectados": properties.get("cantidad_objetos_detectados"),
            })
            for label, count in Counter(properties.get("objetos_detectados", [])).items():
                detection_writer.writerow({"id_imagen": properties.get("id_imagen"), "objeto_detectado": label, "conteo_objeto": count})


if __name__ == "__main__":
    main()
