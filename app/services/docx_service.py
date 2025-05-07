import os
import tempfile
from docxtpl import DocxTemplate

class DocxServiceError(Exception):
    """Exception personnalisée pour les erreurs liées au traitement de fichiers DOCX."""
    pass

class DocxService:
    @staticmethod
    def fill_template(template_path: str, context: dict) -> str:
        """
        Remplit un fichier Word (.docx) avec les données du contexte.
        Retourne le chemin du fichier temporaire généré.
        """
        try:
            doc = DocxTemplate(template_path)
            doc.render(context)

            fd, output_path = tempfile.mkstemp(suffix=".docx")
            os.close(fd)
            doc.save(output_path)

            return output_path
        except Exception as e:
            raise DocxServiceError(f"Erreur lors du remplissage du modèle : {str(e)}")