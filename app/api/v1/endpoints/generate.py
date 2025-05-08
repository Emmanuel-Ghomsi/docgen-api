from fastapi import APIRouter, UploadFile, Form, File, HTTPException, status
from fastapi.responses import FileResponse
from app.schemas.generate_schema import GenerateRequest, GenerateResponse
from app.services.docx_service import DocxService, DocxServiceError
from app.services.convert_service import ConvertService, ConvertServiceError
from app.utils.file_utils import save_uploaded_file, get_template_path, remove_files
from app.core.config import settings
from app.core.logger import logger
import os
import base64
import uuid
import json

router = APIRouter()

@router.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Générer un document à partir d’un modèle Word et le convertir",
    description="""
    Remplit un modèle Word avec les données fournies et retourne un fichier converti en PDF, DOCX ou XLSX.
    
    **Étapes :**
    1. Envoi du template `.docx`
    2. Remplissage avec les données JSON
    3. Conversion dans le format souhaité
    4. Encodage en base64 du fichier (optionnel dans l'avenir)
    """,
    response_description="Fichier généré avec succès",
    status_code=status.HTTP_200_OK,
)
async def generate_document(
    file: UploadFile = File(..., description="Fichier Word modèle (.docx)"),
    options: str = Form(..., description="Paramètres : format, données, nom du fichier modèle")
):
    logger.info(f"✅ Requête reçue - fichier: {file.filename}")
    
    # Vérifie l’extension
    if not file.filename.endswith(".docx"):
        logger.warning("❌ Le fichier n'est pas un .docx")
        raise HTTPException(status_code=422, detail="Le fichier doit être au format .docx")
    
    # Parse manuellement le JSON
    try:
        options_obj = GenerateRequest(**json.loads(options))
        logger.info(f"🧾 Options parsées avec succès : format={options_obj.format}, template={options_obj.template_filename}")
    except Exception as e:
        logger.error(f"❌ Erreur de parsing JSON : {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erreur dans les paramètres JSON : {str(e)}")
    
    temp_template_path = filled_docx_path = output_path = None

    try:
        logger.info("📥 Sauvegarde du fichier template...")
        temp_template_path = save_uploaded_file(file, settings.TEMPLATE_DIR)

        template_path = get_template_path(options_obj.template_filename)
        logger.info(f"📄 Template utilisé : {template_path}")

        logger.info("🧩 Remplissage du template avec les données...")
        filled_docx_path = DocxService.fill_template(template_path, options_obj.data)

        logger.info(f"🔁 Conversion vers le format {options_obj.format.upper()}...")
        output_path = ConvertService.convert(filled_docx_path, options_obj.format)
        logger.info(f"✅ Fichier généré avec succès : {output_path}")

        # ✅ Étape 5 : Encodage base64
        with open(output_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        filename = f"{uuid.uuid4()}.{options_obj.format}"
        logger.info(f"📤 Téléchargement en cours sous le nom : {filename}")

        return GenerateResponse(
            filename=filename,
            content_base64=encoded,
            message=f"Fichier généré avec succès au format {options_obj.format.upper()}."
        )

    except (DocxServiceError, ConvertServiceError) as e:
        logger.error(f"❌ Erreur fonctionnelle : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # ✅ Ne supprime PAS le fichier dans app/templates (il est persistant)
        remove_files([p for p in [filled_docx_path, output_path] if p])
        
@router.post(
    "/generate/download",
    response_model=GenerateResponse,
    summary="Générer un document à partir d’un modèle Word et lance automatiquement le téléchargement",
    description="Remplit un modèle Word avec les données fournies et retourne un fichier converti en PDF, DOCX ou XLSX.",
    response_description="Fichier généré avec succès",
    status_code=status.HTTP_200_OK,
)
async def generate_document_download(
    file: UploadFile = File(..., description="Fichier Word modèle (.docx)"),
    options: str = Form(..., description="Paramètres : format, données, nom du fichier modèle")
):
    logger.info(f"✅ Requête reçue - fichier: {file.filename}")
    
    if not file.filename.endswith(".docx"):
        logger.warning("❌ Le fichier n'est pas un .docx")
        raise HTTPException(status_code=422, detail="Le fichier doit être au format .docx")

    try:
        options_obj = GenerateRequest(**json.loads(options))
        logger.info(f"🧾 Options parsées avec succès : format={options_obj.format}, template={options_obj.template_filename}")
    except Exception as e:
        logger.error(f"❌ Erreur de parsing JSON : {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erreur JSON : {str(e)}")

    temp_template_path = filled_docx_path = output_path = None

    try:
        logger.info("📥 Sauvegarde du fichier template...")
        temp_template_path = save_uploaded_file(file, settings.TEMPLATE_DIR)
        
        template_path = get_template_path(options_obj.template_filename)
        logger.info(f"📄 Template utilisé : {template_path}")

        logger.info("🧩 Remplissage du template avec les données...")
        filled_docx_path = DocxService.fill_template(template_path, options_obj.data)

        logger.info(f"🔁 Conversion vers le format {options_obj.format.upper()}...")
        output_path = ConvertService.convert(filled_docx_path, options_obj.format)
        logger.info(f"✅ Fichier généré avec succès : {output_path}")

        final_filename = f"{uuid.uuid4()}.{options_obj.format}"
        logger.info(f"📤 Téléchargement en cours sous le nom : {final_filename}")

        # ✅ retourne un téléchargement direct
        return FileResponse(
            output_path,
            filename=final_filename,
            media_type="application/octet-stream"
        )

    except (DocxServiceError, ConvertServiceError) as e:
        logger.exception("❌ Erreur inattendue lors de la génération")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", tags=["Monitoring"])
def health_check():
    return {"status": "ok", "message": "Service opérationnel"}