# plugin by @deleteduser420
# ported to telethon by @mrconfused (@sandy1709)

import os

from html_telegraph_poster import TelegraphPoster

from ..utils import admin_cmd, edit_or_reply, humanbytes, sudo_cmd
from . import CMD_HELP, runcmd, yaml_format


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


async def file_data(reply):
    hmm = ""
    if reply.file.name:
        hmm += f"Name  :  {reply.file.name}<br>"
    if reply.file.mime_type:
        hmm += f"Mime type  :  {reply.file.mime_type}<br>"
    if reply.file.size:
        hmm += f"Size  :  {humanbytes(reply.file.size)}<br>"
    if reply.date:
        hmm += f"Date  :  {yaml_format(reply.date)}<br>"
    if reply.file.id:
        hmm += f"Id  :  {reply.file.id}<br>"
    if reply.file.ext:
        hmm += f"Extension  :  '{reply.file.ext}'<br>"
    if reply.file.emoji:
        hmm += f"Emoji  :  {reply.file.emoji}<br>"
    if reply.file.title:
        hmm += f"Title  :  {reply.file.title}<br>"
    if reply.file.performer:
        hmm += f"Performer  :  {reply.file.performer}<br>"
    if reply.file.duration:
        hmm += f"Duration  :  {reply.file.duration} seconds<br>"
    if reply.file.height:
        hmm += f"Height :  {reply.file.height}<br>"
    if reply.file.width:
        hmm += f"Width  :  {reply.file.width}<br>"
    if reply.file.sticker_set:
        hmm += f"Sticker set  :\
            \n {yaml_format(reply.file.sticker_set)}<br>"
    try:
        if reply.media.document.thumbs:
            hmm += f"Thumb  :\
                \n {yaml_format(reply.media.document.thumbs[-1])}<br>"
    except:
        pass
    return hmm


@bot.on(admin_cmd(pattern="minfo$"))
@bot.on(sudo_cmd(pattern="minfo$", allow_sudo=True))
async def mediainfo(event):
    X_MEDIA = None
    reply = await event.get_reply_message()
    if not reply:
        await edit_or_reply(event, "reply to media to get info")
        return
    if not reply.media:
        await edit_or_reply(event, "reply to media to get info")
        return
    catevent = await edit_or_reply(event, "`Gathering ...`")
    X_MEDIA = reply.file.mime_type
    if (not X_MEDIA) or (X_MEDIA.startswith(("text"))):
        return await catevent.edit("Reply To a supported Media Format")
    hmm = await file_data(reply)
    file_path = await reply.download_media(Config.TEMP_DIR)
    out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
    if not out:
        out = "Not Supported"
    body_text = f"""
<h2>JSON</h2>
<code>
{hmm}
</code>
<h2>DETAILS</h2>
<code>
{out} 
</code>"""
    link = await post_to_telegraph(f"{X_MEDIA}", body_text)
    await catevent.edit(
        f"ℹ️  <b>MEDIA INFO:  <a href ='{link}' > {X_MEDIA}</a></b>",
        parse_mode="HTML",
        link_preview=True,
    )
    os.remove(file_path)


CMD_HELP.update(
    {
        "mediainfo": "**Plugin :** `mediainfo`\
      \n\n**Syntax : **`.minfo` reply to media \
      \n**Usage : ** shows you the media information."
    }
)
