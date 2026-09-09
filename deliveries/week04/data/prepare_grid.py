"""Create a reproducible Mapillary query grid from district boundary GeoJSON."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Iterable


def rings(geometry: dict) -> Iterable[list[list[float]]]:
    if geometry["type"] == "Polygon":
        yield from geometry["coordinates"]
    elif geometry["type"] == "MultiPolygon":
        for polygon in geometry["coordinates"]:
            yield from polygon
    else:
        raise ValueError(f"Unsupported geometry type: {geometry['type']}")


def point_in_ring(lon: float, lat: float, ring: list[list[float]]) -> bool:
    inside = False
    for index, current in enumerate(ring):
        previous = ring[index - 1]
        x1, y1 = current
        x2, y2 = previous
        crosses = (y1 > lat) != (y2 > lat)
        if crosses and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def point_in_polygon(lon: float, lat: float, geometry: dict) -> bool:
    polygon_rings = list(rings(geometry))
    return bool(polygon_rings) and point_in_ring(lon, lat, polygon_rings[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundaries", type=Path, default=Path(__file__).with_name("district_boundaries.geojson"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("acquisition_grid.csv"))
    parser.add_argument("--cell-size", type=float, default=0.01, help="cell width and height in decimal degrees")
    args = parser.parse_args()
    if not 0 < args.cell_size <= 0.01:
        parser.error("--cell-size must be greater than 0 and no more than 0.01 degrees")

    features = json.loads(args.boundaries.read_text(encoding="utf-8"))["features"]
    rows: list[dict[str, str]] = []
    for feature in sorted(features, key=lambda item: item["properties"]["NOMBDIST"]):
        district = feature["properties"]["NOMBDIST"]
        exterior = next(iter(rings(feature["geometry"])))
        longitudes = [point[0] for point in exterior]
        latitudes = [point[1] for point in exterior]
        min_lon, max_lon = min(longitudes), max(longitudes)
        min_lat, max_lat = min(latitudes), max(latitudes)
        lon_start = math.floor(min_lon / args.cell_size) * args.cell_size
        lat_start = math.floor(min_lat / args.cell_size) * args.cell_size
        lon = lon_start
        number = 1
        while lon < max_lon:
            lat = lat_start
            while lat < max_lat:
                center_lon = lon + args.cell_size / 2
                center_lat = lat + args.cell_size / 2
                if point_in_polygon(center_lon, center_lat, feature["geometry"]):
                    rows.append({
                        "cell_id": f"{district.lower().replace(' ', '_')}_{number:02d}",
                        "district": district,
                        "min_lon": f"{lon:.6f}", "min_lat": f"{lat:.6f}",
                        "max_lon": f"{lon + args.cell_size:.6f}", "max_lat": f"{lat + args.cell_size:.6f}",
                        "bbox": f"{lon:.6f},{lat:.6f},{lon + args.cell_size:.6f},{lat + args.cell_size:.6f}",
                    })
                    number += 1
                lat += args.cell_size
            lon += args.cell_size

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["cell_id", "district", "min_lon", "min_lat", "max_lon", "max_lat", "bbox"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} query cells to {args.output}")


if __name__ == "__main__":
    main()
