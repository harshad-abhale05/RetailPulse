# RetailPulse
### End-to-End E-Commerce Data Engineering Pipeline

RetailPulse is an end-to-end data engineering project that builds an analytical data lakehouse using the Brazilian Olist E-Commerce dataset.

The pipeline ingests raw CSV datasets, performs data quality checks, transforms data into analytical Parquet datasets, and executes SQL queries to generate business insights.

The complete pipeline is automated using GitHub Actions and runs on GitHub-hosted cloud runners.

---

## Project Overview

| Metric | Details |
|---|---|
| Source datasets | 9 CSV files |
| Source records | 1.65 million+ |
| Data architecture | Medallion (Bronze, Silver, Gold) |
| Programming language | Python |
| Processing engine | DuckDB |
| Storage format | Apache Parquet |
| Analytics | SQL |
| Automation | GitHub Actions |
| Dataset | Brazilian Olist E-Commerce |

## Technology Stack

- Python
- DuckDB
- SQL
- Apache Parquet
- Git and GitHub
- GitHub Actions
- Kaggle API
- GitHub Codespaces

## Architecture

```text
             Olist E-Commerce Dataset
                      |
                      v
                  Kaggle API
                      |
                      v
             GitHub Actions Runner
                      |
                      v
             BRONZE - INGESTION
             - CSV inspection
             - Row and column profiling
             - Ingestion metadata
                      |
                      v
             SILVER - TRANSFORMATION
             - Data type standardization
             - Data quality validation
             - Relationship validation
             - Geolocation aggregation
             - Parquet generation
                      |
                      v
               GOLD - ANALYTICS
             - Fact tables
             - Dimension tables
             - Analytical datasets
                      |
                      v
                DUCKDB + SQL
             - Monthly revenue
             - Product categories
             - Top sellers
             - Customer reviews
             - Payment distribution
             - Delivery performance
                      |
                      v
               BUSINESS INSIGHTS
                      |
                      v
             GITHUB ACTIONS ARTIFACTS
                (7-day retention)
```

## Medallion Architecture

### 1. Bronze Layer

- Ingests and inspects all nine original CSV datasets.
- Records dataset names, row counts and column information.
- Preserves original source data without modification.
- Generates an ingestion metadata report.

### 2. Silver Layer

- Converts raw CSV datasets into typed Parquet files.
- Standardizes data types.
- Validates row counts and key uniqueness.
- Validates relationships between datasets.
- Aggregates geolocation records by ZIP prefix.
- Preserves incomplete but valid records.
- Handles missing category translations using LEFT JOIN and fallback to original category names.

### 3. Gold Layer

Creates eight analytical datasets.

**Fact tables**
- fact_orders
- fact_order_items
- fact_payments
- fact_reviews

**Dimension tables**
- dim_customers
- dim_products
- dim_sellers
- dim_date

Fact tables are maintained separately to avoid inflated aggregations caused by joining multiple one-to-many relationships.

## Data Quality

The project includes checks for:

- Primary and composite key uniqueness.
- Foreign key relationships.
- Missing geographic matches.
- Untranslated product categories.
- Duplicate review identifiers.
- Incomplete delivery timestamps.
- Canceled orders with delivery timestamps.

Important findings:

- Six core foreign-key relationships passed with zero orphan records.
- 13 products have two untranslated category values.
- 157 customer and 7 seller unique ZIP prefixes have no geolocation match.
- Six canceled orders contain delivery timestamps.

Data is preserved wherever possible rather than deleting records because of incomplete optional information.

Detailed findings are available in [docs/data_quality_findings.md](docs/data_quality_findings.md).

## Business Analytics

Six SQL queries generate business insights:

| SQL Analysis | Purpose |
|---|---|
| Monthly Revenue | Monthly revenue trends |
| Top Product Categories | Category-wise units and revenue |
| Top Sellers | Seller revenue and item performance |
| Customer Review Distribution | Review score distribution |
| Payment Method Distribution | Payment methods and payment value |
| Delivery Performance | Average delivery time |

### Sample Results

- Average delivery time: approximately 12.5 days.
- November 2017 recorded approximately 1.15 million in revenue.
- Credit cards represented approximately 73.9% of payment records.
- 4-star and 5-star reviews represented approximately 77.1% of all reviews.

These figures are based on the current Olist dataset and the definitions used in the project's SQL queries.

## Automated Pipeline

RetailPulse uses GitHub Actions to automate execution.

The workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies.
4. Downloads the Olist dataset using the Kaggle API.
5. Verifies the presence of all nine CSV files.
6. Executes the complete Python pipeline.
7. Uploads generated reports and Parquet datasets as an artifact.

The generated artifact is retained for seven days.

### Run the workflow manually

1. Open the repository's Actions tab.
2. Select RetailPulse Data Pipeline.
3. Click Run workflow.
4. Select the main branch.
5. Start the workflow.

The repository requires a GitHub Actions secret named `KAGGLE_API_TOKEN` containing a valid Kaggle API token.

## Run in GitHub Codespaces

### 1. Clone the repository

```bash
git clone https://github.com/harshad-abhale05/RetailPulse.git
cd RetailPulse
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare source data

Download the Brazilian Olist E-Commerce dataset from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Extract all nine CSV files into:

```text
data/raw/
```

### 4. Execute the pipeline

```bash
python src/run_pipeline.py
```

### 5. View generated outputs

```text
data/
├── raw/
└── processed/
    ├── bronze_ingestion_report.json
    ├── silver_transformation_report.json
    ├── silver/
    └── gold/
```

Generated data files are excluded from Git because they are reproducible pipeline outputs.

## Repository Structure

```text
RetailPulse/
│
├── .github/
│   └── workflows/
│       └── retailpulse.yml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── architecture.md
│   └── data_quality_findings.md
│
├── sql/
│   ├── customer_review_distribution.sql
│   ├── delivery_performance.sql
│   ├── monthly_revenue.sql
│   ├── payment_method_distribution.sql
│   ├── top_product_categories.sql
│   └── top_sellers.sql
│
├── src/
│   ├── gold/
│   │   ├── create_gold.py
│   │   └── run_analytics.py
│   │
│   ├── ingestion/
│   │   ├── bronze_ingestion.py
│   │   └── profile_data.py
│   │
│   ├── transformation/
│   │   └── create_silver.py
│   │
│   ├── validation/
│   │
│   └── run_pipeline.py
│
├── requirements.txt
└── README.md
```

## Cost and Storage

- Developed using GitHub Codespaces.
- Automated execution uses GitHub-hosted runners.
- No paid AWS infrastructure is required.
- Pipeline outputs are temporarily retained through GitHub Actions Artifacts for seven days.
- Raw datasets and generated Parquet files are not committed to the source repository.

## Dataset Attribution

Dataset: Brazilian E-Commerce Public Dataset by Olist.

Source: Kaggle - olistbr/brazilian-ecommerce.

The dataset is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0. Please follow the dataset license and attribution requirements.

---

**RetailPulse - Turning raw e-commerce data into validated analytical insights.**