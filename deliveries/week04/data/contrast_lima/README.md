# Dataset nuevo — Una Lima, dos realidades

Este directorio contiene el dataset principal actual del proyecto: una
comparación de zonas urbanas equivalentes en **San Isidro** y **San Juan de
Lurigancho**. El release final contiene 676 imágenes únicas, 146 secuencias,
12,276 filas agregadas de detecciones y 129 etiquetas distintas.

## Diseño de muestra

No se descargaron ambos distritos completos. Cada distrito tiene tres zonas de
estudio de 0,005° por 0,005° (aprox. 0,55 km por lado), sometidas al mismo
protocolo de consulta. El archivo `study_zones.csv` es la fuente de verdad para
sus identificadores, ubicación y estado. El cribado descartó `san_isidro_02`
por cobertura cero y seleccionó `san_isidro_alt_01` como reemplazo.

La unidad de análisis es una imagen georreferenciada. Las detecciones son una
tabla relacionada por `id_imagen`. Los resultados se normalizarán por 100
imágenes y, si se incorpora la red vial, por tramo; los conteos brutos no se
usarán para comparar los distritos.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `district_boundaries.geojson` | Límites oficiales descargados desde MINAM. |
| `study_zones.csv` | Seis zonas principales y alternativas documentadas. |
| `screening_raw/` | Resultado de una consulta piloto por zona; se ignora en Git. |
| `raw_cells/` | Consultas de la muestra definitiva; se ignora en Git. |
| `acquisition_log.csv` | Bitácora de consultas y errores sin credenciales. |
| `lima_contrast_images.geojson` | Dataset final deduplicado y recortado. |
| `images.csv`, `detections.csv` | Tablas analíticas finales. |

## Recolección

El token se mantiene únicamente en la variable de entorno
`MAPILLARY_ACCESS_TOKEN`. Nunca se escribe en los scripts, archivos de datos o
repositorio. El cribado se ejecutó antes de recolectar las tres zonas
seleccionadas de cada distrito con el mismo límite, cuadrícula y reglas de
reintento.

## Interpretación responsable

Mapillary aporta evidencia visual y detecciones automáticas; no certifica la
existencia, estado ni calidad de infraestructura. La ausencia de una detección
no prueba ausencia de infraestructura. El indicador socioeconómico del INEI se
usa solo para dar contexto al contraste territorial.
