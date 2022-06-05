# credits to @mrconfused and @sandy1709
#    Copyright (C) 2020  sandeep.n(π.$)

import os

from telegraph import exceptions, upload_file

from userbot import Convert, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from . import deEmojify, phcomment, threats, trap, trash

plugin_category = "fun"


@catub.cat_cmd(
    pattern="trash$",
    command=("trash", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}trash",
    },
)
async def _(event):
    "image meme creator."
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="trash.png", rgb=True
    )
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await trash(cat)
    os.remove(output[1])
    await output[0].delete()
    await event.client.send_file(event.chat_id, cat, reply_to=catid)


@catub.cat_cmd(
    pattern="threats$",
    command=("threats", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}threats",
    },
)
async def _(event):
    "image meme creator."
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="threats.png", rgb=True
    )
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await threats(cat)
    await output[0].delete()
    os.remove(output[1])
    await event.client.send_file(event.chat_id, cat, reply_to=catid)


@catub.cat_cmd(
    pattern="trap(?:\s|$)([\s\S]*)",
    command=("trap", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "Description": "creates a trap card",
        "usage": "{tr}trap (name of the person to trap) ; (trapper name)",
    },
)
async def _(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        return await edit_or_reply(
            event,
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap);(trapper name)`",
        )
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="trap.png", rgb=True
    )
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await trap(text1, text2, cat)
    await output[0].delete()
    os.remove(output[1])
    await event.client.send_file(event.chat_id, cat, reply_to=catid)


@catub.cat_cmd(
    pattern="phub(?:\s|$)([\s\S]*)",
    command=("phub", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "description": "pornhub comment creator",
        "usage": "{tr}phub (username);(text in comment)",
    },
)
async def _(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        username, text = input_str.split(";")
    else:
        return await edit_or_reply(
            event,
            "**Syntax :** reply to image or sticker with `.phub (username);(text in comment)`",
        )
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="phub.png", rgb=True
    )
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )

    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await phcomment(cat, text, username)
    await output[0].delete()
    os.remove(output[1])
    await event.client.send_file(event.chat_id, cat, reply_to=catid)
