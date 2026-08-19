# MLS Market Analytics & Tableau Dashboards

An end-to-end analytics project developed during my IDX Exchange Data Analyst Internship. The project transforms multi-period residential real estate records into validated, analysis-ready datasets and interactive market intelligence dashboards.

> **Data privacy:** The source MLS records are confidential and are not included in this repository. This portfolio contains code and methodology only. Public Tableau visualizations present aggregated results rather than row-level transaction data.

## Project Highlights

- Processed 29 monthly listing files and 29 monthly sold files with Python and Pandas.
- Aggregated approximately 1.57 million raw records and prepared approximately 1.06 million residential records for analysis.
- Built reusable checks for missingness, duplicates, invalid dates, geographic anomalies, business-rule violations, and statistical outliers.
- Enriched transaction data with monthly 30-year fixed mortgage rates from FRED.
- Engineered market metrics covering price, inventory, transaction velocity, negotiation strength, and time-to-close.
- Developed Tableau dashboards for market trends, affordability, geographic patterns, and agent/office performance.

## Analytics Workflow

```text
Monthly files
    -> aggregation and residential filtering
    -> exploratory analysis and schema validation
    -> data cleaning and quality flags
    -> mortgage-rate enrichment
    -> feature engineering and market metrics
    -> outlier detection
    -> aggregated Tableau dashboards
```

## Repository Structure

```text
script/
  week1_agregation.py                  Monthly file aggregation
  Week2_EDA.ipynb                      Exploratory analysis and validation
  week3_data_cleaning.ipynb            Cleaning and FRED enrichment
  week4.ipynb                          Date and geographic quality checks
  Week5.ipynb                          Analysis-ready dataset preparation
  week6_feature_engineering_revised.ipynb
                                       Feature engineering and segment summaries
  week7_outlier_detection.py           IQR and business-rule outlier flags
```

## Key Metrics

- Median close price
- Price per square foot
- Days on market
- Close-to-original-list ratio
- New listings and closed sales
- Listing-to-contract and contract-to-close duration
- Agent and office sales volume and transaction counts
- Monthly mortgage rate and affordability indicators

## Tableau Portfolio

View the interactive dashboards on [Tableau Public](https://public.tableau.com/app/profile/ying.wu2772/vizzes).

The portfolio includes:

- Market Overview
- Competitive Analysis Overview
- Price and Affordability Analysis
- Agent and Office Performance Overview

## Tools

- Python
- Pandas and NumPy
- SQL
- Tableau
- Jupyter Notebook
- FRED economic data

## Reproducibility

The original data cannot be distributed. To adapt the workflow to an authorized dataset:

1. Place source files in a local `csv/` directory.
2. Update local input/output paths as needed.
3. Run the scripts and notebooks sequentially from Week 1 through Week 7.
4. Keep generated outputs in the ignored `outputs/` directory.

Field names and availability may differ across MLS or transaction-data providers, so schema mappings may require adjustment.

## Author

Ying Wu  
M.S. Analytics, University of Southern California

