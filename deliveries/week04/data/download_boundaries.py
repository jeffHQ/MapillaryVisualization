"""Download the official reference boundaries for the three study districts."""

from __future__ import annotations

import json
from pathlib import Path

import requests

SERVICE_URL = "https://geoservidorperu.minam.gob.pe/arcgis/rest/services/GEOLOMAS_final/MapServer/0/query"
DISTRICTS = ("MAGDALENA DEL MAR", "SAN ISIDRO", "MIRAFLORES")


def main() -> None:
    output = Path(__file__).with_name("district_boundaries.geojson")
    quoted_names = ",".join(f"'{name}'" for name in DISTRICTS)
    response = requests.get(
        SERVICE_URL,
        params={
            "where": f"NOMBDIST IN ({quoted_names})",
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": "4326",
            "f": "geojson",
        },
        timeout=60,
    )
    response.raise_for_status()
    collection = response.json()
    found = {feature.get("properties", {}).get("NOMBDIST") for feature in collection.get("features", [])}
    missing = set(DISTRICTS) - found
    if missing:
        raise RuntimeError(f"Boundary response is incomplete; missing: {sorted(missing)}")
    collection["metadata"] = {
        "source": "Ministerio del Ambiente del Perú — Límite de los distritos de Lima Metropolitana (INEI, 2017)",
        "service_url": SERVICE_URL,
        "districts": list(DISTRICTS),
        "crs": "EPSG:4326",
    }
    output.write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(collection['features'])} district boundaries to {output}")


if __name__ == "__main__":
    main()
