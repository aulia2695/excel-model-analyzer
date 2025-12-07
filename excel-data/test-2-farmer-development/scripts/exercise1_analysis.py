"""
Exercise 1: Analysis of Farmer Development Plan Data
Ivory Coast - JB Cocoa
Updated for actual column structure
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
    print(f"✓ Columns found: {', '.join(df.columns)}")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# ============================================================================
# STEP 2: DATA UNDERSTANDING & PREPARATION
# ============================================================================
print("\n[STEP 2] Understanding Data Structure...")

# The data appears to be in LONG format where each row is a Variable response
# We need to understand the unique variables
print(f"\nTotal records: {len(df)}")
print(f"Unique farmers: {df['Farmer: Farmer Code'].nunique()}")
print(f"Unique variables: {df['Variable'].nunique()}")
print(f"Visit numbers: {df['Visit Number'].unique()}")

print("\nSample Variables:")
print(df['Variable'].value_counts().head(10))

# ============================================================================
# STEP 3: DATA CLEANING
# ============================================================================
print("\n[STEP 3] Data Cleaning...")

# Standardize Gender values
print("\n3.1 Standardizing Gender values:")
print(f"Original Gender values: {df['Farmer: Gender'].unique()}")
df['Gender_Clean'] = df['Farmer: Gender'].map({
    2: 'Male',
    1: 'Female',
    'Male': 'Male',
    'Female': 'Female',
    'M': 'Male',
    'F': 'Female'
})
print(f"Cleaned Gender values: {df['Gender_Clean'].unique()}")

# Standardize Result and Competence (G/M/B to numeric)
print("\n3.2 Standardizing Result and Competence:")
def standardize_level(value):
    """Convert G/M/B or 2/1/0 to consistent format"""
    if pd.isna(value):
        return None
    value_str = str(value).upper().strip()
    if value_str in ['G', '2', 'GOOD']:
        return 'Good'
    elif value_str in ['M', '1', 'MEDIUM']:
        return 'Medium'
    elif value_str in ['B', '0', 'BAD']:
        return 'Bad'
    return None

df['Result_Clean'] = df['Result'].apply(standardize_level)
df['Competence_Clean'] = df['Competence'].apply(standardize_level)

print(f"Result distribution: {df['Result_Clean'].value_counts().to_dict()}")
print(f"Competence distribution: {df['Competence_Clean'].value_counts().to_dict()}")

# Create Land Size Categories
print("\n3.3 Creating Land Size Categories:")
df['Land_Category'] = pd.cut(
    df['Farm: Total Farm Area HA'],
    bins=[0, 2, 4, float('inf')],
    labels=['< 2 ha', '2-4 ha', '>= 4 ha'],
    include_lowest=True
)
print(f"Land categories: {df['Land_Category'].value_counts().to_dict()}")

# Check for missing values
print("\n3.4 Missing Values Check:")
missing = df[['Farmer: Farmer Code', 'Visit Number', 'Variable', 'Result_Clean', 'Competence_Clean']].isnull().sum()
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
# STEP 4: BASELINE ANALYSIS - ADOPTION & COMPETENCE
# ============================================================================
print("\n[STEP 4] Baseline Analysis - Adoption & Competence...")

# Convert to numeric for calculations
level_map = {'Good': 2, 'Medium': 1, 'Bad': 0}
df['Result_Numeric'] = df['Result_Clean'].map(level_map)
df['Competence_Numeric'] = df['Competence_Clean'].map(level_map)

# Calculate overall adoption per farmer
print("\n4.1 Calculating Overall Adoption per Farmer...")

farmer_adoption = df.groupby('Farmer: Farmer Code').agg({
    'Result_Numeric': ['mean', 'count'],
    'Competence_Numeric': 'mean',
    'Farmer: Full Name': 'first',
    'Gender_Clean': 'first',
    'Farm: Total Farm Area HA': 'first',
    'Land_Category': 'first',
    'Farm: Production - last baseline KG': 'first'
}).reset_index()

# Flatten column names
farmer_adoption.columns = ['Farmer_Code', 'Adoption_Score', 'Variable_Count', 
                           'Competence_Score', 'Full_Name', 'Gender', 
                           'Land_Size', 'Land_Category', 'Production_KG']

# Calculate adoption percentage and categorize
farmer_adoption['Adoption_Percentage'] = (farmer_adoption['Adoption_Score'] / 2 * 100).round(2)
farmer_adoption['Competence_Percentage'] = (farmer_adoption['Competence_Score'] / 2 * 100).round(2)

farmer_adoption['Overall_Adoption'] = farmer_adoption['Adoption_Percentage'].apply(
    lambda x: 'Good' if x >= 66.67 else ('Medium' if x >= 33.33 else 'Bad')
)
farmer_adoption['Overall_Competence'] = farmer_adoption['Competence_Percentage'].apply(
    lambda x: 'Good' if x >= 66.67 else ('Medium' if x >= 33.33 else 'Bad')
)

print("\n4.2 Overall Adoption Distribution:")
adoption_dist = farmer_adoption['Overall_Adoption'].value_counts()
adoption_pct = (adoption_dist / len(farmer_adoption) * 100).round(1)
for level in ['Good', 'Medium', 'Bad']:
    if level in adoption_dist.index:
        print(f"  {level:8s}: {adoption_dist[level]:4d} farmers ({adoption_pct[level]:5.1f}%)")

print("\n4.3 Overall Competence Distribution:")
competence_dist = farmer_adoption['Overall_Competence'].value_counts()
competence_pct = (competence_dist / len(farmer_adoption) * 100).round(1)
for level in ['Good', 'Medium', 'Bad']:
    if level in competence_dist.index:
        print(f"  {level:8s}: {competence_dist[level]:4d} farmers ({competence_pct[level]:5.1f}%)")

# ============================================================================
# STEP 5: PROGRESS TRACKING (Visit 1 vs Visit 2)
# ============================================================================
print("\n[STEP 5] Progress Tracking (Visit 1 → Visit 2)...")

# Check if we have multiple visits
visits = df['Visit Number'].unique()
print(f"Available visits: {sorted(visits)}")

if len(visits) >= 2:
    # Calculate adoption for each visit
    visit_adoption = df.groupby(['Farmer: Farmer Code', 'Visit Number']).agg({
        'Result_Numeric': 'mean'
    }).reset_index()
    
    # Pivot to wide format
    visit_pivot = visit_adoption.pivot(index='Farmer: Farmer Code', 
                                        columns='Visit Number', 
                                        values='Result_Numeric')
    
    # Get visit columns (they might be 1,2 or other numbers)
    visit_cols = sorted(visit_pivot.columns)
    if len(visit_cols) >= 2:
        first_visit = visit_cols[0]
        second_visit = visit_cols[1]
        
        visit_pivot.columns = ['Visit_1_Score', 'Visit_2_Score']
        visit_pivot = visit_pivot.reset_index()
        
        # Calculate progress
        visit_pivot['Score_Change'] = visit_pivot['Visit_2_Score'] - visit_pivot['Visit_1_Score']
        visit_pivot['Progress_Status'] = visit_pivot['Score_Change'].apply(
            lambda x: 'Making Progress' if x > 0.2 else ('Deteriorating' if x < -0.2 else 'Staying Same')
        )
        
        print("\n5.1 Progress Status Distribution:")
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
    visit_pivot = None

# ============================================================================
# STEP 6: PRODUCTION ANALYSIS
# ============================================================================
print("\n[STEP 6] Production Analysis...")

print("\n6.1 Average Production by Gender:")
gender_prod = farmer_adoption.groupby('Gender')['Production_KG'].agg(['mean', 'median', 'count'])
print(gender_prod.round(2))

print("\n6.2 Average Production by Land Size:")
land_prod = farmer_adoption.groupby('Land_Category')['Production_KG'].agg(['mean', 'median', 'count'])
print(land_prod.round(2))

print("\n6.3 Average Production by Adoption Level:")
adoption_prod = farmer_adoption.groupby('Overall_Adoption')['Production_KG'].agg(['mean', 'median', 'count'])
print(adoption_prod.round(2))

# ============================================================================
# STEP 7: PRACTICE-LEVEL ANALYSIS
# ============================================================================
print("\n[STEP 7] Practice-Level Analysis...")

# Get top and bottom performing practices
practice_performance = df.groupby('Variable').agg({
    'Result_Numeric': ['mean', 'count'],
    'Competence_Numeric': 'mean'
}).round(3)

practice_performance.columns = ['Result_Avg', 'Count', 'Competence_Avg']
practice_performance = practice_performance.sort_values('Result_Avg', ascending=False)

print("\n7.1 Top 5 Performing Practices (by Result):")
print(practice_performance.head())

print("\n7.2 Bottom 5 Performing Practices (by Result):")
print(practice_performance.tail())

# ============================================================================
# STEP 8: VISUALIZATIONS
# ============================================================================
print("\n[STEP 8] Creating Visualizations...")

colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red

# 8.1 Adoption Distribution
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

# 8.2 Competence Distribution
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

# 8.3 Adoption vs Competence Heatmap
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

# 8.4 Progress Tracking (if available)
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

# 8.5 Production by Gender
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

# 8.6 Production by Land Size
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

# 8.7 Practice Performance Ranking
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

# 8.8 Production vs Adoption Scatter
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
# STEP 9: RECOMMENDATIONS
# ============================================================================
print("\n[STEP 9] Generating Recommendations...")

recommendations = f"""
{'='*80}
FARMER DEVELOPMENT PLAN ANALYSIS - RECOMMENDATIONS
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Based on analysis of {len(farmer_adoption)} farmers from {df['Visit Number'].nunique()} visit(s),
here are key recommendations for the local Operations Team regarding data 
collection for the upcoming 3,000 farmers:

{'='*80}
RECOMMENDATION 1: DATA COMPLETENESS & QUALITY DURING COLLECTION
{'='*80}

1.1 STANDARDIZE VARIABLE NAMING
   ✓ Current: {df['Variable'].nunique()} unique variables tracked
   ⚠ Issue: Variable names may have inconsistencies
   → Action: Create standard variable codebook for all surveyors
   → Ensure exact spelling and formatting for all 14 core practices

1.2 CONSISTENT CODING SYSTEM
   ✓ Current system uses G/M/B (Good/Medium/Bad)
   → Maintain this system but add validation:
     * Only allow G, M, or B (case-insensitive)
     * Reject entries like "Good", "Medium", "Bad" (use codes only)
     * Implement dropdown lists in survey forms

1.3 GENDER CODING STANDARDIZATION
   ⚠ Current issue: Gender field uses numeric codes (1/2)
   → Problem: Easy to confuse with adoption scores
   → Solution: Use "Male"/"Female" text values instead
   → Alternative: Use M/F if codes are necessary

1.4 LAND SIZE VALIDATION
   ✓ Current range: {farmer_adoption['Land_Size'].min():.2f} - {farmer_adoption['Land_Size'].max():.2f} HA
   → Add validation: Land size must be between 0.1 and 100 HA
   → Flag outliers for immediate verification

1.5 PRODUCTION DATA QUALITY
   → Require production data for ALL farmers
   → Cross-validate: Production should correlate with land size
   → Flag farmers with yield > 3000 kg/ha or < 100 kg/ha

{'='*80}
RECOMMENDATION 2: DATA CLEANING & QUALITY CHECKS
{'='*80}

2.1 DAILY DATA VALIDATION (M&E Assistant)
   → Upload data within 24 hours of collection
   → Run automated quality checks:
     * Missing farmer codes
     * Duplicate records
     * Invalid G/M/B values
     * Missing gender or land size
   → Send daily quality report to Operations Team

2.2 LONG FORMAT DATA STRUCTURE
   ✓ Current: Data in LONG format (one row per variable per farmer)
   → Advantage: Easy to add new variables
   → Challenge: More rows to manage ({len(df)} rows for {len(farmer_adoption)} farmers)
   → Ensure farmer codes are consistent across all rows
   → Validate each farmer has all required variables

2.3 VISIT TRACKING IMPROVEMENTS
   → Clearly document Visit Number (1, 2, 3, etc.)
   → Record exact date of each visit
   → Ensure same surveyor revisits same farmers when possible
   → Create visit schedule to avoid delays

2.4 COMPLETENESS CHECKS
   → Each farmer must have responses for ALL 14 core practices
   → Each variable needs BOTH Result AND Competence scores
   → Current completeness: {(df.groupby('Farmer: Farmer Code')['Variable'].count().mean() / df['Variable'].nunique() * 100):.1f}% average
   → Target: 100% completeness for all farmers

2.5 CROSS-VALIDATION RULES
   → If Result = Bad, Competence should not be Good
   → If Result = Good, investigate if Competence = Bad
   → Production should increase if Adoption improves
   → Land size should remain constant across visits

{'='*80}
RECOMMENDATION 3: OPERATIONAL IMPROVEMENTS FOR 3,000 FARMERS
{'='*80}

3.1 PILOT TESTING (50 FARMERS)
   → Test revised forms with 50 farmers first
   → Identify confusing questions or coding issues
   → Adjust before scaling to 3,000

3.2 SURVEYOR TRAINING
   → Train on exact definitions of G/M/B for each practice
   → Practice coding scenarios
   → Emphasize data quality over speed
   → Provide reference cards with coding examples

3.3 DIGITAL DATA COLLECTION
   → Consider mobile data collection apps (KoBoToolbox, ODK)
   → Benefits:
     * Real-time validation
     * Automatic farmer code lookup
     * GPS coordinates
     * Reduced transcription errors
   → One-time setup cost but long-term efficiency

3.4 QUALITY INCENTIVES
   → Track surveyor quality scores
   → Recognize high-quality data collection
   → Provide feedback on common errors
   → Resurvey if quality score < 80%

3.5 SAMPLING STRATEGY
   → Current: {len(farmer_adoption)} farmers from {df['Farmer: Village'].nunique()} villages
   → For 3,000 farmers:
     * Ensure representative sample across regions
     * Balance gender distribution
     * Include range of farm sizes
     * Target: 30% women, 40% small farms, 30% medium, 30% large

{'='*80}
KEY FINDINGS FROM CURRENT DATA
{'='*80}

ADOPTION LEVELS:
"""

# Add actual findings
for level in ['Good', 'Medium', 'Bad']:
    if level in adoption_dist.index:
        recommendations += f"\n  {level}: {adoption_dist[level]} farmers ({adoption_pct[level]:.1f}%)"

recommendations += f"""

COMPETENCE LEVELS:
"""
for level in ['Good', 'Medium', 'Bad']:
    if level in competence_dist.index:
        recommendations += f"\n  {level}: {competence_dist[level]} farmers ({competence_pct[level]:.1f}%)"

if visit_pivot is not None:
    recommendations += f"""

PROGRESS TRACKING:
"""
    for status in ['Making Progress', 'Staying Same', 'Deteriorating']:
        if status in progress_dist.index:
            recommendations += f"\n  {status}: {progress_dist[status]} farmers ({progress_pct[status]:.1f}%)"

recommendations += f"""

PRODUCTION INSIGHTS:
  Average production: {farmer_adoption['Production_KG'].mean():.2f} KG
  By Gender:
    Male: {farmer_adoption[farmer_adoption['Gender']=='Male']['Production_KG'].mean():.2f} KG
    Female: {farmer_adoption[farmer_adoption['Gender']=='Female']['Production_KG'].mean():.2f} KG
  By Adoption Level:
    Good: {farmer_adoption[farmer_adoption['Overall_Adoption']=='Good']['Production_KG'].mean():.2f} KG
    Medium: {farmer_adoption[farmer_adoption['Overall_Adoption']=='Medium']['Production_KG'].mean():.2f} KG
    Bad: {farmer_adoption[farmer_adoption['Overall_Adoption']=='Bad']['Production_KG'].mean():.2f} KG

{'='*80}
CRITICAL ACTION ITEMS FOR NEXT 3,000 FARMERS
{'='*80}

BEFORE DATA COLLECTION:
1. Revise survey forms with standardized codes
2. Train all surveyors (minimum 2 days)
3. Pilot test with 50 farmers
4. Set up digital data collection system
5. Create data dictionary and coding guide

DURING DATA COLLECTION:
1. Daily data upload and validation
2. Weekly quality reports to Operations Team
3. Immediate feedback to surveyors on errors
4. Monthly progress reviews
5. Continuous improvement of processes

AFTER DATA COLLECTION:
1. Comprehensive data cleaning
2. Analysis and visualization
3. Client report preparation
4. Lessons learned documentation
5. Plan for future data collection rounds

{'='*80}
ESTIMATED IMPACT OF IMPROVEMENTS
{'='*80}

If recommendations are implemented:
→ Data completeness: 95%+ (vs current {(df['Result_Clean'].notna().sum() / len(df) * 100):.1f}%)
→ Data quality score: 90%+ 
→ Time to first analysis: 2 weeks (vs 4-6 weeks)
→ Cost savings: 20%+ (fewer resurveys needed)
→ Stakeholder confidence: High (clean, reliable data)

{'='*80}
END OF RECOMMENDATIONS
{'='*80}
"""

# Save recommendations
rec_file = results_dir / "recommendations.txt"
with open(rec_file, 'w', encoding='utf-8') as f:
    f.write(recommendations)
print(f"✓ Recommendations saved to '{rec_file}'")

# ============================================================================
# STEP 10: SAVE SUMMARY DATA
# ============================================================================
print("\n[STEP 10] Saving Summary Data...")

# Save farmer-level summary
farmer_summary_file = results_dir / "farmer_level_summary.csv"
farmer_adoption.to_csv(farmer_summary_file, index=False)
print(f"✓ Farmer summary saved to '{farmer_summary_file}'")

# Save practice-level summary
practice_summary_file = results_dir / "practice_performance.csv"
practice_performance.to_csv(practice_summary_file)
print(f"✓ Practice performance saved to '{practice_summary_file}'")

# Save overall statistics
stats_data = {
    'Metric': [
        'Total Farmers',
        'Good Adoption', 'Medium Adoption', 'Bad Adoption',
        'Good Competence', 'Medium Competence', 'Bad Competence',
        'Average Production (KG)', 'Average Land Size (HA)',
        'Male Farmers', 'Female Farmers'
    ],
    'Value': [
        len(farmer_adoption),
        len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Good']),
        len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Medium']),
        len(farmer_adoption[farmer_adoption['Overall_Adoption']=='Bad']),
        len(farmer_adoption[farmer_adoption['Overall_Competence']=='Good']),
        len(farmer_adoption[farmer_adoption['Overall_Competence']=='Medium']),
        len(farmer_adoption[farmer_adoption['Overall_Competence']=='Bad']),
        f"{farmer_adoption['Production_KG'].mean():.2f}",
        f"{farmer_adoption['Land_Size'].mean():.2f}",
        len(farmer_adoption[farmer_adoption['Gender']=='Male']),
        len(farmer_adoption[farmer_adoption['Gender']=='Female'])
    ]
}

stats_df = pd.DataFrame(stats_data)
stats_file = results_dir / "analysis_summary.csv"
stats_df.to_csv(stats_file, index=False)
print(f"✓ Analysis summary saved to '{stats_file}'")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\n✓ Analyzed {len(farmer_adoption)} farmers")
print(f"✓ Tracked {df['Variable'].nunique()} different practices")
print(f"✓ Generated 8 visualizations")
