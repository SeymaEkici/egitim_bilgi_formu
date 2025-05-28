from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from Backend.services.pdf_generator import generate_pdf
import os

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.get("/download")
async def download_pdf():
    pdf_path = "output/egitim_bilgileri.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="❌ PDF bulunamadı!")

    return FileResponse(pdf_path, media_type='application/pdf', filename="egitim_bilgileri.pdf")