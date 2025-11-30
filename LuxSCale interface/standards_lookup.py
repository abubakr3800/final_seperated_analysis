"""
Standards Lookup
===============

Provides functionality to look up lighting standards based on room type
and return the required parameters.
"""

import json
from typing import Dict, Optional, List
from pathlib import Path

class StandardsLookup:
    """
    Looks up lighting standards and returns required parameters.
    """
    
    def __init__(self, standards_path: str):
        """
        Initialize standards lookup.
        
        Args:
            standards_path: Path to standards_filtered.json
        """
        self.standards_path = standards_path
        self.standards_data = self._load_standards()
    
    def _load_standards(self) -> Dict:
        """Load standards data"""
        try:
            with open(self.standards_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {'standards': data}
                elif isinstance(data, dict) and 'standards' in data:
                    return data
                else:
                    return {'standards': []}
        except Exception as e:
            print(f"Error loading standards: {e}")
            return {'standards': []}
    
    def find_standard(self, room_type: str) -> Optional[Dict]:
        """
        Find matching standard for a room type.
        
        Args:
            room_type: Room type / utilisation profile
            
        Returns:
            Matching standard or None
        """
        if not self.standards_data or 'standards' not in self.standards_data:
            return None
        
        room_type_lower = room_type.lower()
        
        # Try exact matches first
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            if task_activity == room_type_lower:
                if self._has_lighting_requirements(standard):
                    return standard
        
        # Try partial matches
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            category = standard.get('category', '') or ''
            category = category.lower()
            
            if (room_type_lower in task_activity or 
                room_type_lower in category or
                any(keyword in task_activity for keyword in room_type_lower.split())):
                if self._has_lighting_requirements(standard):
                    return standard
        
        # Try keyword matches
        if any(keyword in room_type_lower for keyword in ['factory', 'industrial', 'warehouse', 'manufacturing']):
            for standard in self.standards_data['standards']:
                task_activity = standard.get('task_or_activity', '') or ''
                task_activity = task_activity.lower()
                if any(keyword in task_activity for keyword in ['industrial', 'factory', 'warehouse', 'manufacturing']):
                    if self._has_lighting_requirements(standard):
                        return standard
        
        # Try general matches
        for standard in self.standards_data['standards']:
            task_activity = standard.get('task_or_activity', '') or ''
            task_activity = task_activity.lower()
            if any(keyword in task_activity for keyword in ['general', 'work', 'office']):
                if self._has_lighting_requirements(standard):
                    return standard
        
        return None
    
    def _has_lighting_requirements(self, standard: Dict) -> bool:
        """Check if standard has lighting requirements"""
        lighting_fields = ['Em_r_lx', 'Em_u_lx', 'Uo', 'Ra', 'RUGL', 'Ez_lx', 'Em_wall_lx', 'Em_ceiling_lx']
        for field in lighting_fields:
            value = standard.get(field)
            if value is not None and value != 0:
                return True
        return False
    
    def get_required_parameters(self, room_type: str) -> Dict:
        """
        Get required parameters for a room type.
        
        Args:
            room_type: Room type / utilisation profile
            
        Returns:
            Dictionary with required parameters
        """
        standard = self.find_standard(room_type)
        
        if not standard:
            return {
                'found': False,
                'message': 'No standard found for this room type'
            }
        
        return {
            'found': True,
            'standard': {
                'ref_no': standard.get('ref_no', ''),
                'category': standard.get('category', ''),
                'task_or_activity': standard.get('task_or_activity', '')
            },
            'requirements': {
                'em_r_lx': standard.get('Em_r_lx'),
                'em_u_lx': standard.get('Em_u_lx'),
                'uo': standard.get('Uo'),
                'ra': standard.get('Ra'),
                'rugl': standard.get('RUGL'),
                'ez_lx': standard.get('Ez_lx'),
                'em_wall_lx': standard.get('Em_wall_lx'),
                'em_ceiling_lx': standard.get('Em_ceiling_lx')
            },
            'specific_requirements': standard.get('specific_requirements', '')
        }

