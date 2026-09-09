"""Collect Mapillary image metadata for a documented grid, one cell at a time."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from acquisition import fetch_images


def append_log(path: Path, row: dict[str, str]) -> None:
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["cell_id", "bbox", "queried_at_utc", "max_images_requested", "images_returned", "status", "notes"])
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def split_bbox(bbox: str) -> list[str]:
    """Split min_lon,min_lat,max_lon,max_lat into four equal child boxes."""
    min_lon, min_lat, max_lon, max_lat = (float(value) for value in bbox.split(","))
    mid_lon = (min_lon + max_lon) / 2
    mid_lat = (min_lat + max_lat) / 2
    return [
        f"{min_lon},{min_lat},{mid_lon},{mid_lat}",
        f"{mid_lon},{min_lat},{max_lon},{mid_lat}",
        f"{min_lon},{mid_lat},{mid_lon},{max_lat}",
        f"{mid_lon},{mid_lat},{max_lon},{max_lat}",
    ]


def fetch_resilient(bbox: str, max_images: int, timeout: int, retries: int, min_cell_size: float, depth: int = 0) -> tuple[list[dict], list[str]]:
    """Retry transient 5xx failures, then subdivide a dense cell if needed."""
    for attempt in range(retries + 1):
        try:
            return fetch_images(bbox, max_images, timeout), [bbox]
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status is None or status < 500 or attempt == retries:
                last_error = exc
                break
            time.sleep(2 ** attempt)
    else:  # pragma: no cover - loop always returns or breaks
        raise RuntimeError("unreachable retry state")

    min_lon, min_lat, max_lon, max_lat = (float(value) for value in bbox.split(","))
    if max(max_lon - min_lon, max_lat - min_lat) <= min_cell_size:
        raise last_error

    features: list[dict] = []
    query_boxes: list[str] = []
    for child_bbox in split_bbox(bbox):
        child_features, child_boxes = fetch_resilient(child_bbox, max_images, timeout, retries, min_cell_size, depth + 1)
        features.extend(child_features)
        query_boxes.extend(child_boxes)
    unique_features = {feature.get("properties", {}).get("id_imagen"): feature for feature in features}
    unique_features.pop(None, None)
    return list(unique_features.values()), query_boxes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    data_dir = Path(__file__).parent
    parser.add_argument("--grid", type=Path, default=data_dir / "acquisition_grid.csv")
    parser.add_argument("--output-dir", type=Path, default=data_dir / "raw_cells")
    parser.add_argument("--log", type=Path, default=data_dir / "acquisition_log.csv")
    parser.add_argument("--district", help="optional exact district name from the grid")
    parser.add_argument("--limit-cells", type=int, help="optional maximum number of selected cells")
    parser.add_argument("--max-images", type=int, default=300)
    parser.add_argument("--pause", type=float, default=1.0, help="seconds between successful requests")
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--retries", type=int, default=2, help="retries before subdividing a 5xx cell")
    parser.add_argument("--min-cell-size", type=float, default=0.0025, help="minimum subdivision width in decimal degrees")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.max_images < 1 or args.pause < 0 or args.retries < 0 or not 0 < args.min_cell_size <= 0.01:
        parser.error("--max-images must be positive; retry and spatial parameters must be valid")

    rows = list(csv.DictReader(args.grid.open(encoding="utf-8")))
    if args.district:
        rows = [row for row in rows if row["district"] == args.district]
    if args.limit_cells:
        rows = rows[: args.limit_cells]
    if not rows:
        parser.error("no grid cells match the requested selection")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        output = args.output_dir / f"{row['cell_id']}.geojson"
        if output.exists() and not args.overwrite:
            print(f"Skipping {row['cell_id']}: output already exists")
            continue
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        try:
            features, query_boxes = fetch_resilient(row["bbox"], args.max_images, args.timeout, args.retries, args.min_cell_size)
            payload = {
                "type": "FeatureCollection",
                "metadata": {"cell_id": row["cell_id"], "district": row["district"], "bbox": row["bbox"], "successful_query_boxes": query_boxes, "feature_count": len(features), "source": "Mapillary Graph API"},
                "features": features,
            }
            output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            append_log(args.log, {"cell_id": row["cell_id"], "bbox": row["bbox"], "queried_at_utc": timestamp, "max_images_requested": str(args.max_images), "images_returned": str(len(features)), "status": "success", "notes": f"successful subqueries: {len(query_boxes)}"})
            print(f"Saved {len(features)} images for {row['cell_id']} using {len(query_boxes)} successful subqueries")
        except Exception as exc:  # log HTTP and API errors without exposing credentials
            append_log(args.log, {"cell_id": row["cell_id"], "bbox": row["bbox"], "queried_at_utc": timestamp, "max_images_requested": str(args.max_images), "images_returned": "", "status": "error", "notes": str(exc)[:300]})
            print(f"Failed {row['cell_id']}: {exc}")
        time.sleep(args.pause)


if __name__ == "__main__":
    main()
