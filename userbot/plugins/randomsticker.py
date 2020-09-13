# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" Command: .dab , .brain
credit: lejend @r4v4n4
"""
import random
from os import remove
from random import choice
from urllib import parse

import requests
from telethon import events, functions, types, utils

from userbot.utils import admin_cmd

BASE_URL = "https://headp.at/pats/{}"
PAT_IMAGE = "pat.jpg"


def choser(cmd, pack, blacklist={}):
    docs = None

    @borg.on(events.NewMessage(pattern=rf"\.{cmd}", outgoing=True))
    async def handler(event):
        await event.delete()
        nonlocal docs
        if docs is None:
            docs = [
                utils.get_input_document(x)
                for x in (
                    await borg(
                        functions.messages.GetStickerSetRequest(
                            types.InputStickerSetShortName(pack)
                        )
                    )
                ).documents
                if x.id not in blacklist
            ]
        await event.respond(file=random.choice(docs))


choser("brain", "supermind")
choser(
    "dab",
    "DabOnHaters",
    {
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
    },
)

# HeadPat Module for Userbot (http://headp.at)
# cmd:- .pat username or reply to msg
# By:- git: jaskaranSM tg: @Zero_cool7870


@borg.on(admin_cmd(pattern="pat ?(.*)", outgoing=True))
async def lastfm(event):
    if event.fwd_from:
        return
    username = event.pattern_match.group(1)
    if not username and not event.reply_to_msg_id:
        await event.edit("`Reply to a message or provide username`")
        return
    resp = requests.get("http://headp.at/js/pats.json")
    pats = resp.json()
    pat = BASE_URL.format(parse.quote(choice(pats)))
    await event.delete()
    with open(PAT_IMAGE, "wb") as f:
        f.write(requests.get(pat).content)
    if username:
        await borg.send_file(event.chat_id, PAT_IMAGE, caption=username)
    else:
        await borg.send_file(event.chat_id, PAT_IMAGE, reply_to=event.reply_to_msg_id)
    remove(PAT_IMAGE)
