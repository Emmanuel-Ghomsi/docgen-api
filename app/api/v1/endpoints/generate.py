from fastapi import APIRouter, UploadFile, Form, File, HTTPException, status
from fastapi.responses import FileResponse
from app.schemas.generate_schema import GenerateRequest, GenerateResponse
from app.services.docx_service import DocxService, DocxServiceError
from app.services.convert_service import ConvertService, ConvertServiceError
from app.utils.file_utils import save_uploaded_file, get_template_path, remove_files
from app.core.config import settings
import os
import base64
import uuid
import json

router = APIRouter()

@router.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Générer un document à partir d’un modèle Word et lancer le téléchargement",
    description="""
    Remplit un modèle Word avec les données fournies et retourne un fichier converti en PDF, DOCX ou XLSX.
    
    **Étapes :**
    1. Envoi du template `.docx`
    2. Remplissage avec les données JSON
    3. Conversion dans le format souhaité
    4. Téléchargement du fichier
    """,
    response_description="Fichier généré avec succès",
    status_code=status.HTTP_200_OK,
)
async def generate_document(
    file: UploadFile = File(..., description="Fichier Word modèle (.docx)"),
    options: str = Form(..., description="Paramètres : format, données, nom du fichier modèle")
):
    # Vérifie l’extension
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=422, detail="Le fichier doit être au format .docx")
    
    # Parse manuellement le JSON
    try:
        options_obj = GenerateRequest(**json.loads(options))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur dans les paramètres JSON : {str(e)}")
    
    temp_template_path = filled_docx_path = output_path = None

    try:
        # Étape 1 - Sauvegarde du fichier modèle
        temp_template_path = save_uploaded_file(file, settings.TEMPLATE_DIR)

        # ✅ Étape 2 : Récupération du chemin réel vers le modèle enregistré (nom venant du JSON)
        template_path = get_template_path(options_obj.template_filename)

        # ✅ Étape 3 : Remplissage du modèle
        filled_docx_path = DocxService.fill_template(template_path, options_obj.data)

        # ✅ Étape 4 : Conversion
        output_path = ConvertService.convert(filled_docx_path, options_obj.format)

        # ✅ Retourne une réponse de type fichier
        return FileResponse(
            output_path,
            filename=f"{uuid.uuid4()}.{options_obj.format}",
            media_type="application/octet-stream"
        )

    except (DocxServiceError, ConvertServiceError) as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.get("/health", tags=["Monitoring"])
def health_check():
    return {"status": "ok", "message": "Service opérationnel"}