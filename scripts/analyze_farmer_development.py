"""
Farmer Development Plan Analysis Script
Analyzes baseline adoption, progress tracking, and production segmentation
Designed for GitHub Actions automation
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

IS_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS') == 'true'

if IS_GITHUB_ACTIONS:
    BASE_PATH = 'excel-data/test-2-farmer-development'
    RAW_PATH = os.path.join(BASE_PATH, 'raw')
    RESULTS_PATH = os.path.join(BASE_PATH, 'results')
    CLEANED_PATH = os.path.join(BASE_PATH, 'cleaned')
    
    # Find the Excel file
    raw_files = [f for f in os.listdir(RAW_PATH) if f.endswith(('.xlsx', '.xls'))]
    if not raw_files:
        print("❌ Error: No Excel file found in raw folder!")
        sys.exit(1)
    INPUT_FILE = os.path.join(RAW_PATH, raw_files[0])
else:
    INPUT_FILE = 'test_2_farmer_development_raw.xlsx'
    RESULTS_PATH = 'results/'
    CLEANED_PATH = 'cleaned/'

os.makedirs(RESULTS_PATH, exist_ok=True)
os.makedirs(CLEANED_PATH, exist_ok=True)

# =============================================================================
# STEP 1: LOAD DATA
# =============================================================================

print("="*70)
print("FARMER DEVELOPMENT PLAN ANALYSIS")
print("="*70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Running in: {'GitHub Actions' if IS_GITHUB_ACTIONS else 'Local'}")
print("="*70)

print("\n[1/6] Loading data...")
print(f"   • Input file: {INPUT_FILE}")

df = pd.read_excel(INPUT_FILE)
print(f"   ✓ Loaded {len(df)} records")

# Display column names for verification
print(f"   • Columns found: {len(df.columns)}")

# =============================================================================
# STEP 2: DATA CLEANING & PREPARATION
# =============================================================================

print("\n[2/6] Cleaning and preparing data...")

# Create cleaned dataframe
df_clean = df.copy()

# Convert adoption scores to numeric (G=2, M=1, B=0)
adoption_mapping = {'G': 2, 'M': 1, 'B': 0}

for col in ['Response', 'Result', 'Competence']:
    if col in df_clean.columns:
        df_clean[f'{col}_numeric'] = df_clean[col].map(adoption_mapping)
        print(f"   ✓ Converted {col} to numeric scores")

# Convert gender to numeric (Male=2, Female=1)
if 'Farmer: Gender' in df_clean.columns:
    gender_mapping = {'Male': 2, 'Female': 1}
    df_clean['Gender_numeric'] = df_clean['Farmer: Gender'].map(gender_mapping)
    print(f"   ✓ Converted Gender to numeric")

# Categorize land size
if 'Farm: Total Farm Area HA' in df_clean.columns:
    df_clean['Farm: Total Farm Area HA'] = pd.to_numeric(df_clean['Farm: Total Farm Area HA'], errors='coerce')
    
    def categorize_land_size(ha):
        if pd.isna(ha):
            return 'Unknown'
        elif ha < 2:
            return '<2ha'
        elif ha < 4:
            return '2-4ha'
        else:
            return '≥4ha'
    
    df_clean['Land_Size_Category'] = df_clean['Farm: Total Farm Area HA'].apply(categorize_land_size)
    print(f"   ✓ Categorized land sizes")

# Convert production to numeric
if 'Farm: Production - last baseline KG' in df_clean.columns:
    df_clean['Farm: Production - last baseline KG'] = pd.to_numeric(
        df_clean['Farm: Production - last baseline KG'], errors='coerce'
    )
    print(f"   ✓ Converted production to numeric")

# Save cleaned data
cleaned_file = os.path.join(CLEANED_PATH, f'farmer_development_cleaned_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
df_clean.to_excel(cleaned_file, index=False)
print(f"   ✓ Saved cleaned data: {cleaned_file}")

# =============================================================================
# STEP 3: BASELINE ADOPTION ANALYSIS
# =============================================================================

print("\n[3/6] Analyzing baseline adoption (G/M/B distribution)...")

adoption_results = {}

for col in ['Response', 'Result', 'Competence']:
    if col in df_clean.columns:
        counts = df_clean[col].value_counts()
        total = counts.sum()
        
        adoption_results[col] = {
            'Good (G)': counts.get('G', 0),
            'Medium (M)': counts.get('M', 0),
            'Bad (B)': counts.get('B', 0),
            'Good %': (counts.get('G', 0) / total * 100) if total > 0 else 0,
            'Medium %': (counts.get('M', 0) / total * 100) if total > 0 else 0,
            'Bad %': (counts.get('B', 0) / total * 100) if total > 0 else 0,
        }
        
        print(f"\n   {col}:")
        print(f"      • Good (G): {counts.get('G', 0)} ({(counts.get('G', 0) / total * 100):.1f}%)")
        print(f"      • Medium (M): {counts.get('M', 0)} ({(counts.get('M', 0) / total * 100):.1f}%)")
        print(f"      • Bad (B): {counts.get('B', 0)} ({(counts.get('B', 0) / total * 100):.1f}%)")

# Create baseline adoption chart
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red

for idx, col in enumerate(['Response', 'Result', 'Competence']):
    if col in adoption_results:
        data = adoption_results[col]
        categories = ['Good', 'Medium', 'Bad']
        values = [data['Good (G)'], data['Medium (M)'], data['Bad (B)']]
        
        axes[idx].bar(categories, values, color=colors)
        axes[idx].set_title(f'{col} Distribution', fontsize=12, weight='bold')
        axes[idx].set_ylabel('Number of Farmers')
        axes[idx].set_xlabel('Adoption Level')
        
        # Add value labels on bars
        for i, v in enumerate(values):
            axes[idx].text(i, v + max(values)*0.02, str(v), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
chart1_path = os.path.join(RESULTS_PATH, 'chart_baseline_adoption.png')
plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
print(f"\n   ✓ Saved chart: chart_baseline_adoption.png")
plt.close()

# =============================================================================
# STEP 4: PROGRESS ANALYSIS (Visit 1 vs Visit 2)
# =============================================================================

print("\n[4/6] Analyzing progress between visits...")

if 'Visit Number' in df_clean.columns and 'Farmer: Farmer Code' in df_clean.columns:
    # Get unique farmers with multiple visits
    farmer_visits = df_clean.groupby('Farmer: Farmer Code')['Visit Number'].nunique()
    farmers_with_2_visits = farmer_visits[farmer_visits >= 2].index
    
    if len(farmers_with_2_visits) > 0:
        progress_data = {
            'Improving': 0,
            'Same': 0,
            'Deteriorating': 0
        }
        
        for farmer_code in farmers_with_2_visits:
            farmer_data = df_clean[df_clean['Farmer: Farmer Code'] == farmer_code].sort_values('Visit Number')
            
            if len(farmer_data) >= 2:
                visit1 = farmer_data.iloc[0]
                visit2 = farmer_data.iloc[-1]
                
                # Compare Result scores
                if 'Result_numeric' in farmer_data.columns:
                    score1 = visit1['Result_numeric']
                    score2 = visit2['Result_numeric']
                    
                    if pd.notna(score1) and pd.notna(score2):
                        if score2 > score1:
                            progress_data['Improving'] += 1
                        elif score2 == score1:
                            progress_data['Same'] += 1
                        else:
                            progress_data['Deteriorating'] += 1
        
        total_farmers = sum(progress_data.values())
        
        if total_farmers > 0:
            print(f"   • Farmers with 2+ visits: {len(farmers_with_2_visits)}")
            print(f"   • Analyzed: {total_farmers} farmers")
            print(f"\n   Progress Status:")
            print(f"      • Improving: {progress_data['Improving']} ({progress_data['Improving']/total_farmers*100:.1f}%)")
            print(f"      • Same level: {progress_data['Same']} ({progress_data['Same']/total_farmers*100:.1f}%)")
            print(f"      • Deteriorating: {progress_data['Deteriorating']} ({progress_data['Deteriorating']/total_farmers*100:.1f}%)")
            
            # Create progress chart
            fig, ax = plt.subplots(figsize=(10, 6))
            categories = list(progress_data.keys())
            values = list(progress_data.values())
            percentages = [v/total_farmers*100 for v in values]
            colors_progress = ['#2ecc71', '#95a5a6', '#e74c3c']
            
            bars = ax.bar(categories, values, color=colors_progress)
            ax.set_title('Farmer Progress: Visit 1 → Visit 2', fontsize=14, weight='bold')
            ax.set_ylabel('Number of Farmers')
            ax.set_xlabel('Progress Status')
            
            # Add percentage labels
            for i, (bar, pct) in enumerate(zip(bars, percentages)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(values[i])}\n({pct:.1f}%)',
                       ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            chart2_path = os.path.join(RESULTS_PATH, 'chart_progress_analysis.png')
            plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
            print(f"\n   ✓ Saved chart: chart_progress_analysis.png")
            plt.close()
        else:
            print("   ⚠ No farmers with comparable visit data found")
    else:
        print("   ⚠ No farmers with multiple visits found")
else:
    print("   ⚠ Required columns for progress analysis not found")

# =============================================================================
# STEP 5: PRODUCTION ANALYSIS BY GENDER
# =============================================================================

print("\n[5/6] Analyzing production by gender...")

if 'Farmer: Gender' in df_clean.columns and 'Farm: Production - last baseline KG' in df_clean.columns:
    production_by_gender = df_clean.groupby('Farmer: Gender')['Farm: Production - last baseline KG'].agg([
        ('Average', 'mean'),
        ('Count', 'count'),
        ('Total', 'sum')
    ]).round(2)
    
    print("\n   Production by Gender:")
    for gender in production_by_gender.index:
        avg = production_by_gender.loc[gender, 'Average']
        count = production_by_gender.loc[gender, 'Count']
        total = production_by_gender.loc[gender, 'Total']
        print(f"      • {gender}: {avg:.2f} kg average ({count} farmers, {total:.2f} kg total)")
    
    # Create gender chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Average production
    ax1.bar(production_by_gender.index, production_by_gender['Average'], color=['#3498db', '#e91e63'])
    ax1.set_title('Average Production by Gender', fontsize=12, weight='bold')
    ax1.set_ylabel('Average Production (KG)')
    ax1.set_xlabel('Gender')
    
    for i, v in enumerate(production_by_gender['Average']):
        ax1.text(i, v + v*0.02, f'{v:.0f} kg', ha='center', va='bottom', fontweight='bold')
    
    # Farmer count
    ax2.bar(production_by_gender.index, production_by_gender['Count'], color=['#3498db', '#e91e63'])
    ax2.set_title('Number of Farmers by Gender', fontsize=12, weight='bold')
    ax2.set_ylabel('Number of Farmers')
    ax2.set_xlabel('Gender')
    
    for i, v in enumerate(production_by_gender['Count']):
        ax2.text(i, v + v*0.02, f'{int(v)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    chart3_path = os.path.join(RESULTS_PATH, 'chart_production_by_gender.png')
    plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
    print(f"\n   ✓ Saved chart: chart_production_by_gender.png")
    plt.close()
else:
    print("   ⚠ Required columns for gender analysis not found")

# =============================================================================
# STEP 6: PRODUCTION ANALYSIS BY LAND SIZE
# =============================================================================

print("\n[6/6] Analyzing production by land size...")

if 'Land_Size_Category' in df_clean.columns and 'Farm: Production - last baseline KG' in df_clean.columns:
    # Order categories
    category_order = ['<2ha', '2-4ha', '≥4ha', 'Unknown']
    
    production_by_land = df_clean.groupby('Land_Size_Category')['Farm: Production - last baseline KG'].agg([
        ('Average', 'mean'),
        ('Count', 'count'),
        ('Total', 'sum')
    ]).round(2)
    
    # Reorder
    production_by_land = production_by_land.reindex([cat for cat in category_order if cat in production_by_land.index])
    
    print("\n   Production by Land Size:")
    for size in production_by_land.index:
        avg = production_by_land.loc[size, 'Average']
        count = production_by_land.loc[size, 'Count']
        total = production_by_land.loc[size, 'Total']
        print(f"      • {size}: {avg:.2f} kg average ({int(count)} farmers, {total:.2f} kg total)")
    
    # Create land size chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors_land = ['#e74c3c', '#f39c12', '#2ecc71', '#95a5a6']
    
    # Average production
    ax1.bar(range(len(production_by_land)), production_by_land['Average'], 
            color=colors_land[:len(production_by_land)])
    ax1.set_title('Average Production by Land Size', fontsize=12, weight='bold')
    ax1.set_ylabel('Average Production (KG)')
    ax1.set_xlabel('Land Size Category')
    ax1.set_xticks(range(len(production_by_land)))
    ax1.set_xticklabels(production_by_land.index, rotation=0)
    
    for i, v in enumerate(production_by_land['Average']):
        ax1.text(i, v + v*0.02, f'{v:.0f} kg', ha='center', va='bottom', fontweight='bold')
    
    # Farmer count
    ax2.bar(range(len(production_by_land)), production_by_land['Count'],
            color=colors_land[:len(production_by_land)])
    ax2.set_title('Number of Farmers by Land Size', fontsize=12, weight='bold')
    ax2.set_ylabel('Number of Farmers')
    ax2.set_xlabel('Land Size Category')
    ax2.set_xticks(range(len(production_by_land)))
    ax2.set_xticklabels(production_by_land.index, rotation=0)
    
    for i, v in enumerate(production_by_land['Count']):
        ax2.text(i, v + v*0.02, f'{int(v)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    chart4_path = os.path.join(RESULTS_PATH, 'chart_production_by_landsize.png')
    plt.savefig(chart4_path, dpi=300, bbox_inches='tight')
    print(f"\n   ✓ Saved chart: chart_production_by_landsize.png")
    plt.close()
else:
    print("   ⚠ Required columns for land size analysis not found")

# =============================================================================
# CREATE EXCEL REPORTS
# =============================================================================

print("\n[7/7] Creating Excel reports...")

# Create comprehensive report
report_file = os.path.join(RESULTS_PATH, f'analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')

with pd.ExcelWriter(report_file, engine='openpyxl') as writer:
    # Sheet 1: Baseline Adoption Summary
    if adoption_results:
        adoption_df = pd.DataFrame(adoption_results).T
        adoption_df.to_excel(writer, sheet_name='Baseline Adoption', index=True)
    
    # Sheet 2: Production by Gender
    if 'Farmer: Gender' in df_clean.columns:
        production_by_gender.to_excel(writer, sheet_name='Production by Gender', index=True)
    
    # Sheet 3: Production by Land Size
    if 'Land_Size_Category' in df_clean.columns:
        production_by_land.to_excel(writer, sheet_name='Production by Land Size', index=True)
    
    # Sheet 4: Data Quality Recommendations
    recommendations = pd.DataFrame({
        'Category': [
            'Data Completeness',
            'Data Completeness',
            'Data Completeness',
            'Data Quality',
            'Data Quality',
            'Data Quality',
            'Data Cleaning',
            'Data Cleaning',
            'Data Cleaning'
        ],
        'Recommendation': [
            'Ensure all mandatory fields are filled (Farmer Code, Gender, Production)',
            'Validate GPS coordinates for farm locations if available',
            'Collect visit dates to track temporal progress accurately',
            'Implement field validation rules in data collection forms',
            'Add range checks for numerical fields (e.g., production > 0)',
            'Standardize categorical responses (avoid mixed case, typos)',
            'Remove duplicate farmer entries before analysis',
            'Flag and investigate outliers in production data',
            'Create data quality dashboard showing completeness rates'
        ],
        'Priority': [
            'High',
            'Medium',
            'High',
            'High',
            'High',
            'Medium',
            'High',
            'Medium',
            'Medium'
        ]
    })
    recommendations.to_excel(writer, sheet_name='Recommendations', index=False)

print(f"   ✓ Saved report: {report_file}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print(f"\n📊 SUMMARY:")
print(f"   • Total records analyzed: {len(df)}")
print(f"   • Unique farmers: {df['Farmer: Farmer Code'].nunique() if 'Farmer: Farmer Code' in df.columns else 'N/A'}")
print(f"   • Variables analyzed: Response, Result, Competence")
print(f"   • Charts generated: 4")
print(f"   • Reports created: 1")
print(f"\n📁 OUTPUT LOCATIONS:")
print(f"   • Results: {RESULTS_PATH}/")
print(f"   • Cleaned data: {CLEANED_PATH}/")
print("\n" + "="*70)
