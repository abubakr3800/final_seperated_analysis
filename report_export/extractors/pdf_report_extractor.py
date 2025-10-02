"""
Advanced PDF Report Extractor
============================

A hybrid PDF extraction system that handles both text-based and scanned PDFs.
Follows the recommended pipeline from guide.txt for mixed report processing.

Features:
- Text-based PDF extraction using pdfplumber and PyMuPDF
- OCR fallback for scanned PDFs using pdf2image + pytesseract
- Intelligent field extraction with regex patterns
- Structured JSON output with comprehensive schema
- Error handling and logging
"""

import pdfplumber
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import re
import json
import os
import logging
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Luminaire:
    """Represents a lighting fixture/luminaire"""
    manufacturer: str
    article_no: str
    power_w: float
    luminous_flux_lm: int
    efficacy_lm_per_w: float
    quantity: int


@dataclass
class RoomLayout:
    """Represents room layout coordinates"""
    x_m: float
    y_m: float
    z_m: float


@dataclass
class Room:
    """Represents a room with its layout"""
    name: str
    arrangement: str
    layout: List[RoomLayout]


@dataclass
class Scene:
    """Represents a lighting scene with performance metrics"""
    scene_name: str
    average_lux: int
    min_lux: int
    max_lux: int
    uniformity: float
    utilisation_profile: str


@dataclass
class LightingSetup:
    """Overall lighting system configuration"""
    number_of_fixtures: int
    fixture_type: str
    mounting_height_m: float
    average_lux: int
    uniformity: float
    total_power_w: float
    luminous_efficacy_lm_per_w: float


@dataclass
class Metadata:
    """Report metadata information"""
    company_name: Optional[str] = None
    project_name: Optional[str] = None
    engineer: Optional[str] = None
    email: Optional[str] = None
    report_title: Optional[str] = None


@dataclass
class ReportData:
    """Complete report data structure"""
    metadata: Metadata
    lighting_setup: Optional[LightingSetup] = None
    luminaires: List[Luminaire] = None
    rooms: List[Room] = None
    scenes: List[Scene] = None
    raw_text: str = ""


class PDFReportExtractor:
    """Main class for extracting data from PDF reports"""
    
    def __init__(self):
        self.text_extractors = [
            self._extract_with_pdfplumber,
            self._extract_with_pymupdf
        ]
        
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    logger.info(f"Extracted text from page {page_num + 1} using pdfplumber")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber: {e}")
            return ""
    
    def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF"""
        try:
            text = ""
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
                logger.info(f"Extracted text from page {page_num + 1} using PyMuPDF")
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with PyMuPDF: {e}")
            return ""
    
    def _ocr_pdf(self, pdf_path: str) -> str:
        """Extract text using OCR (pdf2image + pytesseract)"""
        try:
            logger.info("Starting OCR extraction...")
            text = ""
            pages = convert_from_path(pdf_path, dpi=300, grayscale=True)
            
            for page_num, page in enumerate(pages):
                # Preprocess image for better OCR
                page_text = pytesseract.image_to_string(
                    page, 
                    config='--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;()[]{}@#$%&*-+=/\\|<>?!"\'`~^_'
                )
                if page_text:
                    text += page_text + "\n"
                logger.info(f"OCR completed for page {page_num + 1}")
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error during OCR extraction: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace and line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Fix common OCR errors
        text = re.sub(r'[|]', 'I', text)  # Fix pipe character confusion
        text = re.sub(r'[0]', 'O', text)  # Fix zero/O confusion in words
        
        return text.strip()
    
    def _extract_metadata(self, text: str) -> Metadata:
        """Extract metadata fields from text"""
        metadata = Metadata()
        
        # Company name patterns
        company_patterns = [
            r"(?:Company|Short\s*Cicuit|Short\s*Circuit)\s*Name?\s*[:\-]?\s*(.+)",
            r"Company\s*:\s*(.+)",
            r"Short\s*Cicuit\s*Company\s*[:\-]?\s*(.+)"
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                metadata.company_name = match.group(1).strip()
                break
        
        # Project name patterns
        project_patterns = [
            r"(?:Project\s*Name|Lighting\s*study)\s*[:\-]?\s*(.+)",
            r"Project\s*:\s*(.+)",
            r"Lighting\s*study\s*for\s*(.+)"
        ]
        
        for pattern in project_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                metadata.project_name = match.group(1).strip()
                break
        
        # Engineer patterns
        engineer_patterns = [
            r"Eng\.?\s*([A-Za-z\s]+)",
            r"Engineer\s*[:\-]?\s*(.+)",
            r"Prepared\s*by\s*[:\-]?\s*(.+)"
        ]
        
        for pattern in engineer_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                metadata.engineer = match.group(1).strip()
                break
        
        # Email patterns
        email_pattern = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        email_match = re.search(email_pattern, text)
        if email_match:
            metadata.email = email_match.group(1)
        
        return metadata
    
    def _extract_lighting_setup(self, text: str) -> Optional[LightingSetup]:
        """Extract lighting setup information"""
        try:
            # Number of fixtures
            fixtures_match = re.search(r"(\d+)\s*(?:fixtures?|luminaires?)", text, re.IGNORECASE)
            number_of_fixtures = int(fixtures_match.group(1)) if fixtures_match else 0
            
            # Fixture type
            fixture_type_match = re.search(r"(HighBay\s*\d+\s*watt?|LED\s*\d+\s*watt?)", text, re.IGNORECASE)
            fixture_type = fixture_type_match.group(1) if fixture_type_match else "Unknown"
            
            # Mounting height
            height_match = re.search(r"(\d+\.?\d*)\s*m(?:ounting)?\s*height", text, re.IGNORECASE)
            mounting_height = float(height_match.group(1)) if height_match else 0.0
            
            # Average lux
            avg_lux_match = re.search(r"average\s*lux[:\-]?\s*(\d+)", text, re.IGNORECASE)
            average_lux = int(avg_lux_match.group(1)) if avg_lux_match else 0
            
            # Uniformity
            uniformity_match = re.search(r"uniformity[:\-]?\s*(\d+\.?\d*)", text, re.IGNORECASE)
            uniformity = float(uniformity_match.group(1)) if uniformity_match else 0.0
            
            # Total power
            power_match = re.search(r"total\s*power[:\-]?\s*(\d+\.?\d*)\s*w", text, re.IGNORECASE)
            total_power = float(power_match.group(1)) if power_match else 0.0
            
            # Efficacy
            efficacy_match = re.search(r"efficacy[:\-]?\s*(\d+\.?\d*)\s*lm/w", text, re.IGNORECASE)
            efficacy = float(efficacy_match.group(1)) if efficacy_match else 0.0
            
            return LightingSetup(
                number_of_fixtures=number_of_fixtures,
                fixture_type=fixture_type,
                mounting_height_m=mounting_height,
                average_lux=average_lux,
                uniformity=uniformity,
                total_power_w=total_power,
                luminous_efficacy_lm_per_w=efficacy
            )
        except Exception as e:
            logger.error(f"Error extracting lighting setup: {e}")
            return None
    
    def _extract_luminaires(self, text: str) -> List[Luminaire]:
        """Extract luminaire information"""
        luminaires = []
        
        try:
            # Manufacturer
            manufacturer_match = re.search(r"manufacturer[:\-]?\s*([A-Za-z]+)", text, re.IGNORECASE)
            manufacturer = manufacturer_match.group(1) if manufacturer_match else "Unknown"
            
            # Article number
            article_match = re.search(r"article\s*no[:\-]?\s*([A-Z0-9\s]+)", text, re.IGNORECASE)
            article_no = article_match.group(1).strip() if article_match else "Unknown"
            
            # Power
            power_match = re.search(r"(\d+\.?\d*)\s*w(?:att)?", text, re.IGNORECASE)
            power = float(power_match.group(1)) if power_match else 0.0
            
            # Luminous flux
            flux_match = re.search(r"(\d+)\s*lm", text, re.IGNORECASE)
            flux = int(flux_match.group(1)) if flux_match else 0
            
            # Efficacy
            efficacy_match = re.search(r"(\d+\.?\d*)\s*lm/w", text, re.IGNORECASE)
            efficacy = float(efficacy_match.group(1)) if efficacy_match else 0.0
            
            # Quantity
            quantity_match = re.search(r"quantity[:\-]?\s*(\d+)", text, re.IGNORECASE)
            quantity = int(quantity_match.group(1)) if quantity_match else 1
            
            if manufacturer != "Unknown" or power > 0:
                luminaires.append(Luminaire(
                    manufacturer=manufacturer,
                    article_no=article_no,
                    power_w=power,
                    luminous_flux_lm=flux,
                    efficacy_lm_per_w=efficacy,
                    quantity=quantity
                ))
        except Exception as e:
            logger.error(f"Error extracting luminaires: {e}")
        
        return luminaires
    
    def _extract_rooms(self, text: str) -> List[Room]:
        """Extract room information"""
        rooms = []
        
        try:
            # Room name patterns
            room_patterns = [
                r"Building\s*\d+\s*·\s*Storey\s*\d+\s*·\s*Room\s*\d+",
                r"Room\s*\d+",
                r"Building\s*\d+\s*Storey\s*\d+\s*Room\s*\d+"
            ]
            
            for pattern in room_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Extract coordinates (simplified pattern)
                    coord_pattern = r"(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)"
                    coords = re.findall(coord_pattern, text)
                    
                    layout = []
                    for coord in coords:
                        layout.append(RoomLayout(
                            x_m=float(coord[0]),
                            y_m=float(coord[1]),
                            z_m=float(coord[2])
                        ))
                    
                    rooms.append(Room(
                        name=match,
                        arrangement="A1",  # Default arrangement
                        layout=layout
                    ))
        except Exception as e:
            logger.error(f"Error extracting rooms: {e}")
        
        return rooms
    
    def _extract_scenes(self, text: str) -> List[Scene]:
        """Extract scene information"""
        scenes = []
        
        try:
            # Scene name patterns
            scene_patterns = [
                r"scene\s*name[:\-]?\s*(.+)",
                r"the\s*factory",
                r"working\s*place"
            ]
            
            for pattern in scene_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    scene_name = match.strip() if isinstance(match, str) else "Unknown Scene"
                    
                    # Extract scene metrics (simplified)
                    avg_lux_match = re.search(r"average\s*lux[:\-]?\s*(\d+)", text, re.IGNORECASE)
                    min_lux_match = re.search(r"min\s*lux[:\-]?\s*(\d+)", text, re.IGNORECASE)
                    max_lux_match = re.search(r"max\s*lux[:\-]?\s*(\d+)", text, re.IGNORECASE)
                    uniformity_match = re.search(r"uniformity[:\-]?\s*(\d+\.?\d*)", text, re.IGNORECASE)
                    
                    scenes.append(Scene(
                        scene_name=scene_name,
                        average_lux=int(avg_lux_match.group(1)) if avg_lux_match else 0,
                        min_lux=int(min_lux_match.group(1)) if min_lux_match else 0,
                        max_lux=int(max_lux_match.group(1)) if max_lux_match else 0,
                        uniformity=float(uniformity_match.group(1)) if uniformity_match else 0.0,
                        utilisation_profile="Health care premises - Operating areas (5.46.1 Pre-op and recovery rooms)"
                    ))
        except Exception as e:
            logger.error(f"Error extracting scenes: {e}")
        
        return scenes
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF using multiple methods"""
        logger.info(f"Starting text extraction from: {pdf_path}")
        
        # Try text-based extraction first
        for extractor in self.text_extractors:
            text = extractor(pdf_path)
            if text and len(text) > 50:  # Minimum text threshold
                logger.info(f"Successfully extracted text using {extractor.__name__}")
                return self._clean_text(text)
        
        # Fall back to OCR if text extraction fails
        logger.info("Text extraction failed, falling back to OCR...")
        ocr_text = self._ocr_pdf(pdf_path)
        if ocr_text:
            logger.info("OCR extraction successful")
            return self._clean_text(ocr_text)
        
        logger.warning("All extraction methods failed")
        return ""
    
    def process_report(self, pdf_path: str) -> ReportData:
        """Process a PDF report and extract all relevant data"""
        logger.info(f"Processing report: {pdf_path}")
        
        # Extract text
        text = self.extract_text(pdf_path)
        if not text:
            logger.error("No text could be extracted from the PDF")
            return ReportData(metadata=Metadata(), raw_text="")
        
        # Extract metadata
        metadata = self._extract_metadata(text)
        
        # Extract lighting setup
        lighting_setup = self._extract_lighting_setup(text)
        
        # Extract luminaires
        luminaires = self._extract_luminaires(text)
        
        # Extract rooms
        rooms = self._extract_rooms(text)
        
        # Extract scenes
        scenes = self._extract_scenes(text)
        
        # Create report data
        report_data = ReportData(
            metadata=metadata,
            lighting_setup=lighting_setup,
            luminaires=luminaires,
            rooms=rooms,
            scenes=scenes,
            raw_text=text
        )
        
        logger.info("Report processing completed successfully")
        return report_data
    
    def save_to_json(self, report_data: ReportData, output_path: str = "report_extracted.json"):
        """Save extracted report data to JSON file"""
        try:
            # Convert dataclasses to dictionaries
            data_dict = asdict(report_data)
            
            # Remove raw_text from output (too large for JSON)
            if 'raw_text' in data_dict:
                del data_dict['raw_text']
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Report data saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


def main():
    """Main function to demonstrate usage"""
    import sys
    
    # Initialize extractor
    extractor = PDFReportExtractor()
    
    # Get PDF path from command line argument or use default
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # pdf_path = "NESSTRA Report With 150 watt.pdf"  # Fixed file path (commented out)
        pdf_path = "NESSTRA Report With 150 watt.pdf"  # Default fallback
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        print("Usage: py pdf_report_extractor.py <pdf_file_path>")
        return
    
    # Extract data
    report_data = extractor.process_report(pdf_path)
    
    # Save to JSON
    extractor.save_to_json(report_data)
    
    # Print summary
    print("\n" + "="*50)
    print("EXTRACTION SUMMARY")
    print("="*50)
    print(f"Company: {report_data.metadata.company_name}")
    print(f"Project: {report_data.metadata.project_name}")
    print(f"Engineer: {report_data.metadata.engineer}")
    print(f"Email: {report_data.metadata.email}")
    
    if report_data.lighting_setup:
        print(f"Fixtures: {report_data.lighting_setup.number_of_fixtures}")
        print(f"Fixture Type: {report_data.lighting_setup.fixture_type}")
        print(f"Average Lux: {report_data.lighting_setup.average_lux}")
        print(f"Uniformity: {report_data.lighting_setup.uniformity}")
    
    print(f"Luminaires: {len(report_data.luminaires)}")
    print(f"Rooms: {len(report_data.rooms)}")
    print(f"Scenes: {len(report_data.scenes)}")
    print("="*50)


if __name__ == "__main__":
    main()
