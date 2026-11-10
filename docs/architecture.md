# RetailPulse - Cloud Data Lakehouse Architecture

## 1. Project Objective

Build an end-to-end cloud-based e-commerce data engineering
pipeline using the Brazilian Olist E-Commerce dataset.

The pipeline will ingest, store, validate, transform and analyze
e-commerce data.

## 2. Architecture

Olist CSV Dataset
       |
       v
Python Ingestion (GitHub Codespaces)
       |
       v
AWS S3 - Bronze
       |
       v
AWS Glue / PySpark
       |
       v
AWS S3 - Silver
       |
       v
dbt / SQL Transformations
       |
       v
AWS S3 - Gold
       |
       v
AWS Athena
       |
       v
Power BI Dashboard

Apache Airflow will coordinate pipeline execution.

## 3. Medallion Architecture

### Bronze Layer
- Store all nine original CSV datasets.
- Preserve original source data.
- Maintain ingestion metadata.

### Silver Layer
- Standardize column names and data types.
- Handle missing values appropriately.
- Validate primary and foreign key relationships.
- Preserve valid records with incomplete information.
- Aggregate geolocation by ZIP prefix.
- Preserve review composite key (review_id, order_id).
- Retain untranslated product categories.

### Gold Layer

Planned analytical tables:

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

Payment and order-item facts will remain separate to avoid
duplicating records during analytical joins.

## 4. Technology Stack

- Python
- SQL
- AWS S3
- AWS Glue
- PySpark
- AWS Athena
- dbt
- Apache Airflow
- Power BI

## 5. Data Quality Decisions

- Preserve original source CSV files.
- Do not delete products with missing category translations.
- Preserve incomplete orders.
- Use LEFT JOIN for optional geographic enrichment.
- Use (review_id, order_id) as the review composite key.
- Keep unmatched geolocation coordinates NULL.

## 6. Development Environment

All development and execution will be performed using
GitHub Codespaces and cloud services.

No local-host deployment is required.

AWS resources will only be provisioned after reviewing
their costs and obtaining approval.
