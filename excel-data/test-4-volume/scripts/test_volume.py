import pandas as pd
import numpy as np
from datetime import datetime
import os

class VolumeQuotaAnalyzer:
    """
    Analyzer untuk data transaksi volume dengan sistem kouta.
    Menganalisis apakah transaksi melebihi batas kouta yang ditentukan.
    """
    
    def __init__(self, file_path, kouta_column='Kouta', netto_column='Netto Gudang (Kg)'):
        """
        Initialize analyzer dengan file path dan nama kolom.
        
        Args:
            file_path: Path ke file Excel/CSV
            kouta_column: Nama kolom untuk kouta (default: 'Kouta')
            netto_column: Nama kolom untuk netto gudang (default: 'Netto Gudang (Kg)')
        """
        self.file_path = file_path
        self.kouta_column = kouta_column
        self.netto_column = netto_column
        self.df = None
        self.analysis_result = None
        
    def load_data(self):
        """Load data dari file Excel atau CSV"""
        try:
            if self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
                self.df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            else:
                raise ValueError("Format file tidak didukung. Gunakan .xlsx, .xls, atau .csv")
            
            print(f"✓ Data berhasil dimuat: {len(self.df)} baris")
            return True
        except Exception as e:
            print(f"✗ Error saat memuat data: {str(e)}")
            return False
    
    def validate_columns(self):
        """Validasi keberadaan kolom yang diperlukan"""
        required_columns = [self.kouta_column, self.netto_column]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            print(f"✗ Kolom tidak ditemukan: {', '.join(missing_columns)}")
            print(f"Kolom yang tersedia: {', '.join(self.df.columns.tolist())}")
            return False
        
        print("✓ Semua kolom diperlukan ditemukan")
        return True
    
    def analyze_quota(self, group_by_columns=None):
        """
        Analisis kouta per kelompok data (farmer/propper).
        
        Args:
            group_by_columns: List kolom untuk grouping (misal: ['ID', 'Nama Propper'])
        
        Returns:
            DataFrame dengan hasil analisis
        """
        if self.df is None:
            print("✗ Data belum dimuat. Gunakan load_data() terlebih dahulu.")
            return None
        
        # Jika tidak ada grouping, anggap semua data adalah satu grup
        if group_by_columns is None:
            group_by_columns = []
        
        # Pastikan kolom tanggal ada untuk sorting
        date_column = 'Tanggal Transaksi' if 'Tanggal Transaksi' in self.df.columns else None
        
        if date_column:
            # Convert ke datetime jika belum
            self.df[date_column] = pd.to_datetime(self.df[date_column], errors='coerce')
            # Sort berdasarkan tanggal
            self.df = self.df.sort_values(date_column)
        
        results = []
        
        # Jika ada grouping
        if group_by_columns:
            groups = self.df.groupby(group_by_columns, dropna=False)
        else:
            # Buat dummy group untuk seluruh data
            groups = [(None, self.df)]
        
        for group_key, group_data in groups:
            # Ambil kouta (asumsi sama untuk satu grup)
            kouta = group_data[self.kouta_column].iloc[0]
            
            # Hitung kumulatif
            group_data = group_data.copy()
            group_data['Total_Kumulatif'] = group_data[self.netto_column].cumsum()
            group_data['Sisa_Kouta'] = kouta - group_data['Total_Kumulatif']
            group_data['Status_Kouta'] = group_data['Sisa_Kouta'].apply(
                lambda x: 'Di Bawah Kouta' if x >= 0 else 'OVERQOUTA'
            )
            
            # Tandai baris pertama yang melebihi kouta
            overquota_rows = group_data[group_data['Sisa_Kouta'] < 0]
            if not overquota_rows.empty:
                first_overquota_idx = overquota_rows.index[0]
                group_data.loc[first_overquota_idx, 'Keterangan'] = 'TRANSAKSI PERTAMA YANG MELEBIHI KOUTA'
                
                # Hitung berapa yang seharusnya diinput
                prev_total = group_data.loc[:first_overquota_idx].iloc[-2]['Total_Kumulatif'] if len(group_data.loc[:first_overquota_idx]) > 1 else 0
                should_be = kouta - prev_total
                actual = group_data.loc[first_overquota_idx, self.netto_column]
                excess = group_data.loc[first_overquota_idx, 'Total_Kumulatif'] - kouta
                
                group_data.loc[first_overquota_idx, 'Seharusnya_Input'] = should_be
                group_data.loc[first_overquota_idx, 'Kelebihan'] = excess
            
            results.append(group_data)
        
        self.analysis_result = pd.concat(results, ignore_index=True)
        return self.analysis_result
    
    def generate_report(self, output_file=None):
        """
        Generate laporan analisis dalam format yang mudah dibaca.
        
        Args:
            output_file: Path untuk menyimpan laporan (opsional)
        """
        if self.analysis_result is None:
            print("✗ Belum ada hasil analisis. Jalankan analyze_quota() terlebih dahulu.")
            return
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("LAPORAN ANALISIS VOLUME KOUTA")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Summary per grup (jika ada ID atau Nama Propper)
        if 'ID' in self.analysis_result.columns or 'Nama Propper' in self.analysis_result.columns:
            group_cols = []
            if 'ID' in self.analysis_result.columns:
                group_cols.append('ID')
            if 'Nama Propper' in self.analysis_result.columns:
                group_cols.append('Nama Propper')
            
            groups = self.analysis_result.groupby(group_cols, dropna=False)
            
            for group_key, group_data in groups:
                report_lines.append(f"FARMER/PROPPER: {group_key}")
                report_lines.append("-" * 80)
                
                kouta = group_data[self.kouta_column].iloc[0]
                total_transaksi = len(group_data)
                total_volume = group_data[self.netto_column].sum()
                final_status = group_data['Status_Kouta'].iloc[-1]
                
                report_lines.append(f"Kouta Maksimal    : {kouta} Kg")
                report_lines.append(f"Total Transaksi   : {total_transaksi}")
                report_lines.append(f"Total Volume      : {total_volume:.2f} Kg")
                report_lines.append(f"Status Akhir      : {final_status}")
                
                # Cek apakah ada overquota
                overquota_data = group_data[group_data['Status_Kouta'] == 'OVERQOUTA']
                if not overquota_data.empty:
                    first_over = overquota_data.iloc[0]
                    report_lines.append("")
                    report_lines.append("⚠️  PERINGATAN: KOUTA TERLAMPAUI!")
                    report_lines.append(f"Transaksi pertama overquota: Tanggal {first_over.get('Tanggal Transaksi', 'N/A')}")
                    if 'Seharusnya_Input' in first_over:
                        report_lines.append(f"Volume yang diinput       : {first_over[self.netto_column]:.2f} Kg")
                        report_lines.append(f"Seharusnya hanya input    : {first_over['Seharusnya_Input']:.2f} Kg")
                        report_lines.append(f"Kelebihan                 : {first_over['Kelebihan']:.2f} Kg")
                
                report_lines.append("")
                report_lines.append("Detail Transaksi:")
                report_lines.append("")
                
                # Tampilkan detail transaksi
                for idx, row in group_data.iterrows():
                    status_symbol = "✓" if row['Status_Kouta'] == 'Di Bawah Kouta' else "✗"
                    date_str = row.get('Tanggal Transaksi', 'N/A')
                    if pd.notna(date_str) and isinstance(date_str, pd.Timestamp):
                        date_str = date_str.strftime('%d/%m/%Y')
                    
                    report_lines.append(
                        f"{status_symbol} {date_str} | "
                        f"Netto: {row[self.netto_column]:>8.2f} Kg | "
                        f"Total Kumulatif: {row['Total_Kumulatif']:>8.2f} Kg | "
                        f"Sisa: {row['Sisa_Kouta']:>8.2f} Kg | "
                        f"{row['Status_Kouta']}"
                    )
                
                report_lines.append("")
                report_lines.append("=" * 80)
                report_lines.append("")
        
        # Print ke console
        report_text = "\n".join(report_lines)
        print(report_text)
        
        # Save ke file jika diminta
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\n✓ Laporan disimpan ke: {output_file}")
    
    def export_to_excel(self, output_file):
        """
        Export hasil analisis ke file Excel dengan formatting.
        
        Args:
            output_file: Path untuk file Excel output
        """
        if self.analysis_result is None:
            print("✗ Belum ada hasil analisis. Jalankan analyze_quota() terlebih dahulu.")
            return
        
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                self.analysis_result.to_excel(writer, index=False, sheet_name='Analisis Kouta')
            
            print(f"✓ Data berhasil diekspor ke: {output_file}")
        except Exception as e:
            print(f"✗ Error saat mengekspor data: {str(e)}")


def main():
    """
    Fungsi utama untuk menjalankan analisis.
    Sesuaikan parameter sesuai kebutuhan.
    """
    
    # ==========================
    # KONFIGURASI
    # ==========================
    
    # Path ke file data (sesuaikan dengan lokasi file Anda)
    file_path = "volumen_contoh_sedia.xlsx"  # Atau .csv
    
    # Kolom untuk grouping (jika ingin analisis per farmer/propper)
    group_by = ['ID', 'Nama Propper']  # Set None jika tidak perlu grouping
    
    # Output files
    report_file = "laporan_analisis_kouta.txt"
    excel_output = "hasil_analisis_kouta.xlsx"
    
    # ==========================
    # PROSES ANALISIS
    # ==========================
    
    print("\n" + "="*80)
    print("VOLUME QUOTA ANALYZER")
    print("="*80 + "\n")
    
    # 1. Inisialisasi analyzer
    analyzer = VolumeQuotaAnalyzer(file_path)
    
    # 2. Load data
    if not analyzer.load_data():
        return
    
    # 3. Validasi kolom
    if not analyzer.validate_columns():
        return
    
    # 4. Jalankan analisis
    print("\nMenjalankan analisis kouta...")
    result = analyzer.analyze_quota(group_by_columns=group_by)
    
    if result is not None:
        print(f"✓ Analisis selesai: {len(result)} transaksi diproses\n")
        
        # 5. Generate laporan
        analyzer.generate_report(output_file=report_file)
        
        # 6. Export ke Excel
        analyzer.export_to_excel(excel_output)
        
        print("\n" + "="*80)
        print("ANALISIS SELESAI")
        print("="*80)


if __name__ == "__main__":
    main()
