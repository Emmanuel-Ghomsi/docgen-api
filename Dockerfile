FROM python:3.11-slim

# Installation de LibreOffice et utilitaires nécessaires
RUN apt-get update && apt-get install -y \
    libreoffice \
    unoconv \
    fonts-dejavu \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers
COPY . .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port API
EXPOSE 8000

# Commande de lancement de l’API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]