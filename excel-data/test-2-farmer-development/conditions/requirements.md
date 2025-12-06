# Test 2: Farmer Development Plan Analysis - Conditions

## Background
Analysis of "Farm Development Plan" project database from Ivory Coast.

## Dataset Information
- **Country**: Ivory Coast
- **Sample**: Initial dataset from local Operations Team
- **Future Scale**: 3,000 more farmers in next 6 months
- **Focus**: Farmer demographics and cocoa agronomic practices

## Exercise 1: Analysis Requirements

### Baseline Analysis
1. **Adoption Variables (14 variables)**
   - "Result" (current adoption)
   - "Competence" (skillset)
   - Distribution: Good, Medium, Bad

2. **Progress Tracking**
   - % farmers making progress
   - % staying at same level
   - % deteriorating (1st to 2nd survey)

3. **Production (Yield) Segmentation**
   - By Gender
   - By Land size: <2ha, 2-4ha, ≥4ha

### Recommendations Required
Provide 2-3 most important recommendations on:
- Data completeness/quality during collection
- Data cleaning/quality checks by M&E Assistant and Operations Team

## Exercise 2: Living Income Dashboard

### Requirements
- Draft design of "Living Income Dashboard"
- Visualized data components
- Type of charts with dummy data/formulas
- Can use PPT/Excel (no sophisticated tools needed)

### Data Components
- Cocoa volume per farmer
- Price: 1000 CFA/kg + 40 CFA/kg premium
- Cocoa revenue: 72% of total revenue (baseline study)
- Production costs (labor + inputs)

## Exercise 3: Data Collection Plan

### Scope
- 4 cooperatives (1,000 farmers each)
- Sample: 200 farmers total
- Budget: ~5,000 EUR

### Survey Details
- 20 questions on production costs
- 1 hour per farmer
- Maximum 5 surveys/day (including travel)

### Options for Implementation

#### Option A: Dedicated Field Trainers
- Cost: 200,000 CFA/month
- Includes motorbike and fuel
- Training cost: 100,000 CFA per trainer
- Also perform other tasks (agronomic surveys, farmer training)

#### Option B: Consultant Surveyors
- Cost: 30,000 CFA/day
- Includes motorbike and fuel
- Onboarding: ~1,000 EUR (room, food, travel)
- Already experienced in financial data collection
- Instantly available

### Deliverables
1. Data collection plan (max ½ page)
2. Budget proposal
3. Gantt chart or Org chart
4. Clear instructions for M&E Assistant and Operations Team

## Living Income Calculation Framework

### Steps (DISCO Methodology)
1. Define cocoa sourcing countries/regions
2. Identify living income benchmark (Anker & Anker, LICOP, KIT)
3. Identify average actual farmer incomes
4. Calculate gap: Benchmark - Actual Income

### Formula
```
Living Income Gap = Living Income Benchmark - Average Actual Farmer Income

Where:
- Actual Income = (Cocoa volume × Price) / 0.72
- Price = Base price + Premium
- Production Cost = Labor cost + Input cost
```
