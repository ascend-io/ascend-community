# Python Source Code

Shared Python modules automatically added to the Python path.

## Modules

### `ascend_project_code/transform.py`

Reusable transformation utilities:

- `clean(t: ibis.Table)` - Standardize column names and deduplicate rows

### `nps_analysis.py`

Ascend Module for generating NPS analysis compound components. Configurable categories and thresholds for customer satisfaction analysis.

## Usage

Import modules directly in Python components:

```python
from ascend_project_code.transform import clean
from nps_analysis import NPSAnalysis
```

## Adding New Modules

1. Create a `.py` file in `src/` or a subdirectory
2. Import it in your Python components

> [!NOTE]
> For code shared across multiple projects, distribute as a Python package via `pyproject.toml`.