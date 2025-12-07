"""
Exercise 1: Analysis of Farmer Development Plan Data
Ivory Coast - JB Cocoa
Updated with flexible column detection
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

script_dir = Path(__file__).parent.absolute()
test_dir = script_dir.parent
results_dir = test_dir / "results" / "exercise1"
cleaned_dir = test_dir / "cleaned"

# Create directories
results_dir.mkdir(parents=True, exist_ok=True)
cleaned_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("FARMER DEVELOPMENT PLAN ANALYSIS - EXERCISE 1")
print("Ivory Coast - JB Cocoa")
print("=" * 80)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print(f"\n📁 Working Directories:")
print(f"   Results folder: {results_dir}")
print(f"   Cleaned folder: {cleaned_dir}")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[STEP 1] Loading data...")

try:
    data_file = test_dir / "raw" / "test_2_farmer_development_raw.xlsx"
    df = pd.read_excel(data_file)
    print(f"✓ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    print(f"\n✓ Column names found:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# ============================================================================
# STEP 2: DETECT COLUMN NAMES
# ============================================================================
print("\n[STEP 2] Detecting Column Names...")

# Function to find column by keywords
def find_column(df, keywords, required=True):
    """Find column name that contains any of the keywords"""
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in keywords:
            if keyword.lower() in col_lower:
                return col
    if required:
        print(f"⚠ WARNING: Could not find column with keywords: {keywords}")
    return None

# Detect key columns
farmer_code_col = find_column(df, ['farmer code', 'farmer_code', 'code'])
farmer_name_col = find_column(df, ['full name', 'farmer: full', 'name'], required=False)
visit_col = find_column(df, ['visit number', 'visit', 'round'])
gender_col = find_column(df, ['gender', 'sex'])
land_col = find_column(df, ['farm area', 'total farm', 'land size', 'area ha'])
production_col = find_column(df, ['production', 'yield', 'baseline kg'], required=False)
village_col = find_column(df, ['village', 'location'], required=False)
variable_col = find_column(df, ['variable', 'practice'])
result_col = find_column(df, ['result'])
competence_col = find_column(df, ['competence', 'skill'])

print("\n✓ Detected columns:")
print(f"   Farmer Code: {farmer_code_col}")
print(f"   Full Name: {farmer_name_col}")
print(f"   Visit Number: {visit_col}")
print(f"   Gender: {gender_col}")
print(f"   Land Size: {land_col}")
print(f"   Production: {production_col}")
print(f"   Village: {village_col}")
print(f"   Variable: {variable_col}")
print(f"   Result: {result_col}")
print(f"   Competence: {competence_col}")

# Check if critical columns are found
if not all([farmer_code_col, visit_col, variable_col, result_col, competence_col]):
    print("\n✗ ERROR: Missing critical columns!")
    print("Please check your Excel file has these columns:")
    print("  - Farmer Code (or similar)")
    print("  - Visit Number")
    print("  - Variable")
    print("  - Result")
    print("  - Competence")
    exit(1)

# ============================================================================
# STEP 3: DATA UNDERSTANDING & PREPARATION
# ============================================================================
print("\n[STEP 3] Understanding Data Structure...")

print(f"\nTotal records: {len(df)}")
print(f"Unique farmers: {df[farmer_code_col].nunique()}")
print(f"Unique variables: {df[variable_col].nunique()}")
print(f"Visit numbers: {sorted(df[visit_col].unique())}")

print("\nSample Variables:")
print(df[variable_col].value_counts().head(10))

# ============================================================================
# STEP 4: DATA CLEANING
# ============================================================================
print("\n[STEP 4] Data Cleaning...")

# Standardize Gender values
if gender_col:
    print("\n4.1 Standardizing Gender values:")
    print(f"Original Gender values: {df[gender_col].unique()}")
    df['Gender_Clean'] = df[gender_col].map({
        2: 'Male',
        1: 'Female',
        'Male': 'Male',
        'Female': 'Female',
        'M': 'Male',
        'F': 'Female',
        'male': 'Male',
        'female': 'Female'
    })
    # Fill any remaining NaN with the original value
    df['Gender_Clean'] = df['Gender_Clean'].fillna(df[gender_col])
    print(f"Cleaned Gender values: {df['Gender_Clean'].unique()}")

# Standardize Result and Competence (G/M/B to text)
print("\n4.2 Standardizing Result and Competence:")
def standardize_level(value):
    """Convert G/M/B or 2/1/0 to consistent format"""
    if pd.isna(value):
        return None
    value_str = str(value).upper().strip()
    if value_str in ['G', '2', '2.0', 'GOOD']:
        return 'Good'
    elif value_str in ['M', '1', '1.0', 'MEDIUM']:
        return 'Medium'
    elif value_str in ['B', '0', '0.0', 'BAD']:
        return 'Bad'
    return None

df['Result_Clean'] = df[result_col].apply(standardize_level)
df['Competence_Clean'] = df[competence_col].apply(standardize_level)

print(f"Result distribution:")
print(df['Result_Clean'].value_counts().to_dict())
print(f"\nCompetence distribution:")
print(df['Competence_Clean'].value_counts().to_dict())

# Create Land Size Categories
if land_col:
    print("\n4.3 Creating Land Size Categories:")
    df['Land_Category'] = pd.cut(
        df[land_col],
        bins=[0, 2, 4, float('inf')],
        labels=['< 2 ha', '2-4 ha', '>= 4 ha'],
        include_lowest=True
    )
    print(f"Land categories:")
    print(df['Land_Category'].value_counts().to_dict())

# Check for missing values
print("\n4.4 Missing Values Check:")
critical_cols = [farmer_code_col, visit_col, variable_col, 'Result_Clean', 'Competence_Clean']
missing = df[critical_cols].isnull().sum()
print(missing)

# Remove duplicates
duplicates = df.duplicated().sum()
if duplicates > 0:
    df.drop_duplicates(inplace=True)
    print(f"\n✓ Removed {duplicates} duplicates")

# Save cleaned data
cleaned_file = cleaned_dir / "farmer_development_cleaned.csv"
df.to_csv(cleaned_file, index=False)
print(f"\n✓ Cleaned data saved to '{cleaned_file}'")

# ============================================================================
# STEP 5: BASELINE ANALYSIS - ADOPTION & COMPETENCE
# ============================================================================
print("\n[STEP 5] Baseline Analysis - Adoption & Competence...")

# Convert to numeric for calculations
level_map = {'Good': 2, 'Medium': 1, 'Bad': 0}
df['Result_Numeric'] = df['Result_Clean'].map(level_map)
df['Competence_Numeric'] = df['Competence_Clean'].map(level_map)

# Calculate overall adoption per farmer
print("\n5.1 Calculating Overall Adoption per Farmer...")

# Build aggregation dict dynamically
agg_dict = {
    'Result_Numeric': ['mean', 'count'],
    'Competence_Numeric': 'mean'
}

if farmer_name_col:
    agg_dict[farmer_name_col] = 'first'
if gender_col:
    agg_dict['Gender_Clean'] = 'first'
if land_col:
    agg_dict[land_col] = 'first'
    agg_dict['Land_Category'] = 'first'
if production_col:
    agg_dict[production_col] = 'first'

farmer_adoption = df.groupby(farmer_code_col).agg(agg_dict).reset_index()

# Flatten column names
new_cols = [farmer_code_col, 'Adoption_Score', 'Variable_Count', 'Competence_Score']
if farmer_name_col:
    new_cols.append('Full_Name')
if gender_col:
    new_cols.append('Gender')
if land_col:
    new_cols.extend(['Land_Size', 'Land_Category'])
if production_col:
    new_cols.append('Production_KG')

farmer_adoption.columns = new_cols

# Calculate adoption percentage and categorize
farmer_adoption['Adoption_Percentage'] = (farmer_adoption['Adoption_Score'] / 2 * 100).round(2)
farmer_adoption['Competence_Percentage'] = (farmer_adoption['Competence_Score'] / 2 * 100).round(2)

farmer_adoption['Overall_Adoption'] = farmer_adoption['Adoption_Percentage'].apply(
    lambda x: 'Good' if x >= 66.67 else ('Medium' if x >= 33.33 else 'Bad')
)
farmer_adoption['Overall_Competence'] = farmer_adoption['Competence_Percentage'].apply(
    lambda x: 'Good' if x >= 66.67 else ('Medium' if x >= 33.33 else 'Bad')
)

print("\n5.2 Overall Adoption Distribution:")
adoption_dist = farmer_adoption['Overall_Adoption'].value_counts()
adoption_pct = (adoption_dist / len(farmer_adoption) * 100).round(1)
for level in ['Good', 'Medium', 'Bad']:
    if level in adoption_dist.index:
        print(f"  {level:8s}: {adoption_dist[level]:4d} farmers ({adoption_pct[level]:5.1f}%)")

print("\n5.3 Overall Competence Distribution:")
competence_dist = farmer_adoption['Overall_Competence'].value_counts()
competence_pct = (competence_dist / len(farmer_adoption) * 100).round(1)
for level in ['Good', 'Medium', 'Bad']:
    if level in competence_dist.index:
        print(f"  {level:8s}: {competence_dist[level]:4d} farmers ({competence_pct[level]:5.1f}%)")

# ============================================================================
# STEP 6: PROGRESS TRACKING (Visit 1 vs Visit 2)
# ============================================================================
print("\n[STEP 6] Progress Tracking (Visit 1 → Visit 2)...")

visits = sorted(df[visit_col].unique())
print(f"Available visits: {visits}")

visit_pivot = None
if len(visits) >= 2:
    # Calculate adoption for each visit
    visit_adoption = df.groupby([farmer_code_col, visit_col]).agg({
        'Result_Numeric': 'mean'
    }).reset_index()
    
    # Pivot to wide format
    visit_pivot = visit_adoption.pivot(index=farmer_code_col, 
                                        columns=visit_col, 
                                        values='Result_Numeric')
    
    visit_cols = sorted(visit_pivot.columns)
    if len(visit_cols) >= 2:
        visit_pivot.columns = ['Visit_1_Score', 'Visit_2_Score']
        visit_pivot = visit_pivot.reset_index()
        
        # Calculate progress
        visit_pivot['Score_Change'] = visit_pivot['Visit_2_Score'] - visit_pivot['Visit_1_Score']
        visit_pivot['Progress_Status'] = visit_pivot['Score_Change'].apply(
            lambda x: 'Making Progress' if x > 0.2 else ('Deteriorating' if x < -0.2 else 'Staying Same')
        )
        
        print("\n6.1 Progress Status Distribution:")
        progress_dist = visit_pivot['Progress_Status'].value_counts()
        progress_pct = (progress_dist / len(visit_pivot) * 100).round(1)
        for status in ['Making Progress', 'Staying Same', 'Deteriorating']:
            if status in progress_dist.index:
                print(f"  {status:20s}: {progress_dist[status]:4d} farmers ({progress_pct[status]:5.1f}%)")
    else:
        print("⚠ Not enough visit data for progress tracking")
        visit_pivot = None
else:
    print("⚠ Only one visit found - cannot track progress")

# ============================================================================
# STEP 7: PRODUCTION ANALYSIS
# ============================================================================
print("\n[STEP 7] Production Analysis...")

if production_col and 'Production_KG' in farmer_adoption.columns:
    if gender_col and 'Gender' in farmer_adoption.columns:
        print("\n7.1 Average Production by Gender:")
        gender_prod = farmer_adoption.groupby('Gender')['Production_KG'].agg(['mean', 'median', 'count'])
        print(gender_prod.round(2))
    
    if land_col and 'Land_Category' in farmer_adoption.columns:
        print("\n7.2 Average Production by Land Size:")
        land_prod = farmer_adoption.groupby('Land_Category')['Production_KG'].agg(['mean', 'median', 'count'])
        print(land_prod.round(2))
    
    print("\n7.3 Average Production by Adoption Level:")
    adoption_prod = farmer_adoption.groupby('Overall_Adoption')['Production_KG'].agg(['mean', 'median', 'count'])
    print(adoption_prod.round(2))
else:
    print("⚠ Production column not found - skipping production analysis")

# ============================================================================
# STEP 8: PRACTICE-LEVEL ANALYSIS
# ============================================================================
print("\n[STEP 8] Practice-Level Analysis...")

practice_performance = df.groupby(variable_col).agg({
    'Result_Numeric': ['mean', 'count'],
    'Competence_Numeric': 'mean'
}).round(3)

practice_performance.columns = ['Result_Avg', 'Count', 'Competence_Avg']
practice_performance = practice_performance.sort_values('Result_Avg', ascending=False)

print("\n8.1 Top 5 Performing Practices (by Result):")
print(practice_performance.head())

print("\n8.2 Bottom 5 Performing Practices (by Result):")
print(practice_performance.tail())

# ============================================================================
# STEP 9: VISUALIZATIONS
# ============================================================================
print("\n[STEP 9] Creating Visualizations...")

colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red

# 9.1 Adoption Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

adoption_counts = farmer_adoption['Overall_Adoption'].value_counts()
ax1.pie(adoption_counts, labels=adoption_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90)
ax1.set_title('Baseline: Overall Adoption Distribution', fontsize=14, fontweight='bold')

adoption_counts.plot(kind='bar', ax=ax2, color=colors)
ax2.set_title('Number of Farmers by Adoption Level', fontsize=14, fontweight='bold')
ax2.set_xlabel('Adoption Level')
ax2.set_ylabel('Number of Farmers')
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig(results_dir / '01_baseline_adoption_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 01_baseline_adoption_distribution.png")

# 9.2 Competence Distribution
fig, ax = plt.subplots(figsize=(10, 6))
competence_counts = farmer_adoption['Overall_Competence'].value_counts()
competence_counts.plot(kind='bar', ax=ax, color=colors)
ax.set_title('Baseline: Overall Competence Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Competence Level')
ax.set_ylabel('Number of Farmers')
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig(results_dir / '02_baseline_competence_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 02_baseline_competence_distribution.png")

# 9.3 Adoption vs Competence Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
adoption_competence = pd.crosstab(farmer_adoption['Overall_Adoption'], 
                                   farmer_adoption['Overall_Competence'])
sns.heatmap(adoption_competence, annot=True, fmt='d', cmap='YlGnBu', ax=ax)
ax.set_title('Adoption vs Competence Matrix', fontsize=14, fontweight='bold')
ax.set_xlabel('Competence Level')
ax.set_ylabel('Adoption Level')
plt.tight_layout()
plt.savefig(results_dir / '03_adoption_vs_competence.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 03_adoption_vs_competence.png")

# 9.4 Progress Tracking (if available)
if visit_pivot is not None and len(visit_pivot) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    progress_counts = visit_pivot['Progress_Status'].value_counts()
    progress_counts.plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db', '#e74c3c'])
    ax.set_title('Farmer Progress: Visit 1 to Visit 2', fontsize=14, fontweight='bold')
    ax.set_xlabel('Progress Status')
    ax.set_ylabel('Number of Farmers')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig(results_dir / '04_progress_tracking.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: 04_progress_tracking.png")

# 9.5-9.8 Production visualizations (if production data available)
if production_col and 'Production_KG' in farmer_adoption.columns:
    if gender_col and 'Gender' in farmer_adoption.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        farmer_adoption.groupby('Gender')['Production_KG'].mean().plot(kind='bar', ax=ax, color='#3498db')
        ax.set_title('Average Production by Gender', fontsize=14, fontweight='bold')
        ax.set_xlabel('Gender')
        ax.set_ylabel('Average Production (KG)')
        ax.tick_params(axis='x', rotation=0)
        plt.tight_layout()
        plt.savefig(results_dir / '05_production_by_gender.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created: 05_production_by_gender.png")
    
    if land_col and 'Land_Category' in farmer_adoption.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        farmer_adoption.groupby('Land_Category')['Production_KG'].mean().plot(kind='bar', ax=ax, color='#e67e22')
        ax.set_title('Average Production by Land Size', fontsize=14, fontweight='bold')
        ax.set_xlabel('Land Size Category')
        ax.set_ylabel('Average Production (KG)')
        ax.tick_params(axis='x', rotation=0)
        plt.tight_layout()
        plt.savefig(results_dir / '06_production_by_landsize.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created: 06_production_by_landsize.png")

# 9.7 Practice Performance Ranking
fig, ax = plt.subplots(figsize=(12, 8))
top_bottom = pd.concat([practice_performance.head(7), practice_performance.tail(7)])
colors_practices = ['#2ecc71' if x >= 1.33 else ('#f39c12' if x >= 0.67 else '#e74c3c') 
                   for x in top_bottom['Result_Avg']]
ax.barh(range(len(top_bottom)), top_bottom['Result_Avg'], color=colors_practices)
ax.set_yticks(range(len(top_bottom)))
ax.set_yticklabels(top_bottom.index, fontsize=9)
ax.set_xlabel('Average Result Score (0-2)', fontsize=12)
ax.set_title('Top 7 & Bottom 7 Practice Performance', fontsize=14, fontweight='bold')
ax.axvline(x=0.67, color='red', linestyle='--', alpha=0.3)
ax.axvline(x=1.33, color='green', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(results_dir / '07_practice_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 07_practice_performance.png")

# 9.8 Production vs Land Size Scatter (if data available)
if production_col and land_col and all(col in farmer_adoption.columns for col in ['Production_KG', 'Land_Size']):
    fig, ax = plt.subplots(figsize=(10, 6))
    for level, color in zip(['Good', 'Medium', 'Bad'], colors):
        data = farmer_adoption[farmer_adoption['Overall_Adoption'] == level]
        ax.scatter(data['Land_Size'], data['Production_KG'], 
                  label=level, alpha=0.6, s=50, color=color)
    ax.set_title('Production vs Land Size by Adoption Level', fontsize=14, fontweight='bold')
    ax.set_xlabel('Land Size (HA)')
    ax.set_ylabel('Production (KG)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / '08_production_vs_landsize_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: 08_production_vs_landsize_scatter.png")

# ============================================================================
# STEP 10: SAVE SUMMARY & RECOMMENDATIONS
# ============================================================================
print("\n[STEP 10] Saving Results...")

# Save farmer summary
farmer_summary_file = results_dir / "farmer_level_summary.csv"
farmer_adoption.to_csv(farmer_summary_file, index=False)
print(f"✓ Farmer summary saved")

# Save practice performance
practice_summary_file = results_dir / "practice_performance.csv"
practice_performance.to_csv(practice_summary_file)
print(f"✓ Practice performance saved")

# Save analysis summary
stats_data = {
    'Metric': ['Total Farmers', 'Good Adoption', 'Medium Adoption', 'Bad Adoption'],
    'Value': [
        len(farmer_adoption),
        len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Good']),
        len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Medium']),
        len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Bad'])
    ]
}

stats_df = pd.DataFrame(stats_data)
stats_file = results_dir / "analysis_summary.csv"
stats_df.to_csv(stats_file, index=False)
print(f"✓ Analysis summary saved")

# Generate simple recommendations
recommendations = f"""
FARMER DEVELOPMENT PLAN ANALYSIS - KEY FINDINGS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
- Total Farmers: {len(farmer_adoption)}
- Good Adoption: {len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Good'])} ({len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Good'])/len(farmer_adoption)*100:.1f}%)
- Medium Adoption: {len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Medium'])} ({len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Medium'])/len(farmer_adoption)*100:.1f}%)
- Bad Adoption: {len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Bad'])} ({len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Bad'])/len(farmer_adoption)*100:.1f}%)

RECOMMENDATIONS:
1. Standardize data collection forms with dropdown lists
2. Implement daily data quality checks
3. Train surveyors on G/M/B coding system
4. Use digital data collection tools
5. Pilot test with 50 farmers before scaling to 3,000
"""

rec_file = results_dir / "recommendations.txt"
with open(rec_file, 'w') as f:
    f.write(recommendations)
print(f"✓ Recommendations saved")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\n✓ Analyzed {len(farmer_adoption)} farmers")
print(f"✓ Tracked {df[variable_col].nunique()} practices")
print(f"✓ Generated visualizations and reports")
print("\n" + "="*80)
