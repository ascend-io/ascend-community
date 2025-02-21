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
project_id = bq_dev_profile["profile"]["parameters"]["gcp_project_id"]
dataset_id = bq_dev_profile["profile"]["parameters"]["bigquery_dataset"]
bq_con = ibis.bigquery.connect(project_id=project_id, dataset_id=dataset_id)

## snowflake
# snow_dev_profile = yaml.safe_load(
#     open(os.path.join("projects", "snowflake", "profiles", "dev.yaml"))
# )
# snow_con = ibis.snowflake.connect(
#     account="ascendpartner",
#     user="ASCEND_CODY_DEV",
#     database="ASCEND_CODY_DEV",
#     schema="ASCEND_CODY_DEV4",
#     warehouse="ASCEND_CODY_DEV",
#     role="ASCEND_CODY_DEV",
#     password=os.getenv("SNOWFLAKE_PASSWORD"),
# )
