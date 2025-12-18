"""
dashboard_generator.py
Script untuk generate dashboard visualisasi
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import os
from config import *


class DashboardGenerator:
    """Class untuk generate dashboard visualisasi"""
    
    def __init__(self, summary_df, df_analyzed):
        """
        Initialize DashboardGenerator
        
        Args:
            summary_df: DataFrame summary per farmer
            df_analyzed: DataFrame hasil analisis lengkap
        """
        self.summary = summary_df
        self.df_analyzed = df_analyzed
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def generate_dashboard(self, output_path=None):
        """
        Generate dashboard lengkap dengan multiple charts
        
        Args:
            output_path: Path untuk menyimpan dashboard (opsional)
        
        Returns:
            str: Path file yang disimpan
        """
        if output_path is None:
            output_path = os.path.join(CLEANED_DATA_PATH, 'dashboard_kouta.png')
        
        print(f"\n📊 Generating dashboard visualization...")
        
        # Create figure with GridSpec for custom layout
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('DASHBOARD ANALISIS VOLUME KOUTA', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Status Distribution (Pie Chart) - Top Left
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_status_distribution(ax1)
        
        # 2. Compliance Rate (Gauge-like) - Top Middle
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_compliance_rate(ax2)
        
        # 3. Summary Statistics (Text) - Top Right
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_summary_stats(ax3)
        
        # 4. Top 10 Overquota Farmers (Bar Chart) - Middle Row
        ax4 = fig.add_subplot(gs[1, :])
        self._plot_top_overquota(ax4)
        
        # 5. Volume Distribution by Farmer (Box Plot) - Bottom Left
        ax5 = fig.add_subplot(gs[2, 0])
        self._plot_volume_distribution(ax5)
        
        # 6. Trend Over Time (Line Chart) - Bottom Middle & Right
        ax6 = fig.add_subplot(gs[2, 1:])
        self._plot_volume_trend(ax6)
        
        # Save figure
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ Dashboard saved: {output_path}")
        
        plt.close()
        
        return output_path
    
    def _plot_status_distribution(self, ax):
        """Plot pie chart untuk distribusi status"""
        status_counts = self.summary['Status_Akhir'].value_counts()
        
        colors = ['#2ecc71', '#e74c3c']  # Green for compliant, Red for overquota
        explode = [0.05 if status == STATUS_OVERQUOTA else 0 for status in status_counts.index]
        
        wedges, texts, autotexts = ax.pie(
            status_counts.values,
            labels=status_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            shadow=True
        )
        
        # Enhance text
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title('Status Kouta Distribution', fontsize=12, fontweight='bold', pad=10)
    
    def _plot_compliance_rate(self, ax):
        """Plot compliance rate sebagai progress bar"""
        total = len(self.summary)
        compliant = len(self.summary[self.summary['Status_Akhir'] == STATUS_DI_BAWAH])
        rate = (compliant / total * 100) if total > 0 else 0
        
        # Create horizontal bar
        ax.barh([0], [rate], height=0.5, color='#2ecc71', alpha=0.8)
        ax.barh([0], [100-rate], left=[rate], height=0.5, color='#e74c3c', alpha=0.8)
        
        # Add percentage text
        ax.text(50, 0, f'{rate:.1f}%', 
                ha='center', va='center', 
                fontsize=24, fontweight='bold', color='white')
        
        # Styling
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_yticks([])
        ax.set_xlabel('Compliance Rate (%)', fontsize=10)
        ax.set_title('Overall Compliance Rate', fontsize=12, fontweight='bold', pad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    def _plot_summary_stats(self, ax):
        """Plot summary statistics sebagai text"""
        ax.axis('off')
        
        # Calculate statistics
        total_farmers = len(self.summary)
        overquota_farmers = len(self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA])
        total_volume = self.summary['Total_Volume'].sum()
        total_quota = self.summary[COL_KOUTA].sum()
        total_excess = self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA]['Selisih'].sum()
        
        # Create text
        stats_text = f"""
SUMMARY STATISTICS

Total Farmers: {total_farmers}
Compliant: {total_farmers - overquota_farmers}
Overquota: {overquota_farmers}

Total Volume: {total_volume:.2f} Kg
Total Quota: {total_quota:.2f} Kg
Total Excess: {total_excess:.2f} Kg

Avg Volume/Farmer:
{total_volume/total_farmers:.2f} Kg
        """
        
        ax.text(0.1, 0.5, stats_text.strip(), 
                transform=ax.transAxes,
                fontsize=11,
                verticalalignment='center',
                fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.set_title('Key Metrics', fontsize=12, fontweight='bold', pad=10)
    
    def _plot_top_overquota(self, ax):
        """Plot top 10 farmers dengan overquota terbesar"""
        overquota_df = self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA]
        
        if overquota_df.empty:
            ax.text(0.5, 0.5, 'No Overquota Farmers', 
                   ha='center', va='center', fontsize=14, transform=ax.transAxes)
            ax.set_title('Top 10 Overquota Farmers', fontsize=12, fontweight='bold', pad=10)
            ax.axis('off')
            return
        
        top_10 = overquota_df.nlargest(10, 'Selisih')
        
        # Create bars
        bars = ax.barh(range(len(top_10)), top_10['Selisih'], 
                       color='#e74c3c', alpha=0.7, edgecolor='black')
        
        # Add value labels
        for i, (idx, row) in enumerate(top_10.iterrows()):
            ax.text(row['Selisih'] + 0.5, i, f"{row['Selisih']:.2f} Kg",
                   va='center', fontsize=9)
        
        # Set labels
        ax.set_yticks(range(len(top_10)))
        ax.set_yticklabels(top_10[COL_NAMA], fontsize=9)
        ax.set_xlabel('Kelebihan Volume (Kg)', fontsize=10)
        ax.set_title('Top 10 Overquota Farmers', fontsize=12, fontweight='bold', pad=10)
        ax.invert_yaxis()
        
        # Grid
        ax.grid(axis='x', alpha=0.3)
    
    def _plot_volume_distribution(self, ax):
        """Plot distribusi volume per status"""
        compliant = self.summary[self.summary['Status_Akhir'] == STATUS_DI_BAWAH]['Total_Volume']
        overquota = self.summary[self.summary['Status_Akhir'] == STATUS_OVERQUOTA]['Total_Volume']
        
        data_to_plot = []
        labels = []
        colors = []
        
        if not compliant.empty:
            data_to_plot.append(compliant)
            labels.append('Compliant')
            colors.append('#2ecc71')
        
        if not overquota.empty:
            data_to_plot.append(overquota)
            labels.append('Overquota')
            colors.append('#e74c3c')
        
        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                           showmeans=True, meanline=True)
            
            # Color boxes
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
        
        ax.set_ylabel('Total Volume (Kg)', fontsize=10)
        ax.set_title('Volume Distribution', fontsize=12, fontweight='bold', pad=10)
        ax.grid(axis='y', alpha=0.3)
    
    def _plot_volume_trend(self, ax):
        """Plot trend volume over time"""
        if COL_TANGGAL not in self.df_analyzed.columns:
            ax.text(0.5, 0.5, 'No Date Data Available', 
                   ha='center', va='center', fontsize=14, transform=ax.transAxes)
            ax.axis('off')
            return
        
        # Group by date and sum
        daily_volume = self.df_analyzed.groupby(COL_TANGGAL)[COL_NETTO].sum().sort_index()
        cumulative_volume = daily_volume.cumsum()
        
        # Plot
        ax.plot(daily_volume.index, daily_volume.values, 
               marker='o', linewidth=2, markersize=6, 
               label='Daily Volume', color='#3498db', alpha=0.7)
        
        ax2 = ax.twinx()
        ax2.plot(cumulative_volume.index, cumulative_volume.values,
                marker='s', linewidth=2, markersize=5,
                label='Cumulative Volume', color='#e67e22', alpha=0.7)
        
        # Styling
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Daily Volume (Kg)', fontsize=10, color='#3498db')
        ax2.set_ylabel('Cumulative Volume (Kg)', fontsize=10, color='#e67e22')
        ax.set_title('Volume Trend Over Time', fontsize=12, fontweight='bold', pad=10)
        
        # Legends
        ax.legend(loc='upper left', fontsize=9)
        ax2.legend(loc='upper right', fontsize=9)
        
        # Grid
        ax.grid(alpha=0.3)
        
        # Rotate date labels
        ax.tick_params(axis='x', rotation=45)
    
    def generate_simple_charts(self):
        """
        Generate individual chart files (alternative to dashboard)
        """
        print(f"\n📊 Generating individual charts...")
        
        output_files = []
        
        # 1. Status Pie Chart
        fig, ax = plt.subplots(figsize=(8, 6))
        self._plot_status_distribution(ax)
        path1 = os.path.join(CLEANED_DATA_PATH, 'chart_status_distribution.png')
        plt.savefig(path1, dpi=300, bbox_inches='tight')
        plt.close()
        output_files.append(path1)
        print(f"✅ Saved: {path1}")
        
        # 2. Top Overquota Bar Chart
        fig, ax = plt.subplots(figsize=(12, 6))
        self._plot_top_overquota(ax)
        path2 = os.path.join(CLEANED_DATA_PATH, 'chart_top_overquota.png')
        plt.savefig(path2, dpi=300, bbox_inches='tight')
        plt.close()
        output_files.append(path2)
        print(f"✅ Saved: {path2}")
        
        # 3. Volume Distribution
        fig, ax = plt.subplots(figsize=(8, 6))
        self._plot_volume_distribution(ax)
        path3 = os.path.join(CLEANED_DATA_PATH, 'chart_volume_distribution.png')
        plt.savefig(path3, dpi=300, bbox_inches='tight')
        plt.close()
        output_files.append(path3)
        print(f"✅ Saved: {path3}")
        
        return output_files


def main():
    """Test DashboardGenerator"""
    from data_loader import DataLoader
    from quota_analyzer import QuotaAnalyzer
    
    print(SEPARATOR_LINE)
    print("DASHBOARD GENERATOR TEST")
    print(SEPARATOR_LINE)
    
    # Load and analyze data
    loader = DataLoader()
    df = loader.load_data()
    
    if df is not None and loader.validate_columns():
        df = loader.preprocess_data()
        
        analyzer = QuotaAnalyzer(df)
        df_analyzed = analyzer.analyze()
        summary = analyzer.get_summary()
        
        # Generate dashboard
        dashboard_gen = DashboardGenerator(summary, df_analyzed)
        
        # Option 1: Generate full dashboard
        dashboard_gen.generate_dashboard()
        
        # Option 2: Generate individual charts (uncomment if needed)
        # dashboard_gen.generate_simple_charts()
        
        print(f"\n{SEPARATOR_LINE}")
        print("✅ DASHBOARD GENERATOR TEST PASSED")
        print(SEPARATOR_LINE)
    else:
        print(f"\n❌ Test failed")


if __name__ == "__main__":
    main()
