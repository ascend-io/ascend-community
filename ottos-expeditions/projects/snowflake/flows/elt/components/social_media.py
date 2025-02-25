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
        inlinked.rename(CONTENT="inlinked_content")
        .union(metabook.rename(CONTENT="metabook_content"))
        .union(metagram.rename(CONTENT="metagram_content"))
        .union(twitter.rename(CONTENT="tweet_content"))
    )
    return social_media