import random
from os import remove
from random import choice
from urllib import parse

import nekos
import requests
from PIL import Image
from telethon import functions, types, utils

from ..utils import admin_cmd, sudo_cmd

BASE_URL = "https://headp.at/pats/{}"
PAT_IMAGE = "pat.webp"


@borg.on(admin_cmd(pattern="cat$"))
@borg.on(sudo_cmd(pattern="cat$", allow_sudo=True))
async def _(event):
    try:
        await event.delete()
    except BaseException:
        pass
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.cat()).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    img.seek(0)
    await event.client.send_file(
        event.chat_id, open("temp.webp", "rb"), reply_to=reply_to_id
    )
    remove("temp.webp")


# credit to @r4v4n4


@borg.on(admin_cmd(pattern="dab$", outgoing=True))
@borg.on(sudo_cmd(pattern="dab$", allow_sudo=True))
async def handler(event):
    blacklist = {
        1653974154589768377,
        1653974154589768312,
        1653974154589767857,
        1653974154589768311,
        1653974154589767816,
        1653974154589767939,
        1653974154589767944,
        1653974154589767912,
        1653974154589767911,
        1653974154589767910,
        1653974154589767909,
        1653974154589767863,
        1653974154589767852,
        1653974154589768677,
    }
    try:
        await event.delete()
    except BaseException:
        pass
    docs = [
        utils.get_input_document(x)
        for x in (
            await borg(
                functions.messages.GetStickerSetRequest(
                    types.InputStickerSetShortName("DabOnHaters")
                )
            )
        ).documents
        if x.id not in blacklist
    ]
    await event.respond(file=random.choice(docs))


@borg.on(admin_cmd(pattern="brain$", outgoing=True))
@borg.on(sudo_cmd(pattern="brain$", allow_sudo=True))
async def handler(event):
    blacklist = {}
    try:
        await event.delete()
    except BaseException:
        pass
    docs = [
        utils.get_input_document(x)
        for x in (
            await borg(
                functions.messages.GetStickerSetRequest(
                    types.InputStickerSetShortName("supermind")
                )
            )
        ).documents
        if x.id not in blacklist
    ]
    await event.respond(file=random.choice(docs))


# HeadPat Module for Userbot (http://headp.at)
# cmd:- .pat username or reply to msg
# By:- git: jaskaranSM tg: @Zero_cool7870


@borg.on(admin_cmd(pattern="pat$", outgoing=True))
@borg.on(sudo_cmd(pattern="pat$", allow_sudo=True))
async def lastfm(event):
    try:
        await event.delete()
    except BaseException:
        pass
    resp = requests.get("http://headp.at/js/pats.json")
    pats = resp.json()
    pat = BASE_URL.format(parse.quote(choice(pats)))
    with open(PAT_IMAGE, "wb") as f:
        f.write(requests.get(pat).content)
    await event.client.send_file(
        event.chat_id, PAT_IMAGE, reply_to=event.reply_to_msg_id
    )
    remove(PAT_IMAGE)
