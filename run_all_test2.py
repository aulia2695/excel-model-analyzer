"""
Master Script: Run All Test 2 Exercises
Executes complete Farmer Development Plan analysis
"""

import sys
import subprocess
from pathlib import Path
import time

def print_banner(text):
    """Print formatted banner"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def run_exercise(exercise_num, script_name, description):
    """Run individual exercise script"""
    print_banner(f"EXERCISE {exercise_num}: {description}")
    
    start_time = time.time()
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(result.stdout)
        
        elapsed = time.time() - start_time
        print(f"\n✅ Exercise {exercise_num} completed in {elapsed:.2f} seconds")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in Exercise {exercise_num}:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        print("Please ensure all scripts are in the correct location.")
        return False

def check_prerequisites():
    """Check if all required files and directories exist"""
    print_banner("CHECKING PREREQUISITES")
    
    required_files = [
        "excel-data/test-2-farmer-development/raw/test_2_farmer_development_raw.xlsx"
    ]
    
    required_dirs = [
        "excel-data/test-2-farmer-development/scripts/exercise-1-analysis",
        "excel-data/test-2-farmer-development/scripts/exercise-2-dashboard",
        "excel-data/test-2-farmer-development/scripts/exercise-3-data-collection"
    ]
    
    all_good = True
    
    # Check files
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ Found: {file_path}")
        else:
            print(f"✗ Missing: {file_path}")
            all_good = False
    
    # Check directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ Directory: {dir_path}")
        else:
            print(f"✗ Missing directory: {dir_path}")
            all_good = False
    
    # Check Python packages
    required_packages = ['pandas', 'matplotlib', 'seaborn', 'numpy', 'openpyxl']
    print("\nChecking Python packages...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} not installed")
            all_good = False
    
    return all_good

def create_final_summary():
    """Create final summary document"""
    print_banner("CREATING FINAL SUMMARY")
    
    summary = """
================================================================================
TEST 2: FARMER DEVELOPMENT PLAN ANALYSIS - COMPLETE REPORT
================================================================================

PROJECT: MEV Specialist Case 2023 - Farm Development Plan Analysis
DATE: """ + time.strftime("%B %d, %Y") + """
ANALYST: Automated Analysis System

================================================================================
EXECUTIVE SUMMARY
================================================================================

This analysis covers three critical exercises for JB Cocoa's farmer development
and living income monitoring programs in Ivory Coast:

1. BASELINE ANALYSIS OF FARMER DEVELOPMENT DATA
   - Current adoption and competence levels across 14 agronomic variables
   - Progress tracking between survey visits
   - Production yield segmentation by gender and land size
   - Data quality recommendations for scaling to 3,000 farmers

2. LIVING INCOME DASHBOARD DESIGN
   - Comprehensive visualization framework for income monitoring
   - 7 key dashboard components with dummy data mockups
   - Data collection requirements and calculation formulas
   - Implementation guidance for M&E teams

3. DATA COLLECTION SYSTEM SETUP
   - Optimal surveyor selection (2 Consultant Surveyors)
   - Budget allocation (3,907 EUR within 5,000 EUR budget)
   - 8-week project timeline with Gantt chart
   - Sampling strategy for 200 farmers across 4 cooperatives

================================================================================
KEY FINDINGS
================================================================================

EXERCISE 1 INSIGHTS:
• Baseline data reveals adoption levels across farmer population
• Progress tracking identifies improving vs. deteriorating farmers
• Production varies significantly by gender and land size
• Data quality protocols critical for 3,000 farmer expansion

EXERCISE 2 DESIGN:
• Dashboard enables real-time living income gap monitoring
• Waterfall chart visualizes income components and costs
• Regional comparison identifies high/low performing cooperatives
• Designed for both executive and operational audiences

EXERCISE 3 RECOMMENDATIONS:
• Consultant surveyors optimal for one-time baseline collection
• 200-farmer stratified sample provides representative baseline
• 8-week timeline balances speed with data quality
• Budget includes 10% contingency for unforeseen expenses

================================================================================
DELIVERABLES LOCATION
================================================================================

📁 excel-data/test-2-farmer-development/
   ├── 📊 cleaned/
   │   ├── baseline_summary.csv
   │   └── progress_tracking.csv
   │
   ├── 📈 results/
   │   ├── exercise-1-analysis/
   │   │   ├── figures/
   │   │   │   ├── baseline_adoption_distribution.png
   │   │   │   ├── progress_tracking_pie.png
   │   │   │   └── production_segmentation.png
   │   │   └── analysis_report_2pager/
   │   │       └── recommendations.txt
   │   │
   │   ├── exercise-2-dashboard/
   │   │   └── dashboard_design/
   │   │       ├── living_income_dashboard_mockup.png
   │   │       └── design_rationale.txt
   │   │
   │   └── exercise-3-data-collection/
   │       ├── budget_breakdown/
   │       │   ├── budget_breakdown.csv
   │       │   └── budget_visualization.png
   │       ├── gantt_chart/
   │       │   └── project_gantt_chart.png
   │       └── data_collection_plan.txt

================================================================================
NEXT STEPS
================================================================================

1. Review baseline analysis findings with Operations Team
2. Validate Living Income Dashboard design with stakeholders
3. Obtain Manager approval for data collection budget
4. Coordinate with 4 cooperatives for farmer access
5. Initiate consultant surveyor onboarding process

================================================================================
CONTACT
================================================================================

For questions about this analysis, please contact the MEV Specialist team.

Report auto-generated by: Test 2 Analysis System
================================================================================
"""
    
    output_path = Path("excel-data/test-2-farmer-development/results/COMPLETE_ANALYSIS_REPORT.txt")
    with open(output_path, 'w') as f:
        f.write(summary)
    
    print(f"✓ Final summary saved to {output_path}")
    print("\n" + summary)

def main():
    """Main execution function"""
    print_banner("TEST 2: FARMER DEVELOPMENT PLAN ANALYSIS")
    print("Starting comprehensive analysis of all three exercises...\n")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed!")
        print("Please install missing packages with:")
        print("  pip install pandas openpyxl matplotlib seaborn numpy")
        return False
    
    print("\n✅ All prerequisites satisfied!\n")
    
    # Define exercises
    exercises = [
        (1, "excel-data/test-2-farmer-development/scripts/exercise-1-analysis/exercise_1_farmer_analysis.py",
         "Analysis of Farmer Development Plan Data"),
        (2, "excel-data/test-2-farmer-development/scripts/exercise-2-dashboard/exercise_2_living_income_dashboard.py",
         "Living Income Dashboard Design"),
        (3, "excel-data/test-2-farmer-development/scripts/exercise-3-data-collection/exercise_3_data_collection.py",
         "Data Collection System Setup")
    ]
    
    # Run all exercises
    results = []
    for num, script, desc in exercises:
        success = run_exercise(num, script, desc)
        results.append(success)
        
        if not success:
            print(f"\n⚠️  Exercise {num} encountered errors but continuing...")
    
    # Create final summary
    create_final_summary()
    
    # Final status
    print_banner("ANALYSIS COMPLETE")
    
    if all(results):
        print("✅ All exercises completed successfully!")
        return True
    else:
        print("⚠️  Some exercises had errors. Please review output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
