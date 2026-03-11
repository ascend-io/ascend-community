# Flows

Data pipelines organized by platform.

## Platform Directories

| Platform | Flows |
|----------|-------|
| `bigquery/` | #flow:extract-load-bigquery, #flow:transform-bigquery, #flow:metrics-bigquery |
| `databricks/` | #flow:extract-load-databricks, #flow:transform-databricks, #flow:metrics-databricks, #flow:pyspark-databricks |
| `duckdb/` | #flow:extract-load-duckdb, #flow:transform-duckdb, #flow:metrics-duckdb, #flow:jaffle_shop, #flow:extract-load-duckdb-postgres, #flow:transform-duckdb-postgres, #flow:metrics-duckdb-postgres |
| `motherduck/` | #flow:extract-load-motherduck, #flow:transform-motherduck, #flow:metrics-motherduck |
| `snowflake/` | #flow:extract-load-snowflake, #flow:transform-snowflake, #flow:metrics-snowflake, #flow:llm-snowflake |

## Flow Pattern

Each platform follows a consistent pattern:

1. **Extract-Load**: Ingest raw data from GCS and local files
2. **Transform**: Apply business logic and data quality rules
3. **Metrics**: Generate aggregated analytics and KPIs

## Cross-Platform Compatibility

SQL components use Jinja macros from `macros/` for dialect-agnostic transformations where possible.