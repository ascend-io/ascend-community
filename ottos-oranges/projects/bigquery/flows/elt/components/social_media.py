from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("int_inlinked"),
        ref("int_metabook"),
        ref("int_metagram"),
        ref("int_twitter"),
    ]
)
def social_media(int_inlinked, int_metabook, int_metagram, int_twitter, context):
    social_media = (
        int_inlinked.rename(content="inlinked_content")
        .union(int_metabook.rename(content="metabook_content"))
        .union(int_metagram.rename(content="metagram_content"))
        .union(int_twitter.rename(content="tweet_content"))
    )
    return social_media
