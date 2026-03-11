import os
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_abstracts_from_tei(tei_dir="results/tei"):
    """
    Recorre los archivos TEI XML, extrae el texto de la etiqueta <abstract>
    y devuelve un único string gigante con todos los abstracts combinados.
    """
    all_abstracts = ""
    
    # Verificar que el directorio existe
    if not os.path.exists(tei_dir):
        print(f"Error: No se encuentra la carpeta {tei_dir}. Ejecuta extract_xml.py primero.")
        return all_abstracts

    # Recorrer todos los archivos XML generados por Grobid
    for filename in os.listdir(tei_dir):
        if filename.endswith(".tei.xml"):
            filepath = os.path.join(tei_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                # Usamos BeautifulSoup para parsear el XML y extraer el texto del abstract (requiere tener lxml instalado)
                soup = BeautifulSoup(f, "xml") 
                
                # Buscar la etiqueta <abstract> (Grobid siempre usa esta etiqueta)
                abstract_tag = soup.find("abstract")
                
                if abstract_tag:
                    # Extraer solo el texto limpio, separando por espacios
                    text = abstract_tag.get_text(separator=" ", strip=True)
                    all_abstracts += text + " "
                else:
                    print(f"Aviso: No se encontró abstract en {filename}")
                    
    return all_abstracts

def create_wordcloud(text, output_path="results/abstract_wordcloud.png"):
    """
    Genera y guarda una nube de palabras a partir de un texto dado.
    """
    if not text.strip():
        print("No hay texto para generar la nube de palabras.")
        return

    print("Generando la nube de palabras...")
    
    # Configurar la nube de palabras
    # (wordcloud ya filtra por defecto palabras comunes en inglés como 'the', 'and', 'of'...)
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color="white",
        colormap="viridis",
        max_words=100
    ).generate(text)

    # Usar matplotlib para dibujar la imagen sin mostrar ejes
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off") # Ocultar los ejes X e Y
    
    # Guardar la imagen en alta resolución dentro de la carpeta results
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=300)
    print(f"Nube de palabras guardada exitosamente en: {output_path}")

if __name__ == "__main__":
    print("Buscando abstracts en los archivos XML...")
    combined_text = get_abstracts_from_tei()
    
    # Si hemos encontrado texto, generamos la imagen
    if combined_text:
        create_wordcloud(combined_text)