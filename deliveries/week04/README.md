# Week 4 — Dataset Selection and Submission

## Dataset title

**Mapillary image coverage, capture quality and detected urban infrastructure
in the Magdalena del Mar – San Isidro – Miraflores corridor, Lima, Peru.**

## Source and collector

- **Source:** [Mapillary Graph API](https://www.mapillary.com/developer/api-documentation).
- **Collector:** Mapillary contributors; original captures are uploaded by its
  contributor community and made available through Mapillary.
- **Access date:** 2026-09-09.
- **Access method:** authenticated API requests with a Mapillary client access
  token held locally by the team.

## Why this dataset is useful

The data connect location, capture time, sequence, camera characteristics,
image quality, and AI detections. They support a coordinated spatial,
temporal, and multivariate analysis rather than a single map of points.

## Scope and unit of analysis

The final study area is the urban corridor formed by Magdalena del Mar, San
Isidro, and Miraflores. One record in the main table represents one Mapillary
image. A second table aggregates detected-object labels by image. Official
district boundaries are used to retain only images within the study area.

The included `data/sample.geojson` and `data/sample.csv` are a **pilot sample**
of 10 images from Magdalena. They validate the schema and acquisition process;
they must not be interpreted as coverage of all Lima or of the three-district
corridor.

## Geographic and temporal coverage

- **Target geographic coverage:** Magdalena del Mar, San Isidro, and Miraflores,
  Lima, Peru, collected through a reproducible grid of small bounding-box
  requests.
- **Pilot geographic coverage:** a small area in Magdalena near longitude
  -77.0627 to -77.0621 and latitude -12.0940 to -12.0933.
- **Pilot temporal coverage:** 2024-10-05 19:19:19 to 19:56:06 UTC.
- **Collected temporal coverage:** 2015-04-02 to 2026-08-19 UTC.

## Current collected release

The documented 18-cell grid was collected and merged on 2026-09-09. After
de-duplicating by image identifier and clipping points to the three official
district boundaries, the analytical dataset contains **9,938 images**, **1,915
capture sequences**, and **166,475 aggregated image/object-label rows**.

| District | Images retained |
| --- | ---: |
| Magdalena del Mar | 928 |
| San Isidro | 4,697 |
| Miraflores | 4,313 |

The raw API cells contained 10,506 unique image IDs before the spatial clip;
568 points outside the official study-area boundaries were excluded. This
prevents a bounding-box edge from being misclassified as one of the districts.

## Data files

| File | Purpose |
| --- | --- |
| `data/sample.geojson` | Original pilot response transformed to a GeoJSON FeatureCollection. |
| `data/sample.csv` | One row per pilot image, suitable for tabular inspection. |
| `data/detections_sample.csv` | One row per image/object label after aggregation of repeated detections. |
| `data/mapillary_corridor_images.geojson` | Final, de-duplicated and spatially clipped dataset of 9,938 images. |
| `data/images.csv` | Final table with one row per retained Mapillary image. |
| `data/detections.csv` | Final related table of aggregated object labels by image. |
| `data/data_dictionary.csv` | Field definitions, types, formats, and missing-value handling. |
| `data/acquisition.py` | Reproducible API extraction script; it never stores a token in code. |
| `data/build_sample_tables.py` | Converts a GeoJSON extraction into the two CSV tables. |
| `data/acquisition_log.csv` | Template for recording every grid-cell query and its outcome. |
| `data/district_boundaries.geojson` | Official reference boundaries for the three study districts. |
| `data/acquisition_grid.csv` | Automatically generated small bounding boxes used for API queries. |
| `data/collect_grid.py` | Resumable collector that saves one response per grid cell and logs results. |
| `data/merge_cells.py` | Combines cell files and de-duplicates the final GeoJSON by image ID. |

## License, terms, and limitations

Mapillary data are accessed under the applicable
[Mapillary Terms of Use](https://www.mapillary.com/legal/terms) and API
conditions. The final visualization will visibly attribute Mapillary and link
to its website. The team will not redistribute image binaries, expose private
information, or commit access tokens.

Coverage is contributor-generated, so it is not a census of streets or urban
infrastructure. Capture density, device type, dates, and AI detections can be
uneven or missing. Object labels can repeat within an image; therefore the
related detections table stores both the raw count and the aggregated count.

## Reproducible acquisition

1. Install Python 3.10+ and dependencies:

   ```powershell
   python -m pip install -r data/requirements.txt
   ```

2. Set the token only in the current local shell:

   ```powershell
   $env:MAPILLARY_ACCESS_TOKEN = 'MLY|...'
   ```

3. Query one small bounding box and write a raw GeoJSON extraction:

   ```powershell
   python data/acquisition.py --bbox=<min_lon,min_lat,max_lon,max_lat> --output data/raw_cell.geojson --max-images 500
   ```

4. Convert the resulting GeoJSON into image and detections tables:

   ```powershell
   python data/build_sample_tables.py --input data/raw_cell.geojson --images data/images.csv --detections data/detections.csv
   ```

Repeat step 3 for documented grid cells within the three target districts, then
merge and de-duplicate by `id_imagen`. Record every queried cell, date, result
count, and error in the acquisition log before making analytical claims.

The district boundaries are downloaded from the public MINAM geoserver and the
query grid is generated with:

```powershell
python data/download_boundaries.py
python data/prepare_grid.py --cell-size 0.01
```

Start with one cell per district to validate the collection, then run the full
grid. The commands must be executed in the same PowerShell window in which
`MAPILLARY_ACCESS_TOKEN` was set:

```powershell
python data/collect_grid.py --district "MAGDALENA DEL MAR" --limit-cells 1 --max-images 100
python data/collect_grid.py --district "SAN ISIDRO" --limit-cells 1 --max-images 100
python data/collect_grid.py --district "MIRAFLORES" --limit-cells 1 --max-images 100
python data/merge_cells.py
python data/build_sample_tables.py --input data/mapillary_corridor_images.geojson --images data/images.csv --detections data/detections.csv
```

The collector retries server-side failures and, when a dense cell times out,
automatically divides it into boxes as small as 0.0025 degrees. This preserves
the original study grid while adapting to Mapillary response limits.
