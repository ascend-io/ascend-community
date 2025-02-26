# imports
import ibis


# functions
def clean(t: ibis.Table) -> ibis.Table:
    return t.rename("UPPERCASE").distinct()
