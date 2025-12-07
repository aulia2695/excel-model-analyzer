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
    
    # Clean column names - remove extra spaces and standardize
    df.columns = df.columns.str.strip()
    print(f"✓ Original columns: {', '.join(df.columns)}")
    
    # Create column mapping for flexibility (handles variations in column names)
    column_mapping = {}
    for col in df.columns:
        clean_col = col.strip().lower().replace(':', '').replace(' ', '_')
        column_mapping[col] = clean_col
    
    # Rename columns to standardized format
    df.rename(columns={
        col: col.strip() for col in df.columns
    }, inplace=True)
    
    print(f"✓ Columns cleaned and ready for analysis")
    
except Exception as e:
    print(f"✗ Error loading data: {e}")
    print(f"Please check:")
    print(f"  1. File exists at: excel-data/test-2-farmer-development/raw/test_2_farmer_development_raw.xlsx")
    print(f"  2. File is a valid Excel file (.xlsx)")
    print(f"  3. File is not corrupted")
    exit(1)

# ============================================================================
# STEP 2: COLUMN NAME DETECTION (Flexible)
# ============================================================================
print("\n[STEP 2] Detecting column names...")

def find_column(df, possible_names):
    """Find column by checking multiple possible names"""
    for name in possible_names:
        if name in df.columns:
            return name
    # If exact match not found, try case-insensitive partial match
    for col in df.columns:
        col_lower = col.lower().strip()
        for name in possible_names:
            if name.lower().strip() in col_lower or col_lower in name.lower().strip():
                return col
    return None

# Define possible column name variations
farmer_code_col = find_column(df, ['Farmer: Farmer Code', 'Farmer Code', 'farmer_code', 'FarmerCode'])
farmer_name_col = find_column(df, ['Farmer: Full Name', 'Full Name', 'Farmer Name', 'Name'])
visit_col = find_column(df, ['Visit Number', 'Visit', 'VisitNumber'])
village_col = find_column(df, ['Farmer: Village', 'Village'])
gender_col = find_column(df, ['Farmer: Gender', 'Gender'])
education_col = find_column(df, ['Farmer: Educational Level', 'Educational Level', 'Education'])
farm_area_col = find_column(df, ['Farm: Total Farm Area HA', 'Total Farm Area HA', 'Farm Area', 'Farm_Area_Ha'])
production_col = find_column(df, ['Farm: Production - last baseline KG', 'Production', 'Production KG'])
price_col = find_column(df, ['Farm_BL: Average Farm gate cocoa price', 'Cocoa Price', 'Price'])
result_col = find_column(df, ['Result'])
competence_col = find_column(df, ['Competence'])

# Print detected columns
print(f"✓ Detected columns:")
print(f"  - Farmer Code: {farmer_code_col}")
print(f"  - Visit Number: {visit_col}")
print(f"  - Gender: {gender_col}")
print(f"  - Farm Area: {farm_area_col}")
print(f"  - Result: {result_col}")
print(f"  - Competence: {competence_col}")

# Check for essential columns
essential_cols = {
    'Farmer Code': farmer_code_col,
    'Visit Number': visit_col,
    'Result': result_col,
    'Competence': competence_col
}

missing_essential = [name for name, col in essential_cols.items() if col is None]
if missing_essential:
    print(f"\n⚠ WARNING: Missing essential columns: {', '.join(missing_essential)}")
    print(f"Available columns: {', '.join(df.columns)}")
    print(f"Analysis will continue with available data...")

# ============================================================================
# STEP 3: DATA CLEANING
# ============================================================================
print("\n[STEP 3] Data Cleaning...")

# 3.1 Check for missing values
print("\n3.1 Missing Values Check:")
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

# 3.2 Remove duplicates
print("\n3.2 Duplicate Check:")
duplicates = df.duplicated().sum()
print(f"Found {duplicates} duplicate rows")
if duplicates > 0:
    df.drop_duplicates(inplace=True)
    print(f"✓ Removed {duplicates} duplicates")

# 3.3 Data type conversions
print("\n3.3 Data Type Validation:")
if farm_area_col:
    df[farm_area_col] = pd.to_numeric(df[farm_area_col], errors='coerce')
    print(f"✓ Converted {farm_area_col} to numeric")
if production_col:
    df[production_col] = pd.to_numeric(df[production_col], errors='coerce')
    print(f"✓ Converted {production_col} to numeric")
if price_col:
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    print(f"✓ Converted {price_col} to numeric")

# Save cleaned data
df.to_csv('results/cleaned_data.csv', index=False)
print("\n✓ Cleaned data saved to 'results/cleaned_data.csv'")

# ============================================================================
# STEP 4: DATA STRUCTURE ANALYSIS
# ============================================================================
print("\n[STEP 4] Data Structure Analysis...")

if farmer_code_col and visit_col:
    unique_farmers = df[farmer_code_col].nunique()
    unique_visits = df[visit_col].nunique()
    print(f"\n✓ Total unique farmers: {unique_farmers}")
    print(f"✓ Visit numbers found: {sorted(df[visit_col].unique())}")
    
    visit_counts = df.groupby(visit_col)[farmer_code_col].nunique()
    print(f"\n✓ Farmer count by visit:")
    for visit, count in visit_counts.items():
        print(f"  - Visit {visit}: {count} farmers")
else:
    print("⚠ Cannot analyze data structure - missing farmer code or visit number")

# ============================================================================
# STEP 5: CATEGORIZE RESULT AND COMPETENCE
# ============================================================================
print("\n[STEP 5] Categorizing Result and Competence...")

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
if result_col:
    df['Result_Category'] = df[result_col].apply(categorize_score)
    print("✓ Result categorization:")
    print(df['Result_Category'].value_counts())
else:
    print("⚠ Result column not found - skipping Result categorization")
    df['Result_Category'] = 'Unknown'

if competence_col:
    df['Competence_Category'] = df[competence_col].apply(categorize_score)
    print("\n✓ Competence categorization:")
    print(df['Competence_Category'].value_counts())
else:
    print("⚠ Competence column not found - skipping Competence categorization")
    df['Competence_Category'] = 'Unknown'

# ============================================================================
# STEP 6: FARM SIZE SEGMENTATION
# ============================================================================
print("\n[STEP 6] Farm Size Segmentation...")

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

if farm_area_col:
    df['Farm_Size_Category'] = df[farm_area_col].apply(categorize_farm_size)
    print("✓ Farm size distribution:")
    print(df['Farm_Size_Category'].value_counts())
else:
    print("⚠ Farm area column not found - skipping farm size segmentation")
    df['Farm_Size_Category'] = 'Unknown'

# ============================================================================
# STEP 7: PROGRESS TRACKING (VISIT 1 VS VISIT 2)
# ============================================================================
print("\n[STEP 7] Progress Tracking Analysis...")

progress_df = None

if farmer_code_col and visit_col and result_col and competence_col:
    # Create numeric scores for comparison
    score_map = {'Good': 3, 'Medium': 2, 'Bad': 1, 'Unknown': 0}
    df['Result_Score'] = df['Result_Category'].map(score_map)
    df['Competence_Score'] = df['Competence_Category'].map(score_map)
    
    # Get farmers who have both visits
    farmers_with_multiple_visits = df[df[visit_col].isin([1, 2])].groupby(farmer_code_col).filter(
        lambda x: len(x[visit_col].unique()) > 1
    )
    
    if len(farmers_with_multiple_visits) > 0:
        print(f"✓ Found {farmers_with_multiple_visits[farmer_code_col].nunique()} farmers with multiple visits")
        
        # Create pivot for comparison
        progress_data = []
        
        for farmer_code in farmers_with_multiple_visits[farmer_code_col].unique():
            farmer_data = df[df[farmer_code_col] == farmer_code].sort_values(visit_col)
            
            if len(farmer_data) >= 2:
                visit1 = farmer_data[farmer_data[visit_col] == 1].iloc[0] if len(farmer_data[farmer_data[visit_col] == 1]) > 0 else None
                visit2 = farmer_data[farmer_data[visit_col] == 2].iloc[0] if len(farmer_data[farmer_data[visit_col] == 2]) > 0 else None
                
                if visit1 is not None and visit2 is not None:
                    progress_entry = {
                        'Farmer_Code': farmer_code,
                        'Result_V1': visit1['Result_Category'],
                        'Result_V2': visit2['Result_Category'],
                        'Result_Score_V1': visit1['Result_Score'],
                        'Result_Score_V2': visit2['Result_Score'],
                        'Competence_V1': visit1['Competence_Category'],
                        'Competence_V2': visit2['Competence_Category'],
                        'Competence_Score_V1': visit1['Competence_Score'],
                        'Competence_Score_V2': visit2['Competence_Score']
                    }
                    
                    if gender_col and gender_col in visit1.index:
                        progress_entry['Gender'] = visit1[gender_col]
                    if farm_area_col and farm_area_col in visit1.index:
                        progress_entry['Farm_Size'] = visit1[farm_area_col]
                        progress_entry['Farm_Size_Category'] = visit1['Farm_Size_Category']
                    
                    progress_data.append(progress_entry)
        
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
    else:
        print("⚠ No farmers with multiple visits found")
else:
    print("⚠ Missing required columns for progress tracking")

# ============================================================================
# STEP 8: SEGMENTATION ANALYSIS
# ============================================================================
print("\n[STEP 8] Segmentation Analysis...")

# 8.1 Gender Analysis
if gender_col:
    print("\n8.1 Analysis by Gender:")
    try:
        gender_result = pd.crosstab(df[gender_col], df['Result_Category'], normalize='index') * 100
        print("Result by Gender (%):")
        print(gender_result.round(2))
        
        gender_competence = pd.crosstab(df[gender_col], df['Competence_Category'], normalize='index') * 100
        print("\nCompetence by Gender (%):")
        print(gender_competence.round(2))
    except Exception as e:
        print(f"⚠ Could not perform gender analysis: {e}")
else:
    print("\n8.1 Gender column not found - skipping gender analysis")
    gender_result = None
    gender_competence = None

# 8.2 Farm Size Analysis
if farm_area_col:
    print("\n8.2 Analysis by Farm Size:")
    try:
        size_result = pd.crosstab(df['Farm_Size_Category'], df['Result_Category'], normalize='index') * 100
        print("Result by Farm Size (%):")
        print(size_result.round(2))
        
        size_competence = pd.crosstab(df['Farm_Size_Category'], df['Competence_Category'], normalize='index') * 100
        print("\nCompetence by Farm Size (%):")
        print(size_competence.round(2))
    except Exception as e:
        print(f"⚠ Could not perform farm size analysis: {e}")
else:
    print("\n8.2 Farm area column not found - skipping farm size analysis")
    size_result = None
    size_competence = None

# ============================================================================
# STEP 9: PRODUCTION/YIELD ANALYSIS
# ============================================================================
print("\n[STEP 9] Production/Yield Analysis...")

if production_col and farm_area_col:
    # Calculate yield (kg/ha)
    df['Yield_kg_per_ha'] = df[production_col] / df[farm_area_col]
    
    print("\n9.1 Yield Statistics:")
    print(f"Average yield: {df['Yield_kg_per_ha'].mean():.2f} kg/ha")
    print(f"Median yield: {df['Yield_kg_per_ha'].median():.2f} kg/ha")
    print(f"Min yield: {df['Yield_kg_per_ha'].min():.2f} kg/ha")
    print(f"Max yield: {df['Yield_kg_per_ha'].max():.2f} kg/ha")
    
    # Yield by segments
    if gender_col:
        print("\n9.2 Yield by Gender:")
        yield_gender = df.groupby(gender_col)['Yield_kg_per_ha'].agg(['mean', 'median', 'count'])
        print(yield_gender.round(2))
    
    print("\n9.3 Yield by Farm Size:")
    yield_size = df.groupby('Farm_Size_Category')['Yield_kg_per_ha'].agg(['mean', 'median', 'count'])
    print(yield_size.round(2))
else:
    print("⚠ Production or farm area column not found - skipping yield analysis")

# ============================================================================
# STEP 10: LIVING INCOME CALCULATION
# ============================================================================
print("\n[STEP 10] Living Income Analysis...")

if production_col:
    # Constants (based on requirements)
    BASE_PRICE_CFA = 1000  # CFA per kg
    PREMIUM_CFA = 40       # CFA per kg
    TOTAL_PRICE_CFA = BASE_PRICE_CFA + PREMIUM_CFA
    COCOA_REVENUE_PERCENTAGE = 0.72  # 72% of total revenue
    
    # Calculate cocoa revenue
    df['Cocoa_Revenue_CFA'] = df[production_col] * TOTAL_PRICE_CFA
    
    # Calculate total income (cocoa is 72% of total)
    df['Total_Income_CFA'] = df['Cocoa_Revenue_CFA'] / COCOA_REVENUE_PERCENTAGE
    
    print(f"\n✓ Average cocoa production: {df[production_col].mean():.2f} kg")
    print(f"✓ Average cocoa revenue: {df['Cocoa_Revenue_CFA'].mean():,.0f} CFA")
    print(f"✓ Average total income: {df['Total_Income_CFA'].mean():,.0f} CFA")
    
    # Note: Living Income Benchmark would need to be added
    print("\n⚠ Note: Living Income Gap calculation requires benchmark data (Anker & Anker/LICOP)")
else:
    print("⚠ Production column not found - skipping living income analysis")

# ============================================================================
# STEP 11: DATA VISUALIZATION
# ============================================================================
print("\n[STEP 11] Creating Visualizations...")

# 11.1 Result Distribution
plt.figure(figsize=(10, 6))
result_counts = df['Result_Category'].value_counts()
colors = {'Good': '#2ecc71', 'Medium': '#f39c12', 'Bad': '#e74c3c', 'Unknown': '#95a5a6'}
result_colors = [colors.get(x, '#95a5a6') for x in result_counts.index]
plt.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', colors=result_colors, startangle=90)
plt.title('Distribution of Result Categories', fontsize=16, fontweight='bold')
plt.savefig('results/01_result_distribution_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 01_result_distribution_pie.png")

# 11.2 Competence Distribution
plt.figure(figsize=(10, 6))
comp_counts = df['Competence_Category'].value_counts()
comp_colors = [colors.get(x, '#95a5a6') for x in comp_counts.index]
plt.pie(comp_counts, labels=comp_counts.index, autopct='%1.1f%%', colors=comp_colors, startangle=90)
plt.title('Distribution of Competence Categories', fontsize=16, fontweight='bold')
plt.savefig('results/02_competence_distribution_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 02_competence_distribution_pie.png")

# 11.3 Progress Tracking (if available)
if progress_df is not None and len(progress_df) > 0:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Result progress
    result_prog = progress_df['Result_Progress_Category'].value_counts()
    result_prog = result_prog.reindex(['Improved', 'Stable', 'Declined'], fill_value=0)
    ax1.bar(result_prog.index, result_prog.values, color=['#2ecc71', '#95a5a6', '#e74c3c'])
    ax1.set_title('Result Progress (Visit 1 → Visit 2)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Farmers')
    ax1.grid(axis='y', alpha=0.3)
    
    # Competence progress
    comp_prog = progress_df['Competence_Progress_Category'].value_counts()
    comp_prog = comp_prog.reindex(['Improved', 'Stable', 'Declined'], fill_value=0)
    ax2.bar(comp_prog.index, comp_prog.values, color=['#2ecc71', '#95a5a6', '#e74c3c'])
    ax2.set_title('Competence Progress (Visit 1 → Visit 2)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Number of Farmers')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/03_progress_tracking.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: 03_progress_tracking.png")

# 11.4 Gender Analysis (if available)
if gender_col and gender_result is not None and gender_competence is not None:
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        gender_result.plot(kind='bar', ax=ax1, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
        ax1.set_title('Result by Gender', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Gender')
        ax1.set_ylabel('Percentage (%)')
        ax1.legend(title='Result Category', bbox_to_anchor=(1.05, 1))
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        gender_competence.plot(kind='bar', ax=ax2, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
        ax2.set_title('Competence by Gender', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Gender')
        ax2.set_ylabel('Percentage (%)')
        ax2.legend(title='Competence Category', bbox_to_anchor=(1.05, 1))
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/04_gender_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created: 04_gender_analysis.png")
    except Exception as e:
        print(f"⚠ Could not create gender analysis chart: {e}")

# 11.5 Farm Size Analysis (if available)
if farm_area_col and size_result is not None and size_competence is not None:
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        size_result.plot(kind='bar', ax=ax1, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
        ax1.set_title('Result by Farm Size', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Farm Size')
        ax1.set_ylabel('Percentage (%)')
        ax1.legend(title='Result Category', bbox_to_anchor=(1.05, 1))
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        size_competence.plot(kind='bar', ax=ax2, color=['#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
        ax2.set_title('Competence by Farm Size', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Farm Size')
        ax2.set_ylabel('Percentage (%)')
        ax2.legend(title='Competence Category', bbox_to_anchor=(1.05, 1))
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/05_farm_size_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created: 05_farm_size_analysis.png")
    except Exception as e:
        print(f"⚠ Could not create farm size analysis chart: {e}")

# 11.6 Yield Analysis (if available)
if production_col and farm_area_col and 'Yield_kg_per_ha' in df.columns:
    try:
        plt.figure(figsize=(12, 6))
        df.boxplot(column='Yield_kg_per_ha', by='Farm_Size_Category', ax=plt.gca())
        plt.title('Yield Distribution by Farm Size', fontsize=16, fontweight='bold')
        plt.suptitle('')
        plt.xlabel('Farm Size Category')
        plt.ylabel('Yield (kg/ha)')
        plt.savefig('results/06_yield_by_farm_size.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created: 06_yield_by_farm_size.png")
    except Exception as e:
        print(f"⚠ Could not create yield chart: {e}")

# 11.7 Income Distribution (if available)
if 'Total_Income_CFA' in df.columns:
    try:
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
    except Exception as e:
        print(f"⚠ Could not create income distribution chart: {e}")

# 11.8 Result vs Competence Correlation
try:
    if len(df[(df['Result_Category'] != 'Unknown') & (df['Competence_Category'] != 'Unknown')]) > 0:
        plt.figure(figsize=(10, 8))
        correlation_data = pd.crosstab(df['Result_Category'], df['Competence_Category'])
        sns.heatmap(correlation_data, annot=True, fmt='d', cmap='YlGnBu', square=True, linewidths=1)
        plt.title('Result vs Competence Correlation', fontsize=16, fontweight='bold')
        plt.xlabel('Competence Category')
        plt.ylabel('Result Category')
        plt.savefig('results/08_result_competence_correlation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created: 08_result_competence_correlation.png")
except Exception as e:
    print(f"⚠ Could not create correlation heatmap: {e}")

# ============================================================================
# STEP 12: COMPREHENSIVE REPORT
# ============================================================================
print("\n[STEP 12] Generating Comprehensive Report...")

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
"""

if farmer_code_col:
    report += f"Unique Farmers: {df[farmer_code_col].nunique()}\n"
if visit_col:
    report += f"Visits Tracked: {sorted(df[visit_col].unique())}\n"

report += f"""
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
"""

if gender_col and gender_result is not None:
    report += f"\n3.1 Gender Analysis:\n{gender_result.to_string()}\n"
else:
    report += "\n3.1 Gender Analysis: Not available\n"

if farm_area_col and size_result is not None:
    report += f"\n3.2 Farm Size Analysis:\n{size_result.to_string()}\n"
else:
    report += "\n3.2 Farm Size Analysis: Not available\n"

report += f"""
{'='*80}
4. PRODUCTION & YIELD ANALYSIS
{'='*80}
"""

if production_col and farm_area_col and 'Yield_kg_per_ha' in df.columns:
    report += f"""
Average Yield: {df['Yield_kg_per_ha'].mean():.2f} kg/ha
Median Yield: {df['Yield_kg_per_ha'].median():.2f} kg/ha
"""
    if gender_col:
        report += f"\nYield by Gender:\n{df.groupby(gender_col)['Yield_kg_per_ha'].agg(['mean', 'median', 'count']).to_string()}\n"
    
    report += f"\nYield by Farm Size:\n{df.groupby('Farm_Size_Category')['Yield_kg_per_ha'].agg(['mean', 'median', 'count']).to_string()}\n"
else:
    report += "\n⚠ Production/yield data not available\n"

report += f"""
{'='*80}
5. LIVING INCOME ANALYSIS
{'='*80}
"""

if production_col and 'Cocoa_Revenue_CFA' in df.columns:
    BASE_PRICE_CFA = 1000
    PREMIUM_CFA = 40
    TOTAL_PRICE_CFA = BASE_PRICE_CFA + PREMIUM_CFA
    
    report += f"""
Average Production: {df[production_col].mean():.2f} kg
Cocoa Price: {TOTAL_PRICE_CFA} CFA/kg (Base: {BASE_PRICE_CFA} + Premium: {PREMIUM_CFA})
Average Cocoa Revenue: {df['Cocoa_Revenue_CFA'].mean():,.0f} CFA
Average Total Income: {df['Total_Income_CFA'].mean():,.0f} CFA

⚠ Note: Living Income Gap requires benchmark data (Anker & Anker/LICOP/KIT)
"""
else:
    report += "\n⚠ Income data not available\n"

report += f"""
{'='*80}
6. DATA QUALITY RECOMMENDATIONS
{'='*80}

Based on the analysis, here are critical recommendations:

6.1 DATA COMPLETENESS:
"""

if len(missing_df) > 0:
    report += "\n  Priority Areas with Missing Data:\n"
    for idx, row in missing_df.head(5).iterrows():
        report += f"  - {row['Column']}: {row['Missing_Percent']:.1f}% missing\n"
    report += "\n  ⚠ ACTION: Implement mandatory field validation during data collection\n"
else:
    report += "\n  ✓ No significant missing data issues found\n"

report += f"""
6.2 DATA QUALITY CHECKS:
  1. Standardize Result/Competence values for consistency
  2. Validate farm size entries (ensure realistic ranges)
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
  - results/data_with_categories.csv
"""

if progress_df is not None:
    report += "  - results/progress_tracking.csv\n"

report += """
Visualizations (as available):
  - results/01_result_distribution_pie.png
  - results/02_competence_distribution_pie.png
  - results/03_progress_tracking.png
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

# Count generated files
import glob
png_files = glob.glob('results/*.png')
csv_files = glob.glob('results/*.csv')
print(f"✓ {len(png_files)} visualizations created")
print(f"✓ {len(csv_files)} data files generated")
print(f"✓ 1 comprehensive report generated")

print("\nThank you for using the Farmer Development Analysis System!")
print("="*80)
