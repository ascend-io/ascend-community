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
        inlinked.rename(content="inlinked_content")
        .union(metabook.rename(content="metabook_content"))
        .union(metagram.rename(content="metagram_content"))
        .union(twitter.rename(content="tweet_content"))
    )
    return social_media
