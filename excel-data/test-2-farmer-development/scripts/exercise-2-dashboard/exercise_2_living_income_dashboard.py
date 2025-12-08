"""
Exercise 2: Living Income Dashboard Design
Creates visualization mockup with dummy data showing dashboard components
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

class LivingIncomeDashboard:
    def __init__(self):
        """Initialize dashboard designer"""
        self.results_dir = Path("excel-data/test-2-farmer-development/results/exercise-2-dashboard/dashboard_design")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
    def create_dashboard_mockup(self):
        """Create comprehensive dashboard design with dummy data"""
        print("\n📊 Creating Living Income Dashboard Mockup...")
        
        # Create figure with custom layout
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(4, 3, hspace=0.4, wspace=0.3)
        
        # Color scheme
        colors = {
            'primary': '#2c3e50',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db'
        }
        
        # Title
        fig.suptitle('LIVING INCOME DASHBOARD - JB COCOA IVORY COAST', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # 1. KPI Cards (Top Row)
        self._create_kpi_cards(fig, gs, colors)
        
        # 2. Income Gap Waterfall Chart
        ax2 = fig.add_subplot(gs[1, :2])
        self._create_waterfall_chart(ax2, colors)
        
        # 3. Living Income Achievement Gauge
        ax3 = fig.add_subplot(gs[1, 2])
        self._create_gauge_chart(ax3, colors)
        
        # 4. Income Components Breakdown
        ax4 = fig.add_subplot(gs[2, 0])
        self._create_income_breakdown(ax4, colors)
        
        # 5. Cost Structure
        ax5 = fig.add_subplot(gs[2, 1])
        self._create_cost_structure(ax5, colors)
        
        # 6. Regional Comparison
        ax6 = fig.add_subplot(gs[2, 2])
        self._create_regional_comparison(ax6, colors)
        
        # 7. Progress Over Time
        ax7 = fig.add_subplot(gs[3, :])
        self._create_progress_timeline(ax7, colors)
        
        # Save dashboard
        output_path = self.results_dir / "living_income_dashboard_mockup.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✓ Dashboard mockup saved to {output_path}")
        
    def _create_kpi_cards(self, fig, gs, colors):
        """Create KPI indicator cards"""
        kpis = [
            {'title': 'Avg. Actual Income', 'value': '2,856,000 CFA', 'subtitle': 'per household/year', 'color': colors['info']},
            {'title': 'Living Income Benchmark', 'value': '3,612,000 CFA', 'subtitle': 'Ivory Coast 2023', 'color': colors['primary']},
            {'title': 'Income Gap', 'value': '-756,000 CFA', 'subtitle': '-21% below benchmark', 'color': colors['danger']},
            {'title': 'Farmers Below LI', 'value': '68%', 'subtitle': 'of surveyed farmers', 'color': colors['warning']},
        ]
        
        for i, kpi in enumerate(kpis):
            ax = fig.add_subplot(gs[0, i % 4])
            ax.axis('off')
            
            # Create card
            rect = mpatches.FancyBboxPatch((0.1, 0.2), 0.8, 0.6, 
                                          boxstyle="round,pad=0.05", 
                                          facecolor=kpi['color'], 
                                          edgecolor='none', alpha=0.2)
            ax.add_patch(rect)
            
            # Add text
            ax.text(0.5, 0.7, kpi['title'], ha='center', va='center', 
                   fontsize=11, fontweight='bold', color=colors['primary'])
            ax.text(0.5, 0.5, kpi['value'], ha='center', va='center', 
                   fontsize=16, fontweight='bold', color=kpi['color'])
            ax.text(0.5, 0.3, kpi['subtitle'], ha='center', va='center', 
                   fontsize=9, color='gray')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
    
    def _create_waterfall_chart(self, ax, colors):
        """Create waterfall chart showing income gap components"""
        categories = ['Living Income\nBenchmark', 'Cocoa\nRevenue', 'Other\nRevenue', 
                     'Labor\nCosts', 'Input\nCosts', 'Actual\nIncome']
        values = [3612000, -2520000, -720000, 450000, 306000, 2856000]
        
        # Calculate cumulative values
        cumulative = [3612000]
        for v in values[1:-1]:
            cumulative.append(cumulative[-1] + v)
        cumulative.append(2856000)
        
        # Plot bars
        colors_list = [colors['primary'], colors['success'], colors['info'], 
                      colors['danger'], colors['danger'], colors['warning']]
        
        for i, (cat, val, cum, col) in enumerate(zip(categories, values, cumulative, colors_list)):
            if i == 0:
                ax.bar(i, val, color=col, alpha=0.7, edgecolor='black', linewidth=1.5)
            elif i == len(categories) - 1:
                ax.bar(i, val, color=col, alpha=0.7, edgecolor='black', linewidth=1.5)
            else:
                bottom = cum - val if val < 0 else cum - val
                ax.bar(i, abs(val), bottom=bottom, color=col, alpha=0.7, 
                      edgecolor='black', linewidth=1.5)
                
                # Connection lines
                if i > 0:
                    ax.plot([i-0.4, i-0.6], [cumulative[i-1], cumulative[i-1]], 
                           'k--', linewidth=1, alpha=0.5)
        
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, fontsize=9)
        ax.set_ylabel('Amount (CFA)', fontsize=10, fontweight='bold')
        ax.set_title('Living Income Gap Breakdown', fontsize=12, fontweight='bold', pad=10)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(axis='y', alpha=0.3)
    
    def _create_gauge_chart(self, ax, colors):
        """Create gauge chart for living income achievement"""
        achievement = 79  # 79% of living income benchmark
        
        # Create semi-circle
        theta = np.linspace(0, np.pi, 100)
        
        # Background arc
        r = 1
        x_bg = r * np.cos(theta)
        y_bg = r * np.sin(theta)
        ax.fill_between(x_bg, 0, y_bg, color='lightgray', alpha=0.3)
        
        # Achievement arc
        theta_achieve = np.linspace(0, np.pi * (achievement / 100), 100)
        x_achieve = r * np.cos(theta_achieve)
        y_achieve = r * np.sin(theta_achieve)
        ax.fill_between(x_achieve, 0, y_achieve, color=colors['warning'], alpha=0.7)
        
        # Center text
        ax.text(0, 0.3, f'{achievement}%', ha='center', va='center', 
               fontsize=24, fontweight='bold', color=colors['primary'])
        ax.text(0, 0.1, 'of Living Income', ha='center', va='center', 
               fontsize=10, color='gray')
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.2, 1.2)
        ax.axis('off')
        ax.set_title('LI Achievement Rate', fontsize=12, fontweight='bold', pad=10)
    
    def _create_income_breakdown(self, ax, colors):
        """Create pie chart for income sources"""
        sources = ['Cocoa Revenue\n(72%)', 'Other Crops\n(18%)', 
                  'Livestock\n(6%)', 'Off-farm\n(4%)']
        sizes = [72, 18, 6, 4]
        colors_pie = [colors['success'], colors['info'], colors['warning'], colors['primary']]
        
        ax.pie(sizes, labels=sources, autopct='', colors=colors_pie, 
              startangle=90, textprops={'fontsize': 9})
        ax.set_title('Income Sources', fontsize=12, fontweight='bold', pad=10)
    
    def _create_cost_structure(self, ax, colors):
        """Create horizontal bar for cost structure"""
        costs = ['Labor Cost', 'Fertilizer', 'Pesticides', 'Other Inputs']
        amounts = [450000, 200000, 106000, 50000]
        colors_bar = [colors['danger'], colors['warning'], colors['info'], colors['primary']]
        
        y_pos = np.arange(len(costs))
        ax.barh(y_pos, amounts, color=colors_bar, alpha=0.7)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(costs, fontsize=9)
        ax.set_xlabel('Amount (CFA)', fontsize=9, fontweight='bold')
        ax.set_title('Production Cost Structure', fontsize=12, fontweight='bold', pad=10)
        ax.grid(axis='x', alpha=0.3)
    
    def _create_regional_comparison(self, ax, colors):
        """Create regional comparison bar chart"""
        regions = ['Coop A', 'Coop B', 'Coop C', 'Coop D']
        benchmark = [3612000] * 4
        actual = [2950000, 2700000, 3100000, 2600000]
        
        x = np.arange(len(regions))
        width = 0.35
        
        ax.bar(x - width/2, benchmark, width, label='LI Benchmark', 
              color=colors['primary'], alpha=0.7)
        ax.bar(x + width/2, actual, width, label='Actual Income', 
              color=colors['success'], alpha=0.7)
        
        ax.set_ylabel('Income (CFA)', fontsize=9, fontweight='bold')
        ax.set_title('Regional Comparison', fontsize=12, fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(regions, fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=0.3)
    
    def _create_progress_timeline(self, ax, colors):
        """Create timeline showing progress over quarters"""
        quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024']
        avg_income = [2650000, 2700000, 2750000, 2800000, 2820000, 2856000]
        farmers_surveyed = [50, 50, 50, 50, 150, 200]
        
        ax2 = ax.twinx()
        
        # Line for average income
        line1 = ax.plot(quarters, avg_income, marker='o', linewidth=2.5, 
                       color=colors['success'], label='Avg. Income')
        ax.axhline(y=3612000, color=colors['danger'], linestyle='--', 
                  linewidth=2, label='LI Benchmark', alpha=0.7)
        
        # Bars for farmers surveyed
        bars = ax2.bar(quarters, farmers_surveyed, alpha=0.3, 
                      color=colors['info'], label='Farmers Surveyed')
        
        # Labels and formatting
        ax.set_xlabel('Quarter', fontsize=10, fontweight='bold')
        ax.set_ylabel('Average Income (CFA)', fontsize=10, fontweight='bold', color=colors['success'])
        ax2.set_ylabel('Number of Farmers', fontsize=10, fontweight='bold', color=colors['info'])
        ax.set_title('Living Income Progress Over Time', fontsize=12, fontweight='bold', pad=10)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        
        # Combined legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    def create_design_rationale(self):
        """Document dashboard design decisions"""
        print("\n📝 Creating design rationale document...")
        
        rationale = """
================================================================================
LIVING INCOME DASHBOARD - DESIGN RATIONALE
================================================================================

DASHBOARD COMPONENTS:

1. KPI CARDS (Top Row)
   Purpose: Quick overview of key metrics
   Metrics:
   - Average Actual Income (current farmer income)
   - Living Income Benchmark (target)
   - Income Gap (difference and %)
   - % Farmers Below LI (population insight)
   
   Rationale: Executives need instant snapshot of program performance

2. WATERFALL CHART (Middle Left)
   Purpose: Visualize income gap components
   Shows: Benchmark → Revenue sources → Cost deductions → Actual income
   
   Formula: Actual Income = Cocoa Revenue + Other Revenue - Labor Cost - Input Cost
   
   Rationale: Identifies which factors contribute most to income gap

3. GAUGE CHART (Middle Right)
   Purpose: Show overall achievement vs. benchmark
   Displays: % of Living Income Benchmark achieved
   
   Calculation: (Actual Income / LI Benchmark) × 100
   
   Rationale: Visual indicator of progress toward goal

4. INCOME BREAKDOWN (Bottom Left)
   Purpose: Understand revenue diversification
   Shows: % contribution from cocoa vs. other sources
   
   Assumption: 72% cocoa revenue (from baseline study)
   
   Rationale: Helps identify opportunities for income diversification

5. COST STRUCTURE (Bottom Center)
   Purpose: Analyze production cost components
   Shows: Labor, fertilizer, pesticide, other input costs
   
   Rationale: Identifies cost reduction opportunities

6. REGIONAL COMPARISON (Bottom Right)
   Purpose: Compare cooperatives against benchmark
   Shows: Actual income vs. benchmark by cooperative
   
   Rationale: Identifies high/low performing regions for targeted intervention

7. PROGRESS TIMELINE (Bottom Full Width)
   Purpose: Track income improvement over time
   Shows: Quarterly average income trend + # farmers surveyed
   
   Rationale: Demonstrates program impact and data collection scale

================================================================================
DATA REQUIREMENTS:

Primary Data (Must Collect):
✓ Cocoa production volume (kg/farmer)
✓ Cocoa price received (CFA/kg)
✓ Other crop revenue
✓ Labor costs (hired + family labor valuation)
✓ Input costs (fertilizer, pesticides)

Secondary Data (Can Use Estimates Initially):
✓ Living Income Benchmark (3,612,000 CFA - KIT/Anker methodology)
✓ % Cocoa revenue of total income (72% from baseline study)

Calculated Metrics:
✓ Cocoa Revenue = Production (kg) × Price (CFA/kg)
✓ Total Revenue = Cocoa Revenue / 0.72
✓ Total Costs = Labor Costs + Input Costs
✓ Actual Income = Total Revenue - Total Costs
✓ Income Gap = LI Benchmark - Actual Income

================================================================================
IMPLEMENTATION NOTES:

1. Start with simple calculations using averages
2. As data collection scales to 3,000 farmers, add:
   - Drill-down by village/cooperative
   - Farmer-level income distribution histogram
   - Intervention impact tracking
   
3. Update frequency: Quarterly (aligned with harvest cycles)

4. Target audience: 
   - Executives: KPI cards, gauge, timeline
   - Program managers: Waterfall, regional comparison
   - Field teams: Cost structure, income breakdown

================================================================================
"""
        
        output_path = self.results_dir / "design_rationale.txt"
        with open(output_path, 'w') as f:
            f.write(rationale)
        
        print(f"✓ Design rationale saved to {output_path}")
    
    def run_full_design(self):
        """Execute complete Exercise 2"""
        print("=" * 80)
        print("EXERCISE 2: LIVING INCOME DASHBOARD DESIGN")
        print("=" * 80)
        
        self.create_dashboard_mockup()
        self.create_design_rationale()
        
        print("\n" + "=" * 80)
        print("✅ EXERCISE 2 DASHBOARD DESIGN COMPLETE!")
        print("=" * 80)

if __name__ == "__main__":
    designer = LivingIncomeDashboard()
    designer.run_full_design()
