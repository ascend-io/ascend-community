import pandas as pd
import re

from ascend.resources import read
from ascend.application.context import ComponentExecutionContext


@read()
def read_guides(context: ComponentExecutionContext) -> pd.DataFrame:
    df = pd.read_csv(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/seed/guides.csv"
    )
    
    # Convert column names to snake_case
    df.columns = [
        re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower().replace(' ', '_').replace('-', '_')
        for col in df.columns
    ]
    
    return df