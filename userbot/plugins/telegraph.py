# telegraph utils for catuserbot
import os
import random
import string
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.utils import get_display_name
from urlextract import URLExtract

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from . import BOTLOG, BOTLOG_CHATID, catub, reply_id

LOGS = logging.getLogger(__name__)

plugin_category = "utils"

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


@catub.cat_cmd(
    pattern="(t(ele)?g(raph)?) ?(m|t|media|text)(?:\s|$)([\s\S]*)",
    command=("telegraph", plugin_category),
    info={
        "header": "To get telegraph link.",
        "description": "Reply to text message to paste that text on telegraph you can also pass input along with command \
            So that to customize title of that telegraph and reply to media file to get sharable link of that media(atmost 5mb is supported)",
        "options": {
            "m or media": "To get telegraph link of replied sticker/image/video/gif.",
            "t or text": "To get telegraph link of replied text you can use custom title.",
        },
        "usage": [
            "{tr}tgm",
            "{tr}tgt <title(optional)>",
            "{tr}telegraph media",
            "{tr}telegraph text <title(optional)>",
        ],
    },
)  # sourcery no-me  # sourcery skip: low-code-quality, low-code-qualitytrics
async def _(event):
    "To get telegraph link."
    catevent = await edit_or_reply(event, "`processing........`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Created New Telegraph account {auth_url} for the current session. \n**Do not give this url to anyone, even if they say they are from Telegram!**",
        )
    optional_title = event.pattern_match.group(5)
    if not event.reply_to_msg_id:
        return await catevent.edit(
            "`Reply to a message to get a permanent telegra.ph link.`",
        )

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()
    if input_str in ["media", "m"]:
        downloaded_file_name = await event.client.download_media(
            r_message, Config.TEMP_DIR
        )
        await catevent.edit(f"`Downloaded to {downloaded_file_name}`")
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            media_urls = upload_file(downloaded_file_name)
        except exceptions.TelegraphException as exc:
            await catevent.edit(f"**Error : **\n`{exc}`")
            os.remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms = (end - start).seconds
            os.remove(downloaded_file_name)
            await catevent.edit(
                f"**link : **[telegraph](https://graph.org{media_urls[0]})\
                    \n**Time Taken : **`{ms} seconds.`",
                link_preview=True,
            )
    elif input_str in ["text", "t"]:
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        # apparently, all Users do not have last_name field
        if optional_title:
            title_of_page = optional_title
        page_content = r_message.message
        if r_message.media:
            if page_content != "":
                title_of_page = page_content
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8") + "\n"
            os.remove(downloaded_file_name)
        page_content = page_content.replace("\n", "<br>")
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
        except Exception as e:
            LOGS.info(e)
            title_of_page = "".join(
                random.choice(list(string.ascii_lowercase + string.ascii_uppercase))
                for _ in range(16)
            )
            response = telegraph.create_page(title_of_page, html_content=page_content)
        end = datetime.now()
        ms = (end - start).seconds
        cat = f"https://graph.org/{response['path']}"
        await catevent.edit(
            f"**link : ** [telegraph]({cat})\
                 \n**Time Taken : **`{ms} seconds.`",
            link_preview=True,
        )


@catub.cat_cmd(
    pattern="ctg(?: |$)([\s\S]*)",
    command=("ctg", plugin_category),
    info={
        "header": "Reply to link To get link preview using telegrah.s.",
        "usage": "{tr}ctg <reply/text>",
    },
)
async def ctg(event):
    "To get link preview"
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me link to search..**", 20)
    urls = extractor.find_urls(input_str)
    if not urls:
        return await edit_delete(event, "**There no link to search in the text..**", 20)
    chat = "@chotamreaderbot"
    catevent = await edit_or_reply(event, "```Processing...```")
    async with event.client.conversation(chat) as conv:
        try:
            msg_flag = await conv.send_message(urls[0])
        except YouBlockedUserError:
            await edit_or_reply(
                catevent, "**Error:** Trying to unblock & retry, wait a sec..."
            )
            await catub(unblock("chotamreaderbot"))
            msg_flag = await conv.send_message(urls[0])
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        if response.text.startswith(""):
            await edit_or_reply(catevent, "Am I Dumb Or Am I Dumb?")
        else:
            await catevent.delete()
            await event.client.send_message(
                event.chat_id, response, reply_to=reply_to_id, link_preview=True
            )
        await delete_conv(event, chat, msg_flag)
