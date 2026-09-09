# Week 5 — Team and Project Proposal

## Team

**Team name:** DINAMITA

| Member | Primary responsibility |
| --- | --- |
| Jeffry Arturo Hilario Quintana | Data engineering and reproducible acquisition |
| Jeffry Vargas | GIS, spatial analysis, and visualization |
| Fatima Margarita Villon Zarate | User experience, narrative, and evaluation |

## Working title

**Coverage, recency, and capture quality of Mapillary urban imagery in the
Magdalena del Mar – San Isidro – Miraflores corridor.**

## Files

| File | Purpose |
| --- | --- |
| `ProjectProposal.tex` / `ProjectProposal.pdf` | Editable source and PDF of the 2–3 page proposal. |
| `PresentationWeek05.tex` / `PresentationWeek05.pdf` | Editable source and PDF of the concise Week 5 slide presentation. |
| `README.md` | Team, responsibilities, links, and repository structure. |
| `../week04/` | Revised dataset package used by the proposal. |
| `Magdalena.geojson` | Legacy 10-image pilot, retained only for traceability; it is not the analytical dataset. |

## Relevant links

- Repository: `https://github.com/jeffHQ/MapillaryVisualization`
- Data source: [Mapillary developer documentation](https://www.mapillary.com/developer/api-documentation)
- Dataset package: [`../week04/`](../week04/)

## Scope decision

The project does **not** claim to analyze every image in Lima Metropolitana or
to compare Lima with Bogotá and Cairo. The study is intentionally focused on a
three-district corridor so that its collection, cleaning, analytical questions,
and later D3 implementation remain feasible within the semester.

## Dataset status

The initial pilot was used to validate the pipeline. The revised Week 4 package
now contains 9,938 de-duplicated and spatially clipped images from 18 grid
cells, plus 166,475 aggregated image/object-label rows. The access token
remains local and is not committed.
