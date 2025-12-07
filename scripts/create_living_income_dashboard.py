"""
Living Income Dashboard Creator (Exercise 2)
Creates visual dashboard with dummy data for demonstration
Can be adapted with real data later
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# Create output directory
OUTPUT_DIR = 'excel-data/test-2-farmer-development/results/living-income-dashboard'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("="*70)
print("LIVING INCOME DASHBOARD GENERATOR")
print("Exercise 2: Dashboard Design with Dummy Data")
print("="*70)

# =============================================================================
# DUMMY DATA GENERATION
# =============================================================================

print("\n[1/7] Generating dummy data...")

# Constants
LIVING_INCOME_BENCHMARK = 2_500_000  # CFA
COCOA_PRICE_PER_KG = 1_000  # CFA
PREMIUM_PER_KG = 40  # CFA
COCOA_REVENUE_PCT = 0.72  # 72% of total revenue from cocoa

# Generate farmer data
np.random.seed(42)
n_farmers = 200

farmer_data = {
    'farmer_id': [f'F{i:04d}' for i in range(1, n_farmers+1)],
    'cooperative': np.random.choice(['Coop A', 'Coop B', 'Coop C', 'Coop D'], n_farmers),
    'cocoa_volume_kg': np.random.normal(1200, 300, n_farmers).clip(200, 3000),
    'household_size': np.random.randint(3, 9, n_farmers),
}

df = pd.DataFrame(farmer_data)

# Calculate incomes
df['cocoa_revenue'] = df['cocoa_volume_kg'] * (COCOA_PRICE_PER_KG + PREMIUM_PER_KG)
df['total_income'] = df['cocoa_revenue'] / COCOA_REVENUE_PCT
df['other_income'] = df['total_income'] - df['cocoa_revenue']
df['income_gap'] = LIVING_INCOME_BENCHMARK - df['total_income']
df['below_benchmark'] = df['total_income'] < LIVING_INCOME_BENCHMARK

# Production costs
df['labor_cost'] = df['cocoa_volume_kg'] * np.random.uniform(400, 600, n_farmers)
df['input_cost'] = df['cocoa_volume_kg'] * np.random.uniform(250, 400, n_farmers)
df['total_cost'] = df['labor_cost'] + df['input_cost']
df['net_income'] = df['total_income'] - df['total_cost']

print(f"   ✓ Generated data for {n_farmers} farmers")
print(f"   • Average total income: {df['total_income'].mean():,.0f} CFA")
print(f"   • Average income gap: {df['income_gap'].mean():,.0f} CFA")
print(f"   • % below benchmark: {df['below_benchmark'].mean()*100:.1f}%")

# =============================================================================
# CHART 1: KPI CARDS
# =============================================================================

print("\n[2/7] Creating KPI dashboard...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Top KPI Cards
kpi_data = [
    ('Living Income\nBenchmark', f'{LIVING_INCOME_BENCHMARK:,.0f}\nCFA', '#3498db'),
    ('Average Farmer\nIncome', f'{df["total_income"].mean():,.0f}\nCFA', '#2ecc71'),
    ('Average Income\nGap', f'{df["income_gap"].mean():,.0f}\nCFA', '#e74c3c'),
    ('% Farmers Below\nBenchmark', f'{df["below_benchmark"].mean()*100:.1f}%', '#f39c12'),
]

for idx, (label, value, color) in enumerate(kpi_data):
    ax = fig.add_subplot(gs[0, idx if idx < 3 else 2])
    ax.text(0.5, 0.6, value, ha='center', va='center', fontsize=24, fontweight='bold', color=color)
    ax.text(0.5, 0.3, label, ha='center', va='center', fontsize=10, color='#555')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor=color, linewidth=3))

# =============================================================================
# CHART 2: INCOME DISTRIBUTION
# =============================================================================

print("[3/7] Creating income distribution chart...")

ax2 = fig.add_subplot(gs[1, 0])
bins = [0, 1_000_000, 1_500_000, 2_000_000, 2_500_000, 3_500_000]
labels = ['<1M', '1-1.5M', '1.5-2M', '2-2.5M', '>2.5M']

hist_data = pd.cut(df['total_income'], bins=bins, labels=labels).value_counts().sort_index()
colors_hist = ['#e74c3c' if i < 3 else '#2ecc71' for i in range(len(hist_data))]

ax2.bar(range(len(hist_data)), hist_data.values, color=colors_hist, alpha=0.7, edgecolor='black')
ax2.axvline(x=3.5, color='red', linestyle='--', linewidth=2, label='Benchmark')
ax2.set_xticks(range(len(hist_data)))
ax2.set_xticklabels(labels, rotation=0)
ax2.set_xlabel('Income Level (CFA)', fontweight='bold')
ax2.set_ylabel('Number of Farmers', fontweight='bold')
ax2.set_title('Income Distribution', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# Add value labels
for i, v in enumerate(hist_data.values):
    ax2.text(i, v + 2, str(v), ha='center', va='bottom', fontweight='bold')

# =============================================================================
# CHART 3: INCOME COMPOSITION
# =============================================================================

print("[4/7] Creating income composition chart...")

ax3 = fig.add_subplot(gs[1, 1])
income_sources = [
    df['cocoa_revenue'].mean(),
    df['other_income'].mean() * 0.65,  # Other crops
    df['other_income'].mean() * 0.25,  # Livestock
    df['other_income'].mean() * 0.10,  # Other
]
labels_pie = ['Cocoa (72%)', 'Other Crops (18%)', 'Livestock (7%)', 'Other (3%)']
colors_pie = ['#8B4513', '#2ecc71', '#f39c12', '#95a5a6']

wedges, texts, autotexts = ax3.pie(income_sources, labels=labels_pie, colors=colors_pie,
                                     autopct='%1.1f%%', startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax3.set_title('Income Sources', fontsize=12, fontweight='bold')

# =============================================================================
# CHART 4: PRODUCTION COST BREAKDOWN
# =============================================================================

print("[5/7] Creating cost breakdown chart...")

ax4 = fig.add_subplot(gs[1, 2])
avg_labor = df['labor_cost'].mean()
avg_input = df['input_cost'].mean()

bars = ax4.bar(['Production\nCosts'], [avg_labor + avg_input], color='#ecf0f1', edgecolor='black', linewidth=2)
ax4.bar(['Production\nCosts'], [avg_labor], color='#3498db', label=f'Labor: {avg_labor:,.0f} CFA')
ax4.bar(['Production\nCosts'], [avg_input], bottom=[avg_labor], color='#e67e22', 
        label=f'Input: {avg_input:,.0f} CFA')

ax4.set_ylabel('Cost (CFA)', fontweight='bold')
ax4.set_title('Average Production Costs', fontsize=12, fontweight='bold')
ax4.legend(loc='upper right')
ax4.grid(axis='y', alpha=0.3)

# Add total label
total_cost = avg_labor + avg_input
ax4.text(0, total_cost + total_cost*0.05, f'Total: {total_cost:,.0f} CFA', 
         ha='center', va='bottom', fontweight='bold', fontsize=10)

# =============================================================================
# CHART 5: REGIONAL COMPARISON
# =============================================================================

print("[6/7] Creating regional comparison chart...")

ax5 = fig.add_subplot(gs[2, :2])
regional_data = df.groupby('cooperative').agg({
    'total_income': 'mean',
    'income_gap': 'mean',
    'farmer_id': 'count'
}).round(0)
regional_data.columns = ['Avg Income', 'Avg Gap', 'Farmers']
regional_data['Gap %'] = (regional_data['Avg Gap'] / LIVING_INCOME_BENCHMARK * 100).round(1)

x = np.arange(len(regional_data))
width = 0.35

bars1 = ax5.bar(x - width/2, regional_data['Avg Income'], width, label='Average Income', 
                color='#2ecc71', alpha=0.7)
ax5.axhline(y=LIVING_INCOME_BENCHMARK, color='red', linestyle='--', linewidth=2, label='Benchmark')

ax5.set_xlabel('Cooperative', fontweight='bold')
ax5.set_ylabel('Income (CFA)', fontweight='bold')
ax5.set_title('Regional Comparison: Average Income vs Benchmark', fontsize=12, fontweight='bold')
ax5.set_xticks(x)
ax5.set_xticklabels(regional_data.index)
ax5.legend()
ax5.grid(axis='y', alpha=0.3)

# Add value labels
for i, (bar, gap_pct) in enumerate(zip(bars1, regional_data['Gap %'])):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:,.0f}\n({gap_pct:.0f}% gap)',
            ha='center', va='bottom', fontsize=8, fontweight='bold')

# =============================================================================
# CHART 6: INCOME GAP WATERFALL
# =============================================================================

print("[7/7] Creating income gap waterfall chart...")

ax6 = fig.add_subplot(gs[2, 2])

# Waterfall components
waterfall_data = {
    'Cocoa\nRevenue': df['cocoa_revenue'].mean(),
    'Other\nIncome': df['other_income'].mean(),
    'Total\nIncome': 0,  # Will be cumulative
    'Gap to\nBenchmark': df['income_gap'].mean(),
}

categories = list(waterfall_data.keys())
values = list(waterfall_data.values())

# Calculate cumulative
cumulative = [0, values[0], values[0] + values[1], values[0] + values[1]]
values[2] = values[0] + values[1]  # Total income

colors_waterfall = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']

# Plot bars
for i, (cat, val, cum, color) in enumerate(zip(categories, values, cumulative, colors_waterfall)):
    if i < 3:
        ax6.bar(i, val, bottom=cum, color=color, edgecolor='black', linewidth=1)
        ax6.text(i, cum + val/2, f'{val:,.0f}', ha='center', va='center', 
                fontweight='bold', fontsize=8, color='white')
    else:
        # Gap bar (negative)
        ax6.bar(i, -val, bottom=LIVING_INCOME_BENCHMARK, color=color, edgecolor='black', linewidth=1)
        ax6.text(i, LIVING_INCOME_BENCHMARK - val/2, f'{-val:,.0f}', ha='center', va='center',
                fontweight='bold', fontsize=8, color='white')

# Benchmark line
ax6.axhline(y=LIVING_INCOME_BENCHMARK, color='red', linestyle='--', linewidth=2, label='Benchmark')

ax6.set_xticks(range(len(categories)))
ax6.set_xticklabels(categories, fontsize=9)
ax6.set_ylabel('Amount (CFA)', fontweight='bold')
ax6.set_title('Income Gap Analysis', fontsize=12, fontweight='bold')
ax6.legend()
ax6.grid(axis='y', alpha=0.3)

# =============================================================================
# SAVE DASHBOARD
# =============================================================================

plt.suptitle('LIVING INCOME DASHBOARD - IVORY COAST 2024', 
             fontsize=16, fontweight='bold', y=0.98)

dashboard_path = os.path.join(OUTPUT_DIR, f'living_income_dashboard_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved dashboard: {dashboard_path}")
plt.close()

# =============================================================================
# CREATE EXCEL REPORT
# =============================================================================

print("\n[8/8] Creating Excel report...")

excel_path = os.path.join(OUTPUT_DIR, f'living_income_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    # Summary sheet
    summary = pd.DataFrame({
        'Metric': [
            'Living Income Benchmark',
            'Average Farmer Income',
            'Average Income Gap',
            '% Farmers Below Benchmark',
            'Total Farmers Surveyed',
            'Average Cocoa Revenue',
            'Average Other Income',
            'Average Labor Cost',
            'Average Input Cost',
            'Average Net Income'
        ],
        'Value': [
            f'{LIVING_INCOME_BENCHMARK:,.0f} CFA',
            f'{df["total_income"].mean():,.0f} CFA',
            f'{df["income_gap"].mean():,.0f} CFA',
            f'{df["below_benchmark"].mean()*100:.1f}%',
            n_farmers,
            f'{df["cocoa_revenue"].mean():,.0f} CFA',
            f'{df["other_income"].mean():,.0f} CFA',
            f'{df["labor_cost"].mean():,.0f} CFA',
            f'{df["input_cost"].mean():,.0f} CFA',
            f'{df["net_income"].mean():,.0f} CFA'
        ]
    })
    summary.to_excel(writer, sheet_name='Summary', index=False)
    
    # Regional data
    regional_data.to_excel(writer, sheet_name='Regional Comparison')
    
    # Full dataset
    df.round(2).to_excel(writer, sheet_name='Farmer Data', index=False)

print(f"✓ Saved Excel report: {excel_path}")

print("\n" + "="*70)
print("DASHBOARD GENERATION COMPLETE!")
print("="*70)
print(f"\nFiles created:")
print(f"  • Dashboard PNG: {dashboard_path}")
print(f"  • Excel Report: {excel_path}")
print("="*70)
