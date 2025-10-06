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
    
    def _safe_float(self, value_str):
        """Try to convert a string to float; return None on failure.
        Accepts 123, 123.45, 1,234.56 (commas converted to dots).
        """
        if value_str is None:
            return None
        s = str(value_str).strip()
        # convert comma decimal separators to dot (and remove thousands separators if present)
        s = s.replace(',', '.')
        # remove any characters that are not digits or dot
        s = re.sub(r'[^\d.]', '', s)
        # reject empty or a lone dot
        if not re.match(r'^\d+(\.\d+)?$', s):
            return None
        try:
            return float(s)
        except Exception:
            return None

    def __init__(self, alias_file: str = "aliases.json"):
        """
        Initialize the Final PDF Extractor.
        Supports both external alias file and built-in defaults.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alias_path = os.path.join(base_dir, alias_file)

        # Default aliases (used if JSON missing or broken)
        default_aliases = {
            "places": {
                "Factory": ["factory", "the factory", "industrial hall", "workshop", "production hall"],
                "Office": ["office", "workplace", "open office", "meeting room"],
                "Classroom": ["classroom", "lecture hall", "study room"],
                "Corridor": ["corridor", "hallway", "passage", "hall"],
                "Warehouse": ["warehouse", "storage hall", "stock room"],
                "Parking": ["parking", "garage", "car park"],
                "Hospital Ward": ["ward", "patient room"],
                "Retail": ["shop", "store", "retail"],
                "IT Room": ["server room", "it room"]
            },
            "parameters": {
                "average_lux": ["ē", "eavg", "average lux", "lux", "illumination", "lighting level"],
                "min_lux": ["emin", "minimum lux", "e_min"],
                "max_lux": ["emax", "maximum lux", "e_max"],
                "uniformity": ["uniformity", "uo", "emin/eavg", "e_min/e_avg"],
                "glare_related": ["g1", "g2", "index"],
                "power_w": ["power", "watt", "p"],
                "luminous_flux_lm": ["lm", "lumens", "φluminaire"],
                "luminous_efficacy_lm_per_w": ["lm/w", "efficacy", "luminous efficacy"]
            }
        }

        # Try loading external aliases.json, otherwise fallback
        try:
            if os.path.exists(alias_path):
                with open(alias_path, "r", encoding="utf-8") as f:
                    self.aliases = json.load(f)
                print(f"✓ Loaded aliases from {alias_path}")
            else:
                raise FileNotFoundError
        except Exception as e:
            print(f"⚠️ Using default aliases (reason: {e})")
            self.aliases = default_aliases

        # Text extractors
        self.text_extractors = [
            self._extract_with_pdfplumber,
            self._extract_with_pymupdf
        ]

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

    # def process_report(self, pdf_path: str) -> Dict[str, Any]:
    #     """
    #     Main processing function that handles the complete PDF extraction workflow.
        
    #     This is the primary method that orchestrates the entire extraction process:
    #     1. Extracts text from the PDF using the best available method
    #     2. Parses the text to extract structured data
    #     3. Returns comprehensive report data
        
    #     Args:
    #         pdf_path (str): Path to the PDF file to process
            
    #     Returns:
    #         Dict[str, Any]: Complete structured data extracted from the PDF
    #     """
    #     print(f"Processing: {pdf_path}")
        
    #     # Extract text using the fallback chain
    #     text = self.extract_text(pdf_path)
    #     print(f"Extracted {len(text)} characters")
        
    #     # Parse the extracted text into structured data
    #     data = self.parse_report(text, os.path.basename(pdf_path))
        
    #     return data

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
    # def _extract_metadata(self, text: str, data: Dict[str, Any]):
    def _extract_metadata(self, text: str, data: Dict[str, Any], pdf_path: str):
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

        # project_patterns = [
        #     r"(Project\s*Name|Lighting study.*?)\n",  # Multi-line project name
        #     r"Project\s*Name[:\-]?\s*(.+)",  # Structured project name field
        #     r"Lighting\s*study\s*for\s*(.+)"  # Descriptive project name format
        # ]
        # for pattern in project_patterns:
        #     match = re.search(pattern, text, re.IGNORECASE)  # Case-insensitive matching
        #     if match:
        #         data["metadata"]["project_name"] = match.group(0).strip()  # Clean whitespace
        #         break  # Use first successful match

        # --- Improved project name extraction ---

        try:
            with pdfplumber.open(pdf_path) as pdf:
                first_page = pdf.pages[0]
                first_text = first_page.extract_text().strip().splitlines()
                # Take first non-empty, non-"Description" line
                for line in first_text:
                    clean = line.strip()
                    if clean and not re.match(r"(?i)description|images|technical|company|ico", clean):
                        data["metadata"]["project_name"] = clean
                        break
        except Exception as e:
            print("⚠️ Could not extract project name from first page:", e)

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
        """Extract lighting setup values using aliases and robust fallbacks (supports Ē)."""
        lighting_setup = {}

        number_pattern = r"([0-9]+(?:[.,][0-9]+)?)"

        # 1) Alias-driven extraction (safe, uses word boundaries)
        params = self.aliases.get("parameters", {})
        for standard, variations in params.items():
            if standard in lighting_setup:
                continue
            for alias in variations:
                # Use boundaries to avoid partial-word matches (e.g., 'lm' in 'film')
                # Match number + optional unit right after
                pattern = rf"(?<!\w){re.escape(alias)}(?!\w)\s*[:=]?\s*{number_pattern}\s*([A-Za-z/]+)?"
                m = re.search(pattern, text, re.IGNORECASE | re.UNICODE)
                if m:
                    val = self._safe_float(m.group(1))
                    unit = (m.group(2) or "").lower().strip()

                    # --- Intelligent unit handling ---
                    if val is not None:
                        # --- Explicit unit-based mapping ---
                        if re.search(r"\blm/?w\b", unit) or "efficacy" in alias.lower():
                            lighting_setup["luminous_efficacy_lm_per_w"] = val
                        elif re.search(r"\bw(att)?s?\b", unit):
                            lighting_setup["power_w"] = val
                        else:
                            lighting_setup[standard] = val
                    break

        # 2) Fallback: compact DIALux-like line with numbers (avg, min, max, Uo, g1, index)
        if not lighting_setup.get("average_lux") or not lighting_setup.get("min_lux"):
            compact = re.compile(
                rf"(?:(?:Ē|Eavg|Average|E)\s*[:=]?\s*)?{number_pattern}\s*lx?"
                rf"[\s\n]+(?:(?:Emin|Min)?\s*[:=]?\s*)?{number_pattern}\s*lx?"
                rf"[\s\n]+(?:(?:Emax|Max)?\s*[:=]?\s*)?{number_pattern}\s*lx?"
                rf"[\s\n]+{number_pattern}"
                rf"[\s\n]+{number_pattern}"
                rf"[\s\n]+([A-Za-z0-9]+)",
                re.UNICODE
            )
            m = compact.search(text)
            if m:
                avg = self._safe_float(m.group(1))
                emin = self._safe_float(m.group(2))
                emax = self._safe_float(m.group(3))
                uo = self._safe_float(m.group(4))
                g1 = self._safe_float(m.group(5))
                index = m.group(6)
                if avg is not None: lighting_setup.setdefault("average_lux", avg)
                if emin is not None: lighting_setup.setdefault("min_lux", emin)
                if emax is not None: lighting_setup.setdefault("max_lux", emax)
                if uo is not None: lighting_setup.setdefault("uniformity", uo)
                if g1 is not None: lighting_setup.setdefault("g1", g1)
                lighting_setup.setdefault("index", index)

        data["lighting_setup"].update(lighting_setup)

    # -----------------------------------------------------
    # LUMINAIRE EXTRACTION
    # -----------------------------------------------------
    # def _extract_luminaires(self, text: str, data: Dict[str, Any]):
    #     """
    #     Extract luminaire (lighting fixture) information from the PDF text.
        
    #     This method searches for and extracts detailed specifications of lighting
    #     fixtures including manufacturer, article number, power consumption,
    #     luminous flux, and efficacy. It uses a comprehensive regex pattern
    #     to match the standard luminaire specification format.
        
    #     Args:
    #         text (str): Raw text extracted from the PDF
    #         data (Dict[str, Any]): Data dictionary to populate with luminaire info
    #     """
    #     # Comprehensive luminaire specification pattern
    #     # Matches format: "36 Philips BY698P LED265CW G2 WB 150.0 W 21750 lm 145.0 lm/W"
    #     # Group 1: Quantity (e.g., "36")
    #     # Group 2: Manufacturer (e.g., "Philips")
    #     # Group 3: Article number/model (e.g., "BY698P LED265CW G2 WB")
    #     # Group 4: Power in watts (e.g., "150.0")
    #     # Group 5: Luminous flux in lumens (e.g., "21750")
    #     # Group 6: Efficacy in lm/W (e.g., "145.0")
    #     luminaire_matches = re.findall(
    #         r"(\d+)\s+"                           # Group 1: Quantity (digits only)
    #         r"([A-Za-z]+)\s+"                     # Group 2: Manufacturer (letters only)
    #         r"([A-Za-z0-9\- ]+)\s+"              # Group 3: Article/model (letters, numbers, hyphens, spaces)
    #         r"(\d+\.?\d*)\s*W\s+"                # Group 4: Power in watts (decimal number + "W")
    #         r"(\d+\.?\d*)\s*lm\s+"               # Group 5: Luminous flux in lumens (decimal number + "lm")
    #         r"(\d+\.?\d*)\s*lm/W",               # Group 6: Efficacy in lm/W (decimal number + "lm/W")
    #         text
    #     )
        
    #     # Process each matched luminaire specification
    #     for match in luminaire_matches:
    #         data["luminaires"].append({
    #             "quantity": int(match[0]),                    # Quantity of fixtures (convert to integer)
    #             "manufacturer": match[1],                     # Manufacturer name (e.g., "Philips")
    #             "article_no": match[2],                       # Article/model number (e.g., "BY698P LED265CW G2 WB")
    #             "power_w": float(match[3]),                   # Power consumption in watts (convert to float)
    #             "luminous_flux_lm": float(match[4]),          # Luminous flux in lumens (convert to float)
    #             "efficacy_lm_per_w": float(match[5])          # Efficacy in lumens per watt (convert to float)
    #         })

    # def _extract_luminaires(self, text: str, data: Dict[str, Any]):
    #     """Extract luminaire data using regex + alias-based matching."""

    #     # Handle DIALux layout-style luminaires
    #     dialux_style = re.findall(
    #         r"Manufacturer\s*[:\-]?\s*([A-Za-z0-9 ]+)\s*"
    #         r"Article\s*(?:name|no)\s*[:\-]?\s*([A-Za-z0-9\- /]+)\s*"
    #         r"P\s*[:=]?\s*([\d.]+)\s*W\s*"
    #         r"(?:Φ[Ll]uminaire|φ[Ll]uminaire)\s*[:=]?\s*([\d.]+)\s*lm",
    #         text
    #     )
    #     for m in dialux_style:
    #         manufacturer, article_no, power, lumens = m
    #         data["luminaires"].append({
    #             "manufacturer": manufacturer.strip(),
    #             "article_no": article_no.strip(),
    #             "power_w": float(power),
    #             "luminous_flux_lm": float(lumens)
    #         })

    #     # Primary regex (structured)
    #     luminaire_matches = re.findall(
    #         r"(\d+)\s+([A-Za-z]+)\s+([A-Za-z0-9\- ]+)\s+(\d+\.?\d*)\s*W\s+(\d+\.?\d*)\s*lm\s+(\d+\.?\d*)\s*lm/W",
    #         text
    #     )
    #     for match in luminaire_matches:
    #         data["luminaires"].append({
    #             "quantity": int(match[0]),
    #             "manufacturer": match[1],
    #             "article_no": match[2],
    #             "power_w": float(match[3]),
    #             "luminous_flux_lm": float(match[4]),
    #             "efficacy_lm_per_w": float(match[5])
    #         })

    #     # Fallback only if none found
    #     if data["luminaires"]:
    #         return

    #     # Fallback: alias-driven scanning
    #     if not data["luminaires"]:
    #         luminaire_data = {}
    #         for standard, variations in self.aliases["parameters"].items():
    #             for alias in variations:
    #                 match = re.search(rf"{alias}\s*[:=]?\s*([\d.]+)", text, re.IGNORECASE)
    #                 if match:
    #                     value = match.group(1)
    #                     # ✅ Prevent crashes on bad matches (e.g., ".")
    #                     if re.match(r"^\d+(\.\d+)?$", value):
    #                         luminaire_data[standard] = float(value)
    #                     break
    #         if luminaire_data:
    #             data["luminaires"].append(luminaire_data)

    def _extract_luminaires(self, text, data):
        luminaire_section = re.search(
            r"Luminaire list\s+Φtotal\s+Ptotal\s+Luminous efficacy\s+([\s\S]+?)(?:Calculation surface|$)",
            text,
            flags=re.IGNORECASE,
        )
        if not luminaire_section:
            return

        section_text = luminaire_section.group(1)

        # Extract totals
        totals_match = re.search(
            r"([\d\.]+)\s*lm\s+([\d\.]+)\s*W\s+([\d\.]+)\s*lm/W",
            section_text,
            flags=re.IGNORECASE,
        )
        if totals_match:
            data["lighting_setup"]["luminous_flux_total"] = float(totals_match.group(1))
            data["lighting_setup"]["power_w"] = float(totals_match.group(2))
            data["lighting_setup"]["luminous_efficacy_lm_per_w"] = float(totals_match.group(3))

        # Extract per-luminaire line
        for match in re.findall(
            r"(\d+)\s+([A-Za-z]+)\s+([\w\-\/]+)\s+([A-Za-z0-9\s\-\+x/]+?)\s+([\d\.]+)\s*W\s+([\d\.]+)\s*lm\s+([\d\.]+)\s*lm/W",
            section_text,
        ):
            pcs, manuf, art_no, name, pw, lm, eff = match
            data["luminaires"].append({
                "quantity": int(pcs),
                "manufacturer": manuf,
                "article_no": art_no,
                "article_name": name.strip(),
                "power_w": float(pw),
                "luminous_flux_lm": float(lm),
                "luminous_efficacy_lm_per_w": float(eff),
            })

        print(f"✅ Extracted {len(data['luminaires'])} luminaires")

    # def _extract_layout(self, pdf_path: str):
    #     """
    #     Extract luminaire layout coordinates (X, Y, Z) from table structures in the PDF.
        
    #     This version uses pdfplumber’s built-in table extraction to avoid regex misreads
    #     and interference between unrelated tables.

    #     Returns:
    #         list[dict]: Each dict contains {'x_m': float, 'y_m': float, 'z_m': float}
    #     """
    #     # import pdfplumber

    #     layout_coords = []

    #     try:
    #         with pdfplumber.open(pdf_path) as pdf:
    #             for page in pdf.pages:
    #                 tables = page.extract_tables()

    #                 for table in tables:
    #                     if not table or len(table) < 2:
    #                         continue

    #                     headers = [str(h).strip().lower() for h in table[0] if h]
    #                     # --- Normalize headers using aliases (for variations like "installation height") ---
    #                     for i, h in enumerate(headers):
    #                         for std, alts in self.aliases["parameters"].items():
    #                             if any(a.lower() in h for a in alts):
    #                                 headers[i] = std
    #                                 break

    #                     print(f"📄 Page {page.page_number} headers detected: {headers}")
    #                     print(f"✓ Found layout table on page {page.page_number} with headers: {headers}")
                        
    #                     # Identify layout table by keywords
    #                     if any(h in headers for h in ["x", "y", "z", "mounting height", "luminaire", "x (m)"]):
    #                         for row in table[1:]:
    #                             if not row:
    #                                 continue

    #                             # Attempt to read X, Y, Z from first 3 numeric columns
    #                             numeric_values = []
    #                             for cell in row:
    #                                 try:
    #                                     val = float(str(cell).replace(',', '.'))
    #                                     numeric_values.append(val)
    #                                 except:
    #                                     pass

    #                             if len(numeric_values) >= 3:
    #                                 # Convert to meters if units seem large
    #                                 x, y, z = numeric_values[:3]
    #                                 if max(x, y, z) > 100:  # looks like mm
    #                                     x, y, z = x / 1000, y / 1000, z / 1000

    #                                 layout_coords.append({
    #                                     "x_m": x,
    #                                     "y_m": y,
    #                                     "z_m": z
    #                                 })
                            
    #                         print(f"✅ Extracted {len(layout_coords)} coordinates so far from page {page.page_number}")
                            
    #                         if layout_coords:
    #                             print(f"✅ Found {len(layout_coords)} layout points.")
    #                         else:
    #                             print("⚠️ No layout points detected on this page.")
    #         # Sort from rightmost to leftmost (optional for interference fix)
    #         layout_coords.sort(key=lambda c: c["x_m"], reverse=True)

    #     except Exception as e:
    #         print(f"⚠️ Layout extraction error: {e}")

    #     # Aggregate all coordinates found across pages
    #     if layout_coords:
    #         print(f"✓ Extracted {len(layout_coords)} layout points total")
    #     return layout_coords

    def _extract_layout(self, text):
        layout_blocks = re.findall(
            r"1st luminaire \(X/Y/Z\)\s*([\d\.]+)\s*m\s*/\s*([\d\.]+)\s*m\s*/\s*([\d\.]+)\s*m([\s\S]+?)(?=9 x|Luminaire list|$)",
            text,
            flags=re.IGNORECASE,
        )

        layout_coords = []
        for block in layout_blocks:
            x0, y0, z0, rest = block
            layout_coords.append({
                "X": float(x0),
                "Y": float(y0),
                "Z": float(z0),
            })
            # find all coordinate triplets in the rest of the block
            for m in re.findall(r"([\d\.]+)\s*m\s+([\d\.]+)\s*m\s+([\d\.]+)\s*m", rest):
                x, y, z = map(float, m)
                layout_coords.append({"X": x, "Y": y, "Z": z})
        print(f"✅ Extracted {len(layout_coords)} layout points")
        return layout_coords

    # -----------------------------------------------------
    # ROOM EXTRACTION
    # -----------------------------------------------------
    # def _extract_rooms(self, text: str, data: Dict[str, Any]):
    def _extract_rooms(self, text: str, data: Dict[str, Any], pdf_path: str):
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
        # coord_patterns = [
        #     r"(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m",  # Meters with unit labels
        #     r"(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm",  # Millimeters with unit labels
        #     r"X\s*[:\-]?\s*(\d+\.?\d*)\s*mm\s*Y\s*[:\-]?\s*(\d+\.?\d*)\s*mm\s*Z\s*[:\-]?\s*(\d+\.?\d*)\s*mm",  # Labeled mm coordinates
        #     r"X\s*[:\-]?\s*(\d+\.?\d*)\s*Y\s*[:\-]?\s*(\d+\.?\d*)\s*Z\s*[:\-]?\s*(\d+\.?\d*)"  # Labeled meter coordinates
        # ]

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
        # Iterate over each regex pattern designed to match room names in various formats
        for pattern in room_patterns:
            # Find all matches of the current pattern in the text (case-insensitive)
            matches = re.findall(pattern, text, re.IGNORECASE)
            # For each matched room name string
            for match in matches:
                # Normalize the matched room name using alias mapping or cleaning
                normalized = self.normalize_place(match)
                # Check if this normalized room name is already in the all_rooms list (avoid duplicates)
                if normalized not in [r["name"] for r in all_rooms]:
                    # If not already present, add it as a new room entry (dictionary with "name" key)
                    all_rooms.append({"name": normalized})
        # Extract and process coordinate data from all coordinate patterns
        all_coords = []
        # for coord_pattern in coord_patterns:
        #     matches = re.findall(coord_pattern, text, re.IGNORECASE)  # Case-insensitive matching
        #     for match in matches:
        #         try:
        #             # Extract X, Y, Z coordinate values and convert to float
        #             x, y, z = float(match[0]), float(match[1]), float(match[2])
                    
        #             # Unit conversion: check if pattern ends with "mm" (millimeter coordinates)
        #             if coord_pattern.endswith("mm"):
        #                 # Convert millimeters to meters (divide by 1000)
        #                 x, y, z = x/1000, y/1000, z/1000
                    
        #             # Add coordinate to collection with proper units (always in meters)
        #             all_coords.append({"x_m": x, "y_m": y, "z_m": z})
        #         except Exception:
        #             # Skip invalid coordinate matches (non-numeric values, conversion errors)
        #             continue

        # Extract structured layout coordinates using pdfplumber
        # all_coords = self._extract_layout(pdf_path)
        all_coords = self._extract_layout(text)

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
        # for r in data["rooms"]:
        #     unique[r["name"].lower()] = r  # Use lowercase name as key for deduplication

        for r in data["rooms"]:
            # clean_name = re.sub(r"\s+", " ", r["name"].strip().lower())
            clean = re.sub(r"[\W_]+", "", r["name"].lower())
            if clean not in unique:
                unique[clean] = r

        data["rooms"] = list(unique.values())  # Convert back to list of unique rooms

    # -----------------------------------------------------
    # SCENE EXTRACTION
    # -----------------------------------------------------
    def _extract_scenes(self, text: str, data: Dict[str, Any]):
        """
        Extract scene data (lighting performance metrics) from the report text.

        This function attempts to extract scene-related information such as average lux,
        minimum lux, maximum lux, uniformity, glare index, and other relevant metrics.
        It uses a robust regular expression to match common scene tables, and falls back
        to an alias-based search if the main pattern is not found.

        Args:
            text (str): The full extracted text from the PDF report.
            data (Dict[str, Any]): The main data dictionary to populate with scene info.

        Populates:
            data["scenes"]: A list of scene dictionaries, each containing extracted metrics.
        """

        # -----------------------------------------------------
        # 1. Attempt to extract scenes using a comprehensive regex pattern
        # -----------------------------------------------------
        # This pattern is designed to match scene tables with the following structure:
        #   [Scene Name] [Average Lux] [Min Lux] [Max Lux] [Uniformity] [G1] [Index]
        # It supports various label forms (e.g., Ē, Eavg, Average, E) and optional scene names.
        scene_pattern = re.compile(
            r"(?:([A-Za-z ]+)\s+)?"
            r"(?:(?:Ē|Eavg|Average|E)\s*[:=]?\s*)?([\d.]+)\s*lx?"      # Average lux
            r"[\s\n]+(?:(?:Emin|Min)?\s*[:=]?\s*)?([\d.]+)\s*lx?"      # Min lux
            r"[\s\n]+(?:(?:Emax|Max)?\s*[:=]?\s*)?([\d.]+)\s*lx?"      # Max lux
            r"[\s\n]+([\d.]+)"                                         # Uniformity (Uo)
            r"[\s\n]+([\d.]+)"                                         # G1 (glare index)
            r"[\s\n]+([A-Za-z0-9]+)",                                  # Index (e.g., CG1)
            re.UNICODE
        )

        # Find all matches of the scene pattern in the text
        matches = scene_pattern.findall(text)
        for sm in matches:
            # sm is a tuple: (scene_name, avg, emin, emax, uo, g1, index)
            # If scene name is missing, use a default label
            scene_name = sm[0].strip() if sm[0] else "Scene"
            avg, emin, emax, uo, g1, index = sm[1:]

            # Append the extracted scene data to the scenes list
            data["scenes"].append({
                "scene_name": scene_name,
                "average_lux": float(avg),
                "min_lux": float(emin),
                "max_lux": float(emax),
                "uniformity": float(uo),
                "g1": float(g1),
                "index": index
            })

        # -----------------------------------------------------
        # 2. Fallback: Use alias-based search if no scenes were found
        # -----------------------------------------------------
        # If the main regex did not match any scenes, try to extract scene metrics
        # by searching for each parameter using all known aliases.
        if not data["scenes"]:
            alias_scene = {}  # Temporary dict to collect found parameters

            # Iterate over all standard parameter names and their aliases
            for standard, variations in self.aliases["parameters"].items():
                for alias in variations:
                    # Search for the alias followed by a number (the value)
                    match = re.search(rf"{alias}\s*[:=]?\s*([\d.]+)", text, re.IGNORECASE)
                    if match:
                        # Store the value under the standard parameter name
                        alias_scene[standard] = float(match.group(1))
                        break  # Stop after the first matching alias for this parameter

            # If any parameters were found, create a default scene entry
            if alias_scene:
                alias_scene["scene_name"] = "Default Scene"
                data["scenes"].append(alias_scene)
    # -----------------------------------------------------
    # MASTER PARSER
    # -----------------------------------------------------
    # MAIN PARSING METHOD
    # -----------------------------------------------------
    def parse_report(self, text: str, pdf_path: str, filename: str = "report.pdf") -> Dict[str, Any]:
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
        # self._extract_metadata(text, data)           # Extract basic report information
        self._extract_metadata(text, data, pdf_path)           # Extract basic report information
        self._extract_lighting_setup(text, data)     # Extract lighting system configuration
        self._extract_luminaires(text, data)         # Extract fixture specifications
        # self._extract_rooms(text, data)              # Extract room layouts and coordinates
        self._extract_rooms(text, data, pdf_path)
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
        # TEMP DEBUG: Save extracted text to inspect structure
        debug_txt = os.path.splitext(os.path.basename(pdf_path))[0] + "_debug.txt"
        with open(debug_txt, "w", encoding="utf-8") as dbg:
            dbg.write(text)
        print(f"🧩 Saved extracted text to {debug_txt}")

        # Parse the extracted text into structured data
        return self.parse_report(text, pdf_path, os.path.basename(pdf_path))
    
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
        # If no PDF file path is provided, print a detailed error message in red and exit.
        # This prevents accidental processing with a hardcoded default file and ensures
        # the user is clearly informed about the correct usage.
        error_msg = (
            "\033[91m[ERROR]\033[0m No PDF file path provided.\n"
            "Usage: python final_extractor.py [pdf_file_path]\n"
            "Please specify the path to the PDF file you want to process."
        )
        print(error_msg)
        sys.exit(1)
    
    # Process the PDF and extract structured data
    result = extractor.process_report(pdf_path)

    # Generate output filename based on input PDF name
    out_file = f"{os.path.basename(pdf_path)}_extracted.json"
    
    # Save extracted data to JSON file with proper formatting
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)  # Pretty-print JSON with UTF-8 encoding

    print(f"✓ Results saved to {out_file}")
