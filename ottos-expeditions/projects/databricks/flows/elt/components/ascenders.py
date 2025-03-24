from pyspark.sql import DataFrame

from ascend.resources import ref, pyspark
from ascend.application.context import ComponentExecutionContext


@pyspark(
    inputs=[
        ref("staff"),
        ref("routes"),
        ref("guides"),
        ref("route_closures"),
        ref("telemetry"),
        ref("weather"),
        ref("sales"),
        ref("social_media"),
        ref("feedback"),
    ]
)
def ascenders(
    staff: DataFrame,
    routes: DataFrame,
    guides: DataFrame,
    route_closures: DataFrame,
    telemetry: DataFrame,
    weather: DataFrame,
    sales: DataFrame,
    social_media: DataFrame,
    feedback: DataFrame,
    context: ComponentExecutionContext,
) -> DataFrame:
    # TODO: more interesting logic here
    return telemetry
