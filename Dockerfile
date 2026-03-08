# Usamos una versión de Python "Slim" que es mucho más pequeña
FROM python:3.10-slim

# Evitamos que Python genere archivos basura (.pyc)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalamos las librerías necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Comando para arrancar con Gunicorn (el estándar profesional)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
