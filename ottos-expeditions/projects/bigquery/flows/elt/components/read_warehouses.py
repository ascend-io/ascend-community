import pandas as pd

from ascend.resources import read
from ascend.application.context import ComponentExecutionContext


@read()
def read_warehouses(context: ComponentExecutionContext) -> pd.DataFrame:
    df = pd.read_csv(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/seed/warehouses.csv",
        sep=";",
    )

    return df