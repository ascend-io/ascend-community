# ruff: noqa
import ibis
import ibis.selectors as s

from faker import Faker

from ottos_oranges.lib.synthetic.common import *

from ottos_oranges.lib.synthetic.email import *
from ottos_oranges.lib.synthetic.store import *
from ottos_oranges.lib.synthetic.social import *
from ottos_oranges.lib.synthetic.common import *
from ottos_oranges.lib.synthetic.website import *
from ottos_oranges.lib.synthetic.telemetry import *

ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 40
ibis.options.repr.interactive.max_depth = 8
ibis.options.repr.interactive.max_columns = None

faker = Faker()

bootstrap_sql = """
create secret containername (
    TYPE AZURE,
    PROVIDER CONFIG,
    ACCOUNT_NAME 'codyascend'
);
""".strip(";").strip()


ibis.get_backend().raw_sql(bootstrap_sql)
