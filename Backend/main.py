import os
from fastapi import FastAPI
from Backend.routers import docx_router, html_router, log_router, pdf_router, word_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docx_router.router)
app.include_router(html_router.router)
app.include_router(log_router.router)
app.include_router(pdf_router.router)
app.include_router(word_router.router)

app.mount("/js", StaticFiles(directory="templates/js"), name="js")

@app.get("/")
def root():
    return {"message": "Eğitim Bilgi Formu Backend Çalışıyor 🚀"}

if __name__ == "__main__":
    import uvicorn

    file_path = input("Lütfen dönüştürmek istediğiniz .docx dosyasının tam yolunu girin: ")

    if os.path.exists(file_path) and file_path.endswith(".docx"):
        print(f"✅ Dosya bulundu: {file_path}")
    else:
        print("❌ Geçersiz dosya yolu! Lütfen doğru bir .docx dosyası girin.")
        exit(1)

    uvicorn.run("Backend.main:app", host="127.0.0.1", port=8001, reload=True)
