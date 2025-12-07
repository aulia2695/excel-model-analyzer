"""
Farmer Development Plan Analysis - Exercise 1
Analyzes farmer demographics, adoption practices, and production data
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Define paths
BASE_PATH = Path("excel-data/test-2-farmer-development")
RAW_PATH = BASE_PATH / "raw" / "test_2_farmer_development_raw.xlsx"
CLEANED_PATH = BASE_PATH / "cleaned"
RESULTS_PATH = BASE_PATH / "results"

# Create directories if they don't exist
CLEANED_PATH.mkdir(parents=True, exist_ok=True)
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("FARMER DEVELOPMENT PLAN ANALYSIS - EXERCISE 1")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD AND CLEAN DATA
# ============================================================================
print("\n[STEP 1] Loading raw data...")

try:
    df = pd.read_excel(RAW_PATH)
    print(f"✓ Loaded {len(df)} records from raw data")
    print(f"✓ Columns: {list(df.columns)}")
except FileNotFoundError:
    print(f"✗ ERROR: File not found at {RAW_PATH}")
    print("Please ensure the Excel file exists at the correct path")
    exit(1)

# Display basic info
print(f"\n✓ Total records: {len(df)}")
print(f"✓ Unique farmers: {df['Farmer: Farmer Code'].nunique()}")
print(f"✓ Visit numbers: {sorted(df['Visit Number'].unique())}")

# ============================================================================
# STEP 2: DATA CLEANING
# ============================================================================
print("\n[STEP 2] Cleaning data...")

# Create a copy for cleaning
df_clean = df.copy()

# Clean column names (remove extra spaces)
df_clean.columns = df_clean.columns.str.strip()

# Data quality checks
quality_issues = []

# Check for missing critical fields
critical_fields = ['Farmer: Farmer Code', 'Visit Number', 'Variable', 'Result', 'Competence']
for field in critical_fields:
    missing_count = df_clean[field].isna().sum()
    if missing_count > 0:
        quality_issues.append(f"Missing {field}: {missing_count} records")

# Check Result and Competence values (should be 0, 1, or 2)
if 'Result' in df_clean.columns:
    invalid_result = df_clean[~df_clean['Result'].isin([0, 1, 2, np.nan])]['Result'].unique()
    if len(invalid_result) > 0:
        quality_issues.append(f"Invalid Result values: {invalid_result}")

if 'Competence' in df_clean.columns:
    invalid_comp = df_clean[~df_clean['Competence'].isin([0, 1, 2, np.nan])]['Competence'].unique()
    if len(invalid_comp) > 0:
        quality_issues.append(f"Invalid Competence values: {invalid_comp}")

# Check Land Area (should be positive)
if 'Farm: Total Farm Area HA' in df_clean.columns:
    negative_area = (df_clean['Farm: Total Farm Area HA'] < 0).sum()
    if negative_area > 0:
        quality_issues.append(f"Negative land area: {negative_area} records")

# Check Production (should be positive)
if 'Farm: Production - last baseline KG' in df_clean.columns:
    negative_prod = (df_clean['Farm: Production - last baseline KG'] < 0).sum()
    if negative_prod > 0:
        quality_issues.append(f"Negative production: {negative_prod} records")

# Print quality issues
if quality_issues:
    print("\n⚠ DATA QUALITY ISSUES FOUND:")
    for issue in quality_issues:
        print(f"  - {issue}")
else:
    print("✓ No major data quality issues detected")

# Remove duplicates
initial_count = len(df_clean)
df_clean = df_clean.drop_duplicates()
if len(df_clean) < initial_count:
    print(f"✓ Removed {initial_count - len(df_clean)} duplicate records")

# Save cleaned data
cleaned_file = CLEANED_PATH / "farmer_development_cleaned.csv"
df_clean.to_csv(cleaned_file, index=False)
print(f"\n✓ Cleaned data saved to: {cleaned_file}")

# ============================================================================
# ANALYSIS 1.1: BASELINE DISTRIBUTION (Good/Medium/Bad)
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1.1: BASELINE DISTRIBUTION (Result & Competence)")
print("=" * 80)

# Map values to categories
category_map = {0: 'Bad (B)', 1: 'Medium (M)', 2: 'Good (G)'}

# Analysis by Variable for Result
result_dist = df_clean.groupby(['Variable', 'Result']).size().reset_index(name='Count')
result_dist['Category'] = result_dist['Result'].map(category_map)
result_pivot = result_dist.pivot_table(
    index='Variable', 
    columns='Category', 
    values='Count', 
    fill_value=0
)

# Calculate percentages
result_pivot_pct = result_pivot.div(result_pivot.sum(axis=1), axis=0) * 100
result_pivot_pct = result_pivot_pct.round(1)

print("\n📊 RESULT (Current Adoption) Distribution:")
print(result_pivot_pct)

# Analysis by Variable for Competence
comp_dist = df_clean.groupby(['Variable', 'Competence']).size().reset_index(name='Count')
comp_dist['Category'] = comp_dist['Competence'].map(category_map)
comp_pivot = comp_dist.pivot_table(
    index='Variable', 
    columns='Category', 
    values='Count', 
    fill_value=0
)

# Calculate percentages
comp_pivot_pct = comp_pivot.div(comp_pivot.sum(axis=1), axis=0) * 100
comp_pivot_pct = comp_pivot_pct.round(1)

print("\n📊 COMPETENCE (Skillset) Distribution:")
print(comp_pivot_pct)

# Save results
result_pivot_pct.to_csv(RESULTS_PATH / "1_1_result_distribution.csv")
comp_pivot_pct.to_csv(RESULTS_PATH / "1_1_competence_distribution.csv")

# ============================================================================
# ANALYSIS 1.2: PROGRESS TRACKING (Visit 1 vs Visit 2)
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1.2: PROGRESS TRACKING (Visit 1 vs Visit 2)")
print("=" * 80)

# Filter for farmers with both visits
visit1 = df_clean[df_clean['Visit Number'] == 1].copy()
visit2 = df_clean[df_clean['Visit Number'] == 2].copy()

# Merge on Farmer Code and Variable
progress_df = visit1.merge(
    visit2,
    on=['Farmer: Farmer Code', 'Variable'],
    suffixes=('_V1', '_V2'),
    how='inner'
)

print(f"\n✓ Analyzing {len(progress_df)} farmer-variable pairs with both visits")

# Calculate progress for Result
progress_df['Result_Change'] = progress_df['Result_V2'] - progress_df['Result_V1']
progress_df['Result_Progress'] = progress_df['Result_Change'].apply(
    lambda x: 'Making Progress' if x > 0 else ('Staying Same' if x == 0 else 'Deteriorating')
)

# Calculate progress for Competence
progress_df['Competence_Change'] = progress_df['Competence_V2'] - progress_df['Competence_V1']
progress_df['Competence_Progress'] = progress_df['Competence_Change'].apply(
    lambda x: 'Making Progress' if x > 0 else ('Staying Same' if x == 0 else 'Deteriorating')
)

# Summary statistics for Result
result_progress = progress_df['Result_Progress'].value_counts()
result_progress_pct = (result_progress / len(progress_df) * 100).round(1)

print("\n📈 RESULT Progress Summary:")
for status, pct in result_progress_pct.items():
    count = result_progress[status]
    print(f"  {status}: {pct}% ({count} farmers)")

# Summary statistics for Competence
comp_progress = progress_df['Competence_Progress'].value_counts()
comp_progress_pct = (comp_progress / len(progress_df) * 100).round(1)

print("\n📈 COMPETENCE Progress Summary:")
for status, pct in comp_progress_pct.items():
    count = comp_progress[status]
    print(f"  {status}: {pct}% ({count} farmers)")

# Save detailed progress data
progress_summary = pd.DataFrame({
    'Metric': ['Result', 'Result', 'Result', 'Competence', 'Competence', 'Competence'],
    'Status': ['Making Progress', 'Staying Same', 'Deteriorating'] * 2,
    'Count': [
        result_progress.get('Making Progress', 0),
        result_progress.get('Staying Same', 0),
        result_progress.get('Deteriorating', 0),
        comp_progress.get('Making Progress', 0),
        comp_progress.get('Staying Same', 0),
        comp_progress.get('Deteriorating', 0)
    ],
    'Percentage': [
        result_progress_pct.get('Making Progress', 0),
        result_progress_pct.get('Staying Same', 0),
        result_progress_pct.get('Deteriorating', 0),
        comp_progress_pct.get('Making Progress', 0),
        comp_progress_pct.get('Staying Same', 0),
        comp_progress_pct.get('Deteriorating', 0)
    ]
})

progress_summary.to_csv(RESULTS_PATH / "1_2_progress_tracking.csv", index=False)

# ============================================================================
# ANALYSIS 1.3: PRODUCTION BY GENDER AND LAND SIZE
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1.3: AVERAGE PRODUCTION (YIELD) SEGMENTATION")
print("=" * 80)

# Get unique farmer data (avoid duplicates from multiple variables)
farmer_data = df_clean[['Farmer: Farmer Code', 'Farmer: Gender', 
                        'Farm: Total Farm Area HA', 
                        'Farm: Production - last baseline KG']].drop_duplicates()

# A) Average Production by Gender
print("\n📊 Average Production by GENDER:")
gender_prod = farmer_data.groupby('Farmer: Gender')['Farm: Production - last baseline KG'].agg([
    ('Count', 'count'),
    ('Average_KG', 'mean'),
    ('Median_KG', 'median'),
    ('Std_Dev', 'std')
]).round(2)
print(gender_prod)

# B) Average Production by Land Size
# Create land size categories
farmer_data['Land_Category'] = pd.cut(
    farmer_data['Farm: Total Farm Area HA'],
    bins=[0, 2, 4, float('inf')],
    labels=['<2ha', '2-4ha', '≥4ha'],
    right=False
)

print("\n📊 Average Production by LAND SIZE:")
landsize_prod = farmer_data.groupby('Land_Category')['Farm: Production - last baseline KG'].agg([
    ('Count', 'count'),
    ('Average_KG', 'mean'),
    ('Median_KG', 'median'),
    ('Std_Dev', 'std')
]).round(2)
print(landsize_prod)

# Calculate yield per hectare
farmer_data['Yield_per_HA'] = (
    farmer_data['Farm: Production - last baseline KG'] / 
    farmer_data['Farm: Total Farm Area HA']
)

print("\n📊 Average YIELD PER HECTARE by Land Size:")
yield_per_ha = farmer_data.groupby('Land_Category')['Yield_per_HA'].agg([
    ('Count', 'count'),
    ('Average_KG_per_HA', 'mean'),
    ('Median_KG_per_HA', 'median')
]).round(2)
print(yield_per_ha)

# Save results
gender_prod.to_csv(RESULTS_PATH / "1_3_production_by_gender.csv")
landsize_prod.to_csv(RESULTS_PATH / "1_3_production_by_landsize.csv")
yield_per_ha.to_csv(RESULTS_PATH / "1_3_yield_per_hectare.csv")

# ============================================================================
# ANALYSIS 1.4: DATA QUALITY RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1.4: RECOMMENDATIONS FOR 3,000 FARMER SURVEY")
print("=" * 80)

recommendations = """
📋 TOP 3 RECOMMENDATIONS FOR DATA COLLECTION & QUALITY:

1. DATA COMPLETENESS DURING COLLECTION:
   ✓ Mandatory field validation: Ensure Farmer Code, Visit Number, Gender, 
     Land Area, and all 14 Variables are collected for every farmer
   ✓ Real-time data validation: Use mobile data collection tools with 
     built-in validation rules (e.g., Result/Competence only accept 0,1,2)
   ✓ Training protocol: Train surveyors on the importance of complete data, 
     especially for critical fields needed for segmentation analysis

2. DATA CLEANING / QUALITY CHECKS:
   ✓ Automated range checks: Flag records with negative values, impossible 
     yields (>5000 kg/ha), or land areas >20ha for manual review
   ✓ Duplicate detection: Check for duplicate Farmer Code + Visit Number 
     combinations before data entry
   ✓ Consistency checks: Verify that Visit 2 data exists only for farmers 
     with Visit 1 baseline data

3. STANDARDIZATION & DOCUMENTATION:
   ✓ Code standardization: Use consistent Farmer Code format across all 
     cooperatives (e.g., COOP-001-0001)
   ✓ Data dictionary: Maintain clear definitions for each variable, 
     especially the 14 adoption variables
   ✓ Quality control sampling: M&E Assistant should review 10% of surveys 
     randomly for accuracy and completeness within 48 hours of collection

📊 CURRENT DATA QUALITY METRICS:
"""

print(recommendations)

# Calculate current data quality metrics
total_records = len(df_clean)
complete_records = df_clean.dropna(subset=critical_fields).shape[0]
completeness_rate = (complete_records / total_records * 100).round(1)

print(f"  - Overall completeness rate: {completeness_rate}%")
print(f"  - Records with both visits: {len(progress_df)} farmer-variable pairs")
print(f"  - Unique farmers tracked: {df_clean['Farmer: Farmer Code'].nunique()}")

# Save recommendations
with open(RESULTS_PATH / "1_4_recommendations.txt", 'w') as f:
    f.write(recommendations)
    f.write(f"\n  - Overall completeness rate: {completeness_rate}%\n")
    f.write(f"  - Records with both visits: {len(progress_df)} farmer-variable pairs\n")
    f.write(f"  - Unique farmers tracked: {df_clean['Farmer: Farmer Code'].nunique()}\n")

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - SUMMARY")
print("=" * 80)

print(f"""
✓ All analyses completed successfully!

📁 Output Files Created:
  1. Cleaned Data: {CLEANED_PATH / 'farmer_development_cleaned.csv'}
  2. Result Distribution: {RESULTS_PATH / '1_1_result_distribution.csv'}
  3. Competence Distribution: {RESULTS_PATH / '1_1_competence_distribution.csv'}
  4. Progress Tracking: {RESULTS_PATH / '1_2_progress_tracking.csv'}
  5. Production by Gender: {RESULTS_PATH / '1_3_production_by_gender.csv'}
  6. Production by Land Size: {RESULTS_PATH / '1_3_production_by_landsize.csv'}
  7. Yield per Hectare: {RESULTS_PATH / '1_3_yield_per_hectare.csv'}
  8. Recommendations: {RESULTS_PATH / '1_4_recommendations.txt'}

📊 Key Findings:
  - Total farmers analyzed: {df_clean['Farmer: Farmer Code'].nunique()}
  - Variables tracked: {df_clean['Variable'].nunique()}
  - Farmers with progress data: {len(progress_df)} records
  - Data completeness: {completeness_rate}%

💡 Next Steps:
  1. Review the output CSV files in the 'results' folder
  2. Create visualizations for the 2-pager report
  3. Share recommendations with the Operations Team
  4. Prepare for the 3,000 farmer survey rollout
""")

print("=" * 80)
print("Script execution completed!")
print("=" * 80)
