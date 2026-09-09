# Week 5 — Team and Project Proposal

## Team

**Team name:** DINAMITA

| Member | Primary responsibility |
| --- | --- |
| Jeffry Arturo Hilario Quintana | Data engineering, acquisition and data quality |
| Jeffry Vargas | GIS, spatial analysis and visualization |
| Fatima Margarita Villon Zarate | User experience, narrative and evaluation |

## Working title

**Una Lima, dos realidades: brechas en la infraestructura urbana observable entre
San Isidro y San Juan de Lurigancho.**

## Files

| File | Purpose |
| --- | --- |
| `ProjectProposal.tex` / `ProjectProposal.pdf` | Editable source and PDF of the 2–3 page proposal. |
| `PresentationWeek05.tex` / `PresentationWeek05.pdf` | Editable source and PDF of the concise Week 5 slide presentation. |
| `README.md` | Team, scope, responsibilities and links. |
| `Magdalena.geojson` | Legacy 10-image pilot from the previous scope; it is not part of the new proposal or its future dataset. |

## Scope decision

The project will compare **matched urban study zones** in San Isidro and San
Juan de Lurigancho. It will not classify residents, rank districts, or claim
that an automated detection certifies infrastructure quality. The goal is to
explore how evidence of pedestrian and road infrastructure appears across a
socioeconomically contrasting urban context, and to let users inspect the
images behind every aggregated pattern.

## Dataset plan

The main dataset will be rebuilt after Week 5 using the same Mapillary
collection pipeline with a symmetric sampling protocol: three equivalent study
zones per district, fixed query grid, identical limits and logged retries. It
will combine Mapillary image metadata and object detections with official
district boundaries and an INEI socioeconomic context indicator. The previous
Magdalena–San Isidro–Miraflores dataset is retained in Week 4 only as previous
work; it is not claimed as the dataset for this proposal.

## Relevant links

- Repository: `https://github.com/jeffHQ/MapillaryVisualization`
- Mapillary API: [developer documentation](https://www.mapillary.com/developer/api-documentation)
- Socioeconomic context: [INEI Mapa de Pobreza Provincial y Distrital 2013](https://www.inei.gob.pe/media/DocumentosPublicos/pobreza/2013/Mapa-de-pobreza-provincial-y-distrital-2013.pdf)
