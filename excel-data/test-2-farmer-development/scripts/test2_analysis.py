import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Create results directory
os.makedirs('results', exist_ok=True)

print("=" * 80)
print("FARMER DEVELOPMENT PLAN ANALYSIS - AUTOMATED REPORT")
print("=" * 80)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Location: Ivory Coast")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[STEP 1] Loading data...")

try:
    df = pd.read_excel('excel-data/test-2-farmer-development/raw/test_2_farmer_development_raw.xlsx')
    print(f"✓ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    print(f"✓ Columns: {', '.join(df.columns)}")

# Clean column names - remove extra spaces
    df.columns = df.columns.str.strip()
    print(f"✓ Cleaned column names")

except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# ============================================================================
# STEP 2: DATA CLEANING
# ============================================================================
print("\n[STEP 2] Data Cleaning...")

# 2.1 Check for missing values
print("\n2.1 Missing Values Check:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Column': missing.index,
    'Missing_Count': missing.values,
    'Missing_Percent': missing_pct.values
})
missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

if len(missing_df) > 0:
    print(missing_df.to_string(index=False))
    print(f"\n⚠ Found missing values in {len(missing_df)} columns")
else:
    print("✓ No missing values found")

# 2.2 Remove duplicates
print("\n2.2 Duplicate Check:")
duplicates = df.duplicated().sum()
print(f"Found {duplicates} duplicate rows")
if duplicates > 0:
    df.drop_duplicates(inplace=True)
    print(f"✓ Removed {duplicates} duplicates")

# 2.3 Data type conversions
print("\n2.3 Data Type Validation:")
# Ensure numeric columns are numeric
numeric_cols = ['Farm: Total Farm Area HA', 'Farm: Production - last baseline KG', 'Farm_BL: Average Farm gate cocoa price']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"✓ Converted {col} to numeric")

# Save cleaned data
df.to_csv('results/cleaned_data.csv', index=False)
print("\n✓ Cleaned data saved to 'results/cleaned_data.csv'")

# ============================================================================
# STEP 3: DATA STRUCTURE ANALYSIS
# ============================================================================
print("\n[STEP 3] Data Structure Analysis...")

# Check unique farmers and visits
unique_farmers = df['Farmer: Farmer Code'].nunique()
unique_visits = df['Visit Number'].nunique()
print(f"\n✓ Total unique farmers: {unique_farmers}")
print(f"✓ Visit numbers found: {sorted(df['Visit Number'].unique())}")

# Check visit distribution
visit_counts = df.groupby('Visit Number')['Farmer: Farmer Code'].nunique()
print(f"\n✓ Farmer count by visit:")
for visit, count in visit_counts.items():
    print(f"  - Visit {visit}: {count} farmers")

# ============================================================================
# STEP 4: CATEGORIZE RESULT AND COMPETENCE
# ============================================================================
print("\n[STEP 4] Categorizing Result and Competence...")

def categorize_score(value):
    """Categorize Result/Competence as Good/Medium/Bad"""
    if pd.isna(value):
        return 'Unknown'
    
    value_str = str(value).lower().strip()
    
    # Good indicators
    if any(word in value_str for word in ['good', 'high', 'excellent', 'strong', 'advanced']):
        return 'Good'
    
    # Bad indicators
    if any(word in value_str for word in ['bad', 'low', 'poor', 'weak', 'none', 'beginner']):
        return 'Bad'
    
    # Medium indicators
    if any(word in value_str for word in ['medium', 'moderate', 'fair', 'average', 'intermediate']):
        return 'Medium'
    
    # Default to Medium if unclear
    return 'Medium'

# Apply categorization
df['Result_Category'] = df['Result'].apply(categorize_score)
df['Competence_Category'] = df['Competence'].apply(categorize_score)

print("✓ Result categorization:")
print(df['Result_Category'].value_counts())
print("\n✓ Competence categorization:")
print(df['Competence_Category'].value_counts())

# ============================================================================
# STEP 5: FARM SIZE SEGMENTATION
# ============================================================================
print("\n[STEP 5] Farm Size Segmentation...")

def categorize_farm_size(size):
    """Categorize farm size into <2ha, 2-4ha, ≥4ha"""
    if pd.isna(size):
        return 'Unknown'
    if size < 2:
        return '<2ha'
    elif size < 4:
        return '2-4ha'
    else:
        return '≥4ha'

df['Farm_Size_Category'] = df['Farm: Total Farm Area HA'].apply(categorize_farm_size)

print("✓ Farm size distribution:")
print(df['Farm_Size_Category'].value_counts())

# ============================================================================
# STEP 6: PROGRESS TRACKING (VISIT 1 VS VISIT 2)
# ============================================================================
print("\n[STEP 6] Progress Tracking Analysis...")

# Create numeric scores for comparison
score_map = {'Good': 3, 'Medium': 2, 'Bad': 1, 'Unknown': 0}
df['Result_Score'] = df['Result_Category'].map(score_map)
df['Competence_Score'] = df['Competence_Category'].map(score_map)

# Get farmers who have both visits
farmers_with_multiple_visits = df[df['Visit Number'].isin([1, 2])].groupby('Farmer: Farmer Code').filter(lambda x: len(x['Visit Number'].unique()) > 1)

if len(farmers_with_multiple_visits) > 0:
    print(f"✓ Found {farmers_with_multiple_visits['Farmer: Farmer Code'].nunique()} farmers with multiple visits")
    
    # Create pivot for comparison
    progress_data = []
    
    for farmer_code in farmers_with_multiple_visits['Farmer: Farmer Code'].unique():
        farmer_data = df[df['Farmer: Farmer Code'] == farmer_code].sort_values('Visit Number')
        
        if len(farmer_data) >= 2:
            visit1 = farmer_data[farmer_data['Visit Number'] == 1].iloc[0] if len(farmer_data[farmer_data['Visit Number'] == 1]) > 0 else None
            visit2 = farmer_data[farmer_data['Visit Number'] == 2].iloc[0] if len(farmer_data[farmer_data['Visit Number'] == 2]) > 0 else None
            
            if visit1 is not None and visit2 is not None:
                progress_data.append({
                    'Farmer_Code': farmer_code,
                    'Result_V1': visit1['Result_Category'],
                    'Result_V2': visit2['Result_Category'],
                    'Result_Score_V1': visit1['Result_Score'],
                    'Result_Score_V2': visit2['Result_Score'],
                    'Competence_V1': visit1['Competence_Category'],
                    'Competence_V2': visit2['Competence_Category'],
                    'Competence_Score_V1': visit1['Competence_Score'],
                    'Competence_Score_V2': visit2['Competence_Score'],
                    'Gender': visit1['Farmer: Gender'],
                    'Farm_Size': visit1['Farm: Total Farm Area HA'],
                    'Farm_Size_Category': visit1['Farm_Size_Category']
                })
    
    if progress_data:
        progress_df = pd.DataFrame(progress_data)
        
        # Calculate progress
        progress_df['Result_Progress'] = progress_df['Result_Score_V2'] - progress_df['Result_Score_V1']
        progress_df['Competence_Progress'] = progress_df['Competence_Score_V2'] - progress_df['Competence_Score_V1']
        
        # Categorize progress
        def categorize_progress(score):
            if score > 0:
                return 'Improved'
            elif score == 0:
                return 'Stable'
            else:
                return 'Declined'
        
        progress_df['Result_Progress_Category'] = progress_df['Result_Progress'].apply(categorize_progress)
        progress_df['Competence_Progress_Category'] = progress_df['Competence_Progress'].apply(categorize_progress)
        
        # Calculate percentages
        result_progress_pct = progress_df['Result_Progress_Category'].value_counts(normalize=True) * 100
        competence_progress_pct = progress_df['Competence_Progress_Category'].value_counts(normalize=True) * 100
        
        print("\n✓ RESULT Progress (Visit 1 → Visit 2):")
        for category in ['Improved', 'Stable', 'Declined']:
            pct = result_progress_pct.get(category, 0)
            count = (progress_df['Result_Progress_Category'] == category).sum()
            print(f"  - {category}: {count} farmers ({pct:.1f}%)")
        
        print("\n✓ COMPETENCE Progress (Visit 1 → Visit 2):")
        for category in ['Improved', 'Stable', 'Declined']:
            pct = competence_progress_pct.get(category, 0)
            count = (progress_df['Competence_Progress_Category'] == category).sum()
            print(f"  - {category}: {count} farmers ({pct:.1f}%)")
        
        # Save progress data
        progress_df.to_csv('results/progress_tracking.csv', index=False)
        print("\n✓ Progress tracking data saved")
    else:
        print("⚠ No farmers with complete Visit 1 and Visit 2 data")
        progress_df = None
else:
    print("⚠ No farmers with multiple visits found")
    progress_df = None

# ============================================================================
# STEP 7: SEGMENTATION ANALYSIS
# ============================================================================
print("\n[STEP 7] Segmentation Analysis...")

# 7.1 Gender Analysis
print("\n7.1 Analysis by Gender:")
gender_result = pd.crosstab(df['Farmer: Gender'], df['Result_Category'], normalize='index') * 100
print("Result by Gender (%):")
print(gender_result.round(2))

gender_competence = pd.crosstab(df['Farmer: Gender'], df['Competence_Category'], normalize='index') * 100
print("\nCompetence by Gender (%):")
print(gender_competence.round(2))

# 7.2 Farm Size Analysis
print("\n7.2 Analysis by Farm Size:")
size_result = pd.crosstab(df['Farm_Size_Category'], df['Result_Category'], normalize='index') * 100
print("Result by Farm Size (%):")
print(size_result.round(2))

size_competence = pd.crosstab(df['Farm_Size_Category'], df['Competence_Category'], normalize='index') * 100
print("\nCompetence by Farm Size (%):")
print(size_competence.round(2))

# ============================================================================
# STEP 8: PRODUCTION/YIELD ANALYSIS
# ============================================================================
print("\n[STEP 8] Production/Yield Analysis...")

# Calculate yield (kg/ha)
df['Yield_kg_per_ha'] = df['Farm: Production - last baseline KG'] / df['Farm: Total Farm Area HA']

print("\n8.1 Yield Statistics:")
print(f"Average yield: {df['Yield_kg_per_ha'].mean():.2f} kg/ha")
print(f"Median yield: {df['Yield_kg_per_ha'].median():.2f} kg/ha")
print(f"Min yield: {df['Yield_kg_per_ha'].min():.2f} kg/ha")
print(f"Max yield: {df['Yield_kg_per_ha'].max():.2f} kg/ha")

# Yield by segments
print("\n8.2 Yield by Gender:")
yield_gender = df.groupby('Farmer: Gender')['Yield_kg_per_ha'].agg(['mean', 'median', 'count'])
print(yield_gender.round(2))

print("\n8.3 Yield by Farm Size:")
yield_size = df.groupby('Farm_Size_Category')['Yield_kg_per_ha'].agg(['mean', 'median', 'count'])
print(yield_size.round(2))

# ============================================================================
# STEP 9: LIVING INCOME CALCULATION
# ============================================================================
print("\n[STEP 9] Living Income Analysis...")

# Constants (based on requirements)
BASE_PRICE_CFA = 1000  # CFA per kg
PREMIUM_CFA = 40       # CFA per kg
TOTAL_PRICE_CFA = BASE_PRICE_CFA + PREMIUM_CFA
COCOA_REVENUE_PERCENTAGE = 0.72  # 72% of total revenue

# Calculate cocoa revenue
df['Cocoa_Revenue_CFA'] = df['Farm: Production - last baseline KG'] * TOTAL_PRICE_CFA

# Calculate total income (cocoa is 72% of total)
df['Total_Income_CFA'] = df['Cocoa_Revenue_CFA'] / COCOA_REVENUE_PERCENTAGE

print(f"\n✓ Average cocoa production: {df['Farm: Production - last baseline KG'].mean():.2f} kg")
print(f"✓ Average cocoa revenue: {df['Cocoa_Revenue_CFA'].mean():,.0f} CFA")
print(f"✓ Average total income: {df['Total_Income_CFA'].mean():,.0f} CFA")

# Note: Living Income Benchmark would need to be added based on Anker & Anker or LICOP data
print("\n⚠ Note: Living Income Gap calculation requires benchmark data (Anker & Anker/LICOP)")

# ============================================================================
# STEP 10: DATA VISUALIZATION
# ============================================================================
print("\n[STEP 10] Creating Visualizations...")

# 10.1 Result Distribution
plt.figure(figsize=(10, 6))
result_counts = df['Result_Category'].value_counts()
colors = {'Good': '#2ecc71', 'Medium': '#f39c12', 'Bad': '#e74c3c', 'Unknown': '#95a5a6'}
result_colors = [colors.get(x, '#95a5a6') for x in result_counts.index]
plt.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', colors=result_colors, startangle=90)
plt.title('Distribution of Result Categories', fontsize=16, fontweight='bold')
plt.savefig('results/01_result_distribution_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 01_result_distribution_pie.png")

# 10.2 Competence Distribution
plt.figure(figsize=(10, 6))
comp_counts = df['Competence_Category'].value_counts()
comp_colors = [colors.get(x, '#95a5a6') for x in comp_counts.index]
plt.pie(comp_counts, labels=comp_counts.index, autopct='%1.1f%%', colors=comp_colors, startangle=90)
plt.title('Distribution of Competence Categories', fontsize=16, fontweight='bold')
plt.savefig('results/02_competence_distribution_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 02_competence_distribution_pie.png")

# 10.3 Progress Tracking (if available)
if progress_df is not None and len(progress_df) > 0:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Result progress
    result_prog = progress_df['Result_Progress_Category'].value_counts()
    ax1.bar(result_prog.index, result_prog.values, color=['#2ecc71', '#95a5a6', '#e74c3c'])
    ax1.set_title('Result Progress (Visit 1 → Visit 2)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Farmers')
    ax1.grid(axis='y', alpha=0.3)
    
    # Competence progress
    comp_prog = progress_df['Competence_Progress_Category'].value_counts()
    ax2.bar(comp_prog.index, comp_prog.values, color=['#2ecc71', '#95a5a6', '#e74c3c'])
    ax2.set_title('Competence Progress (Visit 1 → Visit 2)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Number of Farmers')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/03_progress_tracking.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: 03_progress_tracking.png")

# 10.4 Gender Analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
gender_result.plot(kind='bar', ax=ax1, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
ax1.set_title('Result by Gender', fontsize=14, fontweight='bold')
ax1.set_xlabel('Gender')
ax1.set_ylabel('Percentage (%)')
ax1.legend(title='Result Category')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
ax1.grid(axis='y', alpha=0.3)

gender_competence.plot(kind='bar', ax=ax2, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
ax2.set_title('Competence by Gender', fontsize=14, fontweight='bold')
ax2.set_xlabel('Gender')
ax2.set_ylabel('Percentage (%)')
ax2.legend(title='Competence Category')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/04_gender_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 04_gender_analysis.png")

# 10.5 Farm Size Analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
size_result.plot(kind='bar', ax=ax1, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
ax1.set_title('Result by Farm Size', fontsize=14, fontweight='bold')
ax1.set_xlabel('Farm Size')
ax1.set_ylabel('Percentage (%)')
ax1.legend(title='Result Category')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
ax1.grid(axis='y', alpha=0.3)

size_competence.plot(kind='bar', ax=ax2, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
ax2.set_title('Competence by Farm Size', fontsize=14, fontweight='bold')
ax2.set_xlabel('Farm Size')
ax2.set_ylabel('Percentage (%)')
ax2.legend(title='Competence Category')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/05_farm_size_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 05_farm_size_analysis.png")

# 10.6 Yield Analysis
plt.figure(figsize=(12, 6))
df.boxplot(column='Yield_kg_per_ha', by='Farm_Size_Category', ax=plt.gca())
plt.title('Yield Distribution by Farm Size', fontsize=16, fontweight='bold')
plt.suptitle('')
plt.xlabel('Farm Size Category')
plt.ylabel('Yield (kg/ha)')
plt.savefig('results/06_yield_by_farm_size.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 06_yield_by_farm_size.png")

# 10.7 Income Distribution
plt.figure(figsize=(12, 6))
plt.hist(df['Total_Income_CFA'].dropna(), bins=30, color='#3498db', edgecolor='black', alpha=0.7)
plt.axvline(df['Total_Income_CFA'].mean(), color='red', linestyle='--', linewidth=2, 
           label=f"Mean: {df['Total_Income_CFA'].mean():,.0f} CFA")
plt.xlabel('Total Income (CFA)', fontsize=12)
plt.ylabel('Number of Farmers', fontsize=12)
plt.title('Distribution of Total Income', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.savefig('results/07_income_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 07_income_distribution.png")

# 10.8 Result vs Competence Correlation
if len(df[df['Result_Category'] != 'Unknown']) > 0:
    plt.figure(figsize=(10, 8))
    correlation_data = pd.crosstab(df['Result_Category'], df['Competence_Category'])
    sns.heatmap(correlation_data, annot=True, fmt='d', cmap='YlGnBu', square=True, linewidths=1)
    plt.title('Result vs Competence Correlation', fontsize=16, fontweight='bold')
    plt.xlabel('Competence Category')
    plt.ylabel('Result Category')
    plt.savefig('results/08_result_competence_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: 08_result_competence_correlation.png")

# ============================================================================
# STEP 11: COMPREHENSIVE REPORT
# ============================================================================
print("\n[STEP 11] Generating Comprehensive Report...")

report = f"""
{'='*80}
FARMER DEVELOPMENT PLAN ANALYSIS - COMPREHENSIVE REPORT
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Location: Ivory Coast

{'='*80}
1. EXECUTIVE SUMMARY
{'='*80}

Total Records Analyzed: {len(df)}
Unique Farmers: {unique_farmers}
Visits Tracked: {sorted(df['Visit Number'].unique())}

Overall Distribution:
RESULT:
  - Good: {(df['Result_Category'] == 'Good').sum()} ({(df['Result_Category'] == 'Good').sum()/len(df)*100:.1f}%)
  - Medium: {(df['Result_Category'] == 'Medium').sum()} ({(df['Result_Category'] == 'Medium').sum()/len(df)*100:.1f}%)
  - Bad: {(df['Result_Category'] == 'Bad').sum()} ({(df['Result_Category'] == 'Bad').sum()/len(df)*100:.1f}%)

COMPETENCE:
  - Good: {(df['Competence_Category'] == 'Good').sum()} ({(df['Competence_Category'] == 'Good').sum()/len(df)*100:.1f}%)
  - Medium: {(df['Competence_Category'] == 'Medium').sum()} ({(df['Competence_Category'] == 'Medium').sum()/len(df)*100:.1f}%)
  - Bad: {(df['Competence_Category'] == 'Bad').sum()} ({(df['Competence_Category'] == 'Bad').sum()/len(df)*100:.1f}%)

{'='*80}
2. PROGRESS TRACKING (VISIT 1 → VISIT 2)
{'='*80}
"""

if progress_df is not None and len(progress_df) > 0:
    result_improved = (progress_df['Result_Progress_Category'] == 'Improved').sum()
    result_stable = (progress_df['Result_Progress_Category'] == 'Stable').sum()
    result_declined = (progress_df['Result_Progress_Category'] == 'Declined').sum()
    
    comp_improved = (progress_df['Competence_Progress_Category'] == 'Improved').sum()
    comp_stable = (progress_df['Competence_Progress_Category'] == 'Stable').sum()
    comp_declined = (progress_df['Competence_Progress_Category'] == 'Declined').sum()
    
    report += f"""
Farmers with Multiple Visits: {len(progress_df)}

RESULT Progress:
  - Improved: {result_improved} farmers ({result_improved/len(progress_df)*100:.1f}%)
  - Stable: {result_stable} farmers ({result_stable/len(progress_df)*100:.1f}%)
  - Declined: {result_declined} farmers ({result_declined/len(progress_df)*100:.1f}%)

COMPETENCE Progress:
  - Improved: {comp_improved} farmers ({comp_improved/len(progress_df)*100:.1f}%)
  - Stable: {comp_stable} farmers ({comp_stable/len(progress_df)*100:.1f}%)
  - Declined: {comp_declined} farmers ({comp_declined/len(progress_df)*100:.1f}%)
"""
else:
    report += "\n⚠ Insufficient data for progress tracking analysis\n"

report += f"""
{'='*80}
3. SEGMENTATION ANALYSIS
{'='*80}

3.1 Gender Analysis:
{gender_result.to_string()}

3.2 Farm Size Analysis:
{size_result.to_string()}

{'='*80}
4. PRODUCTION & YIELD ANALYSIS
{'='*80}

Average Yield: {df['Yield_kg_per_ha'].mean():.2f} kg/ha
Median Yield: {df['Yield_kg_per_ha'].median():.2f} kg/ha

Yield by Gender:
{yield_gender.to_string()}

Yield by Farm Size:
{yield_size.to_string()}

{'='*80}
5. LIVING INCOME ANALYSIS
{'='*80}

Average Production: {df['Farm: Production - last baseline KG'].mean():.2f} kg
Cocoa Price: {TOTAL_PRICE_CFA} CFA/kg (Base: {BASE_PRICE_CFA} + Premium: {PREMIUM_CFA})
Average Cocoa Revenue: {df['Cocoa_Revenue_CFA'].mean():,.0f} CFA
Average Total Income: {df['Total_Income_CFA'].mean():,.0f} CFA

⚠ Note: Living Income Gap requires benchmark data (Anker & Anker/LICOP/KIT)

{'='*80}
6. DATA QUALITY RECOMMENDATIONS
{'='*80}

Based on the analysis, here are critical recommendations:

6.1 DATA COMPLETENESS:
"""

# Add specific recommendations based on missing data
if len(missing_df) > 0:
    report += "\n  Priority Areas with Missing Data:\n"
    for idx, row in missing_df.head(5).iterrows():
        report += f"  - {row['Column']}: {row['Missing_Percent']:.1f}% missing\n"
    report += "\n  ⚠ ACTION: Implement mandatory field validation during data collection\n"
else:
    report += "\n  ✓ No significant missing data issues found\n"

report += f"""

6.2 DATA QUALITY CHECKS:
  1. Standardize Result/Competence values (currently: {df['Result'].nunique()} unique Result values)
  2. Validate farm size entries (range: {df['Farm: Total Farm Area HA'].min():.2f} - {df['Farm: Total Farm Area HA'].max():.2f} ha)
  3. Ensure consistent visit numbering across all farmers
  4. Implement data validation rules in collection forms

6.3 M&E ASSISTANT & OPERATIONS TEAM GUIDELINES:
  1. Weekly data quality audits on new entries
  2. Cross-check farmer codes for consistency
  3. Validate production data against regional averages
  4. Flag outliers for field verification

{'='*80}
7. ACTIONABLE RECOMMENDATIONS
{'='*80}

7.1 IMMEDIATE ACTIONS:
"""

# Add context-specific recommendations
if progress_df is not None and len(progress_df) > 0:
    declined_pct = (progress_df['Result_Progress_Category'] == 'Declined').sum() / len(progress_df) * 100
    if declined_pct > 10:
        report += f"\n  ⚠ URGENT: {declined_pct:.1f}% of farmers declined - investigate root causes\n"

report += """
  1. Address data quality issues in priority fields
  2. Standardize data entry formats and values
  3. Implement field validation rules
  4. Train data collectors on consistent data entry

7.2 PROGRAM IMPROVEMENTS:
  1. Focus interventions on farmers with "Bad" Result/Competence
  2. Replicate successful practices from "Good" performers
  3. Provide targeted support based on farm size segments
  4. Address gender-specific barriers if significant gaps exist

7.3 MONITORING & EVALUATION:
  1. Track progress quarterly using standardized metrics
  2. Set clear targets for improvement percentages
  3. Monitor yield improvements as success indicator
  4. Calculate Living Income Gap once benchmark data is available

{'='*80}
8. NEXT STEPS FOR SCALING
{'='*80}

Current Status: Initial dataset from local Operations Team
Planned Scale: 3,000 additional farmers in next 6 months

Preparation Required:
  1. Finalize data collection forms based on quality findings
  2. Train field staff on standardized data entry
  3. Set up automated data validation systems
  4. Establish baseline benchmarks for comparison
  5. Create dashboard for real-time monitoring

{'='*80}
9. FILES GENERATED
{'='*80}

Data Files:
  - results/cleaned_data.csv
  - results/progress_tracking.csv (if applicable)

Visualizations:
  - results/01_result_distribution_pie.png
  - results/02_competence_distribution_pie.png
  - results/03_progress_tracking.png (if applicable)
  - results/04_gender_analysis.png
  - results/05_farm_size_analysis.png
  - results/06_yield_by_farm_size.png
  - results/07_income_distribution.png
  - results/08_result_competence_correlation.png

{'='*80}
END OF REPORT
{'='*80}
"""

# Save report
with open('results/COMPREHENSIVE_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ Comprehensive report saved to 'results/COMPREHENSIVE_REPORT.txt'")

# Save enhanced data
df.to_csv('results/data_with_categories.csv', index=False)
print("✓ Enhanced data saved to 'results/data_with_categories.csv'")

# Print summary to console
print(report)

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\n✓ All results saved in 'results/' folder")
print(f"✓ {len([f for f in os.listdir('results') if f.endswith('.png')])} visualizations created")
print(f"✓ {len([f for f in os.listdir('results') if f.endswith('.csv')])} data files generated")
print(f"✓ 1 comprehensive report generated")
print("\nThank you for using the Farmer Development Analysis System!")
print("="*80)
