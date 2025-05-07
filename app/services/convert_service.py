import os
import platform
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

            if platform.system() == "Windows":
                # Utilise LibreOffice en ligne de commande
                command = [
                    "soffice",
                    "--headless",
                    "--convert-to", output_format,
                    "--outdir", output_dir,
                    input_path
                ]
            else:
                # Utilise unoconv sur Linux
                command = [
                    "unoconv",
                    "-f", output_format,
                    "-o", output_dir,
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
                    f"Le fichier converti est introuvable après la conversion.\nCommande : {' '.join(command)}"
                )

            return output_path

        except FileNotFoundError as e:
            raise ConvertServiceError(
                f"Commande introuvable : {command[0]}\nAssure-toi que le programme est installé et accessible via PATH."
            )

        except subprocess.CalledProcessError as e:
            raise ConvertServiceError(
                f"Erreur lors de l'exécution de la commande : {' '.join(command)}\n"
                f"stderr: {e.stderr.decode().strip() if e.stderr else str(e)}"
            )
