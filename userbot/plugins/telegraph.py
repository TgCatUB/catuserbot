# telegraph utils for catuserbot

import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, hmention

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


@bot.on(admin_cmd(pattern="telegraph (media|text) ?(.*)"))
@bot.on(sudo_cmd(pattern="telegraph (media|text) ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(event, "<code>processing........</code>", "html")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "Created New Telegraph account {} for the current session. \n**Do not give this url to anyone, even if they say they are from Telegram!**".format(
                auth_url
            ),
        )
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "media":
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            await catevent.edit(
                "Downloaded to {} in {} seconds.".format(downloaded_file_name, ms),
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await catevent.edit("**Error : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                media_urls = upload_file(downloaded_file_name)
                jisan = "https://telegra.ph{}".format(media_urls[0])
                os.remove(downloaded_file_name)
                await catevent.edit(
                    f"<b><i>➥ Uploaded to :- <a href = {jisan}>Telegraph</a></i></b>\
                    \n<b><i>➥ Uploaded in {ms + ms_two} seconds .</i></b>\n<b><i>➥ Uploaded by :- {hmention}</i></b>",
                    parse_mode="html",
                    link_preview=True,
                )
        elif input_str == "text":
            user_object = await event.client.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await event.client.download_media(
                    r_message, Config.TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.now()
            ms = (end - start).seconds
            cat = f"https://telegra.ph/{response['path']}"
            await catevent.edit(
                f"<b><i>➥ Pasted to :- <a href = {cat}>Telegraph</a></i></b>\
                \n<b><i>➥ Pasted in {ms} seconds .</i></b>",
                parse_mode="html",
                link_preview=True,
            )
    else:
        await catevent.edit(
            "`Reply to a message to get a permanent telegra.ph link. (Inspired by @ControllerBot)`",
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CMD_HELP.update(
    {
        "telegraph": "__**PLUGIN NAME :** Telegraph__\
     \n\n📌** CMD ➥** `.telegraph media`\
     \n**USAGE   ➥  **Reply to any image or video to upload it to telgraph(video must be less than 5mb)\
     \n\n📌** CMD ➥** `.telegraph text`\
     \n**USAGE   ➥  **Reply to any text file or any message to paste it to telegraph\
    "
    }
)
