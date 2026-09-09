"""Merge raw Mapillary grid-cell GeoJSON files and remove duplicate image IDs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from prepare_grid import point_in_polygon


def district_for_feature(feature: dict, district_features: list[dict]) -> str | None:
    """Assign an image point to an official district polygon."""
    coordinates = feature.get("geometry", {}).get("coordinates", [])
    if len(coordinates) < 2:
        return None
    lon, lat = coordinates[0], coordinates[1]
    for district in district_features:
        if point_in_polygon(lon, lat, district["geometry"]):
            return district["properties"]["NOMBDIST"]
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    data_dir = Path(__file__).parent
    parser.add_argument("--input-dir", type=Path, default=data_dir / "raw_cells")
    parser.add_argument("--output", type=Path, default=data_dir / "mapillary_corridor_images.geojson")
    parser.add_argument("--boundaries", type=Path, default=data_dir / "district_boundaries.geojson")
    args = parser.parse_args()
    files = sorted(args.input_dir.glob("*.geojson"))
    if not files:
        parser.error("no .geojson cell files found")
    district_features = json.loads(args.boundaries.read_text(encoding="utf-8"))["features"]

    seen: set[str] = set()
    features = []
    sources = []
    excluded_outside_study_area = 0
    for file in files:
        collection = json.loads(file.read_text(encoding="utf-8"))
        sources.append(file.name)
        study_zone = collection.get("metadata", {}).get("cell_id", file.stem)
        for feature in collection.get("features", []):
            image_id = feature.get("properties", {}).get("id_imagen")
            if not image_id or image_id in seen:
                continue
            district = district_for_feature(feature, district_features)
            if not district:
                excluded_outside_study_area += 1
                continue
            seen.add(image_id)
            feature.setdefault("properties", {})["distrito"] = district
            feature["properties"]["zona_estudio"] = study_zone
            features.append(feature)
    payload = {
        "type": "FeatureCollection",
        "metadata": {"source": "Mapillary Graph API", "input_cells": sources, "deduplicated_feature_count": len(features), "excluded_outside_study_area": excluded_outside_study_area},
        "features": features,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Merged {len(files)} cells into {len(features)} unique images at {args.output}")


if __name__ == "__main__":
    main()
