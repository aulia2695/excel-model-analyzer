"""
report_generator.py
Module untuk generate berbagai format report
"""

import pandas as pd
from datetime import datetime
from config import *


class ReportGenerator:
    """Class untuk generate reports"""
    
    def __init__(self, df_analyzed, summary_df):
        """
        Initialize ReportGenerator
        
        Args:
            df_analyzed: DataFrame hasil analisis lengkap
            summary_df: DataFrame summary per farmer
        """
        self.df_analyzed = df_analyzed
        self.summary = summary_df
    
    def generate_all(self):
        """
        Generate semua report sekaligus
        
        Returns:
            dict: Path ke semua file yang dihasilkan
        """
        results = {}
        
        # 1. Excel Report
        results['excel'] = self.generate_excel_report()
        
        # 2. Text Report
        results['text'] = self.generate_text_report()
        
        # 3. CSV Summary
        results['csv'] = self.generate_csv_summary()
        
        return results
    
    def generate_excel_report(self, output_path=None):
        """
        Generate Excel report dengan multiple sheets
        
        Args:
            output_path: Path output (default dari config)
        
        Returns:
            Path file yang disimpan
        """
        if output_path is None:
            output_path = OUTPUT_EXCEL
        
        print(f"\n📊 Generating Excel report...")
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # Sheet 1: Summary per Farmer
                self.summary.to_excel(
                    writer, 
                    sheet_name='Summary', 
                    index=False
                )
                print(f"   ✓ Sheet 'Summary' created")
                
                # Sheet 2: All Transactions (analyzed)
                self.df_analyzed.to_excel(
                    writer,
                    sheet_name='All Transactions',
                    index=False
                )
                print(f"   ✓ Sheet 'All Transactions' created")
                
                # Sheet 3: Overquota Only
                overquota_df = self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA]
                overquota_df.to_excel(
                    writer,
                    sheet_name='Overquota Farmers',
                    index=False
                )
                print(f"   ✓ Sheet 'Overquota Farmers' created ({len(overquota_df)} farmers)")
                
                # Sheet 4: Compliant Only
                compliant_df = self.summary[self.summary['Status_Akhir'] == STATUS_DI_BAWAH]
                compliant_df.to_excel(
                    writer,
                    sheet_name='Compliant Farmers',
                    index=False
                )
                print(f"   ✓ Sheet 'Compliant Farmers' created ({len(compliant_df)} farmers)")
            
            print(f"✅ Excel report saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating Excel: {str(e)}")
            return None
    
    def generate_text_report(self, output_path=None):
        """
        Generate detailed text report
        
        Args:
            output_path: Path output (default dari config)
        
        Returns:
            Path file yang disimpan
        """
        if output_path is None:
            output_path = OUTPUT_REPORT
        
        print(f"\n📄 Generating text report...")
        
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("LAPORAN ANALISIS VOLUME KOUTA")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Source: {INPUT_FILE}")
        lines.append("")
        
        # Overall Statistics
        total_farmers = len(self.summary)
        overquota_count = len(self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA])
        compliant_count = total_farmers - overquota_count
        
        total_volume = self.summary['Total_Volume'].sum()
        total_quota = self.summary[COL_KOUTA].sum()
        total_excess = self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA]['Selisih'].sum()
        
        lines.append("RINGKASAN KESELURUHAN")
        lines.append("-" * 80)
        lines.append(f"Total Farmers            : {total_farmers}")
        lines.append(f"Compliant Farmers        : {compliant_count} ({compliant_count/total_farmers*100:.1f}%)")
        lines.append(f"Overquota Farmers        : {overquota_count} ({overquota_count/total_farmers*100:.1f}%)")
        lines.append("")
        lines.append(f"Total Volume             : {total_volume:,.2f} Kg")
        lines.append(f"Total Quota              : {total_quota:,.2f} Kg")
        lines.append(f"Total Excess Volume      : {total_excess:,.2f} Kg")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
        
        # Detail per Farmer (Overquota only)
        if overquota_count > 0:
            lines.append("DETAIL FARMER OVERQUOTA")
            lines.append("=" * 80)
            lines.append("")
            
            overquota_farmers = self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA]
            overquota_farmers = overquota_farmers.sort_values('Selisih', ascending=False)
            
            for idx, row in overquota_farmers.iterrows():
                lines.append(f"Farmer ID   : {row[COL_ID]}")
                lines.append(f"Name        : {row[COL_NAMA]}")
                lines.append(f"Quota       : {row[COL_KOUTA]:,.2f} Kg")
                lines.append(f"Total Volume: {row['Total_Volume']:,.2f} Kg")
                lines.append(f"Excess      : {row['Selisih']:,.2f} Kg ({row['Persentase_Penggunaan']:.1f}% of quota)")
                lines.append(f"Transactions: {row['Total_Transaksi']} ({row['Transaksi_Overquota']} overquota)")
                
                # Detail transactions for this farmer
                farmer_trans = self.df_analyzed[self.df_analyzed[COL_ID] == row[COL_ID]]
                
                lines.append("")
                lines.append("Transaction Details:")
                lines.append(f"{'Date':<12} {'Volume (Kg)':>12} {'Cumulative':>12} {'Remaining':>12} {'Status':<20}")
                lines.append("-" * 80)
                
                for _, trans in farmer_trans.iterrows():
                    date_str = trans[COL_TANGGAL].strftime('%d/%m/%Y') if pd.notna(trans[COL_TANGGAL]) else 'N/A'
                    status_symbol = "✓" if trans['Status_Transaksi'] == STATUS_DI_BAWAH else "✗"
                    
                    lines.append(
                        f"{date_str:<12} "
                        f"{trans[COL_NETTO]:>12.2f} "
                        f"{trans['Total_Kumulatif']:>12.2f} "
                        f"{trans['Sisa_Kouta']:>12.2f} "
                        f"{status_symbol} {trans['Status_Transaksi']}"
                    )
                
                lines.append("")
                lines.append("-" * 80)
                lines.append("")
        
        # Compliant Farmers Summary
        lines.append("FARMER COMPLIANT")
        lines.append("=" * 80)
        
        compliant_farmers = self.summary[self.summary['Status_Akhir'] == STATUS_DI_BAWAH]
        
        if len(compliant_farmers) > 0:
            lines.append(f"Total: {len(compliant_farmers)} farmers")
            lines.append("")
            lines.append(f"{'Farmer Name':<30} {'Quota (Kg)':>12} {'Used (Kg)':>12} {'Usage %':>10}")
            lines.append("-" * 80)
            
            for _, row in compliant_farmers.iterrows():
                lines.append(
                    f"{row[COL_NAMA]:<30} "
                    f"{row[COL_KOUTA]:>12.2f} "
                    f"{row['Total_Volume']:>12.2f} "
                    f"{row['Persentase_Penggunaan']:>9.1f}%"
                )
        else:
            lines.append("No compliant farmers found.")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"End of Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        
        # Save to file
        report_text = "\n".join(lines)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            
            print(f"✅ Text report saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error saving text report: {str(e)}")
            return None
    
    def generate_csv_summary(self, output_path=None):
        """
        Generate CSV summary (simple format for further analysis)
        
        Args:
            output_path: Path output (default dari config)
        
        Returns:
            Path file yang disimpan
        """
        if output_path is None:
            output_path = OUTPUT_SUMMARY
        
        print(f"\n📊 Generating CSV summary...")
        
        try:
            self.summary.to_csv(output_path, index=False)
            print(f"✅ CSV summary saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error saving CSV: {str(e)}")
            return None


def main():
    """Test ReportGenerator"""
    from data_loader import DataLoader
    from quota_analyzer import QuotaAnalyzer
    
    print(SEPARATOR_LINE)
    print("REPORT GENERATOR TEST")
    print(SEPARATOR_LINE)
    
    # Load and analyze data
    loader = DataLoader()
    df = loader.load_data()
    
    if df is not None and loader.validate_columns():
        df = loader.preprocess_data()
        
        analyzer = QuotaAnalyzer(df)
        df_analyzed = analyzer.analyze()
        summary = analyzer.get_summary()
        
        # Generate reports
        reporter = ReportGenerator(df_analyzed, summary)
        results = reporter.generate_all()
        
        print(f"\n{SEPARATOR_LINE}")
        print("✅ REPORT GENERATOR TEST PASSED")
        print(f"{SEPARATOR_LINE}")
        
        print(f"\n📁 Generated files:")
        for report_type, path in results.items():
            if path:
                print(f"   {report_type}: {path}")
    else:
        print(f"\n❌ Test failed")


if __name__ == "__main__":
    main()
