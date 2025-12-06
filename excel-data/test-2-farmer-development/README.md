This folder contains Excel files for analysis.

# Test 2: Farmer Development Plan Analysis (Ivory Coast)

## Project Overview
Analysis of the "Farm Development Plan" database containing farmer demographics and cocoa agronomic practices in Ivory Coast. This project aims to establish a baseline and develop a Living Income monitoring system.

## Background
- **Country**: Ivory Coast
- **Project**: Farm Development Plan (implemented last year)
- **Current Sample**: Initial dataset from local Operations Team
- **Scale**: Planning to survey 3,000 more farmers in next 6 months

## Folder Structure
```
test-2-farmer-development/
├── raw/                 # Original survey data
├── cleaned/             # Processed datasets
├── scripts/             # Analysis and calculation scripts
├── results/             # Reports, dashboards, visualizations
└── conditions/          # Project requirements and methodology
    └── requirements.md
```

## Main Objectives

### Exercise 1: Baseline Analysis
Create a 2-pager report for chocolate maker clients covering:

**1. Adoption & Competence Baseline**
- 14 Adoption variables analysis
- Distribution: Good, Medium, Bad farmers
- "Result" (current adoption) vs "Competence" (skillset)

**2. Progress Tracking**
- % farmers making progress
- % staying at same level
- % deteriorating (1st to 2nd survey)

**3. Production Analysis (Yield)**
Segmented by:
- Gender (male/female farmers)
- Land size: <2ha, 2-4ha, ≥4ha

### Exercise 2: Living Income Dashboard
Design visualization dashboard showing:
- Living income benchmark
- Actual farmer incomes
- Income gaps
- Key drivers and trends

### Exercise 3: Data Collection System
Set up production cost data collection at sample scale:
- 200 farmers from 4 cooperatives (1,000 farmers each)
- Survey on labor costs and input costs
- Budget: ~5,000 EUR

## Key Metrics

### Living Income Components
```
Actual Income = (Cocoa Volume × Price) ÷ 0.72
Price = 1,000 CFA/kg + 40 CFA/kg (premium)
Cocoa Revenue = 72% of total farmer revenue
Production Cost = Labor Cost + Input Cost
```

### Income Gap Calculation
```
Living Income Gap = Benchmark - Actual Income
```

## Data Collection Options

### Option A: Field Trainers
- Cost: 200,000 CFA/month
- Training: 100,000 CFA per trainer
- Multi-tasking (surveys + farmer training)

### Option B: Consultant Surveyors
- Cost: 30,000 CFA/day
- Onboarding: ~1,000 EUR
- Experienced in financial data collection

## Analysis Checklist

### Baseline Report
- [ ] Analyze 14 adoption variables
- [ ] Calculate farmer distribution (Good/Medium/Bad)
- [ ] Track progress from 1st to 2nd survey
- [ ] Segment yield by gender and land size
- [ ] Provide data quality recommendations

### Living Income System
- [ ] Design dashboard mockup
- [ ] Define data collection methodology
- [ ] Create budget proposal
- [ ] Develop implementation plan (Gantt/Org chart)
- [ ] Set up quality control procedures

## Deliverables
- ⬜ 2-pager baseline report
- ⬜ Living Income Dashboard design
- ⬜ Data collection plan (max ½ page)
- ⬜ Budget breakdown
- ⬜ Implementation timeline
- ⬜ Data quality recommendations

## Sample Statistics
- **Cooperatives**: 4 regions
- **Total farmers per coop**: 1,000
- **Sample size**: 200 farmers
- **Survey duration**: 1 hour/farmer
- **Max surveys/day**: 5 (including travel)

## Tools & Technologies
- **Data Analysis**: Excel, Python, R
- **Visualization**: Power BI, Tableau, Excel charts
- **Budget Planning**: Excel, Google Sheets
- **Project Management**: Gantt charts, org diagrams

## References
- DISCO Living Income Framework
- Anker & Anker Methodology
- KIT Demystifying Study
- See `conditions/requirements.md` for full details

## Notes
Focus on decision-making process and assumptions rather than finding "perfect" answers. Document all choices and rationale.
