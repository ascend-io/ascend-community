import pandas as pd
from ascend.application.context import ComponentExecutionContext
from ascend.resources import read


@read()
def read_guides(context: ComponentExecutionContext) -> pd.DataFrame:
    df = pd.read_csv("gs://ascend-ottos-expeditions/lakev0/seed/guides.csv")
    return df
