# imports
import ibis

# random comment
# functions
def clean(t: ibis.Table) -> ibis.Table:
    return t.rename("snake_case").distinct()
