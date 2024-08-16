# Google Maps Scraper
Este Scraper surgio como proyecto personal para cubrir una necesidad de conseguir los datos de las locaciones o negocios en google maps especificos que cumplieran con una condicion de busqueda ( la que se encuentra en el input.txt) y que se encuentren en una locacion determinada ( las que se encuentran en el archivo links.txt).

Partiendo como base del proyecto creado por amineboutarfi (https://github.com/amineboutarfi/google_maps_scraper)

# Mejoras
Se agregaron los archivos `links.txt` y  `links_names.txt` para poder hacer multiples busquedas una en cada locacion de interes.
Se mejoraron los tiempos de busqueda.
Se corrigio un error al leer el archivo de inputs que tomaba el salto de linea.
Comente las partes del codigo que no usaba.
Agregue la linea para apagar el equipo al finalizar la busqueda para poder dejarlo prendido toda la noche.
Se creo el archivo `reports.txt` para registrar el reporte de la consola debido a que al apagarse el equipo este se borraba.

## To Install:
- (Optional: create & activate a virtual environment) `virtualenv venv`, then `source venv/bin/activate`

- `pip install -r requirements.txt`
- `playwright install chromium`

## to Run:
1. Add searches in `input.txt`, each search should be in a new line as shown in the example (check `input.txt`)
2. Then run: `python3 main.py` 
3. If you pass `-t=<how many>` it will be applied to all the searches. 

## Tips.

## To Run.
1. Añade las palabras claves que quieras buscar en `input.txt`, deben estar separadas por un salto de linea.
2. Añade los links de las localizaciones donde quieras hacer las busquedas en el archivo `links.txt`,deben estar separadas por un salto de linea(en el archivo se encuentran las ciudades mas importantes de argentina).
4. añade los nombres de las ciudades o locaciones en el archivo `links_names.txt`.
3. Opcionalmente puedes descomentar la linea en la que se apaga el equipo (fue agregada para dejar el script funcionando toda la noche)
4. Luego corre: `python3 main.py`

