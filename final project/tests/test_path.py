#!/usr/bin/env python3
import os
import sys

# Test the path resolution
current_dir = os.path.dirname(__file__)
print(f"Current dir: {current_dir}")

# Test the path from api_server.py perspective
api_dir = os.path.dirname(os.path.join(current_dir, "src", "api_server.py"))
print(f"API dir: {api_dir}")

# Test the standards path
standards_path = os.path.join(api_dir, "..", "..", "standard_export", "output", "enhanced_standards.json")
print(f"Standards path: {standards_path}")
print(f"File exists: {os.path.exists(standards_path)}")

# Test absolute path
abs_path = os.path.abspath(standards_path)
print(f"Absolute path: {abs_path}")
print(f"Absolute file exists: {os.path.exists(abs_path)}")
