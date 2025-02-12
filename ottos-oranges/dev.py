import ibis

from faker import Faker

from ottos_oranges.datagen import *  # noqa
from ottos_oranges.sources.email import *  # noqa
from ottos_oranges.sources.store import *  # noqa
from ottos_oranges.sources.social import *  # noqa
from ottos_oranges.sources.common import *  # noqa
from ottos_oranges.sources.website import *  # noqa
from ottos_oranges.sources.telemetry import *  # noqa

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
