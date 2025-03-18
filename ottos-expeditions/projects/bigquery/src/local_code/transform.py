# imports
import ibis


# functions
# TODO: handle snowflake vs databricks
def clean(t: ibis.Table) -> ibis.Table:
    return t.rename("snake_case").distinct()
