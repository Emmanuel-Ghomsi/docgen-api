from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.v1.endpoints import generate
from app.core.config import settings

app = FastAPI(
    title="Document Generator API",
    description="Service RESTful pour remplir des modèles Word et les convertir (PDF, DOCX, XLSX)",
    version="1.0.0"
)

# Middleware CORS (si usage frontal prévu)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(generate.router, prefix=settings.API_PREFIX, tags=["Génération de documents"])

# Personnalisation éventuelle du schéma OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi