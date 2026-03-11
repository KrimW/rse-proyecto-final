import os
import pytest

# Importamos las funciones que hemos creado en nuestros scripts de la carpeta src
from src.extract_links import extract_links_from_tei
from src.count_figures import count_figures_in_tei
from src.generate_wordcloud import get_abstracts_from_tei


############## TEST 1 - Extracción de enlaces. ######################

def test_extracted_links_are_valid():
    """
    Comprueba que la función devuelve una lista y que las URL son válidas.
    """
    links = extract_links_from_tei(tei_dir="tests/test_data")
    
    # Afirmación 1: El resultado DEBE ser una lista
    assert isinstance(links, list), "El resultado debe ser una estructura de lista"
    
    # Afirmación 2: Cada URL debe empezar por http o https
    if len(links) > 0:
        for item in links:
            url = item["url"]
            assert url.startswith("http://") or url.startswith("https://"), f"URL inválida: {url}"

############## TEST 2 - Conteo de figuras. ######################

def test_figure_counts_format_and_logic():
    """
    Comprueba que el conteo de figuras devuelve un diccionario y 
    que no existen artículos con un número negativo de figuras.
    """
    counts = count_figures_in_tei(tei_dir="tests/test_data")
    
    # Afirmación 1: El resultado DEBE ser un diccionario
    assert isinstance(counts, dict), "El resultado debe ser un diccionario"
    
    # Afirmación 2: Las cantidades deben ser números enteros y mayores o iguales a 0
    for paper_name, num_figures in counts.items():
        assert isinstance(num_figures, int), "El número de figuras debe ser un número entero"
        assert num_figures >= 0, "Un artículo no puede tener figuras negativas"

############## TEST 3 - Extracción de resúmenes. ######################
def test_abstract_extraction_is_not_empty():
    """
    Comprueba que el extractor de abstracts devuelve un string de texto
    y que ha sido capaz de extraer información de los XMLs.
    """
    text = get_abstracts_from_tei(tei_dir="tests/test_data")
    
    # Afirmación 1: Debe devolver un string
    assert isinstance(text, str), "El abstract extraído debe ser texto (string)"
    
    # Afirmación 2: Como le estamos pasando nuestros 10 XMLs reales, el texto NO puede estar vacío
    assert len(text) > 0, "El texto extraído de los abstracts está vacío"