import calendar
import json
import os
from datetime import datetime
from urllib.parse import quote

import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils, _format, reply_id

plugin_category = "tools"


@catub.cat_cmd(
    pattern="scan( -i)?$",
    command=("scan", plugin_category),
    info={
        "header": "To scan the replied file for virus.",
        "flag": {"i": "to get output as image."},
        "usage": ["{tr}scan", "{tr}scan -i"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if not event.reply_to_msg_id:
        return await edit_or_reply(event, "```Reply to any user message.```")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await edit_or_reply(event, "```reply to a media message```")
    chat = "@VS_Robot"
    if reply_message.sender.bot:
        return await edit_or_reply(event, "```Reply to actual users message.```")
    catevent = await edit_or_reply(event, " `Sliding my tip, of fingers over it`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await event.client.forward_messages(chat, reply_message)
            response1 = await conv.get_response()
            if response1.text:
                await event.client.send_read_acknowledge(conv.chat_id)
                return await catevent.edit(response1.text, parse_mode=_format.parse_pre)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            response3 = await conv.get_response()
            response4 = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await catevent.edit(
                "`You blocked `@VS_Robot` Unblock it and give a try`"
            )
        if not input_str:
            return await edit_or_reply(catevent, response4.text)
        await catevent.delete()
        await event.client.send_file(
            event.chat_id, response3.media, reply_to=(await reply_id(event))
        )


@catub.cat_cmd(
    pattern="decode$",
    command=("decode", plugin_category),
    info={
        "header": "To decode qrcode or barcode",
        "usage": "{tr}decode",
    },
)
async def parseqr(qr_e):
    "To decode qrcode or barcode"
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    # For .decode command, get QR Code/BarCode content from the replied photo.
    downloaded_file_name = await qr_e.client.download_media(
        await qr_e.get_reply_message(), Config.TEMP_DIR
    )
    # parse the Official ZXing webpage to decode the QRCode
    command_to_exec = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + downloaded_file_name + "",
        "https://zxing.org/w/decode",
    ]
    t_response, e_response = (await _catutils.runcmd(command_to_exec))[:2]
    if not t_response:
        return await edit_or_reply(qr_e, f"Failed to decode.\n`{e_response}`")
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await edit_or_reply(qr_e, qr_contents)
    if os.path.exists(downloaded_file_name):
        os.remove(downloaded_file_name)


@catub.cat_cmd(
    pattern="barcode ?(.*)",
    command=("barcode", plugin_category),
    info={
        "header": "To get barcode of given text.",
        "usage": "{tr}barcode <text>",
        "example": "{tr}barcode www.google.com",
    },
)
async def _(event):
    "to make barcode of given content."
    catevent = await edit_or_reply(event, "...")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = await reply_id(event)
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") + "\r\n" for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await event.client.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        os.remove(filename)
    except Exception as e:
        return await catevent.edit(str(e))
    end = datetime.now()
    ms = (end - start).seconds
    await edit_delete(catevent, "Created BarCode in {} seconds".format(ms))


@catub.cat_cmd(
    pattern="makeqr(?: |$)([\s\S]*)",
    command=("makeqr", plugin_category),
    info={
        "header": "To get makeqr of given text.",
        "usage": "{tr}makeqr <text>",
        "example": "{tr}makeqr www.google.com",
    },
)
async def make_qr(makeqr):
    "make a QR Code containing the given content."
    input_str = makeqr.pattern_match.group(1)
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = await reply_id(makeqr)
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = "".join(media.decode("UTF-8") + "\r\n" for media in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(
        makeqr.chat_id, "img_file.webp", reply_to=reply_msg_id
    )
    os.remove("img_file.webp")
    await makeqr.delete()


@catub.cat_cmd(
    pattern="cal (.*)",
    command=("cal", plugin_category),
    info={
        "header": "To get calendar of given month and year.",
        "usage": "{tr}cal year ; month",
        "examples": "{tr}cal 2021 ; 5",
    },
)
async def _(event):
    "To get calendar of given month and year."
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(";")
    if len(input_sgra) != 2:
        return await edit_delete(event, "**Syntax : **`.cal year ; month `", 5)

    yyyy = input_sgra[0]
    mm = input_sgra[1]
    try:
        output_result = calendar.month(int(yyyy.strip()), int(mm.strip()))
        await edit_or_reply(event, f"```{output_result}```")
    except Exception as e:
        await edit_delete(event, f"**Error:**\n`{str(e)}`", 5)


@catub.cat_cmd(
    pattern="ifsc (.*)",
    command=("ifsc", plugin_category),
    info={
        "header": "to get details of the relevant bank or branch.",
        "usage": "{tr}ifsc <ifsc code>",
        "examples": "{tr}ifsc SBIN0016086",
    },
)
async def _(event):
    "to get details of the relevant bank or branch."
    input_str = event.pattern_match.group(1)
    url = "https://ifsc.razorpay.com/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 200:
        return await edit_or_reply(event, "`{}`: {}".format(input_str, r.text))

    b = r.json()
    a = json.dumps(b, sort_keys=True, indent=4)
    # https://stackoverflow.com/a/9105132/4723940
    await edit_or_reply(event, str(a))


@catub.cat_cmd(
    pattern="color (.*)",
    command=("color", plugin_category),
    info={
        "header": "To get color pic of given hexa color code.",
        "usage": "{tr}color <colour code>",
        "examples": "{tr}color #ff0000",
    },
)
async def _(event):
    "To get color pic of given hexa color code."
    input_str = event.pattern_match.group(1)
    message_id = await reply_id(event)
    if not input_str.startswith("#"):
        return await edit_or_reply(
            event, "**Syntax : **`.color <color_code>` example : `.color #ff0000`"
        )
    try:
        usercolor = ImageColor.getrgb(input_str)
    except Exception as e:
        return await event.edit(str(e))
    else:
        im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
        im.save("cat.png", "PNG")
        input_str = input_str.replace("#", "#COLOR_")
        await event.client.send_file(
            event.chat_id,
            "cat.png",
            force_document=False,
            caption=input_str,
            reply_to=message_id,
        )
        os.remove("cat.png")
        await event.delete()


@catub.cat_cmd(
    pattern="xkcd(?: |$)(.*)",
    command=("xkcd", plugin_category),
    info={
        "header": "Searches for the query for the relevant XKCD comic.",
        "usage": "{tr}xkcd <query>",
    },
)
async def _(event):
    "Searches for the query for the relevant XKCD comic."
    catevent = await edit_or_reply(event, "`processiong...........`")
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url, params={"action": "xkcd", "query": quote(input_str)}
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if not r.ok:
        return await catevent.edit("xkcd n.{} not found!".format(xkcd_id))
    data = r.json()
    year = data.get("year")
    month = data["month"].zfill(2)
    day = data["day"].zfill(2)
    xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
    safe_title = data.get("safe_title")
    data.get("transcript")
    alt = data.get("alt")
    img = data.get("img")
    data.get("title")
    output_str = """[\u2060]({})**{}**
[XKCD ]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(
        img, input_str, xkcd_link, safe_title, alt, day, month, year
    )
    await catevent.edit(output_str, link_preview=True)
