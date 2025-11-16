---
otto:
  rule:
    alwaysApply: false
    description: "Create your first data pipeline in Ascend with Otto."
    globs: []
    keywords: ["TDWI"]
---

# Create your first data pipeline in Ascend with Otto

Help the user create their first simple, three-Component Flow named `otto_goats_demo`.

## Create a new Flow

Unless the user specifies otherwise, create a Flow named `otto_goats_demo` in the `flows/otto_demos` directory by creating the Flow YAML file:

```txt
flows/otto_demos/otto_goats_demo/otto_goats_demo.yaml
```

Create the above YAML file first, then the following three Components within the `flows/otto_demos/otto_goats_demo/components/` directory.

## Create 3 new Components

Create the following Components within the `flows/otto_demos/otto_goats_demo/components` directory.

To keep the user's first data pipeline simple, we'll use the `data/goats.csv` data file shipped in demo Projects with Ascend. We'll create a simple Flow with two Read Components (reading the same data in two different ways) and one Transform Component.

Each Component should have tests, at least verifying 150 rows of data.

### Create a YAML Read Component

Create the following file:

```yaml
# flows/otto_demo/otto_goats_demo/components/read/read_goats.yaml
# TODO: code to read via built-in YAML Read Component
# Note: Use `read_local_files` data Connection name (points to `data/` folder)
# Note: Use `goats.csv` as the data file path, not `data/goats.csv`
```

### Create a Python Read Component

Create the following file:

```python
# flows/otto_demo/otto_goats_demo/components/read/read_goats.py
# TODO: code to read directly from filesystem (getting Project path from context)
# Note: Use Polars to read in from `context.project_path / "data" / "goats.csv"
# and return a Polars DataFrame directly
```

### Create a SQL file

```yaml
-- flows/otto_demo/otto_goats_demo/components/transform_goats.sql
-- TODO: code to union & run distinct
-- Note: Use `SELECT DISTINCT [COLUMNS] FROM [UNION OF REF'D READ COMPONENTS]`
```

## Ensure the build is passing and run the Flow (agent mode)

Running in agent mode, ensure the build is successful. Run the Flow for the user, fixing runtime errors if possible get the Flow run succeeding.

