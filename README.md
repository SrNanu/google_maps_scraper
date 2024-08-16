# Scraper de Google Maps

Este scraper surgió como un proyecto personal para cubrir la necesidad de obtener datos de locaciones o negocios específicos en Google Maps que cumplan con una condición de búsqueda (la cual se encuentra en `input.txt`) y que estén ubicados en una localización determinada (las cuales se encuentran en el archivo `links.txt`).

Este proyecto se basa en el creado por [amineboutarfi](https://github.com/amineboutarfi/google_maps_scraper).

## Mejoras

- Se añadieron los archivos `links.txt` y `links_names.txt` para realizar búsquedas múltiples, una en cada locación de interés.
- Se mejoraron los tiempos de búsqueda.
- Se corrigió un error al leer el archivo de inputs que tomaba el salto de línea.
- Se comentaron las partes del código que no se utilizaban.
- Se añadió una línea para apagar el equipo al finalizar la búsqueda, permitiendo que el script funcione durante la noche.
- Se creó el archivo `reports.txt` para registrar el reporte de la consola, ya que el reporte se borraba al apagarse el equipo.

## Instalación

- (Opcional: crea y activa un entorno virtual) `virtualenv venv`, luego `source venv/bin/activate`

- `pip install -r requirements.txt`
- `playwright install chromium`

## Ejecución

1. Añade las palabras clave que quieras buscar en `input.txt`, cada una en una nueva línea.
2. Añade los enlaces de las localizaciones donde quieras realizar las búsquedas en el archivo `links.txt`, cada uno en una nueva línea (el archivo contiene las ciudades más importantes de Argentina).
3. Añade los nombres de las ciudades o localizaciones en el archivo `links_names.txt`.
4. Opcionalmente, puedes descomentar la línea en la que se apaga el equipo (fue añadida para dejar el script funcionando durante la noche).
5. Luego corre: `python3 main.py`
