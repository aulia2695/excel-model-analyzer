"""
Exercise 1: Farmer Development Plan Analysis
Analyzes baseline adoption, progress tracking, and production segmentation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class FarmerAnalyzer:
    def __init__(self, raw_data_path):
        """Initialize with raw data"""
        self.raw_data_path = Path(raw_data_path)
        self.df = None
        self.cleaned_dir = Path("excel-data/test-2-farmer-development/cleaned")
        self.results_dir = Path("excel-data/test-2-farmer-development/results/exercise-1-analysis")
        
    def load_data(self):
        """Load and prepare raw data"""
        print("📂 Loading raw data...")
        self.df = pd.read_excel(self.raw_data_path)
        print(f"✓ Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        return self
    
    def categorize_data(self):
        """Categorize Result, Competence, Gender, and Land Size"""
        print("\n🏷️  Categorizing data...")
        
        # Map Result and Competence (G=2, M=1, B=0)
        adoption_map = {'G': 2, 'M': 1, 'B': 0}
        if 'Result' in self.df.columns:
            self.df['Result_Category'] = self.df['Result'].map(adoption_map)
        if 'Competence' in self.df.columns:
            self.df['Competence_Category'] = self.df['Competence'].map(adoption_map)
        
        # Map Gender (Male=2, Female=1)
        gender_map = {'Male': 2, 'Female': 1}
        if 'Farmer: Gender' in self.df.columns:
            self.df['Gender_Category'] = self.df['Farmer: Gender'].map(gender_map)
        
        # Categorize land size
        if 'Farm: Total Farm Area HA' in self.df.columns:
            self.df['Land_Size_Category'] = pd.cut(
                self.df['Farm: Total Farm Area HA'],
                bins=[0, 2, 4, float('inf')],
                labels=['<2ha', '2-4ha', '≥4ha'],
                include_lowest=True
            )
        
        print("✓ Data categorization complete")
        return self
    
    def baseline_analysis(self):
        """Analyze baseline Result and Competence distribution"""
        print("\n📊 Performing baseline analysis...")
        
        baseline_data = []
        
        # Get unique variables
        if 'Variable' in self.df.columns:
            variables = self.df['Variable'].unique()
            
            for var in variables:
                var_data = self.df[self.df['Variable'] == var]
                
                # Result distribution
                result_dist = var_data['Result'].value_counts()
                result_pct = (result_dist / len(var_data) * 100).round(2)
                
                # Competence distribution
                comp_dist = var_data['Competence'].value_counts()
                comp_pct = (comp_dist / len(var_data) * 100).round(2)
                
                baseline_data.append({
                    'Variable': var,
                    'Total_Farmers': len(var_data),
                    'Result_Good_%': result_pct.get('G', 0),
                    'Result_Medium_%': result_pct.get('M', 0),
                    'Result_Bad_%': result_pct.get('B', 0),
                    'Competence_Good_%': comp_pct.get('G', 0),
                    'Competence_Medium_%': comp_pct.get('M', 0),
                    'Competence_Bad_%': comp_pct.get('B', 0),
                })
        
        baseline_df = pd.DataFrame(baseline_data)
        
        # Save baseline summary
        output_path = self.cleaned_dir / "baseline_summary.csv"
        baseline_df.to_csv(output_path, index=False)
        print(f"✓ Baseline summary saved to {output_path}")
        
        return baseline_df
    
    def progress_tracking(self):
        """Track farmer progress between Visit 1 and Visit 2"""
        print("\n📈 Tracking farmer progress...")
        
        if 'Visit Number' not in self.df.columns or 'Farmer: Farmer Code' not in self.df.columns:
            print("⚠️  Cannot track progress: missing Visit Number or Farmer Code")
            return None
        
        # Separate visits
        visit1 = self.df[self.df['Visit Number'] == 1].copy()
        visit2 = self.df[self.df['Visit Number'] == 2].copy()
        
        # Merge on Farmer Code and Variable
        merge_cols = ['Farmer: Farmer Code', 'Variable']
        progress_df = pd.merge(
            visit1[merge_cols + ['Result_Category']],
            visit2[merge_cols + ['Result_Category']],
            on=merge_cols,
            suffixes=('_Visit1', '_Visit2'),
            how='inner'
        )
        
        # Calculate progress
        progress_df['Progress'] = progress_df['Result_Category_Visit2'] - progress_df['Result_Category_Visit1']
        progress_df['Progress_Status'] = progress_df['Progress'].apply(
            lambda x: 'Improving' if x > 0 else ('Deteriorating' if x < 0 else 'Same Level')
        )
        
        # Summary statistics
        progress_summary = progress_df['Progress_Status'].value_counts()
        progress_pct = (progress_summary / len(progress_df) * 100).round(2)
        
        print("\n📊 Progress Summary:")
        print(f"  • Improving: {progress_pct.get('Improving', 0):.1f}%")
        print(f"  • Same Level: {progress_pct.get('Same Level', 0):.1f}%")
        print(f"  • Deteriorating: {progress_pct.get('Deteriorating', 0):.1f}%")
        
        # Save progress tracking
        output_path = self.cleaned_dir / "progress_tracking.csv"
        progress_df.to_csv(output_path, index=False)
        print(f"✓ Progress tracking saved to {output_path}")
        
        return progress_df, progress_pct
    
    def production_segmentation(self):
        """Segment production by Gender and Land Size"""
        print("\n🌾 Analyzing production segmentation...")
        
        production_col = 'Farm: Production - last baseline KG'
        
        if production_col not in self.df.columns:
            print("⚠️  Production column not found")
            return None
        
        # Remove duplicates for production analysis (use Visit 1 only)
        prod_df = self.df[self.df['Visit Number'] == 1].copy()
        
        segments = {}
        
        # By Gender
        if 'Farmer: Gender' in prod_df.columns:
            gender_prod = prod_df.groupby('Farmer: Gender')[production_col].agg(['mean', 'median', 'count'])
            segments['Gender'] = gender_prod
            print("\n📊 Average Production by Gender:")
            print(gender_prod)
        
        # By Land Size
        if 'Land_Size_Category' in prod_df.columns:
            land_prod = prod_df.groupby('Land_Size_Category')[production_col].agg(['mean', 'median', 'count'])
            segments['Land_Size'] = land_prod
            print("\n📊 Average Production by Land Size:")
            print(land_prod)
        
        return segments
    
    def create_visualizations(self, baseline_df, progress_pct, segments):
        """Create all visualization charts"""
        print("\n🎨 Creating visualizations...")
        
        figures_dir = self.results_dir / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        
        # 1. Baseline Adoption Distribution (Top Variables)
        if baseline_df is not None and not baseline_df.empty:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            top_vars = baseline_df.nlargest(10, 'Total_Farmers')
            
            # Result distribution
            result_data = top_vars[['Variable', 'Result_Good_%', 'Result_Medium_%', 'Result_Bad_%']].set_index('Variable')
            result_data.plot(kind='barh', stacked=True, ax=ax1, color=['green', 'orange', 'red'])
            ax1.set_title('Result Distribution by Variable (Top 10)', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Percentage')
            ax1.legend(title='Adoption Level', labels=['Good', 'Medium', 'Bad'])
            
            # Competence distribution
            comp_data = top_vars[['Variable', 'Competence_Good_%', 'Competence_Medium_%', 'Competence_Bad_%']].set_index('Variable')
            comp_data.plot(kind='barh', stacked=True, ax=ax2, color=['green', 'orange', 'red'])
            ax2.set_title('Competence Distribution by Variable (Top 10)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Percentage')
            ax2.legend(title='Competence Level', labels=['Good', 'Medium', 'Bad'])
            
            plt.tight_layout()
            plt.savefig(figures_dir / 'baseline_adoption_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created: baseline_adoption_distribution.png")
        
        # 2. Progress Tracking Pie Chart
        if progress_pct is not None:
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = ['#2ecc71', '#95a5a6', '#e74c3c']
            explode = (0.05, 0.05, 0.05)
            
            ax.pie(progress_pct.values, labels=progress_pct.index, autopct='%1.1f%%',
                   colors=colors, explode=explode, startangle=90, textprops={'fontsize': 12})
            ax.set_title('Farmer Progress Between Visit 1 and Visit 2', fontsize=16, fontweight='bold')
            
            plt.savefig(figures_dir / 'progress_tracking_pie.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created: progress_tracking_pie.png")
        
        # 3. Production Segmentation
        if segments:
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # By Gender
            if 'Gender' in segments:
                gender_data = segments['Gender']['mean']
                ax = axes[0]
                gender_data.plot(kind='bar', ax=ax, color=['#3498db', '#e91e63'])
                ax.set_title('Average Production by Gender', fontsize=14, fontweight='bold')
                ax.set_ylabel('Production (KG)')
                ax.set_xlabel('Gender')
                ax.tick_params(axis='x', rotation=0)
            
            # By Land Size
            if 'Land_Size' in segments:
                land_data = segments['Land_Size']['mean']
                ax = axes[1]
                land_data.plot(kind='bar', ax=ax, color=['#f39c12', '#9b59b6', '#1abc9c'])
                ax.set_title('Average Production by Land Size', fontsize=14, fontweight='bold')
                ax.set_ylabel('Production (KG)')
                ax.set_xlabel('Land Size Category')
                ax.tick_params(axis='x', rotation=0)
            
            plt.tight_layout()
            plt.savefig(figures_dir / 'production_segmentation.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created: production_segmentation.png")
    
    def generate_recommendations(self):
        """Generate data quality recommendations"""
        print("\n💡 Generating recommendations...")
        
        recommendations = {
            'Data Completeness': [
                '1. Ensure all 14 adoption variables are captured consistently across all farmers',
                '2. Mandate Visit Number field to track temporal changes effectively',
                '3. Validate Farmer Code uniqueness to prevent duplicate entries',
                '4. Require both Result AND Competence ratings for all variables'
            ],
            'Data Quality': [
                '1. Implement dropdown validation for categorical fields (G/M/B, Gender, Village)',
                '2. Add range validation for numeric fields (Production > 0, Farm Area > 0)',
                '3. Create automated alerts for missing critical fields before survey completion',
                '4. Standardize date formats and ensure Visit 2 date > Visit 1 date'
            ],
            'M&E Assistant Checks': [
                '1. Daily reconciliation of surveys submitted vs. expected',
                '2. Weekly outlier detection for production and farm area values',
                '3. Cross-validation: Production should correlate with Farm Area',
                '4. Flag farmers with deteriorating scores for follow-up visits'
            ]
        }
        
        report_dir = self.results_dir / "analysis_report_2pager"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        with open(report_dir / "recommendations.txt", 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("DATA QUALITY RECOMMENDATIONS FOR 3,000 FARMER EXPANSION\n")
            f.write("=" * 80 + "\n\n")
            
            for category, items in recommendations.items():
                f.write(f"\n{category.upper()}\n")
                f.write("-" * 80 + "\n")
                for item in items:
                    f.write(f"  {item}\n")
        
        print(f"✓ Recommendations saved to {report_dir / 'recommendations.txt'}")
        
        return recommendations
    
    def run_full_analysis(self):
        """Execute complete Exercise 1 analysis"""
        print("=" * 80)
        print("EXERCISE 1: FARMER DEVELOPMENT PLAN ANALYSIS")
        print("=" * 80)
        
        self.load_data()
        self.categorize_data()
        
        baseline_df = self.baseline_analysis()
        progress_data = self.progress_tracking()
        segments = self.production_segmentation()
        
        progress_pct = progress_data[1] if progress_data else None
        
        self.create_visualizations(baseline_df, progress_pct, segments)
        self.generate_recommendations()
        
        print("\n" + "=" * 80)
        print("✅ EXERCISE 1 ANALYSIS COMPLETE!")
        print("=" * 80)

if __name__ == "__main__":
    # Path to raw data
    raw_data_path = "excel-data/test-2-farmer-development/raw/test_2_farmer_development_raw.xlsx"
    
    # Run analysis
    analyzer = FarmerAnalyzer(raw_data_path)
    analyzer.run_full_analysis()
