"""
Python code for re-use within an Ascend Project.

To re-use Python code across multiple Ascend Projects, it should
be distributed as a Python package and installed through the
Project or Flow configuration.
"""

import ibis


def clean(t: ibis.Table) -> ibis.Table:
    if ibis.get_backend(t).name == "snowflake":
        return t.rename("ALL_CAPS").distinct()
    return t.rename("snake_case").distinct()
