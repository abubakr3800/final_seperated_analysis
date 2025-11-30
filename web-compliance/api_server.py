"""
Final API Server for Lighting Compliance Checking
================================================

This API integrates the report_export and standard_export projects to provide
a complete lighting compliance checking service.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path
import tempfile
import json
from datetime import datetime
import uvicorn

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from compliance_checker import ComplianceChecker

# Initialize FastAPI app
app = FastAPI(
    title="Lighting Compliance Checker API",
    description="API for checking lighting compliance against standards",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration - adjust paths relative to web-compliance folder
BASE_DIR = Path(__file__).parent.parent
STANDARDS_PATH = BASE_DIR / "standard_export" / "output" / "standards_filtered.json"
REPORT_API_URL = "http://localhost:5000"  # report_export API URL

# Initialize compliance checker
try:
    compliance_checker = ComplianceChecker(str(STANDARDS_PATH), REPORT_API_URL)
    print(f"✅ Compliance checker initialized successfully")
    print(f"📁 Standards loaded from: {STANDARDS_PATH}")
    print(f"🔗 Report API URL: {REPORT_API_URL}")
except Exception as e:
    print(f"❌ Error initializing compliance checker: {e}")
    compliance_checker = None

@app.get("/")
async def root():
    """API root endpoint with documentation"""
    return {
        "message": "Lighting Compliance Checker API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "POST /check-compliance": "Upload PDF report and get compliance results",
            "POST /check-compliance-detailed": "Upload PDF and get detailed compliance results with all parameters",
            "GET /health": "Check API health status",
            "GET /standards-info": "Get information about loaded standards",
            "GET /": "API documentation (this endpoint)"
        },
        "usage": {
            "upload": "POST /check-compliance-detailed with 'file' field containing PDF",
            "response": "Returns compliance check results with PASS/FAIL status and all extracted parameters"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    status = "healthy" if compliance_checker else "unhealthy"
    
    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "compliance_checker": "ready" if compliance_checker else "error",
            "standards_loaded": bool(compliance_checker and compliance_checker.standards_data),
            "report_api_available": "unknown"  # Could add actual check here
        }
    }

@app.get("/standards-info")
async def get_standards_info():
    """Get information about loaded standards"""
    if not compliance_checker or not compliance_checker.standards_data:
        raise HTTPException(status_code=500, detail="Standards not loaded")
    
    standards_data = compliance_checker.standards_data
    
    return {
        "total_standards": len(standards_data.get('standards', [])),
        "metadata": standards_data.get('metadata', {}),
        "sample_standards": standards_data.get('standards', [])[:5],  # First 5 standards as sample
        "timestamp": datetime.now().isoformat()
    }

@app.post("/check-compliance")
async def check_compliance(file: UploadFile = File(...)):
    """
    Upload a PDF report and get compliance checking results
    
    Args:
        file: PDF file containing lighting report
        
    Returns:
        Compliance check results with PASS/FAIL status
    """
    if not compliance_checker:
        raise HTTPException(status_code=500, detail="Compliance checker not initialized")
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        try:
            # Save uploaded file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Process the report
            result = compliance_checker.process_report(temp_file.name)
            
            # Add file information
            result['file_info'] = {
                'filename': file.filename,
                'size': len(content),
                'upload_time': datetime.now().isoformat()
            }
            
            return JSONResponse(content=result)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except:
                pass

@app.post("/check-compliance-detailed")
async def check_compliance_detailed(file: UploadFile = File(...)):
    """
    Upload a PDF report and get detailed compliance checking results
    
    This endpoint provides more detailed information including:
    - All extracted parameters from the report
    - Complete compliance check results
    - Room-by-room analysis
    - Full report metadata
    
    Args:
        file: PDF file containing lighting report
        
    Returns:
        Detailed compliance check results with all extracted data
    """
    if not compliance_checker:
        raise HTTPException(status_code=500, detail="Compliance checker not initialized")
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        try:
            # Save uploaded file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Extract report data first
            report_data = compliance_checker.extract_report_data(temp_file.name)
            if not report_data:
                raise HTTPException(status_code=500, detail="Failed to extract report data")
            
            # Check compliance
            compliance_result = compliance_checker.check_compliance(report_data)
            
            # Prepare detailed response with all data
            result = {
                'file_info': {
                    'filename': file.filename,
                    'size': len(content),
                    'upload_time': datetime.now().isoformat()
                },
                'extracted_report_data': report_data,
                'compliance_result': compliance_result,
                'timestamp': datetime.now().isoformat()
            }
            
            return JSONResponse(content=result)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except:
                pass

@app.get("/test-connection")
async def test_connection():
    """Test connection to the report extraction API"""
    try:
        import requests
        response = requests.get(f"{REPORT_API_URL}/health", timeout=5)
        if response.status_code == 200:
            return {
                "status": "connected",
                "report_api_status": response.json(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error",
                "message": f"Report API returned status {response.status_code}",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to connect to report API: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/proxy/report-health")
async def proxy_report_health():
    """Proxy endpoint to check report API health (CORS-friendly)"""
    try:
        import requests
        response = requests.get(f"{REPORT_API_URL}/health", timeout=5)
        if response.status_code == 200:
            return JSONResponse(content={
                "status": "healthy",
                "report_api": response.json(),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return JSONResponse(content={
                "status": "error",
                "message": f"Report API returned status {response.status_code}",
                "timestamp": datetime.now().isoformat()
            }, status_code=500)
    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "message": f"Failed to connect to report API: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }, status_code=500)

if __name__ == "__main__":
    print("🚀 Starting Lighting Compliance Checker API (Web-Compliance)...")
    print("=" * 60)
    print("📋 API Endpoints:")
    print("  GET  /                    - API documentation")
    print("  GET  /health              - Health check")
    print("  GET  /standards-info      - Standards information")
    print("  POST /check-compliance    - Upload PDF and get compliance results")
    print("  POST /check-compliance-detailed - Detailed compliance results with all parameters")
    print("  GET  /test-connection     - Test report API connection")
    print("=" * 60)
    print("🌐 Server will start on http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

