
[![DOI](https://zenodo.org/badge/1179290204.svg)](https://doi.org/10.5281/zenodo.18969936)
# Análisis de Textos Científicos con Grobid (RSE)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Documentación](https://img.shields.io/badge/docs-ReadTheDocs-blue.svg)](https://rse-proyecto-final.readthedocs.io/)

Proyecto de la asignatura de Ingeniería de Software de Investigación enfocado en la aplicación de buenas prácticas de Open Science, FAIR y MLOps.

## Descripción
Pipeline automatizado para extraer información de 10 artículos científicos Open Access en formato PDF mediante el motor **Grobid**. El sistema procesa los documentos y genera:
1. Una **Nube de palabras clave** basada en los abstracts.
2. Un **Gráfico de barras** con el conteo de figuras por artículo.
3. Un **Archivo CSV** indexando todos los enlaces (URLs) extraídos de los textos.

##  Instrucciones de Ejecución

El proyecto está diseñado siguiendo los principios **FAIR** y está empaquetado con **Docker** para garantizar su reproducibilidad computacional en cualquier sistema operativo sin conflictos de dependencias.

### Paso 1: Levantar el servidor Grobid
Antes de ejecutar el análisis, es necesario tener una instancia de Grobid activa. Abre una terminal y ejecuta:
```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.2
```

### Paso 2: Ejecutar el Pipeline de Análisis
Abre una **nueva terminal** en la raíz de este repositorio y sigue estos dos pasos:

**1. Construir la imagen del proyecto:**
```bash
docker build -t rse-pipeline .
```

**2. Ejecutar el contenedor (Elige el comando según tu Sistema Operativo):**

*Para usuarios de Mac / Windows (usando Docker Desktop):*
```bash
docker run --rm -v "${PWD}/results:/app/results" -e GROBID_URL="http://host.docker.internal:8070/api/processFulltextDocument" rse-pipeline
```
*(Nota Windows: Si usas la terminal CMD clásica en lugar de PowerShell o Git Bash, cambia `${PWD}` por `%cd%`)*

*Para usuarios de Linux:*
```bash
docker run --rm --network host -v "$(pwd)/results:/app/results" -e GROBID_URL="http://localhost:8070/api/processFulltextDocument" rse-pipeline
```

Una vez finalizado el proceso, los resultados (`.png`, `.csv` y `.tei.xml`) se generarán automáticamente en tu carpeta local `results/`.

## Validación de Datos
Para asegurar la fiabilidad de los datos y evitar cajas negras, se ha realizado el siguiente proceso de validación sobre el output de Grobid:

1. **Abstracts y Nube de Palabras:** Se validó inspeccionando el documento TEI XML, confirmando que la etiqueta `<abstract>` aísla correctamente el resumen del resto del texto.
2. **Figuras:** Se corroboró manualmente comparando con los PDFs originales que Grobid agrupa tanto figuras como tablas bajo la etiqueta XML `<figure>`.
3. **Enlaces (Regex Fallback):** 
   * *Problema:* Durante la inspección, se detectó que Grobid inyecta un falso positivo en la cabecera `<teiHeader>` (un enlace a su propio repositorio) para todos los documentos. Además, ignora enlaces que se encuentran en el texto plano y notas al pie sin asignarles la etiqueta `<ptr>`.
   * *Solución:* Se restringió la búsqueda estructurada a la etiqueta `<text>` (cuerpo) y se implementó un sistema híbrido con **Expresiones Regulares (`re`)** para escanear el texto plano y cazar las URLs que Grobid falla en parsear.


##Testing e Integración Continua (CI)
Se ha implementado una suite de *Unit Tests* usando `pytest`. Las pruebas no se acoplan a los datos reales. 
Para evitar errores de CI por falta de archivos generados localmente, los tests utilizan *Fixtures* controlados (`tests/test_data/fake_paper.tei.xml`). Esta suite se ejecuta automáticamente en la nube mediante **GitHub Actions** en cada push.

## Documentación y Citación
La documentación de código autogenerada (Docs-as-Code) está alojada en [ReadTheDocs](https://rse-proyecto-final.readthedocs.io/).
Para citar este software como producto de investigación, por favor revise los metadatos en formato legible por máquina (`codemeta.json`), el archivo para humanos `CITATION.cff`, o utilice directamente el DOI proporcionado por Zenodo. Distribuido bajo Licencia MIT.
