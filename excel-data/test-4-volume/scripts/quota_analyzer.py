"""
quota_analyzer.py
Module untuk analisis kouta volume
"""

import pandas as pd
from config import *


class QuotaAnalyzer:
    """Class untuk analisis kouta"""
    
    def __init__(self, df):
        """
        Initialize QuotaAnalyzer
        
        Args:
            df: DataFrame yang sudah dipreprocess
        """
        self.df = df.copy()
        self.df_analyzed = None
        self.summary = None
    
    def analyze(self):
        """
        Analisis kouta per farmer
        
        Returns:
            DataFrame dengan analisis lengkap
        """
        print(f"\n🔍 Analyzing quota usage...")
        
        results = []
        
        # Group by farmer ID
        for farmer_id, group in self.df.groupby(COL_ID):
            # Sort by date
            group = group.sort_values(COL_TANGGAL)
            
            # Get quota
            kouta = group[COL_KOUTA].iloc[0]
            nama = group[COL_NAMA].iloc[0]
            
            # Calculate cumulative
            group = group.copy()
            group['Total_Kumulatif'] = group[COL_NETTO].cumsum()
            group['Sisa_Kouta'] = kouta - group['Total_Kumulatif']
            group['Status_Transaksi'] = group['Sisa_Kouta'].apply(
                lambda x: STATUS_DI_BAWAH if x >= 0 else STATUS_OVERQUOTA
            )
            
            # Mark first overquota transaction
            overquota_rows = group[group['Status_Transaksi'] == STATUS_OVERQUOTA]
            if not overquota_rows.empty:
                first_idx = overquota_rows.index[0]
                group.loc[first_idx, 'Keterangan'] = 'TRANSAKSI PERTAMA OVERQUOTA'
            
            results.append(group)
        
        self.df_analyzed = pd.concat(results, ignore_index=True)
        
        print(f"✅ Analysis complete: {len(self.df_analyzed)} transactions processed")
        
        return self.df_analyzed
    
    def get_summary(self):
        """
        Generate summary per farmer
        
        Returns:
            DataFrame summary
        """
        if self.df_analyzed is None:
            print("❌ Run analyze() first")
            return None
        
        print(f"\n📋 Generating summary...")
        
        summary_list = []
        
        for farmer_id, group in self.df_analyzed.groupby(COL_ID):
            kouta = group[COL_KOUTA].iloc[0]
            nama = group[COL_NAMA].iloc[0]
            
            total_volume = group[COL_NETTO].sum()
            total_transaksi = len(group)
            
            # Status akhir (dari transaksi terakhir)
            status_akhir = group['Status_Transaksi'].iloc[-1]
            
            # Hitung selisih dan persentase
            selisih = total_volume - kouta
            persentase = (total_volume / kouta * 100) if kouta > 0 else 0
            
            # Hitung berapa transaksi yang overquota
            transaksi_overquota = len(group[group['Status_Transaksi'] == STATUS_OVERQUOTA])
            
            summary_list.append({
                COL_ID: farmer_id,
                COL_NAMA: nama,
                COL_KOUTA: kouta,
                'Total_Volume': total_volume,
                'Total_Transaksi': total_transaksi,
                'Transaksi_Overquota': transaksi_overquota,
                'Selisih': selisih,
                'Persentase_Penggunaan': persentase,
                'Status_Akhir': status_akhir
            })
        
        self.summary = pd.DataFrame(summary_list)
        
        print(f"✅ Summary generated: {len(self.summary)} farmers")
        
        return self.summary
    
    def print_statistics(self):
        """Print statistik analisis"""
        if self.summary is None:
            print("❌ Generate summary first")
            return
        
        total_farmers = len(self.summary)
        overquota_count = len(self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA])
        compliant_count = total_farmers - overquota_count
        
        total_volume = self.summary['Total_Volume'].sum()
        total_quota = self.summary[COL_KOUTA].sum()
        
        print(f"\n{SEPARATOR_LINE}")
        print("📊 ANALYSIS STATISTICS")
        print(f"{SEPARATOR_LINE}")
        print(f"Total Farmers        : {total_farmers}")
        print(f"Compliant Farmers    : {compliant_count} ({compliant_count/total_farmers*100:.1f}%)")
        print(f"Overquota Farmers    : {overquota_count} ({overquota_count/total_farmers*100:.1f}%)")
        print(f"\nTotal Volume         : {total_volume:,.2f} Kg")
        print(f"Total Quota          : {total_quota:,.2f} Kg")
        print(f"Overall Usage        : {(total_volume/total_quota*100):.1f}%")
        print(f"{SEPARATOR_LINE}")


def main():
    """Test QuotaAnalyzer"""
    from data_loader import DataLoader
    
    print(SEPARATOR_LINE)
    print("QUOTA ANALYZER TEST")
    print(SEPARATOR_LINE)
    
    # Load data
    loader = DataLoader()
    df = loader.load_data()
    
    if df is not None and loader.validate_columns():
        df = loader.preprocess_data()
        
        # Analyze
        analyzer = QuotaAnalyzer(df)
        df_analyzed = analyzer.analyze()
        summary = analyzer.get_summary()
        
        # Print statistics
        analyzer.print_statistics()
        
        print(f"\n{SEPARATOR_LINE}")
        print("✅ QUOTA ANALYZER TEST PASSED")
        print(SEPARATOR_LINE)
    else:
        print(f"\n❌ Test failed")


if __name__ == "__main__":
    main()
