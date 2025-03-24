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
        .union(metabook.rename(content="metabook_content"))
        .union(metagram.rename(content="metagram_content"))
        .union(twitter.rename(content="tweet_content"))
    )
    return social_media
