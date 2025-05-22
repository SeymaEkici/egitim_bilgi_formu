import os
from fastapi import FastAPI
from Backend.routers import docx_router, html_router, log_router, pdf_router, word_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Debug logları
print("🚀 Backend uygulaması başlatılıyor...")
print(f"📂 Çalışma dizini: {os.getcwd()}")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları dahil et
print("🔄 Router'lar yükleniyor...")
app.include_router(docx_router.router)
app.include_router(html_router.router)
app.include_router(log_router.router)
app.include_router(pdf_router.router)
app.include_router(word_router.router)

# Static dosyalar
try:
    app.mount("/js", StaticFiles(directory="templates/js"), name="js")
    print("✅ JS klasörü mount edildi")
except Exception as e:
    print(f"❌ JS klasörü mount edilirken hata: {str(e)}")

@app.get("/")
def root():
    return {"message": "Eğitim Bilgi Formu Backend Çalışıyor 🚀"}

if __name__ == "__main__":
    import uvicorn

    print("\n✅ Backend API sunucusu başlatılıyor...")
    uvicorn.run("Backend.main:app", host="127.0.0.1", port=8001, reload=True)