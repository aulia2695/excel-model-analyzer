"""
Farmer Development Plan Analysis Script
Exercise 1: Analysis of Farmer Development Plan data

Paths:
- Raw data: excel-data/test-2-farmer-development/raw/test_2_farmer_development_raw.xlsx
- Cleaned data: excel-data/test-2-farmer-development/cleaned/
- Results: excel-data/test-2-farmer-development/results/
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Path configurations
BASE_PATH = "excel-data/test-2-farmer-development"
RAW_PATH = f"{BASE_PATH}/raw/test_2_farmer_development_raw.xlsx"
CLEANED_PATH = f"{BASE_PATH}/cleaned"
RESULTS_PATH = f"{BASE_PATH}/results"

# Create directories if they don't exist
os.makedirs(CLEANED_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)

print("="*80)
print("FARMER DEVELOPMENT PLAN - EXERCISE 1 ANALYSIS")
print("="*80)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# 1. DATA LOADING & CLEANING
# ============================================================================
print("1. DATA LOADING & CLEANING")
print("-"*80)

# Load raw data
print(f"Loading data from: {RAW_PATH}")
df = pd.read_excel(RAW_PATH)
print(f"✓ Loaded {len(df)} records")
print(f"✓ Columns: {len(df.columns)}")

# Display column names
print("\nColumn names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

# Data quality checks
print("\n--- Data Quality Checks ---")
initial_records = len(df)
print(f"Initial records: {initial_records}")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"✓ Removed {duplicates} duplicate rows")

# Check missing values
print("\nMissing values by column:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

# Add categorical columns for analysis
print("\n--- Adding Analysis Columns ---")

# 1. Adoption Level (Good/Medium/Bad based on Result and Competence)
def categorize_adoption(value):
    if pd.isna(value):
        return 'Unknown'
    elif value == 2:
        return 'Good'
    elif value == 1:
        return 'Medium'
    elif value == 0:
        return 'Bad'
    else:
        return 'Unknown'

df['Adoption Level - Result'] = df['Result'].apply(categorize_adoption)
df['Adoption Level - Competence'] = df['Competence'].apply(categorize_adoption)
print("✓ Added 'Adoption Level - Result' column (G=2, M=1, B=0)")
print("✓ Added 'Adoption Level - Competence' column (G=2, M=1, B=0)")

# 2. Visit Tracking
def categorize_visit(value):
    if pd.isna(value):
        return 'Unknown'
    elif value == 1:
        return 'Visit 1'
    elif value == 2:
        return 'Visit 2'
    elif value == 3:
        return 'Visit 3'
    else:
        return f'Visit {int(value)}'

df['Visit Tracking'] = df['Visit Number'].apply(categorize_visit)
print("✓ Added 'Visit Tracking' column")

# 3. Gender Farmer (Male/Female categorization)
def categorize_gender(value):
    if pd.isna(value):
        return 'Unknown'
    value_lower = str(value).lower().strip()
    if 'male' in value_lower and 'female' not in value_lower:
        return 'Male'
    elif 'female' in value_lower:
        return 'Female'
    else:
        return value

df['Gender Farmer'] = df['Farmer: Gender'].apply(categorize_gender)
df['Gender Code'] = df['Gender Farmer'].map({'Male': 2, 'Female': 1, 'Unknown': 0})
print("✓ Added 'Gender Farmer' column (Male=2, Female=1)")

# 4. Land Size Category
def categorize_land_size(ha):
    if pd.isna(ha):
        return 'Unknown'
    elif ha < 2:
        return '<2ha'
    elif ha < 4:
        return '2-4ha'
    else:
        return '≥4ha'

df['Land Size Category'] = df['Farm: Total Farm Area HA'].apply(categorize_land_size)
print("✓ Added 'Land Size Category' column (<2ha, 2-4ha, ≥4ha)")

# Save cleaned data
cleaned_file = f"{CLEANED_PATH}/test_2_farmer_development_cleaned.csv"
df.to_csv(cleaned_file, index=False)
print(f"\n✓ Cleaned data saved to: {cleaned_file}")
print(f"✓ Final records after cleaning: {len(df)}")

# ============================================================================
# 2. ANALYSIS 1.1: BASELINE DISTRIBUTION (Result & Competence)
# ============================================================================
print("\n" + "="*80)
print("2. ANALYSIS 1.1: BASELINE DISTRIBUTION")
print("="*80)

# Get unique variables
variables = df['Variable'].dropna().unique()
print(f"Found {len(variables)} unique variables\n")

# Analysis for Result
print("--- RESULT (Current Adoption) Distribution ---")
result_distribution = []

for var in variables:
    var_data = df[df['Variable'] == var]
    total = len(var_data[var_data['Result'].notna()])
    
    if total > 0:
        good = len(var_data[var_data['Result'] == 2])
        medium = len(var_data[var_data['Result'] == 1])
        bad = len(var_data[var_data['Result'] == 0])
        
        result_distribution.append({
            'Variable': var,
            'Total Farmers': total,
            'Good (2)': good,
            'Good %': round(good/total*100, 1),
            'Medium (1)': medium,
            'Medium %': round(medium/total*100, 1),
            'Bad (0)': bad,
            'Bad %': round(bad/total*100, 1)
        })

result_dist_df = pd.DataFrame(result_distribution)
print(result_dist_df.to_string(index=False))

# Save Result distribution
result_file = f"{RESULTS_PATH}/1.1_baseline_result_distribution.csv"
result_dist_df.to_csv(result_file, index=False)
print(f"\n✓ Saved to: {result_file}")

# Analysis for Competence
print("\n--- COMPETENCE (Skillset) Distribution ---")
competence_distribution = []

for var in variables:
    var_data = df[df['Variable'] == var]
    total = len(var_data[var_data['Competence'].notna()])
    
    if total > 0:
        good = len(var_data[var_data['Competence'] == 2])
        medium = len(var_data[var_data['Competence'] == 1])
        bad = len(var_data[var_data['Competence'] == 0])
        
        competence_distribution.append({
            'Variable': var,
            'Total Farmers': total,
            'Good (2)': good,
            'Good %': round(good/total*100, 1),
            'Medium (1)': medium,
            'Medium %': round(medium/total*100, 1),
            'Bad (0)': bad,
            'Bad %': round(bad/total*100, 1)
        })

competence_dist_df = pd.DataFrame(competence_distribution)
print(competence_dist_df.to_string(index=False))

# Save Competence distribution
competence_file = f"{RESULTS_PATH}/1.1_baseline_competence_distribution.csv"
competence_dist_df.to_csv(competence_file, index=False)
print(f"\n✓ Saved to: {competence_file}")

# ============================================================================
# 3. ANALYSIS 1.2: PROGRESS TRACKING (Visit 1 vs Visit 2)
# ============================================================================
print("\n" + "="*80)
print("3. ANALYSIS 1.2: PROGRESS TRACKING (Visit 1 vs Visit 2)")
print("="*80)

# Get farmers with both visits
farmers_with_visits = df.groupby('Farmer: Farmer Code')['Visit Number'].nunique()
farmers_both_visits = farmers_with_visits[farmers_with_visits >= 2].index

print(f"Farmers with multiple visits: {len(farmers_both_visits)}")

progress_results = []

for farmer_code in farmers_both_visits:
    farmer_data = df[df['Farmer: Farmer Code'] == farmer_code].sort_values('Visit Number')
    
    # Get unique variables for this farmer
    farmer_vars = farmer_data['Variable'].unique()
    
    for var in farmer_vars:
        var_data = farmer_data[farmer_data['Variable'] == var]
        
        if len(var_data) >= 2:
            visit1 = var_data[var_data['Visit Number'] == 1]
            visit2 = var_data[var_data['Visit Number'] == 2]
            
            if len(visit1) > 0 and len(visit2) > 0:
                # Result progress
                result1 = visit1['Result'].iloc[0]
                result2 = visit2['Result'].iloc[0]
                
                # Competence progress
                comp1 = visit1['Competence'].iloc[0]
                comp2 = visit2['Competence'].iloc[0]
                
                if pd.notna(result1) and pd.notna(result2):
                    if result2 > result1:
                        result_change = 'Progress'
                    elif result2 == result1:
                        result_change = 'Same'
                    else:
                        result_change = 'Deteriorating'
                else:
                    result_change = 'Unknown'
                
                if pd.notna(comp1) and pd.notna(comp2):
                    if comp2 > comp1:
                        comp_change = 'Progress'
                    elif comp2 == comp1:
                        comp_change = 'Same'
                    else:
                        comp_change = 'Deteriorating'
                else:
                    comp_change = 'Unknown'
                
                progress_results.append({
                    'Farmer Code': farmer_code,
                    'Variable': var,
                    'Result Visit 1': result1,
                    'Result Visit 2': result2,
                    'Result Change': result_change,
                    'Competence Visit 1': comp1,
                    'Competence Visit 2': comp2,
                    'Competence Change': comp_change
                })

progress_df = pd.DataFrame(progress_results)

if len(progress_df) > 0:
    # Summary for Result
    print("\n--- RESULT Progress Summary ---")
    result_summary = progress_df['Result Change'].value_counts()
    result_summary_pct = (result_summary / len(progress_df) * 100).round(1)
    
    result_progress_summary = pd.DataFrame({
        'Status': result_summary.index,
        'Count': result_summary.values,
        'Percentage': result_summary_pct.values
    })
    print(result_progress_summary.to_string(index=False))
    
    # Summary for Competence
    print("\n--- COMPETENCE Progress Summary ---")
    comp_summary = progress_df['Competence Change'].value_counts()
    comp_summary_pct = (comp_summary / len(progress_df) * 100).round(1)
    
    comp_progress_summary = pd.DataFrame({
        'Status': comp_summary.index,
        'Count': comp_summary.values,
        'Percentage': comp_summary_pct.values
    })
    print(comp_progress_summary.to_string(index=False))
    
    # Save detailed progress tracking
    progress_file = f"{RESULTS_PATH}/1.2_progress_tracking_detailed.csv"
    progress_df.to_csv(progress_file, index=False)
    print(f"\n✓ Detailed progress saved to: {progress_file}")
    
    # Save summary
    summary_file = f"{RESULTS_PATH}/1.2_progress_tracking_summary.csv"
    combined_summary = pd.DataFrame({
        'Metric': ['Result - Progress', 'Result - Same', 'Result - Deteriorating',
                   'Competence - Progress', 'Competence - Same', 'Competence - Deteriorating'],
        'Count': [
            result_summary.get('Progress', 0),
            result_summary.get('Same', 0),
            result_summary.get('Deteriorating', 0),
            comp_summary.get('Progress', 0),
            comp_summary.get('Same', 0),
            comp_summary.get('Deteriorating', 0)
        ],
        'Percentage': [
            result_summary_pct.get('Progress', 0),
            result_summary_pct.get('Same', 0),
            result_summary_pct.get('Deteriorating', 0),
            comp_summary_pct.get('Progress', 0),
            comp_summary_pct.get('Same', 0),
            comp_summary_pct.get('Deteriorating', 0)
        ]
    })
    combined_summary.to_csv(summary_file, index=False)
    print(f"✓ Summary saved to: {summary_file}")
else:
    print("⚠ No progress data available (need farmers with Visit 1 and Visit 2)")

# ============================================================================
# 4. ANALYSIS 1.3: PRODUCTION SEGMENTATION
# ============================================================================
print("\n" + "="*80)
print("4. ANALYSIS 1.3: PRODUCTION (YIELD) SEGMENTATION")
print("="*80)

# Get baseline data (usually Visit 1 or most recent)
baseline_df = df[df['Farm: Production - last baseline KG'].notna()].copy()

# Calculate yield per hectare
baseline_df['Yield per HA'] = baseline_df['Farm: Production - last baseline KG'] / baseline_df['Farm: Total Farm Area HA']

print(f"Farmers with production data: {len(baseline_df)}")

# A. Segmentation by Gender
print("\n--- PRODUCTION BY GENDER ---")
gender_production = baseline_df.groupby('Gender Farmer').agg({
    'Farm: Production - last baseline KG': ['count', 'mean', 'std', 'min', 'max'],
    'Yield per HA': ['mean', 'std']
}).round(2)

gender_production.columns = ['_'.join(col).strip() for col in gender_production.columns.values]
gender_production = gender_production.reset_index()
print(gender_production.to_string(index=False))

gender_file = f"{RESULTS_PATH}/1.3_production_by_gender.csv"
gender_production.to_csv(gender_file, index=False)
print(f"\n✓ Saved to: {gender_file}")

# B. Segmentation by Land Size
print("\n--- PRODUCTION BY LAND SIZE ---")
landsize_production = baseline_df.groupby('Land Size Category').agg({
    'Farm: Production - last baseline KG': ['count', 'mean', 'std', 'min', 'max'],
    'Yield per HA': ['mean', 'std'],
    'Farm: Total Farm Area HA': 'mean'
}).round(2)

landsize_production.columns = ['_'.join(col).strip() for col in landsize_production.columns.values]
landsize_production = landsize_production.reset_index()

# Sort by land size category
category_order = ['<2ha', '2-4ha', '≥4ha', 'Unknown']
landsize_production['sort_order'] = landsize_production['Land Size Category'].map({
    '<2ha': 1, '2-4ha': 2, '≥4ha': 3, 'Unknown': 4
})
landsize_production = landsize_production.sort_values('sort_order').drop('sort_order', axis=1)

print(landsize_production.to_string(index=False))

landsize_file = f"{RESULTS_PATH}/1.3_production_by_landsize.csv"
landsize_production.to_csv(landsize_file, index=False)
print(f"\n✓ Saved to: {landsize_file}")

# Combined summary
print("\n--- PRODUCTION SUMMARY ---")
production_summary = pd.DataFrame({
    'Segment': ['Overall', 'Male', 'Female', '<2ha', '2-4ha', '≥4ha'],
    'Avg Production (KG)': [
        baseline_df['Farm: Production - last baseline KG'].mean(),
        baseline_df[baseline_df['Gender Farmer']=='Male']['Farm: Production - last baseline KG'].mean(),
        baseline_df[baseline_df['Gender Farmer']=='Female']['Farm: Production - last baseline KG'].mean(),
        baseline_df[baseline_df['Land Size Category']=='<2ha']['Farm: Production - last baseline KG'].mean(),
        baseline_df[baseline_df['Land Size Category']=='2-4ha']['Farm: Production - last baseline KG'].mean(),
        baseline_df[baseline_df['Land Size Category']=='≥4ha']['Farm: Production - last baseline KG'].mean()
    ],
    'Avg Yield per HA': [
        baseline_df['Yield per HA'].mean(),
        baseline_df[baseline_df['Gender Farmer']=='Male']['Yield per HA'].mean(),
        baseline_df[baseline_df['Gender Farmer']=='Female']['Yield per HA'].mean(),
        baseline_df[baseline_df['Land Size Category']=='<2ha']['Yield per HA'].mean(),
        baseline_df[baseline_df['Land Size Category']=='2-4ha']['Yield per HA'].mean(),
        baseline_df[baseline_df['Land Size Category']=='≥4ha']['Yield per HA'].mean()
    ]
}).round(2)

print(production_summary.to_string(index=False))

summary_file = f"{RESULTS_PATH}/1.3_production_summary.csv"
production_summary.to_csv(summary_file, index=False)
print(f"\n✓ Saved to: {summary_file}")

# ============================================================================
# 5. ANALYSIS 1.4: RECOMMENDATIONS
# ============================================================================
print("\n" + "="*80)
print("5. ANALYSIS 1.4: DATA QUALITY RECOMMENDATIONS")
print("="*80)

# Calculate data quality metrics
total_records = len(df)
missing_production = df['Farm: Production - last baseline KG'].isnull().sum()
missing_gender = df['Farmer: Gender'].isnull().sum()
missing_landsize = df['Farm: Total Farm Area HA'].isnull().sum()
missing_variable = df['Variable'].isnull().sum()
missing_result = df['Result'].isnull().sum()
missing_competence = df['Competence'].isnull().sum()

farmers_single_visit = len(df.groupby('Farmer: Farmer Code')['Visit Number'].nunique()[
    df.groupby('Farmer: Farmer Code')['Visit Number'].nunique() == 1
])

recommendations = f"""
DATA QUALITY RECOMMENDATIONS FOR 3,000 FARMER SURVEY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Current Data Quality Metrics:
- Total records analyzed: {total_records}
- Missing production data: {missing_production} ({missing_production/total_records*100:.1f}%)
- Missing gender data: {missing_gender} ({missing_gender/total_records*100:.1f}%)
- Missing land size data: {missing_landsize} ({missing_landsize/total_records*100:.1f}%)
- Missing variable names: {missing_variable} ({missing_variable/total_records*100:.1f}%)
- Missing Result values: {missing_result} ({missing_result/total_records*100:.1f}%)
- Missing Competence values: {missing_competence} ({missing_competence/total_records*100:.1f}%)
- Farmers with only one visit: {farmers_single_visit}

═══════════════════════════════════════════════════════════════════════════════

RECOMMENDATION 1: COMPLETENESS OF DATA DURING DATA COLLECTION
═══════════════════════════════════════════════════════════════════════════════

Priority: HIGH

Issue: Critical fields have missing values that limit analysis capability.

Actions for Field Teams:
1. Make the following fields MANDATORY in data collection forms:
   - Farmer Code (unique identifier)
   - Gender
   - Total Farm Area (HA)
   - Production baseline (KG)
   - All 14 adoption variables must be surveyed

2. Implement field validation:
   - Surveyors cannot submit forms with blank mandatory fields
   - Use dropdown menus for Gender (Male/Female) to ensure consistency
   - Set valid ranges for numeric fields (e.g., land area: 0.1-20 HA)

3. Ensure Visit 2 completion:
   - Track farmers who completed Visit 1 to ensure Visit 2 happens
   - Progress tracking requires BOTH visits for the same farmer
   - Current gap: {farmers_single_visit} farmers have incomplete visit data

Impact: This will enable complete progress tracking for all 3,000 farmers.

═══════════════════════════════════════════════════════════════════════════════

RECOMMENDATION 2: DATA CLEANING & QUALITY CHECKS BY M&E ASSISTANT
═══════════════════════════════════════════════════════════════════════════════

Priority: HIGH

Issue: Data inconsistencies reduce analysis accuracy and reliability.

Standard Operating Procedure for M&E Assistant:

WEEKLY QUALITY CHECKS:
1. Duplicate Detection:
   - Check for duplicate Farmer Codes within same visit
   - Flag surveys submitted twice for same farmer-variable-visit combination
   
2. Range Validation:
   - Production: 0-10,000 KG (flag outliers for verification)
   - Land Area: 0.1-20 HA (flag outliers)
   - Result/Competence: Must be 0, 1, or 2 ONLY
   
3. Logical Consistency:
   - Visit 2 date must be AFTER Visit 1 date
   - Production should be proportional to land area (yield check)
   - Cross-check: If Result=0 (Bad), Competence should not be 2 (Good)

4. Completeness Report:
   - Generate weekly report showing % completion by cooperative
   - Flag cooperatives with >10% missing data for immediate follow-up

Tools Recommended:
- Use Excel Data Validation or Python scripts for automated checks
- Create standardized data cleaning checklist
- Document all data corrections with reasons

═══════════════════════════════════════════════════════════════════════════════

RECOMMENDATION 3: OPERATIONS TEAM - STANDARDIZATION & TRAINING
═══════════════════════════════════════════════════════════════════════════════

Priority: MEDIUM-HIGH

Issue: Inconsistent surveyor interpretation affects data comparability.

Actions for Operations Team:

1. STANDARDIZE SURVEY PROTOCOL:
   - Create clear definitions for Good/Medium/Bad adoption levels
   - Provide photo examples for each adoption practice
   - Develop scoring rubric: When is it "2" vs "1" vs "0"?

2. SURVEYOR TRAINING (Before 3,000 farmer rollout):
   - 1-day workshop on:
     * How to assess each of the 14 variables consistently
     * How to measure land area accurately (GPS or pacing method)
     * How to estimate production (farmer recall vs records)
   - Conduct inter-rater reliability test:
     * 3 surveyors assess same 5 farmers independently
     * Compare scores - should have 80%+ agreement

3. IMPLEMENT SPOT CHECKS:
   - Operations Manager randomly re-surveys 5% of farmers
   - Compare original vs validation data
   - Identify surveyors needing re-training

4. FEEDBACK LOOP:
   - Monthly meeting: M&E Assistant presents data quality issues
   - Operations Team addresses root causes (e.g., unclear questions)
   - Continuously improve survey instrument

═══════════════════════════════════════════════════════════════════════════════

ADDITIONAL OBSERVATIONS
═══════════════════════════════════════════════════════════════════════════════

Positive Findings:
- {len(variables)} adoption variables are being tracked (good coverage)
- Farmer identification system (Farmer Code) is in place
- Production and land size data provides yield analysis capability

Areas of Concern:
- Visit 2 completion rate needs improvement for progress tracking
- Some variables may have low sample sizes (review distribution)
- Gender data quality critical for segmentation analysis

Quick Wins for Next Survey Round:
1. Pre-print farmer codes on survey forms to reduce data entry errors
2. Use mobile data collection app with built-in validation rules
3. Set up real-time dashboard to monitor data collection progress by cooperative

═══════════════════════════════════════════════════════════════════════════════
END OF RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════════════════
"""

print(recommendations)

# Save recommendations
rec_file = f"{RESULTS_PATH}/1.4_data_quality_recommendations.txt"
with open(rec_file, 'w') as f:
    f.write(recommendations)
print(f"\n✓ Recommendations saved to: {rec_file}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nGenerated Files:")
print(f"1. Cleaned data: {cleaned_file}")
print(f"2. Result distribution: {result_file}")
print(f"3. Competence distribution: {competence_file}")
if len(progress_df) > 0:
    print(f"4. Progress tracking: {progress_file}")
    print(f"5. Progress summary: {summary_file}")
print(f"6. Production by gender: {gender_file}")
print(f"7. Production by land size: {landsize_file}")
print(f"8. Production summary: {summary_file}")
print(f"9. Recommendations: {rec_file}")

print("\n" + "="*80)
print("Ready for 2-pager report generation!")
print("="*80)
