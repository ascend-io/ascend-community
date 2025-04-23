# Otto's Expeditions

This is Otto's Expeditions, the premier Ascend project built on public synthetic data to demonstrate the platform and recommended best practices for each supported Data Plane.

## Structure

Otto's Expeditions may refer to:

- a fictional company
- a Python package publicly available on PyPI
- an Ascend project

The Python package is used to generate the synthetic data.

| Path | Description |
| ---- | ----------- |
| `justfile` | Commands for managing Otto's Expeditions |
| `projects/` | Ascend projects |
| `src/` | Python package source code |
| `oeutils/` | Go utilities source code |

## The `mesh` project and `oeutils`

We have two repositories for Ascend Community, where Otto's Expeditions resides:

- `ascend-io/ascend-community`: public repository
- `ascend-io/ascend-community-internal`: internal repository

The intent is that we can work internally as a real customer would, using our own infrastructure. While we never put secrets in version control, we still want to remove other internal details from the public versions of the project. Moreover, internally we don't want to have to create a Project for each Data Plane. As Ascend employees, we want to work across all supported Data Planes in a single Project.

To solve this, we created the `mesh` project. This project is what we work on internally, with all of our own Profiles and configuration for use on every supported Data Plane. This is where `oeutils` comes in: this is Go code primarily to `oeutils unmesh` the `mesh` project into the `bigquery`, `databricks`, and `snowflake` projects respectively (note we don't publicly release `duckdb` yet).

