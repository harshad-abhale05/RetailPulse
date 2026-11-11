# RetailPulse - E-Commerce Data Lakehouse Architecture

## 1. Project Objective

RetailPulse is an end-to-end e-commerce data engineering pipeline built using the Brazilian Olist E-Commerce dataset.

The objective is to ingest raw datasets, validate data quality, transform data through Bronze, Silver and Gold layers, and generate business insights using SQL.

The pipeline is automated through GitHub Actions.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Development Environment | GitHub Codespaces |
| Programming Language | Python |
| Data Processing Engine | DuckDB |
| Query Language | SQL |
| Storage Format | Apache Parquet |
| Source Dataset | Kaggle Olist E-Commerce |
| Pipeline Automation | GitHub Actions |
| Version Control | Git and GitHub |
| Output Storage | GitHub Actions Artifacts |

## 3. Architecture

```text
          Brazilian Olist Dataset
                    |
                    v
                Kaggle API
                    |
                    v
           GitHub Actions Runner
                    |
                    v
             BRONZE LAYER
          Original CSV Inspection
          Ingestion Metadata Report
                    |
                    v
             SILVER LAYER
            DuckDB Processing
          Data Type Standardization
          Data Quality Validation
          Relationship Validation
          Geolocation Aggregation
                    |
                    v
             GOLD LAYER
             Fact Tables
           Dimension Tables
                    |
                    v
             SQL ANALYTICS
          Monthly Revenue
          Product Categories
          Top Sellers
          Customer Reviews
          Payment Distribution
          Delivery Performance
                    |
                    v
            Business Insights
                    |
                    v
          GitHub Actions Artifacts
             (7-day retention)
```

## 4. Medallion Architecture

### 4.1 Bronze Layer

The Bronze layer handles the original source datasets.

Responsibilities:

- Ingest all nine original Olist CSV datasets.
- Inspect dataset names, columns and row counts.
- Preserve source data without modification.
- Generate an ingestion metadata report.
- Keep original CSV files in the raw data directory.

Output:
- `bronze_ingestion_report.json`

### 4.2 Silver Layer

The Silver layer performs data transformation and validation using Python and DuckDB.

Responsibilities:

- Read original CSV datasets.
- Standardize data types.
- Convert datasets into Parquet format.
- Validate row counts and key uniqueness.
- Validate relationships between datasets.
- Aggregate geolocation records by ZIP prefix.
- Preserve incomplete but valid records.
- Handle missing product category translations using LEFT JOIN and fallback to original category names.

Output:
- Eight transformed Parquet datasets.
- `silver_transformation_report.json`

### 4.3 Gold Layer

The Gold layer creates analytical fact and dimension tables.

**Fact Tables**

| Table | Description |
|---|---|
| fact_orders | Order-level information |
| fact_order_items | Individual order item information |
| fact_payments | Payment-level information |
| fact_reviews | Customer review information |

**Dimension Tables**

| Table | Description |
|---|---|
| dim_customers | Customer information |
| dim_products | Product information |
| dim_sellers | Seller information |
| dim_date | Date dimension |

Eight Gold Parquet datasets are generated.

Fact tables are maintained separately to avoid inflated aggregations caused by joining multiple one-to-many relationships.

## 5. Data Quality and Validation

RetailPulse implements data quality checks at different stages.

### Primary Key Validation

- Validate unique identifiers.
- Validate composite keys for order items, payments and reviews.
- Identify duplicate review identifiers.

### Foreign Key Validation

Validate relationships between:

- Orders and Customers.
- Order Items and Orders.
- Order Items and Products.
- Order Items and Sellers.
- Payments and Orders.
- Reviews and Orders.

### Exception Handling

- Preserve products with missing category translations.
- Preserve unmatched geographic records.
- Retain incomplete delivery records.
- Identify canceled orders with delivery timestamps.
- Avoid deleting valid source records because of missing optional information.

Detailed findings are documented in `data_quality_findings.md`.

## 6. Pipeline Execution Flow

The master pipeline is executed through:

`python src/run_pipeline.py`

Execution sequence:

1. Bronze ingestion.
2. Silver transformation.
3. Silver relationship validation.
4. Gold transformation.
5. Business analytics execution.

The pipeline uses Python scripts and DuckDB SQL queries.

## 7. Storage and Artifact Management

- Raw source files are stored in `data/raw/`.
- Transformed Silver datasets are stored in Parquet format.
- Gold analytical datasets are stored in Parquet format.
- Reports are generated in JSON format.
- Raw and processed data files are excluded from Git.

GitHub Actions uploads successful pipeline outputs as downloadable artifacts.

Artifact retention period: **7 days**.

GitHub Actions Artifacts provide temporary output storage and are not a permanent cloud data lake.

## 8. Automation

GitHub Actions automates the pipeline execution.

The workflow:

1. Checks out the repository.
2. Configures Python.
3. Installs project dependencies.
4. Downloads the Olist dataset using Kaggle API authentication.
5. Verifies the nine source CSV files.
6. Executes the master pipeline.
7. Uploads generated outputs as an artifact.

The workflow can be triggered automatically through configured repository changes or manually using the GitHub Actions interface.

## 9. Cost Policy

The project is designed to avoid paid cloud infrastructure.

- Development uses GitHub Codespaces.
- Automation uses GitHub-hosted runners.
- DuckDB performs local analytical processing within the execution environment.
- GitHub Actions Artifacts provide temporary output storage.
- No paid AWS resources are used.

Free-tier quotas and platform usage limits apply.
