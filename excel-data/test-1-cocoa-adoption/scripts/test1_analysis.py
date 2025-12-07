import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# PATH CONFIGURATION - UPDATED FOR NEW DIRECTORY STRUCTURE
# ============================================================================

# Get the directory where this script is located
script_dir = Path(__file__).parent.absolute()

# Navigate to the test-1-cocoa-adoption directory (parent of scripts/)
test_dir = script_dir.parent

# Define output directories (now inside test-1-cocoa-adoption/)
results_dir = test_dir / "results"
cleaned_dir = test_dir / "cleaned"

# Create directories if they don't exist
results_dir.mkdir(parents=True, exist_ok=True)
cleaned_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("COCOA ADOPTION ANALYSIS - AUTOMATED REPORT")
print("=" * 80)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print(f"\n📁 Working Directories:")
print(f"   Script location: {script_dir}")
print(f"   Test directory:  {test_dir}")
print(f"   Results folder:  {results_dir}")
print(f"   Cleaned folder:  {cleaned_dir}")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[STEP 1] Loading data...")

try:
    # Path to raw data file (relative to test directory)
    data_file = test_dir / "raw" / "test_1_cocoa_adoption_raw.xlsx"
    df = pd.read_excel(data_file)
    print(f"✓ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    print(f"✓ Columns: {', '.join(df.columns)}")
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
    print(f"\n✓ Found missing values in {len(missing_df)} columns")
    
    # Handle missing values - fill with mode for categorical, median for numerical
    for col in missing_df['Column']:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)
    print("✓ Missing values handled")
else:
    print("✓ No missing values found")

# 2.2 Remove duplicates
print("\n2.2 Duplicate Check:")
duplicates = df.duplicated().sum()
print(f"Found {duplicates} duplicate rows")
if duplicates > 0:
    df.drop_duplicates(inplace=True)
    print(f"✓ Removed {duplicates} duplicates")

# 2.3 Check for outliers in Farm size
print("\n2.3 Outlier Detection (Farm size):")
Q1 = df['Farm size'].quantile(0.25)
Q3 = df['Farm size'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['Farm size'] < lower_bound) | (df['Farm size'] > upper_bound)]
print(f"Farm size range: {df['Farm size'].min():.2f} - {df['Farm size'].max():.2f}")
print(f"IQR bounds: {lower_bound:.2f} - {upper_bound:.2f}")
print(f"Found {len(outliers)} outliers (kept for analysis)")

# Save cleaned data - UPDATED PATH
cleaned_data_file = cleaned_dir / "cleaned_data.csv"
df.to_csv(cleaned_data_file, index=False)
print(f"\n✓ Cleaned data saved to '{cleaned_data_file}'")

# ============================================================================
# STEP 3: CALCULATE ADOPTION LEVEL
# ============================================================================
print("\n[STEP 3] Calculating Adoption Level...")

# Define practice columns to evaluate
practice_columns = [
    'Planting Material',
    'Weeding',
    'Tree age',
    'Tree density',
    'Tree health',
    'Debilitating disease',
    'Pruning',
    'Pest disease sanitation',
    'Harvesting',
    'Shade management',
    'Soil condition',
    'Organic matter',
    'Fertilizer formulation',
    'Fertilizer application'
]

# Function to score each practice (customize based on your data values)
def score_practice(value):
    """
    Score each practice. Adjust this function based on your actual data values.
    This is a template - you may need to customize for each column.
    """
    if pd.isna(value):
        return 0
    
    value_str = str(value).lower().strip()
    
    # Good practices (score 2)
    good_indicators = ['yes', 'good', 'high', 'optimal', 'healthy', 'adequate', 
                       'proper', 'regular', 'appropriate', 'suitable', 'improved']
    
    # Medium practices (score 1)
    medium_indicators = ['moderate', 'medium', 'fair', 'average', 'some', 
                         'occasional', 'partial', 'standard']
    
    # Bad practices (score 0)
    bad_indicators = ['no', 'poor', 'low', 'none', 'inadequate', 'bad', 
                      'unhealthy', 'irregular', 'traditional', 'unimproved']
    
    # Check against indicators
    for indicator in good_indicators:
        if indicator in value_str:
            return 2
    
    for indicator in medium_indicators:
        if indicator in value_str:
            return 1
    
    for indicator in bad_indicators:
        if indicator in value_str:
            return 0
    
    # Default to medium if unclear
    return 1

# Calculate score for each practice
print("\nScoring practices...")
for col in practice_columns:
    if col in df.columns:
        df[f'{col}_score'] = df[col].apply(score_practice)
        print(f"✓ Scored: {col}")
    else:
        print(f"⚠ Column not found: {col}")

# Calculate total adoption score
score_columns = [f'{col}_score' for col in practice_columns if col in df.columns]
df['Total_Score'] = df[score_columns].sum(axis=1)
df['Max_Score'] = len(score_columns) * 2  # Maximum possible score

# Calculate adoption percentage
df['Adoption_Percentage'] = (df['Total_Score'] / df['Max_Score'] * 100).round(2)

# Categorize adoption level
def categorize_adoption(percentage):
    if percentage >= 66.67:  # 2/3 or more
        return 'Good'
    elif percentage >= 33.33:  # 1/3 to 2/3
        return 'Medium'
    else:  # Less than 1/3
        return 'Bad'

df['Adoption_Level'] = df['Adoption_Percentage'].apply(categorize_adoption)

# Assign numeric values
adoption_map = {'Good': 2, 'Medium': 1, 'Bad': 0}
df['Adoption_Value'] = df['Adoption_Level'].map(adoption_map)

print(f"\n✓ Adoption Level calculated")
print(f"  - Good adoption: {len(df[df['Adoption_Level']=='Good'])} farmers ({len(df[df['Adoption_Level']=='Good'])/len(df)*100:.1f}%)")
print(f"  - Medium adoption: {len(df[df['Adoption_Level']=='Medium'])} farmers ({len(df[df['Adoption_Level']=='Medium'])/len(df)*100:.1f}%)")
print(f"  - Bad adoption: {len(df[df['Adoption_Level']=='Bad'])} farmers ({len(df[df['Adoption_Level']=='Bad'])/len(df)*100:.1f}%)")

# ============================================================================
# STEP 4: DATA ANALYSIS
# ============================================================================
print("\n[STEP 4] Data Analysis...")

# 4.1 Distribution of adoption levels
print("\n4.1 Adoption Distribution:")
adoption_counts = df['Adoption_Level'].value_counts()
print(adoption_counts)

# 4.2 Relationship between adoption and farm size
print("\n4.2 Adoption vs Farm Size:")
farm_by_adoption = df.groupby('Adoption_Level')['Farm size'].agg(['mean', 'median', 'std', 'min', 'max'])
print(farm_by_adoption.round(2))

# 4.3 Adoption by region
print("\n4.3 Adoption by Region:")
region_adoption = pd.crosstab(df['Region'], df['Adoption_Level'], normalize='index') * 100
print(region_adoption.round(2))

# 4.4 Practice-level analysis
print("\n4.4 Practice Performance (Average Scores):")
practice_scores = {}
for col in practice_columns:
    if col in df.columns:
        score_col = f'{col}_score'
        if score_col in df.columns:
            avg_score = df[score_col].mean()
            practice_scores[col] = avg_score

practice_df = pd.DataFrame(list(practice_scores.items()), columns=['Practice', 'Avg_Score'])
practice_df = practice_df.sort_values('Avg_Score', ascending=False)
practice_df['Performance'] = practice_df['Avg_Score'].apply(
    lambda x: 'Good' if x >= 1.33 else ('Medium' if x >= 0.67 else 'Bad')
)
print(practice_df.to_string(index=False))

# Save analysis results - UPDATED PATH
analysis_summary = pd.DataFrame({
    'Metric': ['Total Farmers', 'Good Adoption', 'Medium Adoption', 'Bad Adoption',
               'Avg Farm Size', 'Avg Adoption Score'],
    'Value': [len(df), 
              len(df[df['Adoption_Level']=='Good']),
              len(df[df['Adoption_Level']=='Medium']),
              len(df[df['Adoption_Level']=='Bad']),
              df['Farm size'].mean(),
              df['Adoption_Percentage'].mean()]
})
analysis_summary_file = results_dir / "analysis_summary.csv"
analysis_summary.to_csv(analysis_summary_file, index=False)

# ============================================================================
# STEP 5: DATA VISUALIZATION
# ============================================================================
print("\n[STEP 5] Creating Visualizations...")

# 5.1 Adoption Level Distribution (Pie Chart)
plt.figure(figsize=(10, 6))
colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red
adoption_counts = df['Adoption_Level'].value_counts()
plt.pie(adoption_counts, labels=adoption_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90)
plt.title('Distribution of Cocoa Adoption Levels', fontsize=16, fontweight='bold')
plt.savefig(results_dir / '01_adoption_distribution_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 01_adoption_distribution_pie.png")

# 5.2 Adoption Level Distribution (Bar Chart)
plt.figure(figsize=(10, 6))
adoption_counts.plot(kind='bar', color=colors)
plt.title('Number of Farmers by Adoption Level', fontsize=16, fontweight='bold')
plt.xlabel('Adoption Level', fontsize=12)
plt.ylabel('Number of Farmers', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.savefig(results_dir / '02_adoption_distribution_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 02_adoption_distribution_bar.png")

# 5.3 Adoption vs Farm Size (Box Plot)
plt.figure(figsize=(10, 6))
df.boxplot(column='Farm size', by='Adoption_Level', ax=plt.gca())
plt.title('Farm Size Distribution by Adoption Level', fontsize=16, fontweight='bold')
plt.suptitle('')  # Remove default title
plt.xlabel('Adoption Level', fontsize=12)
plt.ylabel('Farm Size (Ha)', fontsize=12)
plt.savefig(results_dir / '03_farm_size_by_adoption_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 03_farm_size_by_adoption_boxplot.png")

# 5.4 Adoption vs Farm Size (Scatter Plot)
plt.figure(figsize=(12, 6))
colors_map = {'Good': '#2ecc71', 'Medium': '#f39c12', 'Bad': '#e74c3c'}
for level in ['Good', 'Medium', 'Bad']:
    data = df[df['Adoption_Level'] == level]
    plt.scatter(data['Farm size'], data['Adoption_Percentage'], 
               label=level, alpha=0.6, s=50, color=colors_map[level])
plt.title('Relationship: Farm Size vs Adoption Level', fontsize=16, fontweight='bold')
plt.xlabel('Farm Size (Ha)', fontsize=12)
plt.ylabel('Adoption Percentage (%)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(results_dir / '04_farm_size_vs_adoption_scatter.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 04_farm_size_vs_adoption_scatter.png")

# 5.5 Adoption by Region (Stacked Bar Chart)
plt.figure(figsize=(12, 6))
region_counts = pd.crosstab(df['Region'], df['Adoption_Level'])
region_counts[['Good', 'Medium', 'Bad']].plot(kind='bar', stacked=True, 
                                               color=colors, ax=plt.gca())
plt.title('Adoption Levels by Region', fontsize=16, fontweight='bold')
plt.xlabel('Region', fontsize=12)
plt.ylabel('Number of Farmers', fontsize=12)
plt.legend(title='Adoption Level')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.savefig(results_dir / '05_adoption_by_region_stacked.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 05_adoption_by_region_stacked.png")

# 5.6 Practice Performance Heatmap
plt.figure(figsize=(14, 8))
practice_matrix = df[score_columns].corr()
sns.heatmap(practice_matrix, annot=True, fmt='.2f', cmap='RdYlGn', 
            center=0, square=True, linewidths=1)
plt.title('Correlation Between Farming Practices', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(results_dir / '06_practice_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 06_practice_correlation_heatmap.png")

# 5.7 Top and Bottom Performing Practices
plt.figure(figsize=(12, 8))
practice_df_sorted = practice_df.sort_values('Avg_Score')
colors_practices = ['#e74c3c' if x < 0.67 else ('#f39c12' if x < 1.33 else '#2ecc71') 
                   for x in practice_df_sorted['Avg_Score']]
plt.barh(practice_df_sorted['Practice'], practice_df_sorted['Avg_Score'], color=colors_practices)
plt.xlabel('Average Score', fontsize=12)
plt.title('Practice Performance Ranking', fontsize=16, fontweight='bold')
plt.axvline(x=0.67, color='red', linestyle='--', alpha=0.3, label='Bad/Medium threshold')
plt.axvline(x=1.33, color='green', linestyle='--', alpha=0.3, label='Medium/Good threshold')
plt.legend()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(results_dir / '07_practice_performance_ranking.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 07_practice_performance_ranking.png")

# 5.8 Adoption Score Distribution
plt.figure(figsize=(12, 6))
plt.hist(df['Adoption_Percentage'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
plt.axvline(df['Adoption_Percentage'].mean(), color='red', linestyle='--', 
           linewidth=2, label=f'Mean: {df["Adoption_Percentage"].mean():.1f}%')
plt.xlabel('Adoption Percentage (%)', fontsize=12)
plt.ylabel('Number of Farmers', fontsize=12)
plt.title('Distribution of Adoption Scores', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.savefig(results_dir / '08_adoption_score_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Created: 08_adoption_score_distribution.png")

# ============================================================================
# STEP 6: COMPREHENSIVE REPORT
# ============================================================================
print("\n[STEP 6] Generating Comprehensive Report...")

report = f"""
{'='*80}
COCOA ADOPTION ANALYSIS - COMPREHENSIVE REPORT
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
1. EXECUTIVE SUMMARY
{'='*80}

Total Farmers Analyzed: {len(df)}
Average Farm Size: {df['Farm size'].mean():.2f} Ha
Average Adoption Score: {df['Adoption_Percentage'].mean():.2f}%

Adoption Distribution:
  - Good Adoption (≥66.7%):    {len(df[df['Adoption_Level']=='Good'])} farmers ({len(df[df['Adoption_Level']=='Good'])/len(df)*100:.1f}%)
  - Medium Adoption (33.3-66.7%): {len(df[df['Adoption_Level']=='Medium'])} farmers ({len(df[df['Adoption_Level']=='Medium'])/len(df)*100:.1f}%)
  - Bad Adoption (<33.3%):     {len(df[df['Adoption_Level']=='Bad'])} farmers ({len(df[df['Adoption_Level']=='Bad'])/len(df)*100:.1f}%)

{'='*80}
2. DATA QUALITY SUMMARY
{'='*80}

Original Records: {len(df)}
Duplicates Removed: {duplicates}
Missing Values: {'Yes' if len(missing_df) > 0 else 'None'}
Outliers Detected: {len(outliers)} in Farm Size

{'='*80}
3. KEY FINDINGS
{'='*80}

3.1 Farm Size Analysis:
{farm_by_adoption.to_string()}

3.2 Regional Performance:
{region_adoption.to_string()}

3.3 Practice Performance (Top 5 and Bottom 5):

TOP 5 PERFORMING PRACTICES:
{practice_df.head().to_string(index=False)}

BOTTOM 5 PERFORMING PRACTICES:
{practice_df.tail().to_string(index=False)}

{'='*80}
4. ACTIONABLE RECOMMENDATIONS
{'='*80}

Based on the analysis, here are key recommendations:

4.1 PRIORITY AREAS FOR IMPROVEMENT:
"""

# Add recommendations based on bottom performing practices
bottom_practices = practice_df.tail(3)['Practice'].tolist()
for i, practice in enumerate(bottom_practices, 1):
    report += f"\n  {i}. Improve {practice} through training and support programs"

report += f"""

4.2 REGIONAL FOCUS:
"""

# Identify regions with lowest good adoption
region_good = df.groupby('Region')['Adoption_Level'].apply(lambda x: (x=='Good').sum())
worst_regions = region_good.nsmallest(3).index.tolist()
for i, region in enumerate(worst_regions, 1):
    report += f"\n  {i}. Increase support in {region} region"

report += f"""

4.3 FARM SIZE CONSIDERATIONS:
"""

# Farm size recommendations
avg_good = farm_by_adoption.loc['Good', 'mean'] if 'Good' in farm_by_adoption.index else 0
avg_bad = farm_by_adoption.loc['Bad', 'mean'] if 'Bad' in farm_by_adoption.index else 0

if avg_good > avg_bad:
    report += "\n  - Larger farms show better adoption. Consider scaling programs for smaller farms."
else:
    report += "\n  - Smaller farms show better adoption. Leverage this success for larger farms."

report += f"""

4.4 BEST PRACTICES TO SCALE:
"""

# Best performing practices to scale
top_practices = practice_df.head(3)['Practice'].tolist()
for i, practice in enumerate(top_practices, 1):
    report += f"\n  {i}. Scale successful {practice} approaches to other farmers"

report += f"""

{'='*80}
5. NEXT STEPS
{'='*80}

1. Targeted Training: Focus on bottom-performing practices
2. Regional Support: Allocate resources to regions with low adoption
3. Peer Learning: Connect high-adoption farmers with others
4. Monitoring: Track adoption improvements quarterly
5. Incentives: Consider rewards for adoption improvements

{'='*80}
6. FILES GENERATED
{'='*80}

Data Files:
  - {cleaned_dir}/cleaned_data.csv
  - {results_dir}/analysis_summary.csv

Visualizations:
  - {results_dir}/01_adoption_distribution_pie.png
  - {results_dir}/02_adoption_distribution_bar.png
  - {results_dir}/03_farm_size_by_adoption_boxplot.png
  - {results_dir}/04_farm_size_vs_adoption_scatter.png
  - {results_dir}/05_adoption_by_region_stacked.png
  - {results_dir}/06_practice_correlation_heatmap.png
  - {results_dir}/07_practice_performance_ranking.png
  - {results_dir}/08_adoption_score_distribution.png

{'='*80}
END OF REPORT
{'='*80}
"""

# Save report - UPDATED PATH
report_file = results_dir / "COMPREHENSIVE_REPORT.txt"
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✓ Comprehensive report saved to '{report_file}'")

# Also save enhanced data with adoption scores - UPDATED PATH
enhanced_data_file = results_dir / "data_with_adoption_scores.csv"
df.to_csv(enhanced_data_file, index=False)
print(f"✓ Enhanced data saved to '{enhanced_data_file}'")

# Print summary to console
print(report)

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\n✓ All results saved in '{results_dir}/' folder")
print(f"✓ {len([f for f in os.listdir(results_dir) if f.endswith('.png')])} visualizations created")
print(f"✓ {len([f for f in os.listdir(results_dir) if f.endswith('.csv')])} data files generated")
print(f"✓ 1 comprehensive report generated")
print("\nThank you for using the Cocoa Adoption Analysis System!")
print("="*80)
