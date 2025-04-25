# backend_startup.py
# Place this file in your project root directory and run it

import os
import sys
import subprocess
import time

def check_environment():
    """Check if required packages are installed"""
    print("✅ Checking environment...")
    required_packages = ["fastapi", "uvicorn", "python-docx", "thefuzz", "python-multipart", "jinja2", "pdfkit", "pdf2docx"]
    
    # Check and install missing packages
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✓ {package} is installed")
        except ImportError:
            print(f"  ✗ {package} is missing, attempting to install...")
            subprocess.call([sys.executable, "-m", "pip", "install", package])

def fix_backend_structure():
    """Fix common structural issues in the backend"""
    print("\n✅ Fixing backend structure...")
    
    # Ensure __init__.py files exist
    init_paths = [
        "Backend/__init__.py",
        "Backend/routers/__init__.py",
        "Backend/services/__init__.py",
        "Backend/utils/__init__.py"
    ]
    
    for path in init_paths:
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("# Auto-generated __init__.py file")
            print(f"  ✓ Created {path}")
    
    # Fix HTML router
    html_router_path = "Backend/routers/html_router.py"
    if os.path.exists(html_router_path):
        with open(html_router_path, "r") as f:
            content = f.read()
        
        if "prefix=" not in content:
            content = content.replace(
                "router = APIRouter()",
                "router = APIRouter(prefix=\"/html\", tags=[\"HTML\"])"
            )
            
            with open(html_router_path, "w") as f:
                f.write(content)
            print(f"  ✓ Fixed router prefix in {html_router_path}")

def create_main_app():
    """Create a proper main.py in the correct location"""
    print("\n✅ Creating main application entry point...")
    
    main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import all routers
from Backend.routers import docx_router, html_router, log_router, pdf_router, word_router

# Create FastAPI app
app = FastAPI(title="Eğitim Bilgi Formu API")

# Configure CORS - this is critical for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(docx_router.router)
app.include_router(html_router.router)
app.include_router(log_router.router)
app.include_router(pdf_router.router)
app.include_router(word_router.router)

# Mount static files if directory exists
if os.path.exists("templates/js"):
    app.mount("/js", StaticFiles(directory="templates/js"), name="js")

@app.get("/")
def root():
    return {"message": "Eğitim Bilgi Formu Backend Çalışıyor 🚀"}

# Make sure the output directory exists
os.makedirs("output", exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
"""
    
    with open("main.py", "w") as f:
        f.write(main_content)
    print("  ✓ Created main.py in project root")

def start_backend():
    """Start the backend server"""
    print("\n✅ Starting backend server...")
    print("  ⚠️ If the server fails to start, check the errors and fix them")
    print("  ⚠️ Press Ctrl+C to stop the server when done")
    time.sleep(2)
    
    # Start the backend
    subprocess.call([sys.executable, "main.py"])

if __name__ == "__main__":
    print("\n==== BACKEND SETUP AND DIAGNOSTIC TOOL ====\n")
    
    check_environment()
    fix_backend_structure()
    create_main_app()
    
    print("\n✅ Setup complete! Your backend structure has been fixed.")
    print("   Next steps:")
    print("   1. Run 'python main.py' to start the backend")
    print("   2. Access the API docs at http://127.0.0.1:8001/docs")
    print("   3. Run your frontend separately using a simple HTTP server")
    
    choice = input("\nStart the backend now? (y/n): ")
    if choice.lower() == 'y':
        start_backend()