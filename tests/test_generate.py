import pytest
import os
import json
import base64
import io
from fastapi.testclient import TestClient
from PyPDF2 import PdfReader
from app.main import app

client = TestClient(app)

# 🔧 Nom du fichier modèle à uploader et à référencer dans le JSON
TEMPLATE_FILENAME = "app_templates_client_template.docx"
TEMPLATE_PATH = os.path.join("app", "templates", TEMPLATE_FILENAME)

# ✅ Données simulées
valid_data = {
    "format": "pdf",
    "template_filename": TEMPLATE_FILENAME,
    "data": {
        "reference": "REF001",
        "lastName": "Ghomsi",
        "firstName": "Emmanuel",
        "email": "emmanuel@surrency.co",
        "nationality": "Camerounaise",
        "birthDate": "1992-06-15",
        "taxResidenceCountry": "Cameroun",
        "monthlyIncome": 250000,
        "incomeCurrency": "FCFA"
    }
}

@pytest.mark.skipif(not os.path.exists(TEMPLATE_PATH), reason="Fichier template non trouvé.")
def test_generate_valid_pdf():
    with open(TEMPLATE_PATH, "rb") as template_file:
        response = client.post(
            "/api/v1/generate",
            files={
                "file": (TEMPLATE_FILENAME, template_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            },
            data={
                "options": json.dumps(valid_data)
            }
        )

    assert response.status_code == 200
    result = response.json()
    assert result["filename"].endswith(".pdf")
    assert "content_base64" in result
    assert result["message"].startswith("Fichier généré avec succès")


def test_generate_invalid_file_format():
    with open(__file__, "rb") as fake_file:
        response = client.post(
            "/api/v1/generate",
            files={
                "file": ("fake.txt", fake_file, "text/plain")
            },
            data={
                "options": json.dumps(valid_data)
            }
        )
    assert response.status_code == 422
    assert response.json()["detail"] == "Le fichier doit être au format .docx"


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.skipif(not os.path.exists(TEMPLATE_PATH), reason="Fichier template non trouvé.")
def test_generated_pdf_is_valid():
    with open(TEMPLATE_PATH, "rb") as template_file:
        response = client.post(
            "/api/v1/generate",
            files={
                "file": (TEMPLATE_FILENAME, template_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            },
            data={
                "options": json.dumps(valid_data)
            }
        )

    assert response.status_code == 200
    content = response.json()["content_base64"]
    pdf_bytes = base64.b64decode(content)
    reader = PdfReader(io.BytesIO(pdf_bytes))

    # ✅ Vérifie que le PDF a au moins une page
    assert len(reader.pages) > 0