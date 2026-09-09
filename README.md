# Mapillary Lima Corridor Visualization

Proyecto de visualización para DS5343 — Data Visualization.

El proyecto explora la evidencia visual de infraestructura urbana en zonas
comparables de **San Isidro** y **San Juan de Lurigancho**, dos contextos
socioeconómicos contrastantes de Lima Metropolitana. La unidad principal de
análisis es una imagen georreferenciada; las detecciones de infraestructura se
analizan como una tabla relacionada por identificador de imagen.

## Alcance actual

El dataset principal ya está consolidado: contiene **676 imágenes
georreferenciadas**, sin identificadores duplicados, de seis zonas de estudio
(tres por distrito). Contiene 146 secuencias y 12,276 filas agregadas de
detecciones. La comparación se hará con tasas normalizadas por imagen y cada
patrón podrá revisarse con la evidencia visual de origen. La adquisición se
ejecuta sin subir credenciales al repositorio.

## Entregables

- `deliveries/week04/`: selección, muestra, diccionario y proceso reproducible
  de adquisición del dataset.
- `deliveries/week05/`: propuesta del proyecto y presentación de la propuesta.

## Datos y privacidad

Los datos proceden de la API de Mapillary. Se deben respetar sus términos de
uso y la atribución requerida. El repositorio no contiene tokens, credenciales
ni imágenes descargadas directamente; solo metadatos y enlaces a miniaturas.

## Recolección

Consulta las instrucciones y el comando de ejecución en
[`deliveries/week04/README.md`](deliveries/week04/README.md). El token debe
establecerse localmente en la variable de entorno `MAPILLARY_ACCESS_TOKEN`.
