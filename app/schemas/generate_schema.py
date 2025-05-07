from pydantic import BaseModel, Field
from typing import Optional, Literal
from app.core.constants import SUPPORTED_OUTPUT_FORMATS


class GenerateRequest(BaseModel):
    format: Literal["pdf", "docx", "xlsx"] = Field(..., description="Format de sortie souhaité")
    data: dict = Field(..., description="Données à injecter dans le template")
    template_filename: str = Field(..., description="Nom du fichier template .docx fourni (doit se terminer par .docx)")


class GenerateResponse(BaseModel):
    filename: str = Field(..., description="Nom du fichier généré")
    content_base64: Optional[str] = Field(None, description="Contenu du fichier encodé en base64 (si demandé)")
    message: str = Field(..., description="Message de statut")