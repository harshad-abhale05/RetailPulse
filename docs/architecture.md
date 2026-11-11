# RetailPulse - Cloud-Based E-Commerce Lakehouse

## 1. Project Objective

Build an end-to-end e-commerce data engineering pipeline
using the Brazilian Olist E-Commerce dataset.

The pipeline will ingest, validate, transform and analyze
real-world e-commerce data.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Development | GitHub Codespaces |
| Programming | Python |
| Data processing | DuckDB |
| Storage format | Apache Parquet |
| SQL transformations | dbt Core |
| Pipeline automation | GitHub Actions |
| Dashboard | Streamlit Community Cloud |
| Version control | GitHub |

## 3. Architecture

Olist Dataset (Kaggle)
        |
        v
GitHub Codespaces
        |
        v
Python Ingestion
        |
        v
BRONZE - Original CSV Data
        |
        v
DuckDB Processing
        |
        v
SILVER - Cleaned Parquet Data
        |
        v
dbt Core / SQL
        |
        v
GOLD - Analytics Tables
        |
        v
DuckDB Analytics
        |
        v
Streamlit Dashboard

GitHub Actions will automate pipeline execution.

## 4. Medallion Architecture

### Bronze
- Preserve all nine original Olist CSV datasets.
- Maintain source data without modifications.
- Record ingestion metadata.

### Silver
- Standardize column names and data types.
- Handle missing values appropriately.
- Validate keys and relationships.
- Preserve incomplete but valid records.
- Aggregate geolocation by ZIP prefix.
- Preserve review composite key.
- Retain untranslated product categories.

### Gold

Fact tables:
- fact_order_items
- fact_orders
- fact_payments
- fact_reviews

Dimension tables:
- dim_customers
- dim_products
- dim_sellers
- dim_date

Payment and order-item facts remain separate to avoid
inflated results from many-to-many joins.

## 5. Data Quality Decisions

- Preserve original source data.
- Do not delete products with missing translations.
- Preserve incomplete orders.
- Use LEFT JOIN for optional geographic enrichment.
- Use (review_id, order_id) as the review composite key.
- Keep unmatched geographic coordinates NULL.

## 6. Execution and Storage

- Development and initial processing: GitHub Codespaces.
- Analytical storage: Parquet files.
- Query engine: DuckDB.
- Source code: GitHub repository.

Large source datasets and generated Parquet files must
not be committed to GitHub.

Codespaces storage is not a permanent data lake.
Pipeline outputs will require a separately verified
free storage or artifact strategy for persistence.

## 7. Deployment

The planned dashboard will use Streamlit Community Cloud,
subject to its current resource and deployment limits.

## 8. Cost Policy

The project targets zero out-of-pocket spending.

No paid AWS resources or paid upgrades will be created.
Free-tier quotas and platform limits will be monitored.
