# oeutils

Internal utilities for developing Otto's Expeditions.

## motivation

Otto's Expeditions is a few things:

- a fictional company for Ascend's use
- an Ascend Project (in fact, several! more on that throughout...)
- a PyPI package

The PyPI package installs a command-line interface (CLI) invoked as `ottos-expeditions`, which is used to generate the synthetic data used by the project. In general in the community project, we should develop software for public consumption.

However, we also want to use the Otto's Expeditions project like a real customer would. This presents a challenge since the project is tied to a given Data Plane (BigQuery, Databricks, Snowflake). As internal employees of Ascend, we typically want to work across all of these Data Planes, and perhaps even features that aren't public like the DuckDB Data Plane.

## the `mesh` project

To allow us to work like our users will, we develop internally on the `mesh` project, which combines Otto's Expeditions for every supported data plane and a few internal-only features. Key differences between the `mesh` project and the public Otto's Expeditions projects are:

- using `-<data-plane>` postfixes on Flows and other resources
- supporting multiple Data Planes in the Profiles
- Workspace Profiles for each Ascend employee
- Profiles are filled in (i.e. not using placeholders)
- a BYOVault is used

## the `oeutils` code

We do not want to maintain 4 separate Otto's Expeditions projects. Instead, we maintain the `mesh` project and `unmesh` it to generate the 3 public Otto's Expeditions projects for each Data Plane. This is the purpose of the `oeutils` code.

### language choice

Go was chosen for the `oeutils` code for a few reasons:

- much faster than Python for this type of thing, and I thought it might matter (it doesn't)
- incredibly simple and I thought it'd be good for AI-assisted development (it is!)
- I think we/I might want to lean more on Go

The code is simple enough that we could easily convert it to other languages if the choice made is a burden.

## using `oeutils`

While you can install the CLI, it's strongly recommended not to use `oeutils` directly. Instead, from the `ottos-expeditions` directory (parent directory of `oeutils`), run:

```bash
just unmesh
```
