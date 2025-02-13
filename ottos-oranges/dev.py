import ibis

from faker import Faker

from ottos_oranges.lib.synthetic.common import *  # noqa

from ottos_oranges.lib.synthetic.email import *  # noqa
from ottos_oranges.lib.synthetic.store import *  # noqa
from ottos_oranges.lib.synthetic.social import *  # noqa
from ottos_oranges.lib.synthetic.common import *  # noqa
from ottos_oranges.lib.synthetic.website import *  # noqa
from ottos_oranges.lib.synthetic.telemetry import *  # noqa

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
