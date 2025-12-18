"""
run_analysis.py
Script utama untuk menjalankan seluruh analisis
"""

import sys
from datetime import datetime
from config import *
from data_loader import DataLoader
from quota_analyzer import QuotaAnalyzer
from report_generator import ReportGenerator
from dashboard_generator import DashboardGenerator


def print_banner():
    """Print banner aplikasi"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║           VOLUME QUOTA ANALYZER                                   ║
    ║           Analisis Kouta Transaksi Farmer                         ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"    Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    Input:   {INPUT_FILE}")
    print()


def main():
    """Main function untuk menjalankan analisis"""
    
    # Print banner
    print_banner()
    
    try:
        # =====================
        # STEP 1: LOAD DATA
        # =====================
        print(f"{SEPARATOR_LINE}")
        print("STEP 1/4: LOADING DATA")
        print(f"{SEPARATOR_LINE}")
        
        loader = DataLoader()
        df = loader.load_data()
        
        if df is None:
            print(f"\n❌ FAILED: Could not load data")
            sys.exit(1)
        
        # =====================
        # STEP 2: VALIDATE
        # =====================
        print(f"\n{SEPARATOR_LINE}")
        print("STEP 2/4: VALIDATING DATA")
        print(f"{SEPARATOR_LINE}")
        
        if not loader.validate_columns():
            print(f"\n❌ FAILED: Data validation failed")
            sys.exit(1)
        
        # Preprocess
        df = loader.preprocess_data()
        
        # =====================
        # STEP 3: ANALYZE
        # =====================
        print(f"\n{SEPARATOR_LINE}")
        print("STEP 3/4: ANALYZING QUOTA")
        print(f"{SEPARATOR_LINE}")
        
        analyzer = QuotaAnalyzer(df)
        df_analyzed = analyzer.analyze()
        summary = analyzer.get_summary()
        
        # Print statistics
        analyzer.print_statistics()
        
        # =====================
        # STEP 4: GENERATE REPORTS
        # =====================
        print(f"\n{SEPARATOR_LINE}")
        print("STEP 4/4: GENERATING REPORTS")
        print(f"{SEPARATOR_LINE}")
        
        reporter = ReportGenerator(df_analyzed, summary)
        results = reporter.generate_all()
        
        # =====================
        # COMPLETION
        # =====================
        print(f"\n{SEPARATOR_LINE}")
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"{SEPARATOR_LINE}")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Farmers: {len(summary)}")
        print(f"   Overquota Farmers: {len(summary[summary['Status_Akhir'] == STATUS_OVERQUOTA])}")
        print(f"   Compliance Rate: {((len(summary) - len(summary[summary['Status_Akhir'] == STATUS_OVERQUOTA])) / len(summary) * 100):.2f}%")
        
        print(f"\n📁 OUTPUT LOCATION:")
        print(f"   {CLEANED_DATA_PATH}")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Review the Excel file: {OUTPUT_EXCEL}")
        print(f"   2. Check overquota farmers in 'Overquota' sheet")
        print(f"   3. Read detailed report: {OUTPUT_REPORT}")
        
        print(f"\n{SEPARATOR_LINE}")
        print(f"    Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{SEPARATOR_LINE}\n")
        
        return 0
    
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Analysis interrupted by user")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
