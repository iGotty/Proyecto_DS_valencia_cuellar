# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data science academic project (MINE-4101 - Universidad de los Andes) analyzing user behavior on a food delivery platform. The goal is to identify which newly acquired users (those reaching their 4th order) have the highest potential for growth, enabling the Engagement team to optimize resource allocation.

**Dataset:** 41,667 users × 15 variables, located at `dataset_protegido (1).csv` (15 MB, clean - no nulls/duplicates)

**Language:** Python 3, Spanish documentation/comments (team uses Spanish)

## Common Commands

### Running the Analysis

**Interactive (recommended):**
```bash
jupyter notebook notebooks/entendimiento_datos.ipynb
```

**Modular execution (scripts run independently in any order):**
```bash
cd scripts
python data_quality.py          # Data validation and quality scoring
python affinity_analysis.py      # User preferences (categories, brands, shops)
python univariate_analysis.py    # Individual variable analysis + normality tests
python multivariate_analysis.py  # Correlations, ANOVA, Chi-square tests
python visualizations.py         # Generate 11 PNG charts (saves to ../visualizations/)
```

### Environment Setup

```bash
# Install dependencies
pip install pandas numpy scipy matplotlib seaborn jupyter

# Virtual environment already exists at .venv/
source .venv/bin/activate  # Activate if needed
```

## Code Architecture

### Modular Design Pattern

Each script in `scripts/` follows a **class-based, independent execution** pattern:

1. **data_quality.py** - `DataQualityAnalyzer` class
   - Validates missing values, duplicates, data types, business rules, outliers
   - Outputs quality score (current: 100/100)

2. **affinity_analysis.py** - `AffinityAnalyzer` class
   - Parses dictionary columns (`main_category_counts`, `ka_type_counts`, etc.) using `ast.literal_eval()`
   - Analyzes user preferences across categories, stores, brands
   - Key finding: 6 categories = 80% of orders, brand001 = 40.6% market share

3. **univariate_analysis.py** - `UnivariateAnalyzer` class
   - Descriptive statistics for numeric variables
   - Frequency analysis for categorical variables
   - Normality tests (Shapiro-Wilk, Anderson-Darling)

4. **multivariate_analysis.py** - `MultivariateAnalyzer` class
   - Pearson/Spearman correlations
   - ANOVA, Kruskal-Wallis (numeric vs categorical)
   - Chi-square, Cramér's V (categorical associations)
   - Key finding: `efo_to_four` vs `delta_orders` correlation = -0.201 (fast adopters grow more)

5. **visualizations.py** - `VisualizationGenerator` class
   - Creates 11 high-res PNG charts (300 DPI)
   - Saves to `../visualizations/`

### Script Independence

- Each script reads the full dataset independently
- No shared state between scripts
- Can be run in any order
- All use consistent class structure: `__init__()` → analysis methods → report generation

## Critical Domain Concepts

### Key Variables

- **`delta_orders`**: Growth metric (number of orders AFTER the 4th order)
- **`efo_to_four`**: Days from 1st to 4th order (adoption speed indicator)
- **`categoria_recencia`**: Recency categories with business meaning:
  - Active: ≤7 days
  - Semi-Active: 8-14 days
  - Warm: 15-30 days
  - Cold: 31-90 days
  - Lost: >90 days
- **`r_segment`**: User segmentation from another business line (r_segment002 performs best)

### Dictionary Columns

Four columns store dictionaries as strings and require parsing with `ast.literal_eval()`:
- `main_category_counts`: User's category preferences
- `ka_type_counts`: Store type preferences
- `shop_counts`: Specific shop visit counts
- `brand_counts`: Brand preferences

**Example parsing pattern (used in affinity_analysis.py):**
```python
import ast
df['parsed_dict'] = df['dict_column'].apply(ast.literal_eval)
```

### Key Findings (for context when analyzing)

1. **Adoption speed predicts growth**: Fast adopters (0-7d to 4th order) average 9.5 orders growth vs 4.1 for slow adopters (>21d) - 2.3x difference
2. **Recency is critical**: Active users (≤7d) average 8.97 orders vs 1.29 for lost users (>90d) - 7x impact
3. **Segment002 outperforms**: Highest growth (7.12 orders), fastest adoption (14.58 days)
4. **High exploration, low loyalty**: 96.9% buy from multiple stores, but 6 categories = 80% of orders

## Code Conventions

- **Naming:** snake_case for variables/functions, PascalCase for classes
- **Documentation:** Spanish docstrings and comments (the team works in Spanish)
- **Statistical approach:** Both parametric (Pearson, ANOVA) and non-parametric (Spearman, Kruskal-Wallis) tests
- **Visualization style:** seaborn-darkgrid, "husl" palette, high-res (300 DPI)
- **Console output:** Uses emoji indicators (✅ ⚠️ 📊) for visual feedback

## File Locations

- **Dataset:** `dataset_protegido (1).csv` (project root)
- **Scripts:** `scripts/*.py` (5 analysis modules)
- **Notebook:** `notebooks/entendimiento_datos.ipynb` (1,740 lines, consolidated analysis)
- **Visualizations:** `visualizations/*.png` (11 charts, auto-generated)
- **Documentation:** `documento/*.md` and `documento/*.pdf` (project deliverables)
- **Key findings:** `HALLAZGOS_CLAVE.md` (executive summary)

## Project Status

**Phase 1 (Complete):** Exploratory Data Analysis
- Data collection, quality validation, univariate/multivariate analysis, visualizations, documentation

**Phase 2 (Planned):** Predictive Modeling
- Data preparation, model training (Random Forest, XGBoost, LightGBM), dashboard/API development

## Important Notes

- Dataset is protected (contains user behavior data) - handle according to Colombian data protection laws (Ley 1581 de 2012)
- Scripts output to console - outputs are verbose and include statistical interpretations
- Visualization generation can take 30-60 seconds (creates 11 charts)
- All analysis is reproducible - scripts use consistent random seeds where applicable
- Git workflow: main branch, clean status, commits in Spanish
