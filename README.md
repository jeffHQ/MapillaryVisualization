# Mapillary Lima Corridor Visualization

Proyecto de visualización para DS5343 — Data Visualization.

El proyecto analiza la cobertura, actualidad y calidad de las imágenes de
Mapillary en el corredor urbano **Magdalena del Mar – San Isidro – Miraflores**.
La unidad principal de análisis es una imagen georreferenciada. Las detecciones
de infraestructura se analizan como una tabla relacionada por identificador de
imagen.

## Alcance actual

El dataset principal ya está consolidado: contiene **9,938 imágenes
georreferenciadas**, sin identificadores duplicados y recortadas espacialmente
a los tres distritos del corredor. Proviene de 18 celdas de consulta y contiene
1,915 secuencias y 166,475 filas agregadas de detecciones. La muestra piloto
de 10 imágenes de Magdalena se conserva solamente para validar y documentar el
esquema de datos; no representa el dataset final. La adquisición se ejecuta
sin subir credenciales al repositorio.

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
