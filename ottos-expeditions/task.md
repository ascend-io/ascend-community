# task

Oh no! The `mesh` project's `ascend_project.yaml` has:

```yaml
project:
  # only alphanumeric characters, dashes, and underscores are allowed for the Project name
  name: ottos-expeditions
  # additional packages to install from PyPI
  # https://pypi.org/project/ottos-expeditions/
  # you can use a Flow bootstrap command to install private packages
  pip_packages:
    - ottos-expeditions
  # in Ascend, Parameters are a core concept.
  # Think of parameters as a key:value mapping (dictionary, map, etc.) of variables
  # you can use in your Flows. The hierarchy of parameters is:
  # Project > Profile > Flow > Flow Run.
  # The Parameters below are the top-level variables -- you can think of them as a default
  # -- for all Flows in this project. Profiles are typically used to override Parameters
  parameters:
    data_planes:
      duckdb:
        path: ottos-expeditions.ddb
        max_concurrent_queries: 128
      gcp:
        project_id: ottos-expeditions-development
      bigquery:
        dataset: OTTOS_EXPEDITIONS_DEVELOPMENT
        location: US
      databricks:
        workspace_url: "https://adb-331203153589870.10.azuredatabricks.net/"
        client_id: 61ed841f-69d3-4fa4-8256-aa05c7214281
        cluster_id: 0329-215355-4kz8sqso
        cluster_http_path: sql/protocolv1/o/331203153589870/0329-215355-4kz8sqso
        warehouse_http_path: /sql/1.0/warehouses/34548a67f1781087
        catalog: OTTOS_EXPEDITIONS_DEVELOPMENT
        schema: DEFAULT
      snowflake:
        account: ascendpartner
        user: OTTOS_EXPEDITIONS_DEVELOPMENT
        role: OTTOS_EXPEDITIONS_DEVELOPMENT
        warehouse: OTTOS_EXPEDITIONS_DEVELOPMENT
        database: OTTOS_EXPEDITIONS_DEVELOPMENT
        schema: DEFAULT
        max_concurrent_queries: 20
  # defaults are typically used to specify the default Data Plane Connection
  # used for Flows, specified by a regex pattern on the Flow name
  defaults:
    - kind: Flow
      name:
        regex: .*
      spec:
        data_plane:
          connection_name: data_plane_duckdb
    - kind: Flow
      name:
        regex: .*-bigquery
      spec:
        data_plane:
          connection_name: data_plane_bigquery
    - kind: Flow
      name:
        regex: .*-databricks
      spec:
        data_plane:
          connection_name: data_plane_databricks
    - kind: Flow
      name:
        regex: .*-snowflake
      spec:
        data_plane:
          connection_name: data_plane_snowflake
```

This is great, but the `bigquery` project's `ascend_project.yaml` looks the same!

We have logic in `oeutils` for only keeping the relevant values for a given Data Plane. However at some point, we refactored the parameters to primarily live in the project YAML. The profile YAMLs are much lighter. Also note that currently this will break the non-mesh projects, as all Flows will go into the non-existent DuckDB Data Plane. That is, we need to update the Ascend project YAML to only keep the relevant parametrs for the given Data Plane and only keep the regex for all Flows pointing to it.

Work on refactoring `oeutils` to achieve this behavior, clarifying with the user if needed.
