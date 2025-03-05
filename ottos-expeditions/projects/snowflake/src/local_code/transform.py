# imports
import snowflake


# functions
def clean(t: snowflake.snowpark.Table) -> snowflake.snowpark.Table:
    return t.distinct()
