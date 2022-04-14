#  Copyright (C) 2020  sandeep.n(π.$)
# credits to @mrconfused (@sandy1709)
import asyncio
import os
import re

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import (
    changemymind,
    deEmojify,
    fakegs,
    kannagen,
    moditweet,
    reply_id,
    trumptweet,
    tweets,
)

plugin_category = "fun"


@catub.cat_cmd(
    pattern="fakegs(?:\s|$)([\s\S]*)",
    command=("fakegs", plugin_category),
    info={
        "header": "Fake google search meme",
        "usage": "{tr}fakegs search query ; what you mean text",
        "examples": "{tr}fakegs Catuserbot ; One of the Popular userbot",
    },
)
async def nekobot(cat):
    "Fake google search meme"
    text = cat.pattern_match.group(1)
    reply_to_id = await reply_id(cat)
    if not text:
        if cat.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            return await edit_delete(cat, "`What should i search in google.`", 5)
    cate = await edit_or_reply(cat, "`Connecting to https://www.google.com/ ...`")
    text = deEmojify(text)
    if ";" in text:
        search, result = text.split(";")
    else:
        await edit_delete(
            cat,
            "__How should i create meme follow the syntax as show__ `.fakegs top text ; bottom text`",
            5,
        )
        return
    catfile = await fakegs(search, result)
    await asyncio.sleep(2)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@catub.cat_cmd(
    pattern="trump(?:\s|$)([\s\S]*)",
    command=("trump", plugin_category),
    info={
        "header": "trump tweet sticker with given custom text",
        "usage": "{tr}trump <text>",
        "examples": "{tr}trump Catuserbot is One of the Popular userbot",
    },
)
async def nekobot(cat):
    "trump tweet sticker with given custom text_"
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(cat)

    reply = await cat.get_reply_message()
    if not text:
        if cat.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(cat, "**Trump : **`What should I tweet`", 5)
    cate = await edit_or_reply(cat, "`Requesting trump to tweet...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    catfile = await trumptweet(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@catub.cat_cmd(
    pattern="modi(?:\s|$)([\s\S]*)",
    command=("modi", plugin_category),
    info={
        "header": "modi tweet sticker with given custom text",
        "usage": "{tr}modi <text>",
        "examples": "{tr}modi Catuserbot is One of the Popular userbot",
    },
)
async def nekobot(cat):
    "modi tweet sticker with given custom text"
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(cat)

    reply = await cat.get_reply_message()
    if not text:
        if cat.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(cat, "**Modi : **`What should I tweet`", 5)
    cate = await edit_or_reply(cat, "Requesting modi to tweet...")
    text = deEmojify(text)
    await asyncio.sleep(2)
    catfile = await moditweet(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@catub.cat_cmd(
    pattern="cmm(?:\s|$)([\s\S]*)",
    command=("cmm", plugin_category),
    info={
        "header": "Change my mind banner with given custom text",
        "usage": "{tr}cmm <text>",
        "examples": "{tr}cmm Catuserbot is One of the Popular userbot",
    },
)
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(cat)

    reply = await cat.get_reply_message()
    if not text:
        if cat.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(cat, "`Give text to write on banner, man`", 5)
    cate = await edit_or_reply(cat, "`Your banner is under creation wait a sec...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    catfile = await changemymind(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@catub.cat_cmd(
    pattern="kanna(?:\s|$)([\s\S]*)",
    command=("kanna", plugin_category),
    info={
        "header": "kanna chan sticker with given custom text",
        "usage": "{tr}kanna text",
        "examples": "{tr}kanna Catuserbot is One of the Popular userbot",
    },
)
async def nekobot(cat):
    "kanna chan sticker with given custom text"
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(cat)

    reply = await cat.get_reply_message()
    if not text:
        if cat.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(cat, "**Kanna : **`What should i show you`", 5)
    cate = await edit_or_reply(cat, "`Kanna is writing your text...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    catfile = await kannagen(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@catub.cat_cmd(
    pattern="tweet(?:\s|$)([\s\S]*)",
    command=("tweet", plugin_category),
    info={
        "header": "The desired person tweet sticker with given custom text",
        "usage": "{tr}tweet <username> ; <text>",
        "examples": "{tr}tweet iamsrk ; Catuserbot is One of the Popular userbot",
    },
)
async def nekobot(cat):
    "The desired person tweet sticker with given custom text"
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(cat)

    reply = await cat.get_reply_message()
    if not text:
        if cat.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(
                cat,
                "what should I tweet? Give some text and format must be like `.tweet username ; your text` ",
                5,
            )
    if ";" in text:
        username, text = text.split(";")
    else:
        await edit_delete(
            cat,
            "__what should I tweet? Give some text and format must be like__ `.tweet username ; your text`",
            5,
        )
        return
    cate = await edit_or_reply(cat, f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    catfile = await tweets(text, username)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)
