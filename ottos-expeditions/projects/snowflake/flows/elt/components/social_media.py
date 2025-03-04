from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("inlinked"),
        ref("metabook"),
        ref("metagram"),
        ref("twitter"),
    ]
)
def social_media(inlinked, metabook, metagram, twitter, context):
    social_media = (
        inlinked.rename(CONTENT="INLINKED_CONTENT")
        .union(metabook.rename(CONTENT="METABOOK_CONTENT"))
        .union(metagram.rename(CONTENT="METAGRAM_CONTENT"))
        .union(twitter.rename(CONTENT="TWEET_CONTENT"))
    )
    return social_media