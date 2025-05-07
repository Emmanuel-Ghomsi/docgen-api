# Document Generation Service

Microservice RESTful permettant de :

- Remplir un document `.docx` à partir de données JSON,
- Générer un document `.pdf` ou `.xlsx`,
- Télécharger les fichiers générés.

## 🛠️ Stack technique

- FastAPI (Python 3.11+)
- docxtpl (pour .docx)
- libreoffice (PDF/Excel conversion)
- Docker + Docker Compose

## 🚀 Lancer le service

```bash
docker-compose up --build
```

Accéder à la documentation : http://localhost:8000/docs

## 📦 À venir

- Authentification via token (optionnel)
- Gestion de modèles centralisés