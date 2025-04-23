# oeutils

This is the `oeutils`, or utils for Otto's Expeditions written in Go. These are utils for managing Ascend projects.

Internally, we develop in the `mesh` project across different Data Planes: BigQuery, Databricks, DuckDB, and Snowflake. The main `oeutils unmesh` functionality decomposes the mesh project into one project per data plane. We work internally in an internal-only GitHub repository, then release only these public projects to a public repository for our users. This allows us to work like our users would, with our Profiles and internal details.

The `oeutils unmesh` code removes any internal details and changes some things about the project.

## CLI commands

Reference the `justfile` for project commands like running tests.

