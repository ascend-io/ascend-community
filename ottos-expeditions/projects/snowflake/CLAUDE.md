# Otto's Expeditions Snowflake Project Guide

## Build Commands
- Run tests: `python -m pytest flows/elt/tests/`
- Run single test: `python -m pytest flows/elt/tests/test_ascenders_py.py`
- SQL test: `python -m pytest flows/elt/tests/test_ascenders_sql.sql`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party, then local modules
- **Formatting**: Use black formatter with default settings
- **Types**: Use type hints for function parameters and return values
- **Naming**:
  - Functions/variables: snake_case
  - Classes: PascalCase
  - Constants: UPPER_SNAKE_CASE
- **Error Handling**: Use TestResult for data validation in tests
- **Ascend Patterns**:
  - Use `@transform` decorator for data transformations
  - Use `@singular_test` for component tests
  - Reference data with `ref()` function

## Ascend Framework
- Components can be Python transforms or SQL templates
- Use .sql.jinja for SQL templates
- YAML component configs define connections and metadata