import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException
from Backend.services.docx_reader import read_docx
# Bu import satırını değiştirin:
from Backend.services.data_validator import find_best_match  # İmport et, tanımlama

router = APIRouter(prefix="/docx", tags=["DOCX"])

@router.post("/read")
async def read_uploaded_docx(file: UploadFile = File(...)):
    """
    Kullanıcının yüklediği .docx dosyasını okur ve JSON verisi döndürür.
    """
    try:
        content = await file.read()
        docx_data = read_docx(content)
        
        print(f"\n✅ API İstek Başarılı! JSON Verisi: {docx_data}")  # Log ekle
        return {"parsed_data": docx_data}
    
    except Exception as e:
        error_message = f"DOCX okuma hatası: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    
# Bu fonksiyonu kaldırın, zaten data_validator.py'de var
# def find_best_match(key, choices, threshold=60):  
#    """İsim benzerliği olan keyleri eşleştiriyor"""
#    best_match, score = process.extractOne(key, choices, scorer=fuzz.token_sort_ratio)
#    return best_match if score >= threshold else None