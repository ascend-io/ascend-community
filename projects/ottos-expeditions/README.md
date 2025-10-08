# Otto's Expeditions

Otto's Expeditions is a comprehensive example Ascend Project demonstrating a modern data platform for a fictional outdoor expedition company of the same name. This project showcases end-to-end data engineering workflows across multiple cloud data platforms.

## Overview

Otto's Expeditions provides guided outdoor adventures and this project models their complete data ecosystem including:

- **Customer data**: Expedition bookings, customer feedback, and telemetry
- **Operations data**: Guide assignments, route information, weather conditions
- **Sales data**: Multi-channel sales across physical stores, website, and vendor partnerships
- **Social media**: Engagement data from Twitter, Meta platforms, and LinkedIn
- **Analytics**: Customer satisfaction metrics, operational KPIs, and business intelligence

## Project structure

This project is organized by data platform, with each directory containing a complete Ascend Project configuration:

| Platform | Description | Key features |
|----------|-------------|--------------|
| [`bigquery/`](bigquery/) | Google BigQuery implementation | BigQuery-native SQL transforms, GCS integration |
| [`databricks/`](databricks/) | Databricks implementation | Delta Lake, PySpark, Unity Catalog |
| [`duckdb/`](duckdb/) | DuckDB implementation | Local development, fast analytics |
| [`snowflake/`](snowflake/) | Snowflake implementation | Snowflake-native features, Snowpark |

## Data Architecture

Each platform implementation includes:

### Extract-load Flows
- **Data sources**: Synthetic data generation from the `ottos-expeditions` Python package
- **Storage**: Partitioned data lake with date-based organization
- **Ingestion**: Automated data loading with schema validation

### Transform Flows
- **Data modeling**: Star schema with fact and dimension tables
- **Business logic**: Customer segmentation, route optimization, performance metrics
- **Data quality**: Comprehensive testing and validation

### Analytics & metrics
- **KPIs**: Customer satisfaction, guide performance, route success rates
- **Dashboards**: Executive reporting and operational monitoring
- **ML features**: Customer lifetime value, demand forecasting

## Getting started

### Prerequisites
- [Ascend CLI](https://docs.ascend.io/) installed and configured
- Access to your chosen cloud data platform (BigQuery, Databricks, Snowflake, or DuckDB)
- Python 3.13+ with uv package manager

### Quickstart

1. **Generate sample data**:
   ```bash
   # Generate 7 days of synthetic data
   uv run ottos-expeditions datagen --days 7
   ```

2. **Choose your platform**:
   ```bash
   cd bigquery    # or databricks, duckdb, snowflake
   ```

3. **Configure Connections**:
   - Update `connections/` with your platform credentials
   - Modify `ascend_project.yaml` with your project parameters

4. **Run Flows in the Ascend UI**

## Contribute

This project serves as both an example and a template. Feel free to fork the repository and create a pull request!

We welcome efforts to:
- Extend the data model for your use case
- Add new data sources and transforms
- Implement additional platforms or integrations
- Contribute improvements back to the community

## Resources

- [**Documentation**](https://docs.ascend.io/): Complete guides in each platform directory
- [**Community**](https://ascend.io/slack): Join the Ascend Community for support and discussion
- [**Website**](https://ascend.io): Learn more about Ascend, Agentic Data Engineering platform