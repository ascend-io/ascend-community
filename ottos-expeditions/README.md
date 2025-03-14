# Otto's Expeditions

[![PyPI](https://img.shields.io/pypi/v/ottos-expeditions.svg)](https://pypi.org/project/ottos-expeditions)

Welcome to Otto's Expeditions, an Ascend adventure! 🚀
This repository contains both the Python package and Ascend Projects that power Otto's journey.

## Repository Structure

| Path | Description |
| --- | --- |
| [`src/`](src) | Core Python package source code |
| [`projects/`](projects) | Ascend projects implementation |
| [`pyproject.toml`](pyproject.toml) | Python project configuration |
| [`uv.lock`](uv.lock) | Python package dependency lock file |
| [`justfile`](justfile) | Task automation configuration |
| [`dev.py`](dev.py) | Development utilities script |

## Getting Started

Before running the Ascend projects, ensure you have a working Ascend instance. New to Ascend? Check out the [Ascend Getting Started Guide](https://docs.ascend.io/getting-started).

### Prerequisites

Install the required tools:

```bash
brew install just uv
```

### Installation Options

#### Option 1: Install from PyPI

1. Create and activate a UV virtual environment:
```bash
uv venv ottos_env
source ottos_env/bin/activate
```

2. Install the package:
```bash
uv pip install ottos-expeditions
```

#### Option 2: Development Setup

1. Clone the repository:
```bash
# Using SSH
git clone git@github.com:ascend-io/ascend-community.git

# Or using GitHub CLI
gh repo clone ascend-io/ascend-community
```

2. Navigate to the project directory:
```bash
cd ascend-community/ottos-expeditions
```

3. Set up the development environment:
```bash
just setup
```

4. Activate the virtual environment:
```bash
. .venv/bin/activate
```

### Generate Sample Data

To generate sample data for testing:
```bash
ottos-expeditions datagen --days 7
```
