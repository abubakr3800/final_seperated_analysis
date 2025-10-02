"""
Minimal API server to test basic functionality
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="Minimal Compliance API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Minimal API is running", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Minimal API is working"
    }

@app.post("/test-upload")
async def test_upload(file: UploadFile = File(...)):
    """Test file upload"""
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": file.size if hasattr(file, 'size') else 'unknown',
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🚀 Starting Minimal API Server...")
    print("=" * 40)
    print("📋 Endpoints:")
    print("  GET  /           - Root endpoint")
    print("  GET  /health     - Health check")
    print("  POST /test-upload - Test file upload")
    print("=" * 40)
    print("🌐 Server will start on http://localhost:8000")
    print("=" * 40)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
