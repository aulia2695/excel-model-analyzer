"""
data_loader.py
Module untuk loading dan preprocessing data
"""

import pandas as pd
from pathlib import Path
from config import *


class DataLoader:
    """Class untuk load dan preprocess data"""
    
    def __init__(self, input_file=None):
        """
        Initialize DataLoader
        
        Args:
            input_file: Path ke file input (opsional, default dari config)
        """
        if input_file is None:
            self.input_file = INPUT_FILE
        else:
            self.input_file = Path(input_file)
        
        self.df = None
        
    def load_data(self):
        """
        Load data dari file Excel
        
        Returns:
            DataFrame atau None jika gagal
        """
        print(f"📂 Loading data from: {self.input_file}")
        
        try:
            if not self.input_file.exists():
                print(f"❌ File not found: {self.input_file}")
                return None
            
            # Load Excel
            self.df = pd.read_excel(self.input_file)
            
            print(f"✅ Data loaded successfully")
            print(f"   Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
            
            return self.df
            
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return None
    
    def validate_columns(self):
        """
        Validasi kolom-kolom yang diperlukan
        
        Returns:
            bool: True jika semua kolom ada
        """
        if self.df is None:
            print("❌ Data not loaded yet")
            return False
        
        required_cols = [COL_ID, COL_NAMA, COL_TANGGAL, COL_NETTO, COL_KOUTA]
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {', '.join(missing_cols)}")
            print(f"   Available columns: {', '.join(self.df.columns.tolist())}")
            return False
        
        print(f"✅ All required columns found")
        return True
    
    def preprocess_data(self):
        """
        Preprocess data: convert types, handle nulls, etc.
        
        Returns:
            DataFrame yang sudah dipreprocess
        """
        if self.df is None:
            print("❌ Data not loaded yet")
            return None
        
        print(f"\n🔄 Preprocessing data...")
        
        df = self.df.copy()
        
        # 1. Convert tanggal ke datetime
        if COL_TANGGAL in df.columns:
            df[COL_TANGGAL] = pd.to_datetime(df[COL_TANGGAL], errors='coerce')
            print(f"   ✓ Converted {COL_TANGGAL} to datetime")
        
        # 2. Convert numeric columns
        numeric_cols = [COL_NETTO, COL_KOUTA]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                print(f"   ✓ Converted {col} to numeric")
        
        # 3. Handle missing values
        before_nulls = df.isnull().sum().sum()
        df = df.dropna(subset=[COL_ID, COL_NAMA, COL_NETTO, COL_KOUTA])
        after_nulls = len(self.df) - len(df)
        
        if after_nulls > 0:
            print(f"   ⚠️  Removed {after_nulls} rows with missing critical values")
        
        # 4. Sort by date
        if COL_TANGGAL in df.columns:
            df = df.sort_values([COL_ID, COL_TANGGAL])
            print(f"   ✓ Sorted by {COL_ID} and {COL_TANGGAL}")
        
        print(f"✅ Preprocessing complete")
        print(f"   Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        self.df = df
        return df
    
    def get_summary_info(self):
        """Print summary information about the data"""
        if self.df is None:
            print("❌ Data not loaded yet")
            return
        
        print(f"\n📊 DATA SUMMARY")
        print(f"{SEPARATOR_LINE}")
        print(f"Total Records    : {len(self.df)}")
        print(f"Total Farmers    : {self.df[COL_ID].nunique()}")
        print(f"Date Range       : {self.df[COL_TANGGAL].min()} to {self.df[COL_TANGGAL].max()}")
        print(f"Total Volume     : {self.df[COL_NETTO].sum():,.2f} Kg")
        print(f"Avg Volume/Trans : {self.df[COL_NETTO].mean():,.2f} Kg")
        print(f"{SEPARATOR_LINE}")


def main():
    """Test DataLoader"""
    print(SEPARATOR_LINE)
    print("DATA LOADER TEST")
    print(SEPARATOR_LINE)
    
    loader = DataLoader()
    
    # Load data
    df = loader.load_data()
    
    if df is not None:
        # Validate
        if loader.validate_columns():
            # Preprocess
            df = loader.preprocess_data()
            
            # Show summary
            loader.get_summary_info()
            
            print(f"\n{SEPARATOR_LINE}")
            print("✅ DATA LOADER TEST PASSED")
            print(SEPARATOR_LINE)
        else:
            print(f"\n❌ Validation failed")
    else:
        print(f"\n❌ Test failed")


if __name__ == "__main__":
    main()
