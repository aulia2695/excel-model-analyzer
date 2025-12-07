"""
DEBUG SCRIPT - Check Excel File Structure
This will help us understand the exact column names
"""

import pandas as pd
from pathlib import Path

# Path configuration
script_dir = Path(__file__).parent.absolute()
test_dir = script_dir.parent
data_file = test_dir / "raw" / "test_2_farmer_development_raw.xlsx"

print("=" * 80)
print("DEBUGGING: CHECKING EXCEL FILE STRUCTURE")
print("=" * 80)

# Load data
try:
    df = pd.read_excel(data_file)
    print(f"\n✓ File loaded successfully!")
    print(f"  - Total rows: {len(df)}")
    print(f"  - Total columns: {len(df.columns)}")
except Exception as e:
    print(f"\n✗ ERROR loading file: {e}")
    exit(1)

# Print ALL column names with details
print("\n" + "=" * 80)
print("COLUMN NAMES IN YOUR EXCEL FILE:")
print("=" * 80)
for i, col in enumerate(df.columns, 1):
    # Show column name, type, and sample values
    sample_values = df[col].dropna().head(3).tolist()
    print(f"\n{i}. Column Name: '{col}'")
    print(f"   Data Type: {df[col].dtype}")
    print(f"   Non-null Count: {df[col].notna().sum()} / {len(df)}")
    print(f"   Sample Values: {sample_values}")

# Check for specific keywords
print("\n" + "=" * 80)
print("SEARCHING FOR KEY COLUMNS:")
print("=" * 80)

keywords_to_find = {
    'Farmer Code': ['farmer', 'code'],
    'Visit Number': ['visit', 'round', 'number'],
    'Variable': ['variable', 'practice'],
    'Result': ['result'],
    'Competence': ['competence', 'skill'],
    'Gender': ['gender', 'sex'],
    'Land Size': ['farm', 'area', 'land', 'ha'],
    'Production': ['production', 'yield', 'kg']
}

for key, keywords in keywords_to_find.items():
    print(f"\nLooking for '{key}' (keywords: {keywords}):")
    found = False
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in keywords:
            if keyword.lower() in col_lower:
                print(f"  ✓ FOUND: '{col}'")
                found = True
                break
        if found:
            break
    if not found:
        print(f"  ✗ NOT FOUND")

# Show first few rows
print("\n" + "=" * 80)
print("FIRST 5 ROWS OF DATA:")
print("=" * 80)
print(df.head())

# Check unique values for important columns
print("\n" + "=" * 80)
print("UNIQUE VALUES CHECK:")
print("=" * 80)

for col in df.columns:
    unique_count = df[col].nunique()
    if unique_count < 20:  # Only show if less than 20 unique values
        print(f"\n'{col}': {unique_count} unique values")
        print(f"  Values: {df[col].unique().tolist()}")

print("\n" + "=" * 80)
print("DEBUG COMPLETE!")
print("=" * 80)
print("\nPlease copy this output and share it so we can fix the script.")
