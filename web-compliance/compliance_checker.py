"""
Lighting Compliance Checker
===========================

This module integrates the report_export and standard_export projects to provide
lighting compliance checking functionality.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests
from datetime import datetime

class ComplianceChecker:
    def __init__(self, standards_path: str, report_api_url: str = "http://localhost:5000"):
        """
        Initialize the compliance checker
        
        Args:
            standards_path: Path to the complete_standards.json file
            report_api_url: URL of the report extraction API
        """
        self.standards_path = standards_path
        self.report_api_url = report_api_url
        self.standards_data = self._load_standards()
        self.parameter_mapping = self._load_parameter_mapping()
        
    def _load_standards(self) -> Dict:
        """Load standards data from JSON file"""
        try:
            with open(self.standards_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle both formats:
            # 1. Direct array format (standards_filtered.json)
            if isinstance(data, list):
                return {'standards': data}
            # 2. Dictionary with metadata wrapper (enhanced_standards.json)
            elif isinstance(data, dict) and 'standards' in data:
                return data
            # 3. Fallback: treat as single standard or empty
            else:
                return {'standards': [] if not isinstance(data, list) else data}
        except Exception as e:
            print(f"Error loading standards: {e}")
            return {'standards': []}
    
    def _load_parameter_mapping(self) -> Dict:
        """Load parameter mapping from aliases.json file"""
        try:
            # Method 1: Relative path from this file (web-compliance folder)
            current_file = Path(__file__).resolve()
            # From: web-compliance/compliance_checker.py
            # To: report_export/extractors/aliases.json
            # Go: web-compliance -> final_comparator -> report_export/extractors/aliases.json
            project_root = current_file.parent.parent  # final_comparator root
            aliases_file = project_root / "report_export" / "extractors" / "aliases.json"
            
            # Method 2: Try absolute path
            if not aliases_file.exists():
                absolute_path = Path(r"E:\AI_projects\final_comparator\report_export\extractors\aliases.json")
                if absolute_path.exists():
                    aliases_file = absolute_path
            
            # Method 3: Try from current working directory
            if not aliases_file.exists():
                cwd = Path(os.getcwd())
                # Check if we're in final_comparator or a subdirectory
                if "final_comparator" in str(cwd):
                    # Find final_comparator in the path
                    parts = cwd.parts
                    try:
                        idx = parts.index("final_comparator")
                        root = Path(*parts[:idx+1])
                        aliases_file = root / "report_export" / "extractors" / "aliases.json"
                    except ValueError:
                        # If not found, try direct path from cwd
                        aliases_file = cwd / "report_export" / "extractors" / "aliases.json"
                        if not aliases_file.exists() and cwd.name != "final_comparator":
                            # Go up to find final_comparator
                            for parent in cwd.parents:
                                if parent.name == "final_comparator":
                                    aliases_file = parent / "report_export" / "extractors" / "aliases.json"
                                    break
            
            if aliases_file.exists():
                with open(aliases_file, 'r', encoding='utf-8') as f:
                    aliases = json.load(f)
                    print(f"✓ Loaded aliases from {aliases_file}")
                    return aliases
            else:
                print(f"⚠️ No alias file found, using empty mapping")
                print(f"   Tried: {aliases_file}")
                return {"places": {}, "parameters": {}}
        except Exception as e:
            print(f"Error loading parameter mapping: {e}")
            import traceback
            traceback.print_exc()
            return {"places": {}, "parameters": {}}
    
    def extract_report_data(self, pdf_file_path: str) -> Dict:
        """
        Extract data from PDF report using the report_export API
        
        Args:
            pdf_file_path: Path to the PDF file
            
        Returns:
            Extracted report data
        """
        try:
            with open(pdf_file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.report_api_url}/extract", files=files)
                
            if response.status_code == 200:
                return response.json()['extracted_data']
            else:
                raise Exception(f"API error: {response.json()}")
                
        except Exception as e:
            print(f"Error extracting report data: {e}")
            return {}
    
    def find_matching_standard(self, utilisation_profile: str) -> Optional[Dict]:
        """
        Find matching standard based on utilisation profile
        
        Args:
            utilisation_profile: The utilisation profile from the report
            
        Returns:
            Matching standard or None
        """
        if not self.standards_data or 'standards' not in self.standards_data:
            return None
            
        utilisation_lower = utilisation_profile.lower()
        
        # First try exact matches with uniformity requirements
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            if task_activity == utilisation_lower:
                # Prioritize standards that have uniformity requirements
                if self._has_lighting_requirements(standard) and self._has_uniformity_requirement(standard):
                    return standard
        
        # If no exact match with uniformity, try exact matches without uniformity
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            if task_activity == utilisation_lower:
                # Only return standards that have actual lighting requirements
                if self._has_lighting_requirements(standard):
                    return standard
        
        # Then try partial matches
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            category = standard.get('category', '') or ''
            category = category.lower()
            
            # Check for matches in task_or_activity or category
            if (utilisation_lower in task_activity or 
                utilisation_lower in category or
                any(keyword in task_activity for keyword in utilisation_lower.split())):
                # Prioritize standards that have uniformity requirements
                if self._has_lighting_requirements(standard) and self._has_uniformity_requirement(standard):
                    return standard
        
        # Try to find industrial work standards for factory/industrial profiles
        if any(keyword in utilisation_lower for keyword in ['factory', 'industrial', 'warehouse', 'manufacturing']):
            for standard in self.standards_data['standards']:
                task_activity = standard.get('task_or_activity', '') or ''
                task_activity = task_activity.lower()
                if any(keyword in task_activity for keyword in ['industrial', 'factory', 'warehouse', 'manufacturing']):
                    if self._has_lighting_requirements(standard):
                        return standard
        
        # Try to find general work standards with uniformity
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            if any(keyword in task_activity for keyword in ['general', 'work', 'office']):
                if self._has_lighting_requirements(standard) and self._has_uniformity_requirement(standard):
                    return standard
        
        # Final fallback: find any standard with uniformity requirements
        for standard in self.standards_data['standards']:
            if self._has_lighting_requirements(standard) and self._has_uniformity_requirement(standard):
                return standard
                
        return None
    
    def _has_lighting_requirements(self, standard: Dict) -> bool:
        """Check if a standard has actual lighting requirements"""
        # Check if the standard has any non-null lighting values
        lighting_fields = ['Em_r_lx', 'Em_u_lx', 'Uo', 'Ra', 'RUGL', 'Ez_lx', 'Em_wall_lx', 'Em_ceiling_lx']
        
        for field in lighting_fields:
            value = standard.get(field)
            if value is not None and value != 0:
                return True
        
        return False
    
    def _has_uniformity_requirement(self, standard: Dict) -> bool:
        """Check if a standard has uniformity requirements"""
        uo_value = standard.get('Uo')
        return uo_value is not None and uo_value != 0
    
    def _find_parameter_value(self, data: Dict, parameter_type: str) -> Dict:
        """
        Find parameter value using comprehensive alias mapping from aliases.json
        
        This method searches for parameter values using all known aliases,
        allowing flexible parameter name recognition in extracted reports.
        
        Args:
            data: Dictionary containing extracted report data
            parameter_type: Standard parameter name (e.g., 'average_lux', 'uniformity')
            
        Returns:
            Dict with 'found', 'source', and 'value' keys
        """
        if not self.parameter_mapping or 'parameters' not in self.parameter_mapping:
            return {'found': False, 'source': None, 'value': None}
        
        # Get all aliases for this parameter type
        parameter_aliases = self.parameter_mapping['parameters'].get(parameter_type, [])
        
        # First, try direct match with standard name
        if parameter_type in data and data[parameter_type] is not None:
            return {'found': True, 'source': parameter_type, 'value': data[parameter_type]}
        
        # Then try all aliases
        for alias in parameter_aliases:
            # Try exact match (case-sensitive)
            if alias in data and data[alias] is not None:
                return {'found': True, 'source': alias, 'value': data[alias]}
            
            # Try case-insensitive match
            for key in data.keys():
                if key.lower() == alias.lower() and data[key] is not None:
                    return {'found': True, 'source': key, 'value': data[key]}
            
            # Try partial match (alias is substring of key)
            for key in data.keys():
                if alias.lower() in key.lower() and data[key] is not None:
                    return {'found': True, 'source': key, 'value': data[key]}
        
        return {'found': False, 'source': None, 'value': None}
    
    def check_compliance(self, report_data: Dict) -> Dict:
        """
        Check compliance of report data against standards
        
        Args:
            report_data: Extracted report data
            
        Returns:
            Compliance check results
        """
        results = {
            'overall_compliance': 'UNKNOWN',
            'checks': [],
            'summary': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Extract lighting setup data
            lighting_setup = report_data.get('lighting_setup', {})
            rooms = report_data.get('rooms', [])
            scenes = report_data.get('scenes', [])
            
            if not rooms:
                results['overall_compliance'] = 'ERROR'
                results['error'] = 'No room data found in report'
                return results
            
            # Check each room
            for room_index, room in enumerate(rooms):
                utilisation_profile = room.get('utilisation_profile', '')
                
                # If no utilisation profile in room, try to get from scenes
                if not utilisation_profile:
                    if scenes:
                        # Try to match room to scene by index
                        scene_data = None
                        if room_index < len(scenes):
                            scene_data = scenes[room_index]
                        else:
                            # Fallback to first scene
                            scene_data = scenes[0] if scenes else None
                        
                        if scene_data:
                            scene_name = scene_data.get('scene_name', '').lower()
                            scene_profile = scene_data.get('utilisation_profile', '')
                            
                            # Check scene name for factory/industrial spaces
                            if any(keyword in scene_name for keyword in ['factory', 'industrial', 'warehouse', 'manufacturing', 'production']):
                                # For factory scenes, use industrial standards
                                utilisation_profile = 'Industrial activities and crafts'
                            elif scene_profile:
                                # Use the scene's utilisation profile if it exists
                                utilisation_profile = scene_profile
                            elif 'working place' in scene_name or 'work' in scene_name:
                                # For working places, use general industrial
                                utilisation_profile = 'Industrial activities and crafts'
                
                # If still no utilisation profile, try to infer from room name
                if not utilisation_profile:
                    room_name = room.get('name', '') or ''
                    room_name_lower = room_name.lower()
                    
                    # Check for factory/industrial keywords
                    if any(keyword in room_name_lower for keyword in ['factory', 'industrial', 'warehouse', 'manufacturing', 'production', 'workshop']):
                        utilisation_profile = 'Industrial activities and crafts'
                    elif 'office' in room_name_lower:
                        utilisation_profile = 'Offices'
                    elif 'corridor' in room_name_lower or 'hallway' in room_name_lower:
                        utilisation_profile = 'Traffic zones inside buildings'
                    elif 'storage' in room_name_lower or 'store' in room_name_lower:
                        utilisation_profile = 'General areas inside buildings – Store rooms, cold stores'
                    elif 'building' in room_name_lower or 'room' in room_name_lower:
                        # For generic building/room names in factory context, use industrial
                        # Check project name or other context
                        project_name = report_data.get('metadata', {}).get('project_name', '').lower()
                        if any(keyword in project_name for keyword in ['factory', 'industrial', 'warehouse']):
                            utilisation_profile = 'Industrial activities and crafts'
                        else:
                            utilisation_profile = 'General areas inside buildings'
                    else:
                        # Default fallback
                        utilisation_profile = 'General areas inside buildings'
                
                if not utilisation_profile:
                    continue
                    
                # Find matching standard
                standard = self.find_matching_standard(utilisation_profile)
                if not standard:
                    results['checks'].append({
                        'room': room.get('name', 'Unknown'),
                        'utilisation_profile': utilisation_profile,
                        'status': 'NO_STANDARD_FOUND',
                        'message': 'No matching standard found'
                    })
                    continue
                
                # Find corresponding scene data for this room
                scene_data = None
                if scenes:
                    # Try to match room with scene by index or name
                    room_index = rooms.index(room)
                    if room_index < len(scenes):
                        scene_data = scenes[room_index]
                    else:
                        # Fallback to first scene if no direct match
                        scene_data = scenes[0]
                
                # Use scene data if available, otherwise use lighting_setup
                lighting_data = scene_data if scene_data else lighting_setup
                
                # Perform compliance checks
                check_result = self._perform_room_compliance_check(room, standard, lighting_data)
                results['checks'].append(check_result)
            
            # Determine overall compliance
            results['overall_compliance'] = self._determine_overall_compliance(results['checks'])
            results['summary'] = self._generate_summary(results['checks'])
            
        except Exception as e:
            results['overall_compliance'] = 'ERROR'
            results['error'] = str(e)
            
        return results
    
    def _perform_room_compliance_check(self, room: Dict, standard: Dict, lighting_setup: Dict) -> Dict:
        """Perform compliance check for a single room"""
        check_result = {
            'room': room.get('name', 'Unknown'),
            'utilisation_profile': room.get('utilisation_profile', ''),
            'standard': {
                'ref_no': standard.get('ref_no', ''),
                'category': standard.get('category', ''),
                'task_or_activity': standard.get('task_or_activity', '')
            },
            'checks': {},
            'status': 'PASS'
        }
        
        # Get values from report using alias mapping
        # Try to find average_lux using aliases
        avg_lux_result = self._find_parameter_value(lighting_setup, 'average_lux')
        average_lux = avg_lux_result['value'] if avg_lux_result['found'] else lighting_setup.get('average_lux', 0)
        
        # Try to find uniformity using aliases
        uniformity_result = self._find_parameter_value(lighting_setup, 'uniformity')
        uniformity = uniformity_result['value'] if uniformity_result['found'] else lighting_setup.get('uniformity', 0)
        
        # Check for Ra/CRI using comprehensive parameter mapping
        ra = self._find_parameter_value(lighting_setup, 'color_rendering_ra')
        ra_found = ra['found']
        ra_source = ra['source']
        ra_value = ra['value'] if ra_found else None
        
        # Get required values from standard
        required_lux = standard.get('Em_r_lx', 0) or standard.get('Em_u_lx', 0) or 0
        required_uniformity = standard.get('Uo', 0) or 0
        required_ra = standard.get('Ra', 0) or 0
        
        # Check lux compliance
        if required_lux > 0:
            lux_compliance = average_lux >= required_lux
            check_result['checks']['lux'] = {
                'required': required_lux,
                'actual': average_lux,
                'compliant': lux_compliance,
                'margin': average_lux - required_lux if lux_compliance else required_lux - average_lux
            }
            if not lux_compliance:
                check_result['status'] = 'FAIL'
        
        # Check uniformity compliance
        if required_uniformity > 0:
            uniformity_compliance = uniformity >= required_uniformity
            check_result['checks']['uniformity'] = {
                'required': required_uniformity,
                'actual': uniformity,
                'compliant': uniformity_compliance,
                'margin': uniformity - required_uniformity if uniformity_compliance else required_uniformity - uniformity
            }
            if not uniformity_compliance:
                check_result['status'] = 'FAIL'
        
        # Check Ra compliance (informational only - doesn't affect pass/fail)
        if required_ra > 0:
            if ra_found:
                ra_compliance = ra_value >= required_ra
                check_result['checks']['ra'] = {
                    'required': required_ra,
                    'actual': ra_value,
                    'compliant': ra_compliance,
                    'margin': ra_value - required_ra if ra_compliance else required_ra - ra_value,
                    'found': True,
                    'source': ra_source,
                    'note': f'Found as {ra_source}'
                }
            else:
                check_result['checks']['ra'] = {
                    'required': required_ra,
                    'actual': None,
                    'compliant': None,
                    'margin': None,
                    'found': False,
                    'source': None,
                    'note': f'Ra/CRI not found in report (checked: {", ".join(self.parameter_mapping["parameters"].get("color_rendering_ra", []))})'
                }
            # Note: Ra compliance doesn't affect overall status - it's informational only
        
        return check_result
    
    def _determine_overall_compliance(self, checks: List[Dict]) -> str:
        """Determine overall compliance status"""
        if not checks:
            return 'NO_CHECKS'
        
        statuses = [check['status'] for check in checks]
        
        if 'FAIL' in statuses:
            return 'FAIL'
        elif 'NO_STANDARD_FOUND' in statuses:
            return 'PARTIAL'
        elif all(status == 'PASS' for status in statuses):
            return 'PASS'
        else:
            return 'UNKNOWN'
    
    def _generate_summary(self, checks: List[Dict]) -> Dict:
        """Generate summary statistics"""
        total_checks = len(checks)
        passed = sum(1 for check in checks if check['status'] == 'PASS')
        failed = sum(1 for check in checks if check['status'] == 'FAIL')
        no_standard = sum(1 for check in checks if check['status'] == 'NO_STANDARD_FOUND')
        
        return {
            'total_rooms': total_checks,
            'passed': passed,
            'failed': failed,
            'no_standard_found': no_standard,
            'pass_rate': (passed / total_checks * 100) if total_checks > 0 else 0
        }
    
    def process_report(self, pdf_file_path: str) -> Dict:
        """
        Complete process: extract report data and check compliance
        
        Args:
            pdf_file_path: Path to the PDF file
            
        Returns:
            Complete compliance report
        """
        # Extract report data
        report_data = self.extract_report_data(pdf_file_path)
        if not report_data:
            return {
                'error': 'Failed to extract report data',
                'timestamp': datetime.now().isoformat()
            }
        
        # Check compliance
        compliance_result = self.check_compliance(report_data)
        
        return {
            'report_data': report_data,
            'compliance_result': compliance_result,
            'timestamp': datetime.now().isoformat()
        }

