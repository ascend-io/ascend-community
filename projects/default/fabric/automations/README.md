# Automations

Event-driven and scheduled workflow triggers for Otto's Expeditions.

## Automation Categories

### Extract-Load Automations

Scheduled triggers for data ingestion flows:

- #automation:extract-load-bigquery
- #automation:extract-load-databricks
- #automation:extract-load-duckdb
- #automation:extract-load-duckdb-postgres
- #automation:extract-load-motherduck
- #automation:extract-load-snowflake

### Transform Automations

Triggered after extract-load completes:

- #automation:transform-bigquery
- #automation:transform-databricks
- #automation:transform-duckdb
- #automation:transform-duckdb-postgres
- #automation:transform-motherduck
- #automation:transform-snowflake

### Downstream Automations

Triggered after transform completes:

- #automation:downstreams-bigquery
- #automation:downstreams-databricks
- #automation:downstreams-duckdb
- #automation:downstreams-duckdb-postgres
- #automation:downstreams-motherduck
- #automation:downstreams-snowflake

### Alerting

- #automation:email-on-failure - Sends email alerts on flow failures (disabled by default)
- #automation:otto-email - Otto-powered email notifications

## Configuration

Automation schedules are controlled via profile parameters. See `profiles/` for schedule configuration.