"""
LuxSCale API Server
==================

FastAPI server for generating lighting design reports based on user input.
Creates Dialux-like reports that follow lighting standards.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import uvicorn
import uuid

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator
from compliance_integration import ComplianceIntegration
from standards_lookup import StandardsLookup

# Initialize FastAPI app
app = FastAPI(
    title="LuxSCale API",
    description="API for generating lighting design reports",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BASE_DIR = Path(__file__).parent.parent
STANDARDS_PATH = BASE_DIR / "standard_export" / "output" / "standards_filtered.json"
REPORT_API_URL = "http://localhost:5000"  # For compliance checking

# Initialize components
try:
    standards_lookup = StandardsLookup(str(STANDARDS_PATH))
    report_generator = ReportGenerator(str(STANDARDS_PATH))
    compliance_integration = ComplianceIntegration(str(STANDARDS_PATH), REPORT_API_URL)
    print(f"✅ LuxSCale API initialized successfully")
    print(f"📁 Standards loaded from: {STANDARDS_PATH}")
except Exception as e:
    print(f"❌ Error initializing LuxSCale API: {e}")
    standards_lookup = None
    report_generator = None
    compliance_integration = None

# Storage for generated reports (in production, use a database)
REPORTS_STORAGE = Path(__file__).parent / "reports"
REPORTS_STORAGE.mkdir(exist_ok=True)

# Request Models
class LightingDesignRequest(BaseModel):
    project_name: str = Field(..., description="Project name")
    company_name: Optional[str] = Field(None, description="Company name")
    room_type: str = Field(..., description="Room type / Utilisation profile")
    room_length: float = Field(..., gt=0, description="Room length in meters")
    room_width: float = Field(..., gt=0, description="Room width in meters")
    room_height: float = Field(..., gt=0, description="Room height in meters")
    luminaire_count: int = Field(..., gt=0, description="Number of luminaires")
    luminaire_power: float = Field(..., gt=0, description="Luminaire power in watts")
    luminous_flux: Optional[float] = Field(None, ge=0, description="Luminous flux in lumens")
    efficacy: Optional[float] = Field(None, ge=0, description="Efficacy in lm/W")
    mounting_height: float = Field(..., gt=0, description="Mounting height in meters")
    work_plane_height: float = Field(0.75, ge=0, description="Work plane height in meters")
    manufacturer: Optional[str] = Field(None, description="Manufacturer name")
    article_no: Optional[str] = Field(None, description="Article/model number")

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "LuxSCale API - Lighting Design Report Generator",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "GET /get-standard-requirements": "Get standard requirements for room type",
            "POST /generate-report": "Generate lighting design report",
            "GET /download-report/{report_id}": "Download generated report",
            "GET /health": "Health check"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    status = "healthy" if report_generator and compliance_integration else "unhealthy"
    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "standards_lookup": "ready" if standards_lookup else "error",
            "report_generator": "ready" if report_generator else "error",
            "compliance_integration": "ready" if compliance_integration else "error"
        }
    }

@app.get("/get-standard-requirements")
async def get_standard_requirements(room_type: str):
    """
    Get standard requirements for a specific room type.
    
    Args:
        room_type: Room type / utilisation profile
        
    Returns:
        Standard requirements including required lux, uniformity, Ra, etc.
    """
    if not standards_lookup:
        raise HTTPException(status_code=500, detail="Standards lookup not initialized")
    
    try:
        requirements = standards_lookup.get_required_parameters(room_type)
        return JSONResponse(content=requirements)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get standard requirements: {str(e)}")

@app.post("/generate-report")
async def generate_report(request: LightingDesignRequest):
    """
    Generate a lighting design report based on user input
    
    This endpoint:
    1. Creates a report structure similar to Dialux
    2. Calculates lighting parameters
    3. Checks compliance against standards
    4. Returns complete report with compliance results
    """
    if not report_generator or not compliance_integration:
        raise HTTPException(status_code=500, detail="Report generator not initialized")
    
    try:
        # Validate input
        if not request.luminous_flux and not request.efficacy:
            raise HTTPException(
                status_code=400, 
                detail="Either luminous_flux or efficacy must be provided"
            )
        
        # Generate report data
        report_data = report_generator.generate_report(request.dict())
        
        # Check compliance
        compliance_result = compliance_integration.check_compliance(report_data)
        
        # Create complete report
        complete_report = {
            "generated_at": datetime.now().isoformat(),
            "report_id": str(uuid.uuid4()),
            "report_data": report_data,
            "compliance_result": compliance_result,
            "input_parameters": request.dict()
        }
        
        # Save report
        report_id = complete_report["report_id"]
        report_file = REPORTS_STORAGE / f"{report_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(complete_report, f, indent=2, ensure_ascii=False)
        
        return JSONResponse(content=complete_report)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.get("/download-report/{report_id}")
async def download_report(report_id: str):
    """Download a generated report by ID"""
    report_file = REPORTS_STORAGE / f"{report_id}.json"
    
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=report_file,
        filename=f"luxscale_report_{report_id}.json",
        media_type="application/json"
    )

if __name__ == "__main__":
    print("🚀 Starting LuxSCale API Server...")
    print("=" * 60)
    print("📋 API Endpoints:")
    print("  GET  /                    - API documentation")
    print("  GET  /health              - Health check")
    print("  GET  /get-standard-requirements - Get standard requirements for room type")
    print("  POST /generate-report    - Generate lighting design report")
    print("  GET  /download-report/{id} - Download report")
    print("=" * 60)
    print("🌐 Server will start on http://localhost:8001")
    print("📖 API docs available at http://localhost:8001/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)

