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

## Analysis Tasks

# Test 1: Cocoa Adoption Analysis

## 📋 Overview

This analysis automatically evaluates cocoa farming practices and calculates adoption levels for farmers based on 14 key agricultural practices. The system processes Excel data and generates comprehensive reports with visualizations.

## 🎯 Purpose

**Main Objectives:**
- Assess farmer adoption of best cocoa farming practices
- Identify areas needing improvement
- Provide data-driven recommendations for agricultural extension programs
- Track regional and farm-size patterns in adoption

## 📊 Data Structure

### Required Excel Columns

Your Excel file (`test_1_cocoa_adoption_raw.xlsx`) must contain these columns:

| Column Name | Type | Description |
|-------------|------|-------------|
| `farmer_id` | Text/Number | Unique farmer identifier |
| `first_name` | Text | Farmer's first name |
| `last_name` | Text | Farmer's last name |
| `Farm size` | Number | Farm size in hectares |
| `Region` | Text | Geographic region |
| `gender` | Text | Farmer's gender |
| `season` | Text | Planting/harvest season |

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

## 🔢 Adoption Scoring System

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

## 🤖 Automated Analysis

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

## 📁 File Structure

```
test-1-cocoa-adoption/
├── raw/
│   └── test_1_cocoa_adoption_raw.xlsx    # Your input data
├── scripts/
│   └── test1_analysis.py                  # Analysis script
└── results/                               # Auto-generated results
    ├── COMPREHENSIVE_REPORT.txt           # Full text report
    ├── cleaned_data.csv                   # Cleaned dataset
    ├── data_with_adoption_scores.csv      # Data + calculated scores
    ├── analysis_summary.csv               # Summary statistics
    ├── 01_adoption_distribution_pie.png
    ├── 02_adoption_distribution_bar.png
    ├── 03_farm_size_by_adoption_boxplot.png
    ├── 04_farm_size_vs_adoption_scatter.png
    ├── 05_adoption_by_region_stacked.png
    ├── 06_practice_correlation_heatmap.png
    ├── 07_practice_performance_ranking.png
    └── 08_adoption_score_distribution.png
```
## Understanding the Results

### Interpretation

**Result for 01_adoption_distribution_pie**
- 79% Medium, 11% Good, 10% Bad

**This means:**
- Most farmers have partial adoption (room to improve)
- Small elite group doing excellent
- Small group needs urgent intervention

**Recommended Actions:**
- Focus training on moving Medium → Good
- Share best practices from Good performers
- Intensive support for Bad performers

### For Agricultural Extension Officers
- Identify farmers needing support
- Plan targeted training programs
- Track improvement over time

### For Program Managers
- Allocate resources to regions
- Measure program effectiveness
- Report to stakeholders

### For Researchers
- Analyze adoption patterns
- Study correlations between practices
- Identify success factors

## Customization Options

### Adjusting Score Thresholds

Edit line ~150 in `test1_analysis.py`:

```python
def categorize_adoption(percentage):
    if percentage >= 66.67:  # Change this threshold
        return 'Good'
    elif percentage >= 33.33:  # Change this threshold
        return 'Medium'
    else:
        return 'Bad'
```

### Modifying Practice Scoring

Edit the `score_practice()` function (line ~60) to customize how practice values are interpreted based on your specific data.

### Adding New Practices

To include additional practice columns:

1. Add column name to `practice_columns` list (line ~45)
2. Ensure the column exists in your Excel file
3. Re-run the analysis

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

## Troubleshooting

### Issue: "File not found" error
**Solution:** Check that Excel file path matches exactly in the script (line 28)

### Issue: "Column not found" error
**Solution:** Verify Excel column names match exactly (case-sensitive, check for extra spaces)

### Issue: All farmers scored as "Medium"
**Solution:** Check if practice column values match the scoring keywords, may need to customize `score_practice()` function

### Issue: Charts look wrong
**Solution:** Verify data quality - check for unusual values or missing data

### Issue: GitHub Actions fails
**Solution:** Check the Actions tab logs for specific error messages
