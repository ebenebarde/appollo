# Wir nutzen ein schlankes Python 3.13 Image
FROM python:3.13-slim

WORKDIR /app

# System-Bibliotheken für PostgreSQL installieren
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python-Pakete installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code kopieren
COPY . .

# Port freigeben
EXPOSE 8000

# Startbefehl: Server auf 0.0.0.0 (für Docker Netzwerk) starten
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]