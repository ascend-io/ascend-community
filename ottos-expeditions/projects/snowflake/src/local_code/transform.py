# imports
import ibis


# functions
def clean(t: ibis.Table) -> ibis.Table:
    return t.rename("snake_case").rename("ALL_CAPS").distinct()
