# Backend/routers/html_router.py
from fastapi import APIRouter
from Backend.services.html_generator import generate_html_from_data

router = APIRouter(prefix="/html", tags=["HTML"])  # Add prefix and tags

@router.post("/generate")
async def generate_html_endpoint(data: dict):
    """
    JSON verisini alır ve HTML olarak kaydeder.
    """
    html_path = generate_html_from_data(data)
    return {"message": "HTML başarıyla oluşturuldu!", "html_path": html_path}