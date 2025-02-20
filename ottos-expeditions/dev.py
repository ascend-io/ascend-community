# ruff: noqa
# imports
import os
import yaml
import ibis
import polars as pl
import ibis.selectors as s

from io import BytesIO, StringIO
from faker import Faker
from dotenv import load_dotenv

from ottos_expeditions.lib.synthetic import *

# setup
load_dotenv()

ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 4
ibis.options.repr.interactive.max_depth = 8
ibis.options.repr.interactive.max_columns = None

faker = Faker()

# data connections
## duckdb
ddb_bootstrap_sql = """
create secret containername (
    TYPE AZURE,
    PROVIDER CONFIG,
    ACCOUNT_NAME 'codyascend'
);
""".strip(";").strip()
ddb_con = ibis.duckdb.connect()
ddb_con.raw_sql(ddb_bootstrap_sql)

## bigquery
bq_dev_profile = yaml.safe_load(
    open(os.path.join("projects", "bigquery", "profiles", "dev.yaml"))
)
project_id = bq_dev_profile["profile"]["parameters"]["gcp"]["project_id"]
dataset_id = bq_dev_profile["profile"]["parameters"]["bigquery"]["dataset"]
bq_con = ibis.bigquery.connect(project_id=project_id, dataset_id=dataset_id)

## snowflake
snow_dev_profile = yaml.safe_load(
    open(os.path.join("projects", "snowflake", "profiles", "dev.yaml"))
)
snow_con = ibis.snowflake.connect(
    account=snow_dev_profile["profile"]["parameters"]["snowflake"]["account"],
    user=snow_dev_profile["profile"]["parameters"]["snowflake"]["user"],
    database=snow_dev_profile["profile"]["parameters"]["snowflake"]["database"],
    schema=snow_dev_profile["profile"]["parameters"]["snowflake"]["schema"],
    warehouse=snow_dev_profile["profile"]["parameters"]["snowflake"]["warehouse"],
    role=snow_dev_profile["profile"]["parameters"]["snowflake"]["role"],
    password=os.getenv("SNOWFLAKE_PASSWORD"),
)
