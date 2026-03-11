import os
import requests

def process_pdfs_with_grobid(data_dir="data", output_dir="results/tei"):
    """
    Envía todos los PDFs de un directorio local a la API de Grobid
    y guarda la respuesta en formato TEI XML.
    """
    # 1. Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. La URL de nuestro servidor local de Grobid (configurable por variables de entorno)
    url = os.getenv("GROBID_URL", "http://localhost:8070/api/processFulltextDocument")
    
    # 3. Recorrer todos los archivos de la carpeta de datos
    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(data_dir, filename)
            # Cambiamos la extensión .pdf por .tei.xml para el archivo de salida
            xml_filename = filename.replace(".pdf", ".tei.xml")
            xml_path = os.path.join(output_dir, xml_filename)
            
            # Si el XML ya existe, nos lo saltamos para ahorrar tiempo
            if os.path.exists(xml_path):
                print(f"{filename} ya procesado. Saltando...")
                continue
                
            print(f"Procesando {filename} con Grobid...")
            
            # 4. Abrir el PDF en modo binario ('rb') y enviarlo a la API
            with open(pdf_path, 'rb') as f:
                # Preparamos el archivo para la petición HTTP POST
                files = {'input': (filename, f, 'application/pdf')}
                # Le pedimos a Grobid que no pierda tiempo consolidando datos externos
                data = {'consolidateHeader': '0', 'consolidateCitations': '0'}
                
                try:
                    # Hacemos la llamada al motor de Grobid
                    response = requests.post(url, files=files, data=data)
                    
                    # 5. Comprobar si la petición fue un éxito (Código 200 = OK)
                    if response.status_code == 200:
                        # Guardar la respuesta XML en nuestro ordenador
                        with open(xml_path, 'w', encoding='utf-8') as xml_file:
                            xml_file.write(response.text)
                        print(f"Éxito: Guardado en {xml_path}")
                    else:
                        print(f"Error al procesar {filename}: Código HTTP {response.status_code}")
                
                except requests.exceptions.ConnectionError:
                    print("ERROR: No se puede conectar a Grobid.")
                    return

if __name__ == "__main__":
    # Si ejecutamos este script directamente, llamamos a la función
    print("Iniciando extracción de XMLs...")
    process_pdfs_with_grobid()
    print("¡Proceso terminado!")