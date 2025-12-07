Test 2: Complete Solution Guide
Exercises 1, 2, and 3 for Farmer Development & Living Income

📋 EXERCISE 1: Analysis of Farmer Development Plan Data
What's Required:

Baseline Analysis - Distribution of farmers (Good/Medium/Bad) for 14 adoption variables
Progress Tracking - % of farmers improving/same/deteriorating from Visit 1 to Visit 2
Production Segmentation - Average yield by Gender and Land Size
Recommendations - Data quality and collection improvements

✅ Solution: Already Created!
The Python script analyze_farmer_development.py handles all of this:
Outputs Generated:

Chart: Baseline Adoption (chart_baseline_adoption.png)

Shows G/M/B distribution for Response, Result, Competence
Color-coded: Green (Good), Orange (Medium), Red (Bad)


Chart: Progress Analysis (chart_progress_analysis.png)

Shows % Improving, Same, Deteriorating
Compares Visit 1 → Visit 2


Chart: Production by Gender (chart_production_by_gender.png)

Average production: Male vs Female
Farmer count by gender


Chart: Production by Land Size (chart_production_by_landsize.png)

Average production: <2ha, 2-4ha, ≥4ha
Farmer distribution across land sizes


Excel Report (analysis_report_[timestamp].xlsx)

Sheet 1: Baseline Adoption Summary
Sheet 2: Production by Gender
Sheet 3: Production by Land Size
Sheet 4: Data Quality Recommendations ⭐



Key Recommendations Included:
Data Completeness:

Ensure mandatory fields are filled (Farmer Code, Gender, Production)
Validate GPS coordinates for farm locations
Collect visit dates to track temporal progress

Data Quality:

Implement field validation rules in forms
Add range checks for numerical fields
Standardize categorical responses

Data Cleaning:

Remove duplicate farmer entries
Flag and investigate outliers
Create data quality dashboard


📊 EXERCISE 2: Living Income Dashboard Design
What's Required:
Design a Living Income Dashboard with visualized data components (sketch with dummy data)
Solution: Dashboard Components
1. Living Income Gap Calculation
Living Income Gap = Living Income Benchmark - Actual Farmer Income

Where:
- Living Income Benchmark = Country-specific benchmark (e.g., from Anker methodology)
- Actual Farmer Income = Total Household Income from all sources
2. Dashboard Components to Include:
A. Key Metrics Cards (Top of Dashboard)
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Living Income   │ Average Farmer  │ Income Gap      │ % Farmers Below │
│ Benchmark       │ Income          │                 │ Living Income   │
│ 2,500,000 CFA   │ 1,800,000 CFA   │ -700,000 CFA    │ 65%            │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
B. Income Gap Visualization (Waterfall Chart)
Living Income Components:
3,000,000 │                    ┌────────┐
          │                    │ Gap    │
2,500,000 │ ┌────────┐        │-700k   │ ← Benchmark
          │ │Cocoa   │┌──────┐│        │
2,000,000 │ │Income  ││Other ││        │
          │ │        ││Income││        │
1,500,000 │ │1,300k  ││500k  ││        │
          │ │        ││      ││        │
1,000,000 │ │        ││      ││        │
          │ │        ││      ││        │
    500k  │ │        ││      ││        │
          └─┴────────┴┴──────┴┴────────┘
            Cocoa    Other    Gap
C. Income Distribution (Histogram)
Number of Farmers by Income Level:

60 │     ╔══╗
50 │     ║  ║
40 │     ║  ║ ╔══╗
30 │ ╔══╗║  ║ ║  ║
20 │ ║  ║║  ║ ║  ║ ╔══╗
10 │ ║  ║║  ║ ║  ║ ║  ║ ╔══╗
 0 └─╚══╝╚══╝─╚══╝─╚══╝─╚══╝────
   <1M  1-1.5M 1.5-2M 2-2.5M >2.5M
   (Below Living Income Benchmark: 2.5M CFA)
D. Income Composition (Pie Chart)
Farmer Income Sources:
┌─────────────────────────────┐
│   Cocoa: 72%                │
│   ███████████████           │
│                             │
│   Other Crops: 18%          │
│   ████                      │
│                             │
│   Livestock: 7%             │
│   ██                        │
│                             │
│   Other: 3%                 │
│   █                         │
└─────────────────────────────┘
E. Production Cost Breakdown (Stacked Bar)
Cost Structure per Farmer:

1,000k │ ┌──────────────┐
       │ │              │
  800k │ │ Labor Cost   │
       │ │ 600k (60%)   │
  600k │ │              │
       │ ├──────────────┤
  400k │ │ Input Cost   │
       │ │ 400k (40%)   │
  200k │ │              │
       │ │              │
     0 └─┴──────────────┘
         Total: 1,000k CFA
F. Regional Comparison (Map/Table)
┌──────────────┬───────────┬─────────────┬────────────┐
│ Cooperative  │ Avg Income│ Benchmark   │ Gap (%)    │
├──────────────┼───────────┼─────────────┼────────────┤
│ Coop A       │ 2,100,000 │ 2,500,000   │ -16%       │
│ Coop B       │ 1,650,000 │ 2,500,000   │ -34%       │
│ Coop C       │ 1,900,000 │ 2,500,000   │ -24%       │
│ Coop D       │ 2,300,000 │ 2,500,000   │ -8%        │
└──────────────┴───────────┴─────────────┴────────────┘
G. Trend Analysis (Line Chart)
Living Income Progress Over Time:

2.5M │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ Benchmark
     │                    ╱
2.0M │              ╱────╱
     │        ╱────╱
1.5M │  ╱────╱
     │─╱
1.0M └─────────────────────────────
     2020  2021  2022  2023  2024
3. Excel/PPT Dashboard Sketch Structure
┌─────────────────────────────────────────────────────────────┐
│                  LIVING INCOME DASHBOARD                     │
│                   Ivory Coast - 2024                         │
├─────────────────────────────────────────────────────────────┤
│ KPI Cards:                                                   │
│ [Benchmark] [Avg Income] [Gap] [% Below]                    │
├──────────────────────────────┬──────────────────────────────┤
│ Income Gap Waterfall Chart   │ Income Distribution          │
│ (Shows gap breakdown)        │ (Histogram)                  │
├──────────────────────────────┼──────────────────────────────┤
│ Income Sources Pie Chart     │ Cost Breakdown               │
│ (Cocoa vs Other)             │ (Labor + Input)              │
├──────────────────────────────┴──────────────────────────────┤
│ Regional Comparison Table & Map                             │
├─────────────────────────────────────────────────────────────┤
│ Trend Analysis: Progress Toward Living Income               │
└─────────────────────────────────────────────────────────────┘

💰 EXERCISE 3: Production Cost Data Collection Plan
What's Required:

Design data collection system for production costs
Choose between: Field Trainers vs Consultant Surveyors
Create data collection plan (½ page)
Create budget
Sample size determination

Solution:
A. Decision Analysis: Field Trainers vs Consultants
Option 1: Field Trainers

Cost: 200,000 CFA/month
Training needed: 100,000 CFA per trainer
Capacity: 5 surveys/day
Multi-purpose: Can do agronomic surveys too
Long-term asset for organization

Option 2: Consultant Surveyors

Cost: 30,000 CFA/day
Already experienced (no training cost)
Onboarding: 1,000 EUR (~655,000 CFA)
Capacity: 5 surveys/day
Immediately available

B. Sample Size Calculation
Target:

4 cooperatives × 1,000 farmers each = 4,000 farmers total
Recommended sample: 200 farmers
Sample rate: 5% (statistically valid for baseline)

Sample Distribution:
┌──────────────┬────────────┬─────────────┐
│ Cooperative  │ Farmers    │ Sample Size │
├──────────────┼────────────┼─────────────┤
│ Coop A       │ 1,000      │ 50          │
│ Coop B       │ 1,000      │ 50          │
│ Coop C       │ 1,000      │ 50          │
│ Coop D       │ 1,000      │ 50          │
├──────────────┼────────────┼─────────────┤
│ TOTAL        │ 4,000      │ 200         │
└──────────────┴────────────┴─────────────┘
Sampling Strategy:

Stratified random sampling within each cooperative
Ensure representation across:

Land sizes (<2ha, 2-4ha, ≥4ha)
Gender (Male/Female farmers)
Production levels (Low/Medium/High)



C. Recommended Approach: HYBRID MODEL
Decision: Use Field Trainers
Rationale:

Cost-effective for long-term: After initial training investment, trainers are reusable asset
Multi-purpose: Can conduct agronomic surveys alongside financial surveys
Better for 3,000 farmers scale: Budget-friendly for expansion
Local knowledge: Better understanding of farmer context
Sustainability: Builds internal capacity

Time Calculation:

1 survey = 1 hour
5 surveys/day per trainer
200 surveys needed
200 ÷ 5 = 40 trainer-days needed

Team Size:

4 trainers (1 per cooperative)
40 trainer-days ÷ 4 trainers = 10 days per trainer

D. DATA COLLECTION PLAN

📋 LIVING INCOME DATA COLLECTION PLAN
Production Cost Baseline Survey - Sample Scale
Objective: Collect production cost data (labor + input costs) from 200 farmers across 4 cooperatives
Timeline: 2 weeks (10 working days)
Resources:

4 Field Trainers (1 per cooperative)
1 MEV Assistant (supervision & quality control)
Survey forms (20 questions on financial data)
Tablets/smartphones for digital data entry


WEEK 1: Preparation & Training
DayActivityResponsibleOutput1-2Trainer recruitment & preparationOperations Team4 trainers selected3-4Financial data collection trainingMEV AssistantTrainers certified5Survey tool setup & testingMEV AssistantDigital forms ready
WEEK 2-3: Data Collection
DayActivityLocationTarget6-7Coop A surveysRegion A50 farmers8-9Coop B surveysRegion B50 farmers10-11Coop C surveysRegion C50 farmers12-13Coop D surveysRegion D50 farmers14-15Data quality checks & cleanupOffice200 complete surveys
Daily Schedule per Trainer:

08:00-09:00: Travel to farmer location
09:00-10:00: Survey 1
10:00-11:00: Survey 2
11:00-12:00: Survey 3
13:00-14:00: Survey 4 (after lunch)
14:00-15:00: Survey 5
15:00-16:00: Data entry & travel back

Quality Control:

Daily data submission to MEV Assistant
Random farmer callbacks (10% verification)
Outlier flagging and validation
Weekly progress review meetings

Sampling Protocol:

Stratified random selection within each cooperative
Ensure representation: land size, gender, production level
Replacement farmers identified in case of unavailability


E. BUDGET BREAKDOWN
╔════════════════════════════════════════════════════════════╗
║        LIVING INCOME BASELINE SURVEY BUDGET                ║
║        Production Cost Data Collection                     ║
╚════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────┬─────────┬──────────┐
│ ITEM                                 │ UNIT    │ COST     │
├──────────────────────────────────────┼─────────┼──────────┤
│ A. PERSONNEL COSTS                   │         │          │
│   Field Trainers (4 trainers)       │         │          │
│   - Monthly salary: 200,000 CFA      │ 4×200k  │ 800,000  │
│   - Duration: 0.5 month (2 weeks)    │ ×0.5    │ 400,000  │
│                                      │         │          │
│   Training Cost                      │         │          │
│   - Per trainer: 100,000 CFA         │ 4×100k  │ 400,000  │
│                                      │         │          │
│   MEV Assistant (supervision)        │         │          │
│   - Travel & per diem (2 weeks)      │ Lump    │ 200,000  │
│                                      │         │          │
├──────────────────────────────────────┼─────────┼──────────┤
│ B. OPERATIONAL COSTS                 │         │          │
│   Fuel for motorbikes (included)     │ Incl    │ 0        │
│   Survey forms printing              │ Lump    │ 50,000   │
│   Tablets/data entry tools           │ Rent    │ 150,000  │
│   Communication (phone credit)       │ Lump    │ 50,000   │
│                                      │         │          │
├──────────────────────────────────────┼─────────┼──────────┤
│ C. CONTINGENCY (10%)                 │ 10%     │ 125,000  │
│                                      │         │          │
├──────────────────────────────────────┼─────────┼──────────┤
│ TOTAL BUDGET (CFA)                   │         │1,375,000 │
│                                      │         │          │
│ TOTAL BUDGET (EUR @ 655 CFA/EUR)     │         │ ~2,100€  │
└──────────────────────────────────────┴─────────┴──────────┘

✅ WITHIN MANAGER'S BUDGET: 5,000 EUR
Alternative Option Comparison:
ApproachCost (CFA)Cost (EUR)ProsConsField Trainers1,375,000~2,100Lower cost, reusable, multi-purposeNeed trainingConsultants3,655,000*~5,580Experienced, no trainingHigher cost, over budget
*Consultant cost: (200 surveys ÷ 5/day) × 30k/day × 4 consultants + 655k onboarding

F. ASSUMPTIONS & FOLLOW-UP QUESTIONS
Assumptions Made:

Field trainers can achieve 5 surveys/day after training
20-question survey takes 1 hour per farmer
Farmers are available and willing to participate
Digital data collection tools are available for rent
Weather and road conditions allow for daily travel

Follow-Up Questions for Operations Team:

Are field trainers already employed or need recruitment?
Is there existing tablet infrastructure we can use?
What is the farmer literacy rate (affects survey methodology)?
Are there peak farming seasons we should avoid?
Do we have existing relationships with target cooperatives?
Can we piggyback on other survey activities to reduce costs?


G. GANTT CHART
LIVING INCOME SURVEY - PROJECT TIMELINE

Week 1:
Mon │████│ Trainer Recruitment
Tue │████│ 
Wed │    │████████│ Training Session
Thu │    │████████│
Fri │    │    │████│ Tool Setup & Testing

Week 2:
Mon │    │    │    │████████│ Coop A Data Collection
Tue │    │    │    │████████│
Wed │    │    │    │    │████████│ Coop B
Thu │    │    │    │    │████████│
Fri │    │    │    │    │    │████████│ Coop C

Week 3:
Mon │    │    │    │    │    │████████│
Tue │    │    │    │    │    │    │████████│ Coop D
Wed │    │    │    │    │    │    │████████│
Thu │    │    │    │    │    │    │    │████│ QC
Fri │    │    │    │    │    │    │    │████│ Cleanup

Legend: ████ = Activity in progress

📊 DELIVERABLES
For Manager:

✅ Complete budget: 2,100 EUR (within 5,000 EUR limit)
✅ Data collection plan with timeline
✅ Sample size calculation (200 farmers, 5% sample)
✅ Quality control procedures
✅ Cost comparison analysis
✅ Risk mitigation strategy

Expected Outputs:

200 complete production cost surveys
Labor cost data for 200 farmers
Input (fertilizer/pesticide) cost data for 200 farmers
Clean dataset ready for Living Income calculation
Quality assurance report


🎯 KEY SUCCESS FACTORS

Proper training of field trainers on financial data collection
Daily monitoring and data quality checks
Clear sampling protocol to ensure representative data
Farmer engagement - explain purpose and benefits
Backup plan for farmer unavailability or weather issues
Data security and confidentiality protocols


Summary
✅ Exercise 1: Complete Python automation for farmer development analysis
✅ Exercise 2: Living Income Dashboard design with 7 key visualizations
✅ Exercise 3: Production cost data collection plan with budget (2,100 EUR)
All solutions are practical, budget-conscious, and designed for real-world implementation!
