import os
from src.extract_xml import process_pdfs_with_grobid
from src.generate_wordcloud import get_abstracts_from_tei, create_wordcloud
from src.count_figures import count_figures_in_tei, plot_figure_counts
from src.extract_links import extract_links_from_tei, save_links_to_csv

def run_pipeline():
    print("INICIANDO PIPELINE.")
    
    # 1. Extracción
    print("\n 1. Conectando con Grobid.")
    process_pdfs_with_grobid()
    
    # 2. Wordcloud
    print("\n 2. Generando Nube de Palabras.")
    abstracts = get_abstracts_from_tei()
    if abstracts:
        create_wordcloud(abstracts)
        
    # 3. Conteo de figuras
    print("\n 3. Contando figuras.")
    counts = count_figures_in_tei()
    if counts:
        plot_figure_counts(counts)
        
    # 4. Extracción de Enlaces
    print("\n 4. Extrayendo enlaces.")
    links = extract_links_from_tei()
    if links:
        save_links_to_csv(links)
        
    print("\n PIPELINE COMPLETADO. Revisa la carpeta 'results/'.")

if __name__ == "__main__":
    # Crear carpetas necesarias si no existen
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/tei", exist_ok=True)
    
    run_pipeline()