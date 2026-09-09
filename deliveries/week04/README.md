# Week 4 — Selección y documentación del dataset

## Dataset seleccionado

**Una Lima, dos realidades: evidencia visual de infraestructura urbana en zonas comparables de San Isidro y San Juan de Lurigancho.**

## Fuente y acceso

- **Fuente principal:** [Mapillary Graph API](https://www.mapillary.com/developer/api-documentation).
- **Recolectores originales:** contribuyentes de Mapillary. El equipo conserva metadatos y URLs de miniatura de la API; no descarga ni redistribuye binarios de imágenes.
- **Acceso y colección:** 2026-09-09, mediante Client Token local en `MAPILLARY_ACCESS_TOKEN`.
- **Contexto territorial:** límites distritales del geoservidor público MINAM/INEI y [Mapa de Pobreza Provincial y Distrital 2013 de INEI](https://www.inei.gob.pe/media/DocumentosPublicos/pobreza/2013/Mapa-de-pobreza-provincial-y-distrital-2013.pdf).

## Problema y unidad de análisis

El dataset permite explorar cómo aparece la evidencia visual de elementos peatonales y viales —veredas, cruces, señales, iluminación y marcas— en dos contextos socioeconómicos contrastantes de Lima Metropolitana. No se usa para calificar personas, afirmar causalidad ni certificar el estado físico de una calle. La ausencia de una detección no prueba que la infraestructura no exista.

La unidad de análisis es una **imagen georreferenciada**. Una tabla relacionada almacena cada etiqueta de objeto detectada y su conteo por imagen. La variable `zona_estudio` conserva la trazabilidad de las seis áreas muestreadas.

## Cobertura y diseño de muestra

No se descargaron los distritos completos: San Juan de Lurigancho tiene una extensión muy superior a San Isidro. Se definieron tres ventanas urbanas de 0,005° por 0,005° en cada distrito y se consultaron con la misma cuadrícula, límite de 300 imágenes, reintentos y reglas de deduplicación. Una cuarta zona de San Isidro se evaluó y descartó porque no tuvo cobertura; su alternativa queda documentada en `study_zones.csv`.

| Distrito | Zona de estudio | Imágenes | Secuencias |
| --- | --- | ---: | ---: |
| San Isidro | `san_isidro_01` | 26 | 9 |
| San Isidro | `san_isidro_03` | 331 | 65 |
| San Isidro | `san_isidro_alt_01` | 100 | 35 |
| San Juan de Lurigancho | `san_juan_lurigancho_01` | 27 | 10 |
| San Juan de Lurigancho | `san_juan_lurigancho_02` | 93 | 10 |
| San Juan de Lurigancho | `san_juan_lurigancho_03` | 99 | 17 |

El release consolidado contiene **676 imágenes únicas**, **146 secuencias**, **12,276 filas agregadas de detecciones** y **129 etiquetas distintas**. No tiene IDs duplicados, fechas de captura faltantes ni imágenes fuera de los dos límites oficiales. Se retuvieron 457 imágenes de San Isidro y 219 de San Juan de Lurigancho. Las fechas de captura van de 2016-04-16 a 2024-11-29; esta heterogeneidad temporal será visible en la interfaz y tratada como limitación.

Los totales brutos no se interpretarán como una ventaja o desventaja urbana. La comparación se hará con tasas por 100 imágenes y, si se integra la red vial, por tramo de calle.

## Archivos de datos

| Archivo | Contenido |
| --- | --- |
| `data/contrast_lima/lima_contrast_images.geojson` | Dataset principal deduplicado, recortado a los límites y enriquecido con distrito y zona de estudio. |
| `data/contrast_lima/images.csv` | Una fila por imagen del dataset principal. |
| `data/contrast_lima/detections.csv` | Una fila por combinación imagen–etiqueta, con el conteo agregado. |
| `data/contrast_lima/district_boundaries.geojson` | Límites oficiales de los dos distritos. |
| `data/contrast_lima/study_zones.csv` | Seis zonas seleccionadas, alternativa y zona excluida, con bboxes y justificación. |
| `data/contrast_lima/acquisition_grid.csv` | Las seis consultas definitivas usadas para recolectar. |
| `data/sample.geojson` / `data/sample.csv` | Muestra reproducible y balanceada: dos imágenes por cada zona. |
| `data/detections_sample.csv` | Etiquetas y conteos correspondientes a la muestra de 12 imágenes. |
| `data/data_dictionary.csv` | Diccionario de atributos de las tablas y GeoJSON. |
| `data/contrast_lima/acquisition_log.csv` | Bitácora de las seis consultas definitivas. |

Las respuestas crudas de API se guardan en `contrast_lima/raw_cells/`; se excluyen de Git porque son reproducibles y no son necesarias para explorar las tablas finales.

## Calidad, licencia y límites

La colección se deduplicó por `id_imagen`, se asignó cada punto con point-in-polygon contra límites oficiales y se conservaron fechas, secuencias, calidad y zona de origen. Mapillary es una plataforma colaborativa: la cobertura depende de contribuyentes, dispositivos, fechas y comportamiento de la API. Las detecciones son automáticas y pueden tener falsos positivos, falsos negativos o repeticiones. La visualización mostrará la fotografía subyacente junto con los agregados y sus límites.

Los datos se usan bajo los [Términos de Mapillary](https://www.mapillary.com/legal/terms). La visualización final atribuirá Mapillary; no expondrá tokens ni redistribuirá binarios de imágenes.

## Reproducción

Desde `deliveries/week04`, con Python 3.10+ y el token configurado únicamente en la ventana local de PowerShell:

```powershell
python -m pip install -r data/requirements.txt
$env:MAPILLARY_ACCESS_TOKEN = (Get-Clipboard).Trim()

python data/download_boundaries.py --district "SAN ISIDRO" --district "SAN JUAN DE LURIGANCHO" --output data/contrast_lima/district_boundaries.geojson
python data/contrast_lima/build_collection_grid.py --status selected --output data/contrast_lima/acquisition_grid.csv
python data/collect_grid.py --grid data/contrast_lima/acquisition_grid.csv --output-dir data/contrast_lima/raw_cells --log data/contrast_lima/acquisition_log.csv --max-images 300 --pause 1 --timeout 45
python data/merge_cells.py --input-dir data/contrast_lima/raw_cells --boundaries data/contrast_lima/district_boundaries.geojson --output data/contrast_lima/lima_contrast_images.geojson
python data/build_sample_tables.py --input data/contrast_lima/lima_contrast_images.geojson --images data/contrast_lima/images.csv --detections data/contrast_lima/detections.csv
python data/contrast_lima/export_sample.py --input data/contrast_lima/lima_contrast_images.geojson --output data/sample.geojson --per-zone 2
python data/build_sample_tables.py --input data/sample.geojson --images data/sample.csv --detections data/detections_sample.csv
```

El recolector reintenta errores 5xx y subdivide una celda densa hasta 0,0025°. Los errores y conteos por celda quedan registrados sin revelar credenciales.
