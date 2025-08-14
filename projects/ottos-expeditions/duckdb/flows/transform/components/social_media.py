import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("inlinked"),
        ref("metabook"),
        ref("metagram"),
        ref("twitter"),
    ]
)
def social_media(
    inlinked: ibis.Table,
    metabook: ibis.Table,
    metagram: ibis.Table,
    twitter: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    social_media = (
        inlinked.rename(content="inlinked_content")
        .mutate(timestamp=ibis._["timestamp"].cast("timestamp"))
        .union(
            metabook.rename(content="metabook_content").mutate(
                timestamp=ibis._["timestamp"].cast("timestamp")
            )
        )
        .union(
            metagram.rename(content="metagram_content").mutate(
                timestamp=ibis._["timestamp"].cast("timestamp")
            )
        )
        .union(
            twitter.rename(content="tweet_content").mutate(
                timestamp=ibis._["timestamp"].cast("timestamp")
            )
        )
    )
    return social_media
