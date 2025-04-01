"""
Python code for re-usable data transformation logic.
"""

import ibis


def clean(t: ibis.Table) -> ibis.Table:
    return t.rename("ALL_CAPS").distinct()
