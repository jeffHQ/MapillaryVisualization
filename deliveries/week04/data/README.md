# Data folder

El dataset analítico actual está en [`contrast_lima/`](contrast_lima/). Corresponde a la propuesta **Una Lima, dos realidades** y compara seis zonas de estudio: tres en San Isidro y tres en San Juan de Lurigancho.

- `contrast_lima/lima_contrast_images.geojson`: 676 imágenes únicas con geometría, distrito y zona de estudio.
- `contrast_lima/images.csv`: tabla principal de imágenes.
- `contrast_lima/detections.csv`: tabla relacionada de etiquetas y conteos.
- `sample.geojson`, `sample.csv` y `detections_sample.csv`: muestra pequeña, balanceada y directamente inspeccionable para Week 4.

Los scripts comunes de adquisición, colección, unión y conversión siguen en este directorio. Los scripts específicos del contraste y su bitácora están en `contrast_lima/`. Consulta procedencia, límites y comandos de reproducción en el [README de Week 4](../README.md).
