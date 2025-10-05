"""
Advanced API Server for PDF Report Extraction
============================================

A Flask-based API that accepts PDF file uploads and returns extracted JSON data using
the comprehensive Final PDF Extractor with alias mapping for improved field recognition.

Features:
- Uses Final PDF Extractor with alias-based parameter mapping
- Enhanced room layout extraction with 3D coordinates
- Comprehensive metadata, lighting setup, luminaire, and scene extraction
- Robust error handling and fallback mechanisms
- Automatic cleanup of temporary files

This API provides the most complete extraction capabilities for lighting analysis reports.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from extractors.final_extractor import FinalPDFExtractor
import uuid
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Enable CORS for all routes
CORS(app)

# Configuration
UPLOAD_FOLDER = 'api_uploads'
OUTPUT_FOLDER = 'api_outputs'
ALLOWED_EXTENSIONS = {'pdf'}

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize the Final PDF Extractor with alias mapping
try:
    extractor = FinalPDFExtractor("aliases.json")
    print("✓ Final PDF Extractor initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize Final PDF Extractor: {e}")
    print("Falling back to enhanced parser...")
    from extractors.enhanced_parser import process_report
    extractor = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename):
    """Generate unique filename to avoid conflicts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}_{unique_id}{ext}"


@app.route('/', methods=['GET'])
def home():
    """API home page with usage instructions"""
    return jsonify({
        "message": "Advanced PDF Report Extraction API",
        "version": "2.0",
        "extractor": "Final PDF Extractor with Alias Mapping",
        "features": [
            "Enhanced room layout extraction with 3D coordinates",
            "Alias-based parameter mapping for flexible field recognition",
            "Comprehensive metadata and lighting setup extraction",
            "Advanced luminaire and scene data processing",
            "Robust error handling and fallback mechanisms"
        ],
        "endpoints": {
            "POST /extract": "Upload PDF file and get extracted JSON data",
            "GET /health": "Check API health status",
            "GET /files": "List processed files",
            "GET /download/<file_id>": "Download extracted JSON file"
        },
        "usage": {
            "upload": "POST /extract with 'file' field containing PDF",
            "response": "Returns extracted JSON data and file_id for download",
            "extractor": "Uses Final PDF Extractor with alias mapping for best results"
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "extractor": "Final PDF Extractor with Alias Mapping",
        "version": "2.0",
        "features": [
            "Enhanced room layout extraction",
            "Alias-based parameter mapping",
            "Comprehensive data extraction",
            "Robust error handling"
        ]
    })


@app.route('/extract', methods=['POST'])
def extract_pdf():
    """Extract data from uploaded PDF file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided",
                "message": "Please upload a PDF file using the 'file' field"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "error": "No file selected",
                "message": "Please select a PDF file to upload"
            }), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Invalid file type",
                "message": "Only PDF files are allowed"
            }), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        
        # Save uploaded file
        upload_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(upload_path)
        
        # Extract data from PDF using Final PDF Extractor
        print(f"Processing uploaded file: {unique_filename}")
        
        if extractor:
            # Use Final PDF Extractor (preferred method)
            print("Using Final PDF Extractor with alias mapping...")
            result = extractor.process_report(upload_path)
        else:
            # Fallback to enhanced parser
            print("Using enhanced parser fallback...")
            result = process_report(upload_path)
        
        # Generate output filename
        output_filename = f"{os.path.splitext(unique_filename)[0]}_extracted.json"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Save extracted data
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        
        # Generate file ID for download
        file_id = os.path.splitext(output_filename)[0]
        
        # Clean up uploaded file
        os.remove(upload_path)
        
        # Return success response
        from flask import Response

        # Optional cleanup
        if "_debug" in result:
            del result["_debug"]

        response_data = {
            "success": True,
            "message": "PDF processed successfully",
            "file_id": file_id,
            "original_filename": original_filename,
            "extracted_data": result,
            "download_url": f"/download/{file_id}",
            "timestamp": datetime.now().isoformat()
        }

        # ✅ Force UTF-8 and full JSON content
        return Response(
            json.dumps(response_data, indent=4, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )
        
    except Exception as e:
        # Clean up uploaded file if it exists
        if 'upload_path' in locals() and os.path.exists(upload_path):
            os.remove(upload_path)
        
        return jsonify({
            "error": "Processing failed",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/files', methods=['GET'])
def list_files():
    """List all processed files"""
    try:
        files = []
        for filename in os.listdir(OUTPUT_FOLDER):
            if filename.endswith('_extracted.json'):
                file_path = os.path.join(OUTPUT_FOLDER, filename)
                file_stat = os.stat(file_path)
                file_id = os.path.splitext(filename)[0]
                
                files.append({
                    "file_id": file_id,
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "download_url": f"/download/{file_id}"
                })
        
        return jsonify({
            "success": True,
            "files": files,
            "count": len(files)
        })
        
    except Exception as e:
        return jsonify({
            "error": "Failed to list files",
            "message": str(e)
        }), 500


@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Download extracted JSON file"""
    try:
        filename = f"{file_id}_extracted.json"
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                "error": "File not found",
                "message": f"No file found with ID: {file_id}"
            }), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({
            "error": "Download failed",
            "message": str(e)
        }), 500


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        "error": "File too large",
        "message": "File size exceeds 100MB limit"
    }), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint was not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    print("Starting Advanced PDF Report Extraction API Server...")
    print("=" * 60)
    print("Extractor: Final PDF Extractor with Alias Mapping")
    print("Version: 2.0")
    print("=" * 60)
    print("API Endpoints:")
    print("  GET  /           - API documentation")
    print("  GET  /health     - Health check")
    print("  POST /extract    - Upload PDF and extract data")
    print("  GET  /files      - List processed files")
    print("  GET  /download/<file_id> - Download extracted JSON")
    print("=" * 60)
    print("Features:")
    print("  ✓ Enhanced room layout extraction with 3D coordinates")
    print("  ✓ Alias-based parameter mapping for flexible field recognition")
    print("  ✓ Comprehensive metadata and lighting setup extraction")
    print("  ✓ Advanced luminaire and scene data processing")
    print("  ✓ Robust error handling and fallback mechanisms")
    print("=" * 60)
    print("Server will start on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
