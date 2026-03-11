import os
import csv
import re
from bs4 import BeautifulSoup

def extract_links_from_tei(tei_dir="results/tei"):
    """
    Recorre los archivos TEI XML y extrae los enlaces (URLs).
    Combina la búsqueda por etiquetas XML (<ptr>, <ref>) con una 
    búsqueda por expresiones regulares sobre el texto plano para mayor robustez.
    """
    all_links =[]
    
    if not os.path.exists(tei_dir):
        print(f"Error: Carpeta {tei_dir} no encontrada.")
        return all_links

    # Expresión regular para cazar enlaces web en texto plano
    url_pattern = re.compile(r'https?://[^\s<>"]+')

    for filename in sorted(os.listdir(tei_dir)):
        if filename.endswith(".tei.xml"):
            filepath = os.path.join(tei_dir, filename)
            paper_name = filename.replace(".tei.xml", "")
            
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "xml")
                
                # Nos limitamos estrictamente al cuerpo del artículo (ignoramos metadatos de Grobid)
                text_body = soup.find("text")
                
                if text_body:
                    unique_urls = set()
                    
                    # --- MÉTODO 1: Búsqueda estructurada (Atributos target) ---
                    tags_with_target = text_body.find_all(['ptr', 'ref'], target=True)
                    for tag in tags_with_target:
                        url = tag['target']
                        if url.startswith("http://") or url.startswith("https://"):
                            unique_urls.add(url)
                            
                    # --- MÉTODO 2: Búsqueda en texto plano (Regex) ---
                    # Extraemos todo el texto limpio del cuerpo del artículo
                    raw_text = text_body.get_text(separator=" ")
                    # Buscamos coincidencias con la expresión regular
                    found_urls = url_pattern.findall(raw_text)
                    
                    for url in found_urls:
                        # Limpiamos signos de puntuación finales que se hayan pegado (ej: "http://link.com.")
                        clean_url = url.rstrip('.,;:)')
                        unique_urls.add(clean_url)
                    
                    # Añadir a la lista final
                    for url in unique_urls:
                        all_links.append({
                            "paper": paper_name,
                            "url": url
                        })
                    
    return all_links

def save_links_to_csv(links_data, output_path="results/extracted_links.csv"):
    if not links_data:
        print("No se han encontrado enlaces para guardar.")
        return
        
    print(f"Guardando {len(links_data)} enlaces encontrados en {output_path}...")
    headers = ["paper", "url"]
    with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(links_data)
    print("Archivo CSV generado exitosamente.")

if __name__ == "__main__":
    print("Buscando URLs (vía tags y regex) en los archivos XML...")
    links = extract_links_from_tei()
    if links:
        save_links_to_csv(links)