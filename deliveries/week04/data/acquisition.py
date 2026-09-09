"""Download one bounded set of Mapillary image metadata without storing secrets.

Use a small bounding box per grid cell. The required MAPILLARY_ACCESS_TOKEN
environment variable is intentionally never read from a repository file.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

import requests

API_URL = "https://graph.mapillary.com/images"
FIELDS = ",".join(
    [
        "id",
        "geometry",
        "computed_geometry",
        "captured_at",
        "compass_angle",
        "sequence",
        "thumb_1024_url",
        "camera_type",
        "make",
        "model",
        "is_pano",
        "quality_score",
        "detections.value",
    ]
)


def parse_bbox(value: str) -> str:
    """Validate and normalize a min_lon,min_lat,max_lon,max_lat bounding box."""
    try:
        min_lon, min_lat, max_lon, max_lat = (float(part) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("bbox must have four comma-separated numbers") from exc
    if not (-180 <= min_lon < max_lon <= 180 and -90 <= min_lat < max_lat <= 90):
        raise argparse.ArgumentTypeError("bbox coordinates are invalid or unordered")
    return f"{min_lon},{min_lat},{max_lon},{max_lat}"


def image_to_feature(image: dict[str, Any]) -> dict[str, Any] | None:
    """Keep analysis fields and preserve the source geometry when available."""
    geometry = image.get("computed_geometry") or image.get("geometry")
    if not geometry:
        return None

    raw_detections = image.get("detections", {}).get("data", [])
    labels = [item["value"] for item in raw_detections if item.get("value")]
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "id_imagen": image.get("id"),
            "fecha_captura_timestamp": image.get("captured_at"),
            "angulo_camara": image.get("compass_angle"),
            "id_secuencia": image.get("sequence"),
            "url_miniatura": image.get("thumb_1024_url"),
            "tipo_camara": image.get("camera_type"),
            "marca": image.get("make"),
            "modelo": image.get("model"),
            "es_panoramica": image.get("is_pano"),
            "calidad": image.get("quality_score"),
            "cantidad_objetos_detectados": len(labels),
            "objetos_detectados": labels,
        },
    }


def fetch_images(bbox: str, max_images: int, timeout: int) -> list[dict[str, Any]]:
    token = os.getenv("MAPILLARY_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("Set MAPILLARY_ACCESS_TOKEN locally before running this script.")

    headers = {"Authorization": f"OAuth {token}"}
    params: dict[str, Any] | None = {"fields": FIELDS, "bbox": bbox, "limit": min(max_images, 100)}
    next_url: str | None = API_URL
    features: list[dict[str, Any]] = []

    while next_url and len(features) < max_images:
        response = requests.get(next_url, headers=headers, params=params, timeout=timeout)
        params = None  # paging URLs already include the original parameters
        response.raise_for_status()
        payload = response.json()
        for image in payload.get("data", []):
            feature = image_to_feature(image)
            if feature:
                features.append(feature)
                if len(features) >= max_images:
                    break
        next_url = payload.get("paging", {}).get("next")
        if next_url and len(features) < max_images:
            time.sleep(0.2)
    return features


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bbox", required=True, type=parse_bbox)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-images", type=int, default=500)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    if args.max_images < 1:
        parser.error("--max-images must be positive")

    try:
        features = fetch_images(args.bbox, args.max_images, args.timeout)
    except RuntimeError as exc:
        parser.error(str(exc))
    collection = {
        "type": "FeatureCollection",
        "metadata": {"bbox": args.bbox, "feature_count": len(features), "source": "Mapillary Graph API"},
        "features": features,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(features)} images to {args.output}")


if __name__ == "__main__":
    main()
