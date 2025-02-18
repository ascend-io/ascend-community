# ruff: noqa
# imports
import os
import ibis
import ibis.selectors as s

from faker import Faker
from dotenv import load_dotenv

from ottos_oranges.lib.synthetic import *

# setup
load_dotenv()

ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 4
ibis.options.repr.interactive.max_depth = 8
ibis.options.repr.interactive.max_columns = None

faker = Faker()

# data connections
ddb_bootstrap_sql = """
create secret containername (
    TYPE AZURE,
    PROVIDER CONFIG,
    ACCOUNT_NAME 'codyascend'
);
""".strip(";").strip()

# ibis.get_backend().raw_sql(ddb_bootstrap_sql)
ddb_con = ibis.duckdb.connect()
ddb_con.raw_sql(ddb_bootstrap_sql)

# TODO: read this in from config? discuss local -> cloud in general
bq_con = ibis.bigquery.connect(project_id="ascend-io-cody", dataset_id="DEV3")
snow_con = ibis.snowflake.connect(
    account="ascendpartner",
    user="ASCEND_CODY_DEV",
    database="ASCEND_CODY_DEV",
    schema="ASCEND_CODY_DEV4",
    warehouse="ASCEND_CODY_DEV",
    role="ASCEND_CODY_DEV",
    password=os.getenv("SNOWFLAKE_PASSWORD"),
)
