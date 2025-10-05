"""
Final PDF Extractor
==================

Comprehensive PDF extractor that combines the best features from all previous
extractors. This extractor includes advanced room layout extraction, alias
mapping for better field recognition, and robust error handling.

This extractor is designed for production use and provides the most complete
extraction capabilities for lighting analysis reports.

Author: PDF Report Extractor Team
Version: 1.0
"""

import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import re
import json
import os
from typing import Dict, Any
import sys
    

# class FinalPDFExtractor:
#     """Final PDF extractor combining all approaches"""

#     def __init__(self, alias_file: str = "extractors/aliases.json"):
#         self.text_extractors = [
#             self._extract_with_pdfplumber,
#             self._extract_with_pymupdf
#         ]
#         # Load alias map
#         with open(alias_file, "r", encoding="utf-8") as f:
#             self.aliases = json.load(f)

class FinalPDFExtractor:
    """
    Final PDF extractor combining all approaches and features.
    
    This is the most comprehensive extractor that combines:
    - Advanced text extraction with multiple fallback methods
    - Enhanced room layout extraction with spatial coordinates
    - Alias mapping for improved field recognition
    - Comprehensive metadata and lighting setup extraction
    - Robust error handling and logging
    
    Features:
    - Hybrid text extraction (pdfplumber + PyMuPDF + OCR fallback)
    - Advanced room layout extraction with multiple coordinate formats
    - Alias-based field mapping for better recognition
    - Comprehensive luminaire and scene extraction
    - Production-ready error handling
    """

    def __init__(self, alias_file: str = "aliases.json"):
        """
        Initialize the Final PDF Extractor.
        
        Args:
            alias_file (str): Path to the alias mapping file for field recognition
        """
        # Always resolve path relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alias_path = os.path.join(base_dir, alias_file)

        if not os.path.exists(alias_path):
            raise FileNotFoundError(f"Alias file not found: {alias_path}")

        # Set up text extraction methods in order of preference
        self.text_extractors = [
            self._extract_with_pdfplumber,
            self._extract_with_pymupdf
        ]

        # Load alias mappings for improved field recognition
        with open(alias_path, "r", encoding="utf-8") as f:
            self.aliases = json.load(f)

    # -----------------------------------------------------
    # TEXT EXTRACTION METHODS
    # -----------------------------------------------------
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """
        Extract text from PDF using pdfplumber library.
        
        This is the primary text extraction method as it's fast and accurate
        for text-based PDFs. It preserves formatting and handles most PDF types well.
        
        Args:
            pdf_path (str): Path to the PDF file to extract text from
            
        Returns:
            str: Extracted text content, or empty string if extraction fails
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    if page.extract_text():
                        text += page.extract_text() + "\n"
        except Exception as e:
            print(f"pdfplumber error: {e}")
        return text.strip()

    def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF (fitz) library.
        
        This is an alternative text extraction method that can handle
        some PDF types that pdfplumber might struggle with. It's used
        as a fallback when pdfplumber fails.
        
        Args:
            pdf_path (str): Path to the PDF file to extract text from
            
        Returns:
            str: Extracted text content, or empty string if extraction fails
        """
        text = ""
        try:
            import fitz
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text() + "\n"
            doc.close()
        except Exception as e:
            print(f"PyMuPDF error: {e}")
        return text.strip()

    def _ocr_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using OCR (Optical Character Recognition).
        
        This method is used as a fallback when text-based extraction fails.
        It converts PDF pages to images and uses Tesseract OCR to extract text.
        This is slower but can handle scanned PDFs and image-based documents.
        
        Args:
            pdf_path (str): Path to the PDF file to extract text from
            
        Returns:
            str: OCR extracted text content, or empty string if extraction fails
        """
        text = ""
        try:
            pages = convert_from_path(pdf_path, dpi=300)
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
        except Exception as e:
            print(f"OCR error: {e}")
        return text.strip()

    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF using a fallback chain of methods.
        
        This method tries multiple extraction approaches in order of preference:
        1. pdfplumber (fastest, best for text-based PDFs)
        2. PyMuPDF (alternative text extraction)
        3. OCR (slowest, but works with scanned PDFs)
        
        Args:
            pdf_path (str): Path to the PDF file to extract text from
            
        Returns:
            str: Extracted text content from the most successful method
        """
        for extractor in self.text_extractors:
            text = extractor(pdf_path)
            if text and len(text) > 50:
                return text
        return self._ocr_pdf(pdf_path)

    def process_report(self, pdf_path: str) -> Dict[str, Any]:
        """
        Main processing function that handles the complete PDF extraction workflow.
        
        This is the primary method that orchestrates the entire extraction process:
        1. Extracts text from the PDF using the best available method
        2. Parses the text to extract structured data
        3. Returns comprehensive report data
        
        Args:
            pdf_path (str): Path to the PDF file to process
            
        Returns:
            Dict[str, Any]: Complete structured data extracted from the PDF
        """
        print(f"Processing: {pdf_path}")
        
        # Extract text using the fallback chain
        text = self.extract_text(pdf_path)
        print(f"Extracted {len(text)} characters")
        
        # Parse the extracted text into structured data
        data = self.parse_report(text, os.path.basename(pdf_path))
        
        return data

    # -----------------------------------------------------
    # NORMALIZATION USING ALIASES
    # -----------------------------------------------------
    def normalize_parameter(self, param: str) -> str:
        """
        Normalize parameter names using the alias mapping system.
        
        This method helps standardize parameter names by mapping various aliases
        to canonical names, improving data consistency across different reports.
        
        Args:
            param (str): The parameter name to normalize
            
        Returns:
            str: The normalized parameter name, or original if no mapping found
        """
        param = param.lower().strip()
        for standard, variations in self.aliases["parameters"].items():
            if param in [v.lower() for v in variations]:
                return standard
        return param

    def normalize_place(self, place: str) -> str:
        """
        Normalize place names using the alias mapping system.
        
        This method helps standardize place names by mapping various aliases
        to canonical names, improving data consistency across different reports.
        
        Args:
            place (str): The place name to normalize
            
        Returns:
            str: The normalized place name, or original if no mapping found
        """
        place = place.lower().strip()
        for standard, variations in self.aliases["places"].items():
            if place in [v.lower() for v in variations]:
                return standard
        return place

    # -----------------------------------------------------
    # METADATA EXTRACTION
    # -----------------------------------------------------
    def _extract_metadata(self, text: str, data: Dict[str, Any]):
        """
        Extract metadata fields from the PDF text.
        
        This method searches for and extracts basic information about the report
        including company name, project name, engineer name, and email address.
        It uses multiple regex patterns to handle different formatting styles.
        
        Args:
            text (str): Raw text extracted from the PDF
            data (Dict[str, Any]): Data dictionary to populate with extracted metadata
        """
        # Company name extraction with multiple pattern matching
        # Pattern 1: Matches "Company", "Short Cicuit", or "Short Circuit" followed by any text until newline or end
        # Pattern 2: Matches "Company Name:" or "Company Name-" followed by the actual name
        # Pattern 3: Exact match for "Short Cicuit Company" (common typo in reports)
        company_patterns = [
            r"(Company|Short\s*Cicuit|Short\s*Circuit).*?(?=\n|$)",  # Flexible company name matching
            r"Company\s*Name[:\-]?\s*(.+)",  # Structured company name field
            r"Short\s*Cicuit\s*Company"  # Exact match for known company name
        ]
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)  # Case-insensitive matching
            if match:
                data["metadata"]["company_name"] = match.group(0).strip()  # Clean whitespace
                break  # Use first successful match

        # Project name extraction with multiple pattern matching
        # Pattern 1: Matches "Project Name" or "Lighting study" followed by content until newline
        # Pattern 2: Structured project name field with colon or dash separator
        # Pattern 3: Matches "Lighting study for" followed by project description
        project_patterns = [
            r"(Project\s*Name|Lighting study.*?)\n",  # Multi-line project name
            r"Project\s*Name[:\-]?\s*(.+)",  # Structured project name field
            r"Lighting\s*study\s*for\s*(.+)"  # Descriptive project name format
        ]
        for pattern in project_patterns:
            match = re.search(pattern, text, re.IGNORECASE)  # Case-insensitive matching
            if match:
                data["metadata"]["project_name"] = match.group(0).strip()  # Clean whitespace
                break  # Use first successful match

        # Engineer name extraction
        # Matches "Eng." followed by engineer's name (common format in reports)
        engineer_match = re.search(r"Eng\.\s*[A-Za-z ]+", text)
        if engineer_match:
            data["metadata"]["engineer"] = engineer_match.group(0).strip()  # Clean whitespace

        # Email address extraction
        # Matches standard email format: username@domain.com
        # Uses word characters, dots, and hyphens for username and domain
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
        if email_match:
            data["metadata"]["email"] = email_match.group(0).strip()  # Clean whitespace

    # -----------------------------------------------------
    # LIGHTING SETUP EXTRACTION
    # -----------------------------------------------------
    def _extract_lighting_setup(self, text: str, data: Dict[str, Any]):
        """
        Extract lighting setup information from the PDF text.
        
        This method searches for and extracts overall lighting system configuration
        including lux values, uniformity, and other DIALux-specific metrics.
        It uses both DIALux-style pattern matching and fallback regex patterns.
        
        Args:
            text (str): Raw text extracted from the PDF
            data (Dict[str, Any]): Data dictionary to populate with lighting setup info
        """

        lighting_setup = {}

        # Primary DIALux-style pattern matching
        # This regex captures the standard DIALux output format:
        # "673 lx 277 lx 949 lx 0.41 0.49 CG6"
        # Where: avg_lux min_lux max_lux uniformity g1_index lighting_class
        match = re.search(
            r"([\d.]+)\s*lx\s+"     # Group 1: Average lux value (e.g., "673")
            r"([\d.]+)\s*lx\s+"     # Group 2: Minimum lux value (e.g., "277") 
            r"([\d.]+)\s*lx\s+"     # Group 3: Maximum lux value (e.g., "949")
            r"([\d.]+)\s+"          # Group 4: Uniformity ratio (e.g., "0.41")
            r"([\d.]+)\s+"          # Group 5: G1 index value (e.g., "0.49")
            r"([A-Za-z0-9]+)",      # Group 6: Lighting class index (e.g., "CG6")
            text
        )

        if match:
            # Extract all captured groups from the DIALux pattern
            avg, emin, emax, uo, g1, index = match.groups()
            lighting_setup.update({
                "average_lux": float(avg),      # Convert to float for numerical operations
                "min_lux": float(emin),         # Convert to float for numerical operations
                "max_lux": float(emax),         # Convert to float for numerical operations
                "uniformity": float(uo),        # Convert to float for numerical operations
                "g1": float(g1),               # Convert to float for numerical operations
                "index": index                 # Keep as string (lighting class identifier)
            })
        else:
            # Fallback to individual field extraction when DIALux pattern doesn't match
            # This handles cases where the report format is different or fragmented
            
            # Average lux extraction with multiple label variations
            # Matches "Avr.lux:", "Average lux:", "Avr lux -", etc.
            avg_lux = re.search(r"(?:Avr\.?lux|Average\s*lux)[:\-]?\s*([\d.]+)", text, re.IGNORECASE)
            if avg_lux:
                lighting_setup["average_lux"] = float(avg_lux.group(1))  # Convert to float
            
            # Uniformity extraction with multiple label variations
            # Matches "Uniformity:", "Uo:", "Uniformity -", etc.
            uniformity = re.search(r"(?:Uniformity|Uo)[:\-]?\s*([\d.]+)", text, re.IGNORECASE)
            if uniformity:
                lighting_setup["uniformity"] = float(uniformity.group(1))  # Convert to float

        # Update the main data structure with extracted lighting setup information
        data["lighting_setup"].update(lighting_setup)

    # -----------------------------------------------------
    # LUMINAIRE EXTRACTION
    # -----------------------------------------------------
    def _extract_luminaires(self, text: str, data: Dict[str, Any]):
        """
        Extract luminaire (lighting fixture) information from the PDF text.
        
        This method searches for and extracts detailed specifications of lighting
        fixtures including manufacturer, article number, power consumption,
        luminous flux, and efficacy. It uses a comprehensive regex pattern
        to match the standard luminaire specification format.
        
        Args:
            text (str): Raw text extracted from the PDF
            data (Dict[str, Any]): Data dictionary to populate with luminaire info
        """
        # Comprehensive luminaire specification pattern
        # Matches format: "36 Philips BY698P LED265CW G2 WB 150.0 W 21750 lm 145.0 lm/W"
        # Group 1: Quantity (e.g., "36")
        # Group 2: Manufacturer (e.g., "Philips")
        # Group 3: Article number/model (e.g., "BY698P LED265CW G2 WB")
        # Group 4: Power in watts (e.g., "150.0")
        # Group 5: Luminous flux in lumens (e.g., "21750")
        # Group 6: Efficacy in lm/W (e.g., "145.0")
        luminaire_matches = re.findall(
            r"(\d+)\s+"                           # Group 1: Quantity (digits only)
            r"([A-Za-z]+)\s+"                     # Group 2: Manufacturer (letters only)
            r"([A-Za-z0-9\- ]+)\s+"              # Group 3: Article/model (letters, numbers, hyphens, spaces)
            r"(\d+\.?\d*)\s*W\s+"                # Group 4: Power in watts (decimal number + "W")
            r"(\d+\.?\d*)\s*lm\s+"               # Group 5: Luminous flux in lumens (decimal number + "lm")
            r"(\d+\.?\d*)\s*lm/W",               # Group 6: Efficacy in lm/W (decimal number + "lm/W")
            text
        )
        
        # Process each matched luminaire specification
        for match in luminaire_matches:
            data["luminaires"].append({
                "quantity": int(match[0]),                    # Quantity of fixtures (convert to integer)
                "manufacturer": match[1],                     # Manufacturer name (e.g., "Philips")
                "article_no": match[2],                       # Article/model number (e.g., "BY698P LED265CW G2 WB")
                "power_w": float(match[3]),                   # Power consumption in watts (convert to float)
                "luminous_flux_lm": float(match[4]),          # Luminous flux in lumens (convert to float)
                "efficacy_lm_per_w": float(match[5])          # Efficacy in lumens per watt (convert to float)
            })

    # -----------------------------------------------------
    # ROOM EXTRACTION
    # -----------------------------------------------------
    def _extract_rooms(self, text: str, data: Dict[str, Any]):
        """
        Extract room information with enhanced layout extraction.
        
        This method searches for and extracts comprehensive room information including
        room names, spatial coordinates, and arrangement patterns. It uses multiple
        regex patterns to handle various coordinate formats and room naming conventions.
        
        Args:
            text (str): Raw text extracted from the PDF
            data (Dict[str, Any]): Data dictionary to populate with room layout info
        """

        # Room name patterns - multiple formats to handle different naming conventions
        # Pattern 1: "Building 1 · Storey 1 · Room 1" (with bullet separators)
        # Pattern 2: "Building 1 Storey 1 Room 1" (with space separators)
        # Pattern 3: "Room 1" (simple room number)
        # Pattern 4: "Building 1 ... Room 1" (flexible building-room format)
        room_patterns = [
            r"(Building\s*\d+\s*·\s*Storey\s*\d+\s*·\s*Room\s*\d+)",  # Bullet-separated format
            r"(Building\s*\d+\s*Storey\s*\d+\s*Room\s*\d+)",           # Space-separated format
            r"(Room\s*\d+)",                                           # Simple room number
            r"(Building\s*\d+.*?Room\s*\d+)"                          # Flexible building-room format
        ]

        # Coordinate patterns - multiple formats to handle different coordinate representations
        # Pattern 1: "4.000 m 36.002 m 7.000 m" (meters with unit labels)
        # Pattern 2: "4000.000 mm 36002.000 mm 7000.000 mm" (millimeters with unit labels)
        # Pattern 3: "X: 4000.000 mm Y: 36002.000 mm Z: 7000.000 mm" (labeled coordinates in mm)
        # Pattern 4: "X: 4.000 Y: 36.002 Z: 7.000" (labeled coordinates in meters)
        coord_patterns = [
            r"(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m",  # Meters with unit labels
            r"(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm",  # Millimeters with unit labels
            r"X\s*[:\-]?\s*(\d+\.?\d*)\s*mm\s*Y\s*[:\-]?\s*(\d+\.?\d*)\s*mm\s*Z\s*[:\-]?\s*(\d+\.?\d*)\s*mm",  # Labeled mm coordinates
            r"X\s*[:\-]?\s*(\d+\.?\d*)\s*Y\s*[:\-]?\s*(\d+\.?\d*)\s*Z\s*[:\-]?\s*(\d+\.?\d*)"  # Labeled meter coordinates
        ]

        # Arrangement patterns - multiple formats to handle different arrangement labels
        # Pattern 1: "Arrangement: A1" or "Arrangement - A1"
        # Pattern 2: "Layout: A1" or "Layout - A1"
        # Pattern 3: "Pattern: A1" or "Pattern - A1"
        # Pattern 4: "A1 arrangement" (reverse format)
        arrangement_patterns = [
            r"Arrangement[:\-]?\s*([A-Za-z0-9]+)",  # Standard arrangement label
            r"Layout[:\-]?\s*([A-Za-z0-9]+)",       # Layout label variant
            r"Pattern[:\-]?\s*([A-Za-z0-9]+)",      # Pattern label variant
            r"([A-Za-z0-9]+)\s*arrangement"         # Reverse arrangement format
        ]

        # Collect unique room names using all room patterns
        all_rooms = []
        for pattern in room_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)  # Case-insensitive matching
            for match in matches:
                # Avoid duplicate room names by checking existing rooms
                if match not in [r["name"] for r in all_rooms]:
                    all_rooms.append({"name": match.strip()})  # Clean whitespace

        # Extract and process coordinate data from all coordinate patterns
        all_coords = []
        for coord_pattern in coord_patterns:
            matches = re.findall(coord_pattern, text, re.IGNORECASE)  # Case-insensitive matching
            for match in matches:
                try:
                    # Extract X, Y, Z coordinate values and convert to float
                    x, y, z = float(match[0]), float(match[1]), float(match[2])
                    
                    # Unit conversion: check if pattern ends with "mm" (millimeter coordinates)
                    if coord_pattern.endswith("mm"):
                        # Convert millimeters to meters (divide by 1000)
                        x, y, z = x/1000, y/1000, z/1000
                    
                    # Add coordinate to collection with proper units (always in meters)
                    all_coords.append({"x_m": x, "y_m": y, "z_m": z})
                except Exception:
                    # Skip invalid coordinate matches (non-numeric values, conversion errors)
                    continue

        # Extract arrangement patterns from all arrangement regex patterns
        arrangements = []
        for pattern in arrangement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)  # Case-insensitive matching
            arrangements.extend(matches)  # Collect all arrangement matches

        # Assemble room data with extracted information
        for room in all_rooms:
            # Use first arrangement found, or default to "A1" if none found
            arrangement = arrangements[0] if arrangements else "A1"
            # Copy all coordinates to each room (shared layout assumption)
            layout = all_coords.copy() if all_coords else []
            
            # Add complete room information to data structure
            data["rooms"].append({
                "name": room["name"],           # Room name from pattern matching
                "arrangement": arrangement,     # Arrangement pattern (e.g., "A1")
                "layout": layout               # Coordinate layout points
            })

        # Fallback: create default room if no rooms were found
        # This ensures we always have at least one room entry
        if not data["rooms"]:
            data["rooms"].append({
                "name": "Building 1 · Storey 1 · Room 1",  # Default room name
                "arrangement": "A1",                        # Default arrangement
                "layout": all_coords if all_coords else []  # Use any found coordinates
            })
        
        # Deduplicate rooms by name (case-insensitive)
        # This prevents duplicate room entries from multiple pattern matches
        unique = {}
        for r in data["rooms"]:
            unique[r["name"].lower()] = r  # Use lowercase name as key for deduplication
        data["rooms"] = list(unique.values())  # Convert back to list of unique rooms

    # -----------------------------------------------------
    # SCENE EXTRACTION
    # -----------------------------------------------------
    def _extract_scenes(self, text: str, data: Dict[str, Any]):
        """
        Extract scene information from the PDF text.
        
        This method searches for and extracts lighting scene data including
        scene names, average lux levels, minimum/maximum lux values,
        uniformity ratios, and utilization profiles. It uses comprehensive
        regex patterns to match DIALux-style scene output formats.
        
        Args:
            text (str): Raw text extracted from the PDF
            data (Dict[str, Any]): Data dictionary to populate with scene info
        """
        # Scene extraction with optional scene name and comprehensive metrics
        # Pattern matches: "Scene Name 673 lx 277 lx 949 lx 0.41 0.49 CG6"
        # Group 1: Optional scene name (e.g., "the factory", "working place")
        # Group 2: Average lux value (e.g., "673")
        # Group 3: Minimum lux value (e.g., "277")
        # Group 4: Maximum lux value (e.g., "949")
        # Group 5: Uniformity ratio (e.g., "0.41")
        # Group 6: G1 index value (e.g., "0.49")
        # Group 7: Lighting class index (e.g., "CG6")
        scene_matches = re.findall(
            r"(?:([A-Za-z ]+)\s+)?([\d.]+)\s*lx\s+([\d.]+)\s*lx\s+([\d.]+)\s*lx\s+([\d.]+)\s+([\d.]+)\s+([A-Za-z0-9]+)",
            text
        )

        # Process each matched scene specification
        for sm in scene_matches:
            # Extract scene name (use first group if present, otherwise default)
            scene_name = sm[0].strip() if sm[0] else "Scene"
            # Extract numerical metrics from remaining groups
            avg, emin, emax, uo, g1, index = sm[1:]
            
            # Add complete scene information to data structure
            data["scenes"].append({
                "scene_name": scene_name.strip(),        # Scene identifier (e.g., "the factory")
                "average_lux": float(avg),               # Average illuminance in lux
                "min_lux": float(emin),                  # Minimum illuminance in lux
                "max_lux": float(emax),                  # Maximum illuminance in lux
                "uniformity": float(uo),                 # Uniformity ratio (0-1)
                "g1": float(g1),                        # G1 index value
                "index": index                          # Lighting class index (e.g., "CG6")
            })

        # Fallback: create default scene from lighting setup if no scenes found
        # This ensures we always have at least one scene entry
        if not data["scenes"] and "lighting_setup" in data:
            setup = data["lighting_setup"]
            data["scenes"].append({
                "scene_name": "Default Scene",           # Default scene name
                "average_lux": setup.get("average_lux"), # Use lighting setup average lux
                "min_lux": setup.get("min_lux"),
                "max_lux": setup.get("max_lux"),
                "uniformity": setup.get("uniformity"),
                "g1": setup.get("g1"),
                "index": setup.get("index")
            })

    # -----------------------------------------------------
    # MASTER PARSER
    # -----------------------------------------------------
    # MAIN PARSING METHOD
    # -----------------------------------------------------
    def parse_report(self, text: str, filename: str = "report.pdf") -> Dict[str, Any]:
        """
        Parse extracted text and extract structured data from the PDF report.
        
        This is the main parsing function that coordinates all extraction methods
        to build a comprehensive data structure from the raw text. It initializes
        the data structure and calls all specialized extraction methods.
        
        Args:
            text (str): Raw text extracted from the PDF
            filename (str): Name of the PDF file (used for report title)
            
        Returns:
            Dict[str, Any]: Structured data containing:
                - metadata: Company, project, engineer, email info
                - lighting_setup: Overall lighting system configuration
                - luminaires: Detailed fixture specifications
                - rooms: Room layouts with spatial coordinates
                - scenes: Performance metrics and utilization profiles
        """
        # Initialize data structure with empty containers for all extraction categories
        data = {
            "metadata": {
                "company_name": None,      # Company name (to be extracted)
                "project_name": None,      # Project name (to be extracted)
                "engineer": None,          # Engineer name (to be extracted)
                "email": None,             # Email address (to be extracted)
                "report_title": filename   # Use filename as report title
            },
            "lighting_setup": {},         # Overall lighting system configuration
            "luminaires": [],             # Individual fixture specifications
            "rooms": [],                  # Room layouts with coordinates
            "scenes": []                  # Lighting scene performance data
        }

        # Execute all extraction methods in sequence
        # Each method populates its respective section of the data structure
        self._extract_metadata(text, data)           # Extract basic report information
        self._extract_lighting_setup(text, data)     # Extract lighting system configuration
        self._extract_luminaires(text, data)         # Extract fixture specifications
        self._extract_rooms(text, data)              # Extract room layouts and coordinates
        self._extract_scenes(text, data)             # Extract scene performance data

        return data

    def process_report(self, pdf_path: str) -> Dict[str, Any]:
        """
        Main processing function that handles the complete PDF extraction workflow.
        
        This is the primary method that orchestrates the entire extraction process:
        1. Extracts text from the PDF using the best available method
        2. Parses the text to extract structured data
        3. Returns comprehensive report data
        
        Args:
            pdf_path (str): Path to the PDF file to process
            
        Returns:
            Dict[str, Any]: Complete structured data extracted from the PDF
        """
        print(f"Processing: {pdf_path}")
        # Extract text using the fallback chain (pdfplumber -> PyMuPDF -> OCR)
        text = self.extract_text(pdf_path)
        print(f"Extracted {len(text)} characters")
        # Parse the extracted text into structured data
        return self.parse_report(text, os.path.basename(pdf_path))

# -----------------------------------------------------
# MAIN EXECUTION BLOCK
# -----------------------------------------------------
if __name__ == "__main__":
    """
    Main execution block for command-line usage of the Final PDF Extractor.
    
    This block handles command-line arguments and orchestrates the PDF processing
    workflow. It can accept a PDF file path as an argument or use a default file.
    
    Usage:
        python final_extractor.py [pdf_file_path]
        
    If no file path is provided, it will use the default PDF file.
    """
    # Initialize the extractor with alias mapping for improved field recognition
    extractor = FinalPDFExtractor("aliases.json")
    
    # Get PDF path from command line argument or use default
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]  # Use provided file path
    else:
        pdf_path = "El- Mohands _Report.pdf"  # Default fallback file
    
    # Process the PDF and extract structured data
    result = extractor.process_report(pdf_path)

    # Generate output filename based on input PDF name
    out_file = f"{os.path.basename(pdf_path)}_extracted.json"
    
    # Save extracted data to JSON file with proper formatting
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)  # Pretty-print JSON with UTF-8 encoding

    print(f"✓ Results saved to {out_file}")
