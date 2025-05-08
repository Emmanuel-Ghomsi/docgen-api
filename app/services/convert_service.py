import os
import tempfile
import subprocess
from typing import Literal

class ConvertServiceError(Exception):
    """Exception personnalisée pour les erreurs de conversion."""
    pass

class ConvertService:
    @staticmethod
    def convert(input_path: str, output_format: Literal["pdf", "docx", "xlsx"]) -> str:
        """
        Convertit un fichier DOCX en PDF/DOCX/XLSX.
        Utilise `soffice` sur Windows et `unoconv` sur Linux.
        """
        try:
            output_dir = tempfile.mkdtemp()
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.{output_format}")

            command = [
                "soffice",
                "--headless",
                "--convert-to", output_format,
                "--outdir", output_dir,
                input_path
            ]

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            if not os.path.exists(output_path):
                raise ConvertServiceError(
                    f"Le fichier converti est introuvable : {output_path}\nCommande : {' '.join(command)}"
                )

            return output_path

        except FileNotFoundError:
            raise ConvertServiceError(
                "LibreOffice (soffice) n'est pas installé ou accessible via PATH.\n"
                "Assure-toi d'avoir installé LibreOffice, puis ajoute le dossier `program/` dans le PATH."
            )

        except subprocess.CalledProcessError as e:
            raise ConvertServiceError(
                f"Erreur lors de la conversion avec soffice :\n"
                f"{e.stderr.decode().strip() if e.stderr else str(e)}"
            )
