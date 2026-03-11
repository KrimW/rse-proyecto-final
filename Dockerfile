# Usamos la versión ligera de Python
FROM python:3.13-slim

# VARIABLES DE ENTORNO
# (1) Logs se muestran en tiempo real, (2) Especificamos la versión de Poetry, (3) Para que Poetry instale las dependencias en el entorno global del contenedor, no en uno virtual
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

# Instalamos Poetry en el contenedor
RUN pip install "poetry==$POETRY_VERSION"

# Creamos una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias PRIMERO (para aprovechar la caché de Docker)
COPY pyproject.toml poetry.lock ./

# Instalamos las dependencias (menos las de desarrollo) usando Poetry
RUN poetry install --without dev --no-root

# Copiamos el resto de nuestro código y datos al contenedor
COPY src/ ./src/
COPY data/ ./data/
COPY main.py ./

# Comando por defecto al encender el contenedor
CMD ["python", "main.py"]