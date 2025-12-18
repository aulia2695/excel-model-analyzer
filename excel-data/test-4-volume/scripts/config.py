"""
config.py
Konfigurasi untuk output ke folder results
"""

import os
from pathlib import Path

# =====================================================
# PATH CONFIGURATION
# =====================================================

# Dapatkan path absolut dari script directory
SCRIPT_DIR = Path(__file__).parent.absolute()

# Path ke folder raw (data input)
RAW_DATA_PATH = SCRIPT_DIR.parent / "raw"

# Path ke folder results (data output)
RESULTS_PATH = SCRIPT_DIR.parent / "results"

# Buat folder results jika belum ada
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

# Alias untuk backward compatibility
CLEANED_DATA_PATH = RESULTS_PATH

# =====================================================
# INPUT FILES
# =====================================================

# Nama file input (di folder raw)
INPUT_FILENAME = "volumen_contoh_sedia.xlsx"  # Sesuaikan dengan nama file Anda
INPUT_FILE = RAW_DATA_PATH / INPUT_FILENAME

# =====================================================
# OUTPUT FILES (semua di folder results)
# =====================================================

# Excel output
OUTPUT_EXCEL = RESULTS_PATH / "analisis_kouta_lengkap.xlsx"

# Report text
OUTPUT_REPORT = RESULTS_PATH / "laporan_detail_kouta.txt"

# Summary CSV
OUTPUT_SUMMARY = RESULTS_PATH / "summary_per_farmer.csv"

# Dashboard PNG
OUTPUT_DASHBOARD = RESULTS_PATH / "dashboard_kouta.png"

# Individual charts
OUTPUT_CHART_STATUS = RESULTS_PATH / "chart_status_distribution.png"
OUTPUT_CHART_TOP = RESULTS_PATH / "chart_top_overquota.png"
OUTPUT_CHART_VOLUME = RESULTS_PATH / "chart_volume_distribution.png"

# =====================================================
# COLUMN NAMES
# =====================================================

COL_ID = 'ID'
COL_NAMA = 'Nama Propper'
COL_TANGGAL = 'Tanggal Transaksi'
COL_NETTO = 'Netto Gudang (Kg)'
COL_KOUTA = 'Kouta'

# =====================================================
# STATUS VALUES
# =====================================================

STATUS_DI_BAWAH = 'Di Bawah Kouta'
STATUS_OVERQUOTA = 'OVERQOUTA'

# =====================================================
# UI ELEMENTS
# =====================================================

SEPARATOR_LINE = "=" * 80

# =====================================================
# DISPLAY CONFIGURATION
# =====================================================

def print_paths():
    """Print semua path untuk debugging"""
    print(SEPARATOR_LINE)
    print("KONFIGURASI PATH")
    print(SEPARATOR_LINE)
    print(f"Script Directory : {SCRIPT_DIR}")
    print(f"Raw Data Path    : {RAW_DATA_PATH}")
    print(f"Results Path     : {RESULTS_PATH}")
    print(f"Input File       : {INPUT_FILE}")
    print(f"Output Excel     : {OUTPUT_EXCEL}")
    print(f"Output Report    : {OUTPUT_REPORT}")
    print(f"Output Dashboard : {OUTPUT_DASHBOARD}")
    print(SEPARATOR_LINE)


if __name__ == "__main__":
    print_paths()
    
    # Test: create results folder
    print(f"\n✅ Results folder created at: {RESULTS_PATH}")
    print(f"   Exists: {RESULTS_PATH.exists()}")
