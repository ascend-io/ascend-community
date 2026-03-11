# SQL Macros

Reusable Jinja SQL templates for cross-platform compatibility.

## Available Macros

### `utils.sql`

| Macro | Description | Example |
|-------|-------------|---------|
| `col(col)` | Column reference wrapper | `{{ col('name') }}` |
| `standardize(col_name)` | Lowercase and trim a column | `{{ standardize('email') }}` → `LOWER(TRIM(email))` |

## Usage

Macros are automatically available in SQL components:

```sql
SELECT
    id,
    {{ standardize('customer_name') }} AS customer_name
FROM {{ ref('raw_customers') }}
```