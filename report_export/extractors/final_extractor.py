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
    """Final PDF extractor combining all approaches"""

    def __init__(self, alias_file: str = "aliases.json"):
        # Always resolve path relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alias_path = os.path.join(base_dir, alias_file)

        if not os.path.exists(alias_path):
            raise FileNotFoundError(f"Alias file not found: {alias_path}")

        self.text_extractors = [
            self._extract_with_pdfplumber,
            self._extract_with_pymupdf
        ]

        with open(alias_path, "r", encoding="utf-8") as f:
            self.aliases = json.load(f)

    # -----------------------------------------------------
    # TEXT EXTRACTION METHODS
    # -----------------------------------------------------
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
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
        text = ""
        try:
            pages = convert_from_path(pdf_path, dpi=300)
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
        except Exception as e:
            print(f"OCR error: {e}")
        return text.strip()

    def extract_text(self, pdf_path: str) -> str:
        for extractor in self.text_extractors:
            text = extractor(pdf_path)
            if text and len(text) > 50:
                return text
        return self._ocr_pdf(pdf_path)

    def process_report(self, pdf_path: str) -> Dict[str, Any]:
        """Main processing function"""
        print(f"Processing: {pdf_path}")
        
        # Extract text
        text = self.extract_text(pdf_path)
        print(f"Extracted {len(text)} characters")
        
        # Parse data
        data = self.parse_report(text, os.path.basename(pdf_path))
        
        return data

    # -----------------------------------------------------
    # NORMALIZATION USING ALIASES
    # -----------------------------------------------------
    def normalize_parameter(self, param: str) -> str:
        param = param.lower().strip()
        for standard, variations in self.aliases["parameters"].items():
            if param in [v.lower() for v in variations]:
                return standard
        return param

    def normalize_place(self, place: str) -> str:
        place = place.lower().strip()
        for standard, variations in self.aliases["places"].items():
            if place in [v.lower() for v in variations]:
                return standard
        return place

    # -----------------------------------------------------
    # METADATA EXTRACTION
    # -----------------------------------------------------
    def _extract_metadata(self, text: str, data: Dict[str, Any]):
        # Company name
        company_patterns = [
            r"(Company|Short\s*Cicuit|Short\s*Circuit).*?(?=\n|$)",
            r"Company\s*Name[:\-]?\s*(.+)",
            r"Short\s*Cicuit\s*Company"
        ]
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["metadata"]["company_name"] = match.group(0).strip()
                break

        # Project name
        project_patterns = [
            r"(Project\s*Name|Lighting study.*?)\n",
            r"Project\s*Name[:\-]?\s*(.+)",
            r"Lighting\s*study\s*for\s*(.+)"
        ]
        for pattern in project_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["metadata"]["project_name"] = match.group(0).strip()
                break

        # Engineer
        engineer_match = re.search(r"Eng\.\s*[A-Za-z ]+", text)
        if engineer_match:
            data["metadata"]["engineer"] = engineer_match.group(0).strip()

        # Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
        if email_match:
            data["metadata"]["email"] = email_match.group(0).strip()

    # -----------------------------------------------------
    # LIGHTING SETUP EXTRACTION
    # -----------------------------------------------------
    def _extract_lighting_setup(self, text: str, data: Dict[str, Any]):
        """Extract lighting setup, including DIALux-style blocks"""

        lighting_setup = {}

        # Capture DIALux property row
        match = re.search(
            r"([\d.]+)\s*lx\s+"     # average lux
            r"([\d.]+)\s*lx\s+"     # min lux
            r"([\d.]+)\s*lx\s+"     # max lux
            r"([\d.]+)\s+"          # Uo
            r"([\d.]+)\s+"          # g1
            r"([A-Za-z0-9]+)",      # Index (e.g., CG6)
            text
        )

        if match:
            avg, emin, emax, uo, g1, index = match.groups()
            lighting_setup.update({
                "average_lux": float(avg),
                "min_lux": float(emin),
                "max_lux": float(emax),
                "uniformity": float(uo),
                "g1": float(g1),
                "index": index
            })
        else:
            # Fallback old regexes
            avg_lux = re.search(r"(?:Avr\.?lux|Average\s*lux)[:\-]?\s*([\d.]+)", text, re.IGNORECASE)
            uniformity = re.search(r"(?:Uniformity|Uo)[:\-]?\s*([\d.]+)", text, re.IGNORECASE)
            if avg_lux:
                lighting_setup["average_lux"] = float(avg_lux.group(1))
            if uniformity:
                lighting_setup["uniformity"] = float(uniformity.group(1))

        data["lighting_setup"].update(lighting_setup)

    # -----------------------------------------------------
    # LUMINAIRE EXTRACTION
    # -----------------------------------------------------
    def _extract_luminaires(self, text: str, data: Dict[str, Any]):
        luminaire_matches = re.findall(
            r"(\d+)\s+([A-Za-z]+)\s+([A-Za-z0-9\- ]+)\s+(\d+\.?\d*)\s*W\s+(\d+\.?\d*)\s*lm\s+(\d+\.?\d*)\s*lm/W",
            text
        )
        for match in luminaire_matches:
            data["luminaires"].append({
                "quantity": int(match[0]),
                "manufacturer": match[1],
                "article_no": match[2],
                "power_w": float(match[3]),
                "luminous_flux_lm": float(match[4]),
                "efficacy_lm_per_w": float(match[5])
            })

    # -----------------------------------------------------
    # ROOM EXTRACTION
    # -----------------------------------------------------
    def _extract_rooms(self, text: str, data: Dict[str, Any]):
        """Extract room information with enhanced layout extraction"""

        # Room name patterns
        room_patterns = [
            r"(Building\s*\d+\s*·\s*Storey\s*\d+\s*·\s*Room\s*\d+)",
            r"(Building\s*\d+\s*Storey\s*\d+\s*Room\s*\d+)",
            r"(Room\s*\d+)",
            r"(Building\s*\d+.*?Room\s*\d+)"
        ]

        # Coordinate patterns
        # coord_patterns = [
        #     r"(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m",        # "4.000 m 36.002 m 7.000 m"
        #     r"(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)",            # "4.000, 36.002, 7.000"
        #     r"(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)",                    # "4.000 36.002 7.000"
        #     r"X[:\-]?\s*(\d+\.?\d*)\s*Y[:\-]?\s*(\d+\.?\d*)\s*Z[:\-]?\s*(\d+\.?\d*)",
        #     r"(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm"      # "4000.000 mm 36002.000 mm 7000.000 mm"
        # ]
        coord_patterns = [
            r"(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m\s+(\d+\.?\d*)\s*m",
            r"(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm\s+(\d+\.?\d*)\s*mm",
            r"X\s*[:\-]?\s*(\d+\.?\d*)\s*mm\s*Y\s*[:\-]?\s*(\d+\.?\d*)\s*mm\s*Z\s*[:\-]?\s*(\d+\.?\d*)\s*mm",
            r"X\s*[:\-]?\s*(\d+\.?\d*)\s*Y\s*[:\-]?\s*(\d+\.?\d*)\s*Z\s*[:\-]?\s*(\d+\.?\d*)"
        ]

        # Arrangement patterns
        arrangement_patterns = [
            r"Arrangement[:\-]?\s*([A-Za-z0-9]+)",
            r"Layout[:\-]?\s*([A-Za-z0-9]+)",
            r"Pattern[:\-]?\s*([A-Za-z0-9]+)",
            r"([A-Za-z0-9]+)\s*arrangement"
        ]

        # Collect rooms
        all_rooms = []
        for pattern in room_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match not in [r["name"] for r in all_rooms]:
                    all_rooms.append({"name": match.strip()})

        # Coordinates
        all_coords = []
        for coord_pattern in coord_patterns:
            matches = re.findall(coord_pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    x, y, z = float(match[0]), float(match[1]), float(match[2])
                    if coord_pattern.endswith("mm"):
                        x, y, z = x/1000, y/1000, z/1000
                    all_coords.append({"x_m": x, "y_m": y, "z_m": z})
                except Exception:
                    continue

        # Arrangements
        arrangements = []
        for pattern in arrangement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            arrangements.extend(matches)

        # Assign data
        for room in all_rooms:
            arrangement = arrangements[0] if arrangements else "A1"
            layout = all_coords.copy() if all_coords else []
            data["rooms"].append({
                "name": room["name"],
                "arrangement": arrangement,
                "layout": layout
            })

        if not data["rooms"]:
            data["rooms"].append({
                "name": "Building 1 · Storey 1 · Room 1",
                "arrangement": "A1",
                "layout": all_coords if all_coords else []
            })
        
        # Deduplicate rooms by name
        unique = {}
        for r in data["rooms"]:
            unique[r["name"].lower()] = r
        data["rooms"] = list(unique.values())

    # -----------------------------------------------------
    # SCENE EXTRACTION
    # -----------------------------------------------------
    def _extract_scenes(self, text: str, data: Dict[str, Any]):
        """Extract scene blocks with avg/min/max lux, uniformity, g1, index"""
        # scene_matches = re.findall(
        #     r"([A-Za-z ]+)\s+([\d.]+)\s*lx\s+([\d.]+)\s*lx\s+([\d.]+)\s*lx\s+([\d.]+)\s+([\d.]+)\s+([A-Za-z0-9]+)",
        #     text
        # )
        scene_matches = re.findall(
            r"(?:([A-Za-z ]+)\s+)?([\d.]+)\s*lx\s+([\d.]+)\s*lx\s+([\d.]+)\s*lx\s+([\d.]+)\s+([\d.]+)\s+([A-Za-z0-9]+)",
            text
        )

        for sm in scene_matches:
            # scene_name, avg, emin, emax, uo, g1, index = sm
            scene_name = sm[0].strip() if sm[0] else "Scene"
            avg, emin, emax, uo, g1, index = sm[1:]
            data["scenes"].append({
                "scene_name": scene_name.strip(),
                "average_lux": float(avg),
                "min_lux": float(emin),
                "max_lux": float(emax),
                "uniformity": float(uo),
                "g1": float(g1),
                "index": index
            })

        if not data["scenes"] and "lighting_setup" in data:
            setup = data["lighting_setup"]
            data["scenes"].append({
                "scene_name": "Default Scene",
                "average_lux": setup.get("average_lux"),
                "min_lux": setup.get("min_lux"),
                "max_lux": setup.get("max_lux"),
                "uniformity": setup.get("uniformity"),
                "g1": setup.get("g1"),
                "index": setup.get("index")
            })

    # -----------------------------------------------------
    # MASTER PARSER
    # -----------------------------------------------------
    def parse_report(self, text: str, filename: str = "report.pdf") -> Dict[str, Any]:
        data = {
            "metadata": {
                "company_name": None,
                "project_name": None,
                "engineer": None,
                "email": None,
                "report_title": filename
            },
            "lighting_setup": {},
            "luminaires": [],
            "rooms": [],
            "scenes": []
        }

        self._extract_metadata(text, data)
        self._extract_lighting_setup(text, data)
        self._extract_luminaires(text, data)
        self._extract_rooms(text, data)
        self._extract_scenes(text, data)

        return data

    def process_report(self, pdf_path: str) -> Dict[str, Any]:
        print(f"Processing: {pdf_path}")
        text = self.extract_text(pdf_path)
        print(f"Extracted {len(text)} characters")
        return self.parse_report(text, os.path.basename(pdf_path))

# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
if __name__ == "__main__":
    extractor = FinalPDFExtractor("aliases.json")
    # Get PDF path from command line argument or use default
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "El- Mohands _Report.pdf"
    result = extractor.process_report(pdf_path)

    out_file = f"{os.path.basename(pdf_path)}_extracted.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"✓ Results saved to {out_file}")
