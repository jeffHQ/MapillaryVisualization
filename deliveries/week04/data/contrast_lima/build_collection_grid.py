"""Validate contrast study zones and create a grid accepted by collect_grid.py."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

DATA_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(DATA_DIR))
from prepare_grid import point_in_polygon  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    directory = Path(__file__).parent
    parser.add_argument("--zones", type=Path, default=directory / "study_zones.csv")
    parser.add_argument("--boundaries", type=Path, default=directory / "district_boundaries.geojson")
    parser.add_argument("--output", type=Path, default=directory / "screening_grid.csv")
    parser.add_argument("--role", action="append", choices=("primary", "alternate"), help="role to include; repeat to include more than one")
    parser.add_argument("--status", action="append", help="status to include; repeat to include more than one")
    args = parser.parse_args()

    included_roles = set(args.role or ("primary", "alternate"))
    boundaries = {
        feature["properties"]["NOMBDIST"]: feature["geometry"]
        for feature in json.loads(args.boundaries.read_text(encoding="utf-8"))["features"]
    }
    rows = [row for row in csv.DictReader(args.zones.open(encoding="utf-8")) if row["role"] in included_roles]
    if args.status:
        included_statuses = set(args.status)
        rows = [row for row in rows if row["status"] in included_statuses]
    if not rows:
        parser.error("no study zones match the selected roles")

    output_rows = []
    for row in rows:
        district_geometry = boundaries.get(row["district"])
        if not district_geometry:
            raise ValueError(f"Missing official boundary for {row['district']}")
        min_lon, min_lat, max_lon, max_lat = (float(row[key]) for key in ("min_lon", "min_lat", "max_lon", "max_lat"))
        center_lon, center_lat = (min_lon + max_lon) / 2, (min_lat + max_lat) / 2
        if not point_in_polygon(center_lon, center_lat, district_geometry):
            raise ValueError(f"Center of {row['zone_id']} is outside {row['district']}")
        output_rows.append({
            "cell_id": row["zone_id"],
            "district": row["district"],
            "min_lon": row["min_lon"],
            "min_lat": row["min_lat"],
            "max_lon": row["max_lon"],
            "max_lat": row["max_lat"],
            "bbox": row["bbox"],
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["cell_id", "district", "min_lon", "min_lat", "max_lon", "max_lat", "bbox"])
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Validated and wrote {len(output_rows)} collection zones to {args.output}")


if __name__ == "__main__":
    main()
