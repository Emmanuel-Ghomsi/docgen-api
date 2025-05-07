import os
import shutil
import base64
from datetime import datetime
from typing import Optional
from fastapi import UploadFile

from app.core.config import settings

def save_uploaded_file(uploaded_file: UploadFile, destination_dir: str) -> str:
    os.makedirs(destination_dir, exist_ok=True)
    filename = os.path.basename(uploaded_file.filename)
    destination_path = os.path.join(destination_dir, filename)

    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
        
    return destination_path


def encode_file_to_base64(file_path: str) -> str:
    """
    Encode le contenu d'un fichier en base64.
    """
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_output_filename(prefix: str, extension: str) -> str:
    """
    Génère un nom de fichier avec timestamp, ex : clientfile_20240505_125000.pdf
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def get_template_path(template_filename: str) -> str:
    """
    Retourne le chemin absolu vers le modèle .docx.
    """
    return os.path.join(settings.TEMPLATE_DIR, template_filename)

def remove_files(paths: list[str]) -> None:
    for path in paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass