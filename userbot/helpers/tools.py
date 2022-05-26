from html_telegraph_poster import TelegraphPoster


def media_type(message):
    if message:
        if message.photo:
            return "Photo"
        if message.audio:
            return "Audio"
        if message.voice:
            return "Voice"
        if message.video_note:
            return "Round Video"
        if message.gif:
            return "Gif"
        if message.sticker:
            return "Sticker"
        if message.video:
            return "Video"
        if message.document:
            return "Document"
    return None


async def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "CatUserbot"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=page_title,
        author=auth_name,
        author_url="https://t.me/catuserbot17",
        text=html_format_content,
    )
    return post_page["url"]
