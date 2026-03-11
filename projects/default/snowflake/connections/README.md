# Connections

Data plane and source connections for Otto's Expeditions.

## Data Plane Connections

Each platform has a dedicated data plane connection:

- #connection:data_plane_bigquery - Google BigQuery
- #connection:data_plane_databricks - Databricks Unity Catalog
- #connection:data_plane_duckdb - DuckDB with DuckLake
- #connection:data_plane_duckdb_postgres - DuckDB with Postgres metadata
- #connection:data_plane_motherduck - MotherDuck cloud
- #connection:data_plane_snowflake - Snowflake

## Source Connections

- #connection:read_gcs_lake - GCS bucket for source data
- #connection:read_local_files - Local files in `data/`

## Configuration

Connection parameters are defined in profiles. Each workspace/deployment profile specifies the appropriate catalog, schema, or dataset for data isolation.