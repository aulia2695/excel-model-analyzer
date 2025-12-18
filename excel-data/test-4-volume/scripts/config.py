"""
config.py
Konfigurasi untuk Volume Quota Analyzer
"""

import os

# ===========================
# PATH CONFIGURATION
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "..", "raw")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "..", "cleaned")

# Buat folder cleaned jika belum ada
os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

# ===========================
# FILE CONFIGURATION
# ===========================
INPUT_FILE = "volumen_contoh_sedia.xlsx"  # Sesuaikan dengan nama file Anda
OUTPUT_EXCEL = "hasil_analisis_kouta.xlsx"
OUTPUT_REPORT = "laporan_analisis.txt"
OUTPUT_SUMMARY = "summary_kouta.csv"

# ===========================
# COLUMN NAMES
# ===========================
COL_TANGGAL = "Tanggal Transaksi"
COL_ID = "ID"
COL_NAMA = "Nama Propper"
COL_KOUTA = "Kouta"
COL_NETTO = "Netto Gudang (Kg)"
COL_STATUS_PROGRAM = "Status Program"
COL_STATUS_KAWASAN = "Status Kawasan"

# Kolom yang akan ditambahkan
COL_TOTAL_KUMULATIF = "Total_Kumulatif"
COL_SISA_KOUTA = "Sisa_Kouta"
COL_STATUS_KOUTA = "Status_Kouta"
COL_SEHARUSNYA = "Seharusnya_Input"
COL_KELEBIHAN = "Kelebihan"
COL_KETERANGAN = "Keterangan"

# ===========================
# ANALYSIS PARAMETERS
# ===========================
GROUP_BY_COLUMNS = [COL_ID, COL_NAMA]  # Grouping per farmer
DATE_FORMAT = "%d/%m/%Y"  # Format tanggal output

# ===========================
# STATUS LABELS
# ===========================
STATUS_DI_BAWAH = "Di Bawah Kouta"
STATUS_OVERQUOTA = "OVERQOUTA"
KETERANGAN_OVERQUOTA = "TRANSAKSI OVERQOUTA"

# ===========================
# DISPLAY SETTINGS
# ===========================
DECIMAL_PLACES = 2  # Jumlah desimal untuk angka
SEPARATOR_LINE = "=" * 80
SEPARATOR_DASH = "-" * 80
