"""
API Client for PDF Report Extraction
===================================

Simple client to test the PDF extraction API.
"""

import requests
import json
import os
from pathlib import Path


class PDFExtractionClient:
    """Client for PDF extraction API"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if API is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "API server is not running"}
    
    def extract_pdf(self, pdf_file_path):
        """Extract data from PDF file"""
        try:
            if not os.path.exists(pdf_file_path):
                return {"error": f"File not found: {pdf_file_path}"}
            
            with open(pdf_file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(f"{self.base_url}/extract", files=files)
            
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_files(self):
        """List all processed files"""
        try:
            response = requests.get(f"{self.base_url}/files")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def download_file(self, file_id, save_path=None):
        """Download extracted JSON file"""
        try:
            response = requests.get(f"{self.base_url}/download/{file_id}")
            
            if response.status_code == 200:
                if save_path is None:
                    save_path = f"{file_id}.json"
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                return {"success": True, "saved_to": save_path}
            else:
                return response.json()
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main function to test the API client"""
    client = PDFExtractionClient()
    
    print("PDF Extraction API Client")
    print("=" * 30)
    
    # Check API health
    print("Checking API health...")
    health = client.health_check()
    print(f"Health: {health}")
    
    if "error" in health:
        print("API server is not running. Please start it with:")
        print("py api_server.py")
        return
    
    # Test with a PDF file
    pdf_file = "NESSTRA Report With 150 watt.pdf"
    if os.path.exists(pdf_file):
        print(f"\nExtracting data from: {pdf_file}")
        result = client.extract_pdf(pdf_file)
        
        if "success" in result and result["success"]:
            print("✓ Extraction successful!")
            print(f"File ID: {result['file_id']}")
            print(f"Download URL: {result['download_url']}")
            
            # Show extracted data summary
            data = result["extracted_data"]
            print(f"\nExtracted Data Summary:")
            print(f"  Company: {data['metadata']['company_name']}")
            print(f"  Project: {data['metadata']['project_name']}")
            print(f"  Engineer: {data['metadata']['engineer']}")
            print(f"  Luminaires: {len(data['luminaires'])}")
            print(f"  Rooms: {len(data['rooms'])}")
            print(f"  Scenes: {len(data['scenes'])}")
            
            # Download the file
            print(f"\nDownloading extracted data...")
            download_result = client.download_file(result['file_id'])
            if "success" in download_result:
                print(f"✓ Downloaded to: {download_result['saved_to']}")
        else:
            print(f"✗ Extraction failed: {result}")
    else:
        print(f"PDF file not found: {pdf_file}")
    
    # List all files
    print(f"\nListing all processed files...")
    files = client.list_files()
    if "success" in files and files["success"]:
        print(f"Found {files['count']} processed files:")
        for file_info in files["files"]:
            print(f"  - {file_info['filename']} (ID: {file_info['file_id']})")
    else:
        print(f"Failed to list files: {files}")


if __name__ == "__main__":
    main()
