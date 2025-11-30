import json
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'output')

# Read the standards.json file
input_file = os.path.join(output_dir, 'standards.json')
output_file = os.path.join(output_dir, 'standards_filtered.json')

with open(input_file, 'r', encoding='utf-8') as f:
    standards = json.load(f)

# Filter out entries that have any null values
filtered_standards = []
for entry in standards:
    # Check if any value in the entry is None/null
    has_null = any(value is None for value in entry.values())
    if not has_null:
        filtered_standards.append(entry)

# Write the filtered standards to a new file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_standards, f, indent=2, ensure_ascii=False)

print(f"Original entries: {len(standards)}")
print(f"Filtered entries (no nulls): {len(filtered_standards)}")
print(f"Removed entries: {len(standards) - len(filtered_standards)}")
print(f"Filtered file created: {output_file}")

