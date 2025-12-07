This folder contains Excel files for analysis.

# Test 1: Cocoa Adoption Analysis (Ecuador)

## Project Overview
Analysis of cocoa farming practices and adoption patterns across different farms in Ecuador to improve sustainable cocoa production.

## Objective
Clean, analyze, and present data to gain insights into cocoa adoption patterns. Results will inform decision-making and develop strategies to promote cocoa adoption among farmers.

## Dataset Information
- **Country**: Ecuador
- **Focus**: Agricultural techniques and farming practices
- **Key Variables**: 
  - Farm characteristics (size, location)
  - Farmer demographics (age, gender, experience)
  - Agricultural practices (fertilizer use, pest management, pruning, etc.)
  - Regional and weather factors

## Folder Structure
```
test-1-cocoa-adoption/
├── raw/                 # Original Excel datasets
├── cleaned/             # Processed datasets after cleaning
├── scripts/             # Analysis code (Python/R/Excel)
├── results/             # Visualizations and reports
└── conditions/          # Analysis requirements and criteria
    └── requirements.md
```

## Analysis Overview

This analysis automatically evaluates cocoa farming practices and calculates adoption levels for farmers based on 14 key agricultural practices. The system processes Excel data and generates comprehensive reports with visualizations.

## Purpose

**Main Objectives:**
- Assess farmer adoption of best cocoa farming practices
- Identify areas needing improvement
- Provide data-driven recommendations for agricultural extension programs
- Track regional and farm-size patterns in adoption

## Data Structure

### Required Excel Columns

Excel file (`test_1_cocoa_adoption_raw.xlsx`) must contain these columns:

| Column Name |     Type    |        Description       |
|-------------|-------------|--------------------------|
| `farmer_id` | Text/Number | Unique farmer identifier |
| `first_name`| Text        | Farmer's first name      |
| `last_name` | Text        | Farmer's last name       |
| `Farm size` | Number      | Farm size in hectares    |
| `Region`    | Text        | Geographic region        |
| `gender`    | Text        | Farmer's gender          |
| `season`    | Text        | Planting/harvest season  |

### Practice Columns (Used for Scoring)

These 14 columns are evaluated to calculate adoption levels:

1. `Planting Material` - Quality of planting materials used
2. `Weeding` - Weed management practices
3. `Tree age` - Age distribution of cocoa trees
4. `Tree density` - Optimal spacing and density
5. `Tree health` - Overall tree health status
6. `Debilitating disease` - Disease management
7. `Pruning` - Pruning practices
8. `Pest disease sanitation` - Pest and disease control
9. `Harvesting` - Harvesting techniques
10. `Shade management` - Shade tree management
11. `Soil condition` - Soil quality and management
12. `Organic matter` - Organic matter application
13. `Fertilizer formulation` - Type of fertilizer used
14. `Fertilizer application` - Fertilizer application methods

## Adoption Scoring System

### How Practices are Scored

Each practice column is evaluated and scored:

- **Score 2 (Good)**: Keywords like "yes", "good", "high", "optimal", "healthy", "adequate", "proper", "regular", "improved"
- **Score 1 (Medium)**: Keywords like "moderate", "medium", "fair", "average", "some", "occasional", "standard"
- **Score 0 (Bad)**: Keywords like "no", "poor", "low", "none", "inadequate", "bad", "unhealthy", "traditional"

### Adoption Level Calculation

1. **Total Score** = Sum of all 14 practice scores (0-28 possible)
2. **Adoption Percentage** = (Total Score / 28) × 100
3. **Adoption Level** categorized as:
   - **Good**: ≥66.7% (scoring well on most practices)
   - **Medium**: 33.3% - 66.6% (mixed performance)
   - **Bad**: <33.3% (needs significant improvement)

### Numeric Values

For analysis purposes:
- Good = 2
- Medium = 1
- Bad = 0

## Automated Analysis

### What Gets Analyzed

1. **Data Cleaning**
   - Missing value detection and handling
   - Duplicate removal
   - Outlier identification (Farm size)

2. **Adoption Analysis**
   - Overall adoption distribution
   - Farm size vs adoption relationship
   - Regional adoption patterns
   - Individual practice performance

3. **Visualizations** (8 charts generated)
   - Adoption distribution (pie & bar charts)
   - Farm size analysis (box plot & scatter plot)
   - Regional breakdowns (stacked bar chart)
   - Practice correlations (heatmap)
   - Practice performance ranking
   - Score distribution histogram

4. **Comprehensive Report**
   - Executive summary
   - Key findings
   - Actionable recommendations
   - Next steps

## File Structure

```
test-1-cocoa-adoption/
├── raw/
│   └── test_1_cocoa_adoption_raw.xlsx           # Input data
├── scripts/
│   └── test1_analysis.py                        # Analysis script
├── cleaned/                                     # Auto-generated cleaned data
│   └── cleaned_data.csv                         # Cleaned dataset
└── results/                                     # Auto-generated results
    ├── COMPREHENSIVE_REPORT.txt                 # Full text report
    ├── data_with_adoption_scores.csv            # Data + calculated scores
    ├── analysis_summary.csv                     # Summary statistics
    ├── 01_adoption_distribution_pie.png
    ├── 02_adoption_distribution_bar.png
    ├── 03_farm_size_by_adoption_boxplot.png
    ├── 04_farm_size_vs_adoption_scatter.png
    ├── 05_adoption_by_region_stacked.png
    ├── 06_practice_correlation_heatmap.png
    ├── 07_practice_performance_ranking.png
    └── 08_adoption_score_distribution.png
```

## Generated Files

### In `cleaned/` folder:
- **cleaned_data.csv** - Cleaned dataset with missing values handled and duplicates removed

### In `results/` folder:

**Data Files:**
- **COMPREHENSIVE_REPORT.txt** - Complete analysis report with findings and recommendations
- **data_with_adoption_scores.csv** - Original data plus calculated adoption scores
- **analysis_summary.csv** - Summary statistics and key metrics

**Visualizations:**
- **01_adoption_distribution_pie.png** - Pie chart showing adoption level distribution
- **02_adoption_distribution_bar.png** - Bar chart of farmer counts by adoption level
- **03_farm_size_by_adoption_boxplot.png** - Farm size distribution across adoption levels
- **04_farm_size_vs_adoption_scatter.png** - Relationship between farm size and adoption
- **05_adoption_by_region_stacked.png** - Regional adoption patterns
- **06_practice_correlation_heatmap.png** - Correlations between farming practices
- **07_practice_performance_ranking.png** - Practice scores from worst to best
- **08_adoption_score_distribution.png** - Histogram of adoption percentages

## Understanding the Results

### Interpretation Example

**Result for 01_adoption_distribution_pie**
- 79% Medium, 11% Good, 10% Bad

**This means:**
- Most farmers have partial adoption (room to improve)
- Small elite group doing excellent
- Small group needs urgent intervention

## Running the Analysis

### Method: GitHub Actions (Automatic)
- Push changes to `excel-data/test-1-cocoa-adoption/**`
- Analysis runs automatically
- Results committed back to repository

## Expected Results

**Typical Analysis Shows:**
- Clear adoption categories
- Practice-specific performance
- Regional patterns
- Correlations between practices
- Actionable recommendations

**Processing Time:**
- Small datasets (<1000 rows): 5-10 seconds
- Medium datasets (1000-10000 rows): 15-30 seconds
- Large datasets (>10000 rows): 30-60 seconds

## Notes

- **Data Privacy**: Farmer names are included in cleaned data files
- **Score Interpretation**: Scoring is based on keyword matching - customize if needed
- **Updates**: When you update the Excel file, re-run the analysis to regenerate results
- **Backup**: Original data is never modified - cleaned versions are saved separately
- **Path Structure**: Results and cleaned data are now organized within the test-1-cocoa-adoption folder for better organization
