# plugin by @deleteduser420
# ported to telethon by @mrconfused (@sandy1709)
import os

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import humanbytes, post_to_telegraph
from ..helpers.utils import _catutils, _format

plugin_category = "utils"
LOGS = logging.getLogger(__name__)


async def file_data(reply):
    hmm = ""
    if reply.file.name:
        hmm += f"Name  :  {reply.file.name}<br>"
    if reply.file.mime_type:
        hmm += f"Mime type  :  {reply.file.mime_type}<br>"
    if reply.file.size:
        hmm += f"Size  :  {humanbytes(reply.file.size)}<br>"
    if reply.date:
        hmm += f"Date  :  {_format.yaml_format(reply.date)}<br>"
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
            \n {_format.yaml_format(reply.file.sticker_set)}<br>"
    try:
        if reply.media.document.thumbs:
            hmm += f"Thumb  :\
                \n {_format.yaml_format(reply.media.document.thumbs[-1])}<br>"
    except Exception as e:
        LOGS.info(str(e))
    return hmm


@catub.cat_cmd(
    pattern="minfo$",
    command=("minfo", plugin_category),
    info={
        "header": "To get media information.",
        "description": "reply to media to get information about it",
        "usage": "{tr}minfo",
    },
)
async def mediainfo(event):
    "Media information"
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
    out, err, ret, pid = await _catutils.runcmd(f"mediainfo '{file_path}'")
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
