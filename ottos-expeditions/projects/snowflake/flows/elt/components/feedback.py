from ascend.resources import ref, snowpark

from snowflake.snowpark.types import StringType
from snowflake.snowpark.functions import lit


@snowpark(
    inputs=[
        ref("feedback_ascenders"),
        ref("feedback_stores"),
        ref("feedback_website"),
    ]
)
def feedback(
    feedback_ascenders,
    feedback_stores,
    feedback_website,
    context,
):
    feedback = (
        feedback_ascenders.with_columns(
            ["STORE_ID", "USER_ID"],
            [lit(None, StringType()), lit(None, StringType())],
        )
        .union(
            feedback_stores.with_columns(
                ["ASCENDER_ID", "USER_ID", "STORE_ID"],
                [
                    lit(None, StringType()),
                    lit(None, StringType()),
                    feedback_stores["STORE_ID"].cast(StringType()),
                ],
            )
        )
        .union(
            feedback_website.with_columns(
                ["FEEDBACK", "ASCENDER_ID", "STORE_ID"],
                [
                    lit(None, StringType()),
                    lit(None, StringType()),
                    lit("website", StringType()),
                ],
            )
        )
    )

    return feedback
