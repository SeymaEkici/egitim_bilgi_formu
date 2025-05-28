from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from pdf2docx import Converter
import os

router = APIRouter(prefix="/word", tags=["Word"])

@router.post("/convert")
async def convert_pdf_to_word(file: UploadFile = File(...)):
    """
    Kullanıcının yüklediği PDF dosyasını alır ve Word dosyasına çevirir.
    """
    try:
        # 📌 1️⃣ Dosyayı geçici olarak kaydet
        pdf_path = Path(f"temp_{file.filename}")
        with open(pdf_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # 📌 2️⃣ PDF -> Word dönüşümü
        word_path = pdf_path.with_suffix(".docx")
        cv = Converter(str(pdf_path))
        cv.convert(str(word_path), start=0, end=None)
        cv.close()

        # 📌 3️⃣ Geçici PDF dosyasını temizle
        os.remove(pdf_path)

        print(f"✅ PDF'den Word'e dönüşüm tamamlandı: {word_path}")
        return FileResponse(
            path=word_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=word_path.name
        )

    except Exception as e:
        print(f"❌ PDF dönüştürme hatası: {str(e)}")
        raise Exception("PDF dönüştürme sırasında hata oluştu.")