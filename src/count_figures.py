import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def count_figures_in_tei(tei_dir="results/tei"):
    """
    Recorre los archivos TEI XML y cuenta cuántas etiquetas <figure> hay en cada uno.
    Devuelve un diccionario { "paper_01": 5, "paper_02": 3, ... }
    """
    figure_counts = {}
    
    if not os.path.exists(tei_dir):
        print(f"Error: Carpeta {tei_dir} no encontrada. Ejecuta extract_xml.py primero.")
        return figure_counts

    # Usamos sorted() para que los artículos aparezcan en orden en la gráfica
    for filename in sorted(os.listdir(tei_dir)):
        if filename.endswith(".tei.xml"):
            filepath = os.path.join(tei_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "xml")
                
                # En TEI XML de Grobid, las figuras usan la etiqueta <figure>
                figures = soup.find_all("figure")
                
                # Limpiamos el nombre del archivo para que la etiqueta en el gráfico quede corta
                paper_name = filename.replace(".tei.xml", "")
                figure_counts[paper_name] = len(figures)
                
    return figure_counts

def plot_figure_counts(counts, output_path="results/figure_counts.png"):
    """
    Recibe un diccionario con los conteos y genera un gráfico de barras.
    """
    
    # Separamos el diccionario en dos listas para X y para Y
    papers = list(counts.keys())
    num_figures = list(counts.values())

    plt.figure(figsize=(10, 6))
    
    # Crear un gráfico de barras
    bars = plt.bar(papers, num_figures, color='#4C72B0', edgecolor='black')
    
    # Añadir títulos y etiquetas
    plt.xlabel('Artículos', fontsize=12)
    plt.ylabel('Número de Figuras', fontsize=12)
    plt.title('Cantidad de Figuras detectadas por Artículo', fontsize=14, fontweight='bold')
    
    # Rotar las etiquetas del eje X a 45 grados para que no se pisen entre ellas
    plt.xticks(rotation=45, ha='right')
    
    # Truco Pro: Añadir el número exacto justo encima de cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')

    # Ajustar los márgenes para que no se corte nada
    plt.tight_layout()
    
    # Guardar la imagen
    plt.savefig(output_path, dpi=300)
    print(f"Gráfico guardado exitosamente en: {output_path}")

if __name__ == "__main__":
    print("Contando figuras en los archivos XML...")
    counts = count_figures_in_tei()
    
    if counts:
        plot_figure_counts(counts)