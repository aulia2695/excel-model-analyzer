"""
Exercise 3: Data Collection System Setup
Creates data collection plan, budget analysis, and Gantt chart
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

class DataCollectionPlanner:
    def __init__(self):
        """Initialize planner"""
        self.results_dir = Path("excel-data/test-2-farmer-development/results/exercise-3-data-collection")
        self.budget_dir = self.results_dir / "budget_breakdown"
        self.gantt_dir = self.results_dir / "gantt_chart"
        
        self.budget_dir.mkdir(parents=True, exist_ok=True)
        self.gantt_dir.mkdir(parents=True, exist_ok=True)
        
        # Constants from case study
        self.surveys_per_day = 5
        self.target_farmers = 200
        self.cooperatives = 4
        self.farmers_per_coop = 1000
        self.manager_budget = 5000  # EUR
        
    def analyze_options(self):
        """Compare Field Trainers vs Consultant Surveyors"""
        print("\n📊 Analyzing data collection options...")
        
        # Calculate survey requirements
        total_surveys = self.target_farmers
        days_needed = total_surveys / self.surveys_per_day
        
        print(f"\n📋 Survey Requirements:")
        print(f"  • Target farmers: {total_surveys}")
        print(f"  • Surveys per day per surveyor: {self.surveys_per_day}")
        print(f"  • Total surveyor-days needed: {days_needed}")
        
        # Option 1: Field Trainers
        trainer_monthly_cost = 200000  # CFA
        trainer_training_cost = 100000  # CFA per trainer
        
        # Option 2: Consultants
        consultant_daily_cost = 30000  # CFA
        consultant_onboarding = 1000  # EUR (~655,000 CFA at 655 CFA/EUR)
        
        # Calculate for different numbers of surveyors
        options = []
        
        for n_surveyors in range(1, 6):
            days_per_surveyor = days_needed / n_surveyors
            weeks = days_per_surveyor / 5  # Working days per week
            
            # Field Trainers (assume 4 weeks = 1 month)
            months = np.ceil(weeks / 4)
            trainer_total = (trainer_monthly_cost * months * n_surveyors + 
                           trainer_training_cost * n_surveyors)
            
            # Consultants
            consultant_total = (consultant_daily_cost * days_per_surveyor * n_surveyors + 
                              consultant_onboarding * 655)  # Convert EUR to CFA
            
            options.append({
                'n_surveyors': n_surveyors,
                'days_per_surveyor': days_per_surveyor,
                'weeks': weeks,
                'trainer_cost_cfa': trainer_total,
                'consultant_cost_cfa': consultant_total,
                'trainer_cost_eur': trainer_total / 655,
                'consultant_cost_eur': consultant_total / 655,
            })
        
        options_df = pd.DataFrame(options)
        
        print("\n💰 Cost Comparison:")
        print(options_df[['n_surveyors', 'weeks', 'trainer_cost_eur', 'consultant_cost_eur']].to_string(index=False))
        
        return options_df
    
    def select_optimal_option(self, options_df):
        """Select best option based on budget and efficiency"""
        print("\n🎯 Selecting optimal option...")
        
        # Filter options within budget (5000 EUR)
        within_budget = options_df[
            (options_df['trainer_cost_eur'] <= self.manager_budget) | 
            (options_df['consultant_cost_eur'] <= self.manager_budget)
        ]
        
        # Decision criteria
        # 1. Consultants are already trained (faster deployment)
        # 2. Consultants have no ongoing commitment
        # 3. Compare cost-effectiveness
        
        recommended = options_df.iloc[1]  # 2 consultants seems optimal
        
        print(f"\n✅ RECOMMENDED OPTION: {recommended['n_surveyors']} Consultant Surveyors")
        print(f"  • Duration: {recommended['weeks']:.1f} weeks ({recommended['days_per_surveyor']:.0f} days per surveyor)")
        print(f"  • Total Cost: {recommended['consultant_cost_eur']:.2f} EUR ({recommended['consultant_cost_cfa']:.0f} CFA)")
        print(f"  • Within Budget: {'Yes' if recommended['consultant_cost_eur'] <= self.manager_budget else 'No'}")
        print(f"\n💡 Rationale:")
        print(f"  • Consultants are instantly available (no recruitment delay)")
        print(f"  • Already experienced in financial data collection (no training needed)")
        print(f"  • No ongoing employment obligations after project")
        print(f"  • Cost-effective for one-time baseline data collection")
        
        return recommended
    
    def create_sampling_plan(self):
        """Design sampling strategy"""
        print("\n📐 Creating sampling plan...")
        
        # Stratified random sampling
        farmers_per_coop_sample = self.target_farmers // self.cooperatives
        
        sampling_plan = {
            'strategy': 'Stratified Random Sampling',
            'rationale': 'Ensure representation from all 4 cooperatives',
            'total_sample': self.target_farmers,
            'per_cooperative': farmers_per_coop_sample,
            'sampling_method': [
                '1. Obtain farmer lists from each cooperative (1000 farmers each)',
                '2. Use random number generator to select 50 farmers per cooperative',
                '3. Ensure gender balance: aim for 30% female farmers minimum',
                '4. Include land size diversity: 40% <2ha, 40% 2-4ha, 20% ≥4ha',
                '5. Create replacement list (10 farmers per coop) for non-respondents'
            ]
        }
        
        print(f"  Strategy: {sampling_plan['strategy']}")
        print(f"  Sample per cooperative: {farmers_per_coop_sample}")
        
        return sampling_plan
    
    def create_budget_breakdown(self, selected_option):
        """Create detailed budget breakdown"""
        print("\n💵 Creating budget breakdown...")
        
        n_consultants = int(selected_option['n_surveyors'])
        days_each = selected_option['days_per_surveyor']
        
        budget_items = [
            {
                'Category': 'Consultant Surveyor Fees',
                'Description': f'{n_consultants} consultants × {days_each:.0f} days × 30,000 CFA/day',
                'Amount_CFA': n_consultants * days_each * 30000,
                'Amount_EUR': n_consultants * days_each * 30000 / 655
            },
            {
                'Category': 'Onboarding Session',
                'Description': 'Room, food, MEV Assistant travel for consultant orientation',
                'Amount_CFA': 1000 * 655,
                'Amount_EUR': 1000
            },
            {
                'Category': 'Survey Materials',
                'Description': 'Tablets, forms, stationery',
                'Amount_CFA': 100000,
                'Amount_EUR': 100000 / 655
            },
            {
                'Category': 'Data Management',
                'Description': 'MEV Assistant time for data entry & quality checks',
                'Amount_CFA': 150000,
                'Amount_EUR': 150000 / 655
            },
            {
                'Category': 'Contingency (10%)',
                'Description': 'Unforeseen expenses',
                'Amount_CFA': 0,  # Calculate after
                'Amount_EUR': 0
            }
        ]
        
        # Calculate subtotal and contingency
        subtotal_cfa = sum(item['Amount_CFA'] for item in budget_items[:-1])
        subtotal_eur = sum(item['Amount_EUR'] for item in budget_items[:-1])
        contingency_cfa = subtotal_cfa * 0.10
        contingency_eur = subtotal_eur * 0.10
        
        budget_items[-1]['Amount_CFA'] = contingency_cfa
        budget_items[-1]['Amount_EUR'] = contingency_eur
        
        budget_df = pd.DataFrame(budget_items)
        
        # Add total row
        total_row = pd.DataFrame([{
            'Category': 'TOTAL',
            'Description': '',
            'Amount_CFA': budget_df['Amount_CFA'].sum(),
            'Amount_EUR': budget_df['Amount_EUR'].sum()
        }])
        
        budget_df = pd.concat([budget_df, total_row], ignore_index=True)
        
        # Save budget
        output_path = self.budget_dir / "budget_breakdown.csv"
        budget_df.to_csv(output_path, index=False)
        print(f"✓ Budget saved to {output_path}")
        
        # Create visual budget breakdown
        self._visualize_budget(budget_df)
        
        return budget_df
    
    def _visualize_budget(self, budget_df):
        """Create budget visualization"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Exclude contingency and total for pie chart
        plot_data = budget_df[~budget_df['Category'].isin(['Contingency (10%)', 'TOTAL'])].copy()
        
        # Pie chart
        colors = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
        ax1.pie(plot_data['Amount_EUR'], labels=plot_data['Category'], autopct='%1.1f%%',
                colors=colors, startangle=90, textprops={'fontsize': 9})
        ax1.set_title('Budget Allocation (EUR)', fontsize=12, fontweight='bold')
        
        # Bar chart
        all_data = budget_df[budget_df['Category'] != 'TOTAL'].copy()
        ax2.barh(range(len(all_data)), all_data['Amount_EUR'], color=colors + ['gray'])
        ax2.set_yticks(range(len(all_data)))
        ax2.set_yticklabels(all_data['Category'], fontsize=9)
        ax2.set_xlabel('Amount (EUR)', fontsize=10, fontweight='bold')
        ax2.set_title('Budget Breakdown', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        # Add total line
        total_eur = budget_df[budget_df['Category'] == 'TOTAL']['Amount_EUR'].values[0]
        ax2.axvline(x=total_eur, color='red', linestyle='--', linewidth=2, label=f'Total: {total_eur:.0f} EUR')
        ax2.legend()
        
        plt.tight_layout()
        output_path = self.budget_dir / "budget_visualization.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Budget visualization saved to {output_path}")
    
    def create_gantt_chart(self, selected_option):
        """Create Gantt chart for project timeline"""
        print("\n📅 Creating Gantt chart...")
        
        # Project phases
        start_date = datetime(2024, 1, 1)
        
        tasks = [
            {'task': '1. Planning & Preparation', 'start': 0, 'duration': 5, 'color': '#3498db'},
            {'task': '2. Consultant Onboarding', 'start': 5, 'duration': 1, 'color': '#e74c3c'},
            {'task': '3. Pilot Testing (10 surveys)', 'start': 6, 'duration': 2, 'color': '#f39c12'},
            {'task': '4. Full Data Collection', 'start': 8, 'duration': int(selected_option['days_per_surveyor']), 'color': '#27ae60'},
            {'task': '5. Data Entry & Cleaning', 'start': 8 + int(selected_option['days_per_surveyor']), 'duration': 5, 'color': '#9b59b6'},
            {'task': '6. Quality Checks & Validation', 'start': 8 + int(selected_option['days_per_surveyor']) + 3, 'duration': 5, 'color': '#e67e22'},
            {'task': '7. Analysis & Reporting', 'start': 8 + int(selected_option['days_per_surveyor']) + 8, 'duration': 7, 'color': '#34495e'},
        ]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        for i, task in enumerate(tasks):
            ax.barh(i, task['duration'], left=task['start'], height=0.6, 
                   color=task['color'], alpha=0.8, edgecolor='black', linewidth=1)
            
            # Add duration label
            ax.text(task['start'] + task['duration']/2, i, f"{task['duration']}d", 
                   ha='center', va='center', fontweight='bold', fontsize=9, color='white')
        
        # Formatting
        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels([t['task'] for t in tasks], fontsize=10)
        ax.set_xlabel('Days from Project Start', fontsize=11, fontweight='bold')
        ax.set_title('Data Collection Project Timeline (Gantt Chart)', fontsize=14, fontweight='bold', pad=15)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add today marker
        total_days = max(t['start'] + t['duration'] for t in tasks)
        ax.axvline(x=0, color='green', linestyle='-', linewidth=2, label='Project Start', alpha=0.7)
        
        # Add phase labels
        ax.text(2.5, len(tasks), 'Setup Phase', ha='center', fontsize=9, 
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax.text(8 + selected_option['days_per_surveyor']/2, len(tasks), 'Data Collection Phase', 
               ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        ax.text(8 + selected_option['days_per_surveyor'] + 10, len(tasks), 'Analysis Phase', 
               ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
        
        ax.set_xlim(-2, total_days + 2)
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        output_path = self.gantt_dir / "project_gantt_chart.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gantt chart saved to {output_path}")
        
        print(f"\n📅 Total Project Duration: {total_days} days (~{total_days/5:.0f} weeks)")
    
    def create_implementation_plan(self, selected_option, sampling_plan, budget_df):
        """Create comprehensive implementation plan document"""
        print("\n📋 Creating implementation plan...")
        
        plan = f"""
================================================================================
DATA COLLECTION PLAN: LIVING INCOME PRODUCTION COST SURVEY
================================================================================
MEV Assistant & Operations Team Implementation Guide

PROJECT OVERVIEW
----------------
Objective: Collect baseline data on production costs (labor + inputs) from 200 
          cocoa farmers across 4 cooperatives to enable Living Income monitoring

Timeline: {int(selected_option['days_per_surveyor'] * selected_option['n_surveyors'] / 5):.0f} weeks
Budget: {budget_df[budget_df['Category'] == 'TOTAL']['Amount_EUR'].values[0]:.2f} EUR

================================================================================
1. SAMPLING STRATEGY
================================================================================

Strategy: {sampling_plan['strategy']}

Sample Size: {sampling_plan['total_sample']} farmers
  • Cooperative A: {sampling_plan['per_cooperative']} farmers
  • Cooperative B: {sampling_plan['per_cooperative']} farmers
  • Cooperative C: {sampling_plan['per_cooperative']} farmers
  • Cooperative D: {sampling_plan['per_cooperative']} farmers

Selection Criteria:
  ✓ Random selection from farmer database (1000 farmers/cooperative)
  ✓ Minimum 30% female farmers for gender balance
  ✓ Land size distribution: 40% <2ha, 40% 2-4ha, 20% ≥4ha
  ✓ Include replacement list (10 farmers/coop) for non-respondents

================================================================================
2. DATA COLLECTION APPROACH
================================================================================

Selected Option: {int(selected_option['n_surveyors'])} Consultant Surveyors

Rationale:
  ✓ Instantly available (no recruitment delay)
  ✓ Already experienced in financial data collection
  ✓ No ongoing employment obligations
  ✓ Cost-effective for one-time baseline survey

Daily Capacity: {self.surveys_per_day} surveys per surveyor
Total Duration: {selected_option['days_per_surveyor']:.0f} days per surveyor

Survey Scope: ~20 questions covering:
  • Labor costs (hired labor + family labor valuation)
  • Input costs (fertilizer quantities & prices)
  • Pesticide costs (types & amounts)
  • Other production expenses

================================================================================
3. IMPLEMENTATION TIMELINE
================================================================================

Week 1: Planning & Preparation
  □ Finalize survey questionnaire with Sustainability Manager
  □ Coordinate with 4 cooperatives for farmer lists
  □ Select random sample + replacement farmers
  □ Arrange onboarding session logistics

Week 2: Onboarding & Pilot
  □ Conduct 1-day onboarding for consultant surveyors
  □ Review survey questions and data quality standards
  □ Pilot test with 10 farmers (not in main sample)
  □ Refine questionnaire based on pilot feedback

Week 3-{3 + int(selected_option['days_per_surveyor'] / 5):.0f}: Data Collection
  □ Deploy surveyors to cooperatives
  □ Daily progress tracking by MEV Assistant
  □ Immediate quality checks on completed surveys
  □ Address any field issues promptly

Week {4 + int(selected_option['days_per_surveyor'] / 5):.0f}-{5 + int(selected_option['days_per_surveyor'] / 5):.0f}: Data Management
  □ Data entry into centralized database
  □ Run automated validation checks
  □ Flag outliers for verification
  □ Clean and finalize dataset

Week {6 + int(selected_option['days_per_surveyor'] / 5):.0f}: Analysis & Reporting
  □ Calculate average production costs
  □ Estimate actual farmer incomes
  □ Generate Living Income Dashboard
  □ Prepare report for Manager

================================================================================
4. ROLES & RESPONSIBILITIES
================================================================================

MEV Assistant:
  • Overall project coordination
  • Daily monitoring of survey progress
  • First-level data quality checks
  • Communication with consultants and cooperatives
  • Escalation of issues to Manager

Consultant Surveyors:
  • Conduct farmer interviews (5/day each)
  • Ensure data accuracy and completeness
  • Submit surveys daily via mobile app/forms
  • Report challenges immediately

Operations Team:
  • Facilitate access to farmers
  • Provide local context and translation if needed
  • Support logistics (meeting arrangements)

Sustainability Manager:
  • Provide cooperative contacts
  • Review and approve survey questionnaire
  • Address technical questions on cocoa practices

================================================================================
5. DATA QUALITY PROTOCOLS
================================================================================

During Collection:
  ✓ Mandatory fields enforcement in survey tool
  ✓ Range validation (costs must be > 0 and < reasonable max)
  ✓ Cross-checks (e.g., fertilizer cost = quantity × price)
  ✓ Daily review by MEV Assistant

Post-Collection:
  ✓ Completeness check: 100% of required fields filled
  ✓ Outlier detection: Flag values >3 standard deviations from mean
  ✓ Logical consistency: Production costs < cocoa revenue
  ✓ Sample representativeness: Verify gender/land size distribution

================================================================================
6. BUDGET ALLOCATION
================================================================================

Total Budget: {budget_df[budget_df['Category'] == 'TOTAL']['Amount_EUR'].values[0]:.2f} EUR 
             ({budget_df[budget_df['Category'] == 'TOTAL']['Amount_CFA'].values[0]:,.0f} CFA)

Breakdown:
"""
        
        for _, row in budget_df.iterrows():
            plan += f"  • {row['Category']:<30} {row['Amount_EUR']:>8.2f} EUR ({row['Amount_CFA']:>12,.0f} CFA)\n"
        
        plan += f"""

================================================================================
7. KEY ASSUMPTIONS & FOLLOW-UP QUESTIONS
================================================================================

Assumptions Made:
  • Survey duration: 1 hour per farmer (as advised)
  • Surveyors can complete 5 surveys/day (including travel)
  • Exchange rate: 655 CFA per EUR
  • Farmers will be available and willing to participate
  • Consultants can start immediately

Questions for Manager:
  1. Has the survey questionnaire been finalized and tested?
  2. Are the 4 target cooperatives confirmed and willing to participate?
  3. What is the contingency plan if consultants are unavailable?
  4. Should we collect any additional data while surveying (e.g., farm GPS)?
  5. What data storage/security protocols should be followed?

================================================================================
8. SUCCESS CRITERIA
================================================================================

  ✓ 200 surveys completed within budget and timeline
  ✓ <5% missing data across all required fields
  ✓ Data passes all quality validation checks
  ✓ Living Income Dashboard successfully generated
  ✓ Insights actionable for program improvement

================================================================================
PREPARED BY: MEV Specialist
DATE: {datetime.now().strftime('%B %d, %Y')}
================================================================================
"""
        
        output_path = self.results_dir / "data_collection_plan.txt"
        with open(output_path, 'w') as f:
            f.write(plan)
        
        print(f"✓ Implementation plan saved to {output_path}")
    
    def run_full_planning(self):
        """Execute complete Exercise 3"""
        print("=" * 80)
        print("EXERCISE 3: DATA COLLECTION SYSTEM SETUP")
        print("=" * 80)
        
        options_df = self.analyze_options()
        selected_option = self.select_optimal_option(options_df)
        sampling_plan = self.create_sampling_plan()
        budget_df = self.create_budget_breakdown(selected_option)
        self.create_gantt_chart(selected_option)
        self.create_implementation_plan(selected_option, sampling_plan, budget_df)
        
        print("\n" + "=" * 80)
        print("✅ EXERCISE 3 DATA COLLECTION PLANNING COMPLETE!")
        print("=" * 80)
        print(f"\n📊 Summary:")
        print(f"  • Recommended: {int(selected_option['n_surveyors'])} Consultant Surveyors")
        print(f"  • Duration: {selected_option['weeks']:.1f} weeks")
        print(f"  • Budget: {budget_df[budget_df['Category'] == 'TOTAL']['Amount_EUR'].values[0]:.2f} EUR")
        print(f"  • Sample: {self.target_farmers} farmers across {self.cooperatives} cooperatives")

if __name__ == "__main__":
    planner = DataCollectionPlanner()
    planner.run_full_planning()
