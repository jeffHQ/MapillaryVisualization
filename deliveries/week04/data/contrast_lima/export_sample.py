"""Create a small deterministic, zone-balanced sample from the final GeoJSON."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-zone", type=int, default=2)
    args = parser.parse_args()
    if args.per_zone < 1:
        parser.error("--per-zone must be positive")

    collection = json.loads(args.input.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for feature in collection.get("features", []):
        grouped[feature.get("properties", {}).get("zona_estudio", "unknown")].append(feature)
    selected = []
    for zone in sorted(grouped):
        selected.extend(sorted(grouped[zone], key=lambda item: str(item.get("properties", {}).get("id_imagen", "")))[: args.per_zone])

    payload = {
        "type": "FeatureCollection",
        "metadata": {
            "source": "Deterministic zone-balanced sample of lima_contrast_images.geojson",
            "per_zone": args.per_zone,
            "feature_count": len(selected),
        },
        "features": selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(selected)} sampled images from {len(grouped)} zones to {args.output}")


if __name__ == "__main__":
    main()
