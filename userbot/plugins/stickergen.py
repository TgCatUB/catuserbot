import os
import urllib

from .. import catub
from ..core.managers import edit_delete
from ..helpers.functions import clippy, convert_tosticker, deEmojify, higlighted_text
from ..helpers.utils import reply_id

plugin_category = "fun"


@catub.cat_cmd(
    pattern="(|b)quby(?:\s|$)([\s\S]*)",
    command=("quby", plugin_category),
    info={
        "header": "Make doge say anything.",
        "flags": {
            "b": "Give the sticker on background.",
        },
        "usage": [
            "{tr}quby <text/reply to msg>",
            "{tr}bquby <text/reply to msg>",
        ],
        "examples": [
            "{tr}quby Gib money",
            "{tr}bquby Gib money",
        ],
    },
)
async def quby(event):
    "Make a cool quby text sticker"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edit_delete(
            event, "__What is quby supposed to say? Give some text.__"
        )
    await edit_delete(event, "`Wait, processing.....`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    temp_name = "./temp/quby_temp.png"
    file_name = "./temp/quby.png"
    templait = urllib.request.urlretrieve(
        "https://telegra.ph/file/09f4df5a129758a2e1c9c.jpg", temp_name
    )
    if len(text) < 40:
        font = 80
        wrap = 1.4
        position = (100, 0)
    else:
        font = 60
        wrap = 1.2
        position = (0, 0)
    text = deEmojify(text)
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace="+4",
        position=position,
    )
    if cmd == "b":
        cat = convert_tosticker(file_name)
        await event.client.send_file(
            event.chat_id, cat, reply_to=reply_to_id, force_document=False
        )
    else:
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await event.delete()
    for files in (temp_name, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="(|b)blob(?:\s|$)([\s\S]*)",
    command=("blob", plugin_category),
    info={
        "header": "Give the sticker on background.",
        "flags": {
            "b": "To create knife sticker transparent.",
        },
        "usage": [
            "{tr}blob <text/reply to msg>",
            "{tr}bblob <text/reply to msg>",
        ],
        "examples": [
            "{tr}blob Gib money",
            "{tr}bblob Gib money",
        ],
    },
)
async def knife(event):
    "Make a blob knife text sticker"
    cmd = event.pattern_match.group(1).lower
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edit_delete(
            event, "__What is knife supposed to say? Give some text.__"
        )
    await edit_delete(event, "`Wait, processing.....`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    temp_name = "./temp/knife_temp.png"
    file_name = "./temp/knife.png"
    templait = urllib.request.urlretrieve(
        "https://telegra.ph/file/2188367c8c5f43c36aa59.jpg", temp_name
    )
    if len(text) < 50:
        font = 90
        wrap = 2
        position = (250, -450)
    else:
        font = 60
        wrap = 1.4
        position = (150, 500)
    text = deEmojify(text)
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace="-5",
        position=position,
        direction="upwards",
    )
    if cmd == "b":
        cat = convert_tosticker(file_name)
        await event.client.send_file(
            event.chat_id, cat, reply_to=reply_to_id, force_document=False
        )
    else:
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await event.delete()
    for files in (temp_name, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="(|h)doge(?:\s|$)([\s\S]*)",
    command=("doge", plugin_category),
    info={
        "header": "Make doge say anything.",
        "flags": {
            "h": "To create doge sticker with highligted text.",
        },
        "usage": [
            "{tr}doge <text/reply to msg>",
            "{tr}tdoge <text/reply to msg>",
        ],
        "examples": [
            "{tr}doge Gib money",
            "{tr}hdoge Gib money",
        ],
    },
)
async def doge(event):
    "Make a cool doge text sticker"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edit_delete(
            event, "__What is doge supposed to say? Give some text.__"
        )
    await edit_delete(event, "`Wait, processing.....`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    temp_name = "./temp/doge_temp.jpg"
    file_name = "./temp/doge.jpg"
    templait = urllib.request.urlretrieve(
        "https://telegra.ph/file/6f621b9782d9c925bd6c4.jpg", temp_name
    )
    text = deEmojify(text)
    font, wrap = (90, 2) if len(text) < 90 else (70, 2.5)
    bg, fg, alpha, ls = (
        ("black", "white", 255, "5") if cmd == "h" else ("white", "black", 0, "-40")
    )
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace=ls,
        position=(0, 10),
        align="left",
        background=bg,
        foreground=fg,
        transparency=alpha,
    )
    cat = convert_tosticker(file_name)
    await event.client.send_file(
        event.chat_id, cat, reply_to=reply_to_id, force_document=False
    )
    await event.delete()
    for files in (temp_name, file_name):
        if files and os.path.exists(files):
            os.remove(files)
