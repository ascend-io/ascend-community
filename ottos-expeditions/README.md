# Otto's Expeditions

[![PyPI](https://img.shields.io/pypi/v/ottos-expeditions.svg)](https://pypi.org/project/ottos-expeditions)

Python package and Ascend Projects for Otto's Expeditions!

## Layout

| Path | Description |
| --- | --- |
| [`src/`](src) | Python package source code. |
| [`projects/`](projects) | Ascend projects source code. |
| [`pyproject.toml`](pyproject.toml) | Python project configuration. |
| [`uv.lock`](uv.lock) | Python package lock file. |
| [`justfile`](justfile) | Justfile for running tasks. |
| [`dev.py`](dev.py) | Development script. |

## Running the Ascend projects

See [Ascend's getting started documentation](https://docs.ascend.io/getting-started) to get started with Ascend.

## Python installation

Using `uv` is recommended.

### PyPI

Install the package:

```bash
uv pip install ottos-expeditions
```

### Development

Clone the repo:

```bash
git clone git@github.com:ascend-io/ascend-community.git
```

or:

```bash
gh repo clone ascend-io/ascend-community
```

Change into the directory:

```bash
cd ascend-community/ottos-expeditions
```

Install `just` and `uv`:

```
brew install just uv
```

`just setup`:

```bash
just setup
```

Source the Python vritual environment:

```bash
. .venv/bin/activate
```

Run the data generation:

```bash
ottos-expeditions datagen --days 7
```
