"""
Test Script for PDF Report Extractor
====================================

This script tests the PDF Report Extractor functionality
and validates the extracted data.
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from extractors.pdf_report_extractor import (
    PDFReportExtractor, 
    ReportData, 
    Metadata, 
    LightingSetup,
    Luminaire,
    Room,
    RoomLayout,
    Scene
)


class TestPDFReportExtractor(unittest.TestCase):
    """Test cases for PDF Report Extractor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = PDFReportExtractor()
        self.test_pdf_path = "NESSTRA Report With 150 watt.pdf"
    
    def test_extractor_initialization(self):
        """Test extractor initialization"""
        self.assertIsInstance(self.extractor, PDFReportExtractor)
        self.assertEqual(len(self.extractor.text_extractors), 2)
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "  This   is    a   test  \n\n\n  with   excessive   spaces  "
        clean_text = self.extractor._clean_text(dirty_text)
        expected = "This is a test with excessive spaces"
        self.assertEqual(clean_text, expected)
    
    def test_extract_metadata(self):
        """Test metadata extraction"""
        test_text = """
        Company Name: Short Cicuit Company
        Project Name: Lighting study for nesstra factory with HighBay light
        Eng. Mostafa Emad
        mostafaattalla122@gmail.com
        """
        
        metadata = self.extractor._extract_metadata(test_text)
        
        self.assertEqual(metadata.company_name, "Short Cicuit Company")
        self.assertEqual(metadata.project_name, "Lighting study for nesstra factory with HighBay light")
        self.assertEqual(metadata.engineer, "Mostafa Emad")
        self.assertEqual(metadata.email, "mostafaattalla122@gmail.com")
    
    def test_extract_lighting_setup(self):
        """Test lighting setup extraction"""
        test_text = """
        36 fixtures
        HighBay 150 watt
        mounting height 7.0m
        average lux: 673
        uniformity: 0.41
        total power: 5400.0W
        efficacy: 145.0 lm/w
        """
        
        setup = self.extractor._extract_lighting_setup(test_text)
        
        self.assertIsNotNone(setup)
        self.assertEqual(setup.number_of_fixtures, 36)
        self.assertEqual(setup.fixture_type, "HighBay 150 watt")
        self.assertEqual(setup.mounting_height_m, 7.0)
        self.assertEqual(setup.average_lux, 673)
        self.assertEqual(setup.uniformity, 0.41)
        self.assertEqual(setup.total_power_w, 5400.0)
        self.assertEqual(setup.luminous_efficacy_lm_per_w, 145.0)
    
    def test_extract_luminaires(self):
        """Test luminaire extraction"""
        test_text = """
        manufacturer: Philips
        article no: BY698P LED265CW G2 WB
        150 watt
        21750 lm
        145.0 lm/w
        quantity: 36
        """
        
        luminaires = self.extractor._extract_luminaires(test_text)
        
        self.assertEqual(len(luminaires), 1)
        luminaire = luminaires[0]
        self.assertEqual(luminaire.manufacturer, "Philips")
        self.assertEqual(luminaire.article_no, "BY698P LED265CW G2 WB")
        self.assertEqual(luminaire.power_w, 150.0)
        self.assertEqual(luminaire.luminous_flux_lm, 21750)
        self.assertEqual(luminaire.efficacy_lm_per_w, 145.0)
        self.assertEqual(luminaire.quantity, 36)
    
    def test_extract_scenes(self):
        """Test scene extraction"""
        test_text = """
        scene name: the factory
        average lux: 673
        min lux: 277
        max lux: 949
        uniformity: 0.41
        """
        
        scenes = self.extractor._extract_scenes(test_text)
        
        self.assertEqual(len(scenes), 1)
        scene = scenes[0]
        self.assertEqual(scene.scene_name, "the factory")
        self.assertEqual(scene.average_lux, 673)
        self.assertEqual(scene.min_lux, 277)
        self.assertEqual(scene.max_lux, 949)
        self.assertEqual(scene.uniformity, 0.41)
    
    @patch('pdfplumber.open')
    def test_extract_with_pdfplumber(self, mock_pdfplumber):
        """Test pdfplumber text extraction"""
        # Mock pdfplumber response
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test text from pdfplumber"
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        text = self.extractor._extract_with_pdfplumber("test.pdf")
        
        self.assertEqual(text, "Test text from pdfplumber")
        mock_pdfplumber.assert_called_once_with("test.pdf")
    
    @patch('fitz.open')
    def test_extract_with_pymupdf(self, mock_fitz):
        """Test PyMuPDF text extraction"""
        # Mock PyMuPDF response
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Test text from PyMuPDF"
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_doc.load_page.return_value = mock_page
        mock_fitz.return_value = mock_doc
        
        text = self.extractor._extract_with_pymupdf("test.pdf")
        
        self.assertEqual(text, "Test text from PyMuPDF")
        mock_fitz.assert_called_once_with("test.pdf")
    
    def test_save_to_json(self):
        """Test JSON saving functionality"""
        # Create test report data
        metadata = Metadata(
            company_name="Test Company",
            project_name="Test Project"
        )
        
        report_data = ReportData(
            metadata=metadata,
            raw_text="Test text"
        )
        
        # Save to JSON
        output_file = "test_output.json"
        self.extractor.save_to_json(report_data, output_file)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Verify content
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data['metadata']['company_name'], "Test Company")
        self.assertEqual(data['metadata']['project_name'], "Test Project")
        
        # Clean up
        os.remove(output_file)


class TestDataStructures(unittest.TestCase):
    """Test data structure classes"""
    
    def test_metadata_creation(self):
        """Test Metadata dataclass"""
        metadata = Metadata(
            company_name="Test Company",
            project_name="Test Project",
            engineer="Test Engineer",
            email="test@example.com"
        )
        
        self.assertEqual(metadata.company_name, "Test Company")
        self.assertEqual(metadata.project_name, "Test Project")
        self.assertEqual(metadata.engineer, "Test Engineer")
        self.assertEqual(metadata.email, "test@example.com")
    
    def test_lighting_setup_creation(self):
        """Test LightingSetup dataclass"""
        setup = LightingSetup(
            number_of_fixtures=36,
            fixture_type="HighBay 150 watt",
            mounting_height_m=7.0,
            average_lux=673,
            uniformity=0.41,
            total_power_w=5400.0,
            luminous_efficacy_lm_per_w=145.0
        )
        
        self.assertEqual(setup.number_of_fixtures, 36)
        self.assertEqual(setup.fixture_type, "HighBay 150 watt")
        self.assertEqual(setup.mounting_height_m, 7.0)
        self.assertEqual(setup.average_lux, 673)
        self.assertEqual(setup.uniformity, 0.41)
        self.assertEqual(setup.total_power_w, 5400.0)
        self.assertEqual(setup.luminous_efficacy_lm_per_w, 145.0)
    
    def test_luminaire_creation(self):
        """Test Luminaire dataclass"""
        luminaire = Luminaire(
            manufacturer="Philips",
            article_no="BY698P LED265CW G2 WB",
            power_w=150.0,
            luminous_flux_lm=21750,
            efficacy_lm_per_w=145.0,
            quantity=36
        )
        
        self.assertEqual(luminaire.manufacturer, "Philips")
        self.assertEqual(luminaire.article_no, "BY698P LED265CW G2 WB")
        self.assertEqual(luminaire.power_w, 150.0)
        self.assertEqual(luminaire.luminous_flux_lm, 21750)
        self.assertEqual(luminaire.efficacy_lm_per_w, 145.0)
        self.assertEqual(luminaire.quantity, 36)


def run_integration_test():
    """Run integration test with actual PDF file"""
    print("=" * 60)
    print("INTEGRATION TEST")
    print("=" * 60)
    
    extractor = PDFReportExtractor()
    pdf_path = "NESSTRA Report With 150 watt.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"✗ Integration test skipped - PDF file not found: {pdf_path}")
        return False
    
    try:
        # Process the actual PDF
        report_data = extractor.process_report(pdf_path)
        
        # Validate results
        print("✓ PDF processing completed")
        print(f"✓ Company: {report_data.metadata.company_name}")
        print(f"✓ Project: {report_data.metadata.project_name}")
        print(f"✓ Engineer: {report_data.metadata.engineer}")
        print(f"✓ Email: {report_data.metadata.email}")
        
        if report_data.lighting_setup:
            print(f"✓ Fixtures: {report_data.lighting_setup.number_of_fixtures}")
            print(f"✓ Average Lux: {report_data.lighting_setup.average_lux}")
        
        print(f"✓ Luminaires: {len(report_data.luminaires)}")
        print(f"✓ Rooms: {len(report_data.rooms)}")
        print(f"✓ Scenes: {len(report_data.scenes)}")
        
        # Save test output
        extractor.save_to_json(report_data, "integration_test_output.json")
        print("✓ Integration test output saved to: integration_test_output.json")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("PDF REPORT EXTRACTOR - TEST SUITE")
    print("=" * 60)
    
    # Run unit tests
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run integration test
    print("\n" + "=" * 60)
    run_integration_test()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
