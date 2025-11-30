"""
Compliance Integration
=====================

Integrates with the compliance checker to verify generated reports
against lighting standards.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path to import compliance checker
sys.path.append(str(Path(__file__).parent.parent / "web-compliance"))

try:
    from compliance_checker import ComplianceChecker
except ImportError:
    # Fallback: try from final project
    sys.path.append(str(Path(__file__).parent.parent / "final project" / "src"))
    from compliance_checker import ComplianceChecker

class ComplianceIntegration:
    """
    Integrates compliance checking into the report generation process.
    
    Uses the existing compliance checker to verify that generated reports
    meet lighting standards requirements.
    """
    
    def __init__(self, standards_path: str, report_api_url: str = "http://localhost:5000"):
        """
        Initialize compliance integration.
        
        Args:
            standards_path: Path to standards_filtered.json
            report_api_url: URL of report API (not used for generated reports, but required for ComplianceChecker)
        """
        self.standards_path = standards_path
        self.compliance_checker = ComplianceChecker(standards_path, report_api_url)
    
    def check_compliance(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check compliance of generated report against standards.
        
        Args:
            report_data: Generated report data structure
            
        Returns:
            Compliance check results
        """
        try:
            # Use the compliance checker's check_compliance method
            compliance_result = self.compliance_checker.check_compliance(report_data)
            return compliance_result
        except Exception as e:
            # Return error result if compliance check fails
            return {
                'overall_compliance': 'ERROR',
                'checks': [],
                'summary': {
                    'total_rooms': 0,
                    'passed': 0,
                    'failed': 0,
                    'no_standard_found': 0,
                    'pass_rate': 0.0
                },
                'error': str(e),
                'timestamp': None
            }

