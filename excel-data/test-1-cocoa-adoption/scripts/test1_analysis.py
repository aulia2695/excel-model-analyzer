"""
Test 1: Cocoa Adoption Analysis (Ecuador)
Data cleaning, analysis, and visualization for cocoa farming practices
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
sns.set_style("whitegrid")

# ============================================================================
# 1. DATA LOADING
# ============================================================================

def load_data(filepath):
    """Load Excel data from raw folder"""
    try:
        df = pd.read_excel(filepath)
        print(f"✓ Data loaded successfully!")
        print(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return None

# ============================================================================
# 2. DATA CLEANING
# ============================================================================

def check_missing_values(df):
    """Check and report missing values"""
    print("\n" + "="*60)
    print("MISSING VALUES ANALYSIS")
    print("="*60)
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_pct.values
    })
    
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(
        'Missing_Count', ascending=False
    )
    
    if len(missing_df) > 0:
        print(missing_df.to_string(index=False))
    else:
        print("✓ No missing values found!")
    
    return missing_df

def remove_duplicates(df):
    """Remove duplicate rows"""
    print("\n" + "="*60)
    print("DUPLICATE REMOVAL")
    print("="*60)
    
    initial_rows = len(df)
    df_clean = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    
    print(f"Initial rows: {initial_rows}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final rows: {len(df_clean)}")
    
    return df_clean

def handle_outliers(df, columns, method='iqr'):
    """
    Detect and handle outliers using IQR method
    
    Parameters:
    - df: DataFrame
    - columns: list of numeric columns to check
    - method: 'iqr' or 'zscore'
    """
    print("\n" + "="*60)
    print("OUTLIER DETECTION")
    print("="*60)
    
    outlier_info = {}
    
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outlier_count = len(outliers)
                
                outlier_info[col] = {
                    'count': outlier_count,
                    'percentage': (outlier_count / len(df)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
                
                print(f"\n{col}:")
                print(f"  Outliers found: {outlier_count} ({outlier_info[col]['percentage']:.2f}%)")
                print(f"  Valid range: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    return outlier_info

# ============================================================================
# 3. DATA ANALYSIS
# ============================================================================

def analyze_adoption_distribution(df, adoption_column):
    """Analyze distribution of cocoa adoption"""
    print("\n" + "="*60)
    print("ADOPTION DISTRIBUTION ANALYSIS")
    print("="*60)
    
    if adoption_column in df.columns:
        distribution = df[adoption_column].value_counts()
        distribution_pct = df[adoption_column].value_counts(normalize=True) * 100
        
        print("\nCount:")
        print(distribution)
        print("\nPercentage:")
        print(distribution_pct.round(2))
        
        return distribution
    else:
        print(f"✗ Column '{adoption_column}' not found!")
        return None

def analyze_by_farm_size(df, farm_size_col, target_col):
    """Analyze relationship between farm size and target variable"""
    print("\n" + "="*60)
    print("FARM SIZE ANALYSIS")
    print("="*60)
    
    if farm_size_col in df.columns and target_col in df.columns:
        grouped = df.groupby(farm_size_col)[target_col].agg(['mean', 'median', 'count'])
        print(grouped)
        return grouped
    else:
        print(f"✗ Required columns not found!")
        return None

def analyze_by_region(df, region_col, adoption_col):
    """Analyze adoption rates by region"""
    print("\n" + "="*60)
    print("REGIONAL ANALYSIS")
    print("="*60)
    
    if region_col in df.columns and adoption_col in df.columns:
        regional = df.groupby(region_col)[adoption_col].agg(['mean', 'count'])
        regional = regional.sort_values('mean', ascending=False)
        print(regional)
        return regional
    else:
        print(f"✗ Required columns not found!")
        return None

def correlation_analysis(df, numeric_columns):
    """Analyze correlations between numeric variables"""
    print("\n" + "="*60)
    print("CORRELATION ANALYSIS")
    print("="*60)
    
    # Select only numeric columns that exist
    available_cols = [col for col in numeric_columns if col in df.columns]
    
    if len(available_cols) > 1:
        corr_matrix = df[available_cols].corr()
        print(corr_matrix)
        return corr_matrix
    else:
        print("✗ Not enough numeric columns for correlation analysis!")
        return None

# ============================================================================
# 4. VISUALIZATION
# ============================================================================

def create_adoption_chart(df, adoption_column, output_path='../results/'):
    """Create bar chart for adoption distribution"""
    if adoption_column not in df.columns:
        print(f"✗ Column '{adoption_column}' not found!")
        return
    
    plt.figure(figsize=(10, 6))
    df[adoption_column].value_counts().plot(kind='bar', color='steelblue')
    plt.title('Cocoa Adoption Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Adoption Level', fontsize=12)
    plt.ylabel('Number of Farmers', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    filename = f"{output_path}adoption_distribution.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved: {filename}")
    plt.close()

def create_farm_size_chart(df, farm_size_col, target_col, output_path='../results/'):
    """Create chart showing relationship between farm size and target variable"""
    if farm_size_col not in df.columns or target_col not in df.columns:
        print(f"✗ Required columns not found!")
        return
    
    plt.figure(figsize=(10, 6))
    grouped = df.groupby(farm_size_col)[target_col].mean()
    grouped.plot(kind='bar', color='forestgreen')
    plt.title('Average Adoption by Farm Size', fontsize=16, fontweight='bold')
    plt.xlabel('Farm Size', fontsize=12)
    plt.ylabel(f'Average {target_col}', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    filename = f"{output_path}farm_size_analysis.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved: {filename}")
    plt.close()

def create_regional_chart(df, region_col, adoption_col, output_path='../results/'):
    """Create chart showing adoption by region"""
    if region_col not in df.columns or adoption_col not in df.columns:
        print(f"✗ Required columns not found!")
        return
    
    plt.figure(figsize=(12, 6))
    regional = df.groupby(region_col)[adoption_col].mean().sort_values(ascending=False)
    regional.plot(kind='barh', color='coral')
    plt.title('Average Adoption by Region', fontsize=16, fontweight='bold')
    plt.xlabel('Average Adoption Rate', fontsize=12)
    plt.ylabel('Region', fontsize=12)
    plt.tight_layout()
    
    filename = f"{output_path}regional_analysis.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved: {filename}")
    plt.close()

def create_correlation_heatmap(df, numeric_columns, output_path='../results/'):
    """Create correlation heatmap"""
    available_cols = [col for col in numeric_columns if col in df.columns]
    
    if len(available_cols) > 1:
        plt.figure(figsize=(10, 8))
        corr_matrix = df[available_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, linewidths=1, fmt='.2f')
        plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filename = f"{output_path}correlation_heatmap.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved: {filename}")
        plt.close()

# ============================================================================
# 5. REPORT GENERATION
# ============================================================================

def generate_summary_report(df, output_path='../results/'):
    """Generate text summary report"""
    report = []
    report.append("="*70)
    report.append("COCOA ADOPTION ANALYSIS - SUMMARY REPORT")
    report.append("="*70)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n1. DATASET OVERVIEW")
    report.append(f"   Total Records: {len(df)}")
    report.append(f"   Total Columns: {len(df.columns)}")
    report.append(f"\n2. COLUMN NAMES")
    for i, col in enumerate(df.columns, 1):
        report.append(f"   {i}. {col}")
    
    report.append(f"\n3. DATA TYPES")
    for col, dtype in df.dtypes.items():
        report.append(f"   {col}: {dtype}")
    
    report.append(f"\n4. BASIC STATISTICS")
    report.append(str(df.describe()))
    
    report_text = "\n".join(report)
    
    filename = f"{output_path}analysis_summary_report.txt"
    with open(filename, 'w') as f:
        f.write(report_text)
    
    print(f"\n✓ Summary report saved: {filename}")
    return report_text

# ============================================================================
# 6. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("TEST 1: COCOA ADOPTION ANALYSIS - ECUADOR")
    print("="*70)
    
    # STEP 1: Load data
    filepath = '../raw/test1_cocoa_practices_adoption.xlsx'
    df = load_data(filepath)
    
    if df is None:
        print("\n✗ Analysis stopped: Could not load data")
        return
    
    # STEP 2: Data Cleaning
    print("\n" + "="*70)
    print("DATA CLEANING")
    print("="*70)
    
    # Check missing values
    missing_info = check_missing_values(df)
    
    # Remove duplicates
    df_clean = remove_duplicates(df)
    
    # Handle outliers (specify your numeric columns here)
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    outlier_info = handle_outliers(df_clean, numeric_cols)
    
    # STEP 3: Save cleaned data
    output_file = '../cleaned/test1_cocoa_adoption_cleaned.xlsx'
    df_clean.to_excel(output_file, index=False)
    print(f"\n✓ Cleaned data saved: {output_file}")
    
    # STEP 4: Data Analysis
    print("\n" + "="*70)
    print("DATA ANALYSIS")
    print("="*70)
    
    # NOTE: Replace these column names with your actual column names
    # adoption_col = 'adoption_level'  # Replace with your column name
    # farm_size_col = 'farm_size'      # Replace with your column name
    # region_col = 'region'            # Replace with your column name
    
    # Uncomment and modify based on your actual columns:
    # analyze_adoption_distribution(df_clean, adoption_col)
    # analyze_by_farm_size(df_clean, farm_size_col, adoption_col)
    # analyze_by_region(df_clean, region_col, adoption_col)
    # correlation_analysis(df_clean, numeric_cols)
    
    # STEP 5: Create Visualizations
    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70)
    
    # Uncomment and modify based on your actual columns:
    # create_adoption_chart(df_clean, adoption_col)
    # create_farm_size_chart(df_clean, farm_size_col, adoption_col)
    # create_regional_chart(df_clean, region_col, adoption_col)
    # create_correlation_heatmap(df_clean, numeric_cols)
    
    # STEP 6: Generate Report
    generate_summary_report(df_clean)
    
    print("\n" + "="*70)
    print("✓ ANALYSIS COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review cleaned data in: cleaned/")
    print("2. Check visualizations in: results/")
    print("3. Read summary report in: results/")
    print("4. Update column names in this script to match your data")
    print("="*70)

if __name__ == "__main__":
    main()
