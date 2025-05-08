FROM python:3.11-slim

# Installation de LibreOffice (soffice) et dépendances nécessaires
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    fonts-dejavu \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copie du projet
COPY . .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Port exposé
EXPOSE 8000

# Lancement de l'API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]