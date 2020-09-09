"""
credits to @mrconfused and @sandy1709
"""
import glob

#    Copyright (C) 2020  sandeep.n(π.$)
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import catmusic, catmusicvideo


@borg.on(admin_cmd(pattern="song( (.*)|$)"))
@borg.on(sudo_cmd(pattern="song( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await edit_or_reply(event, "`What I am Supposed to find `")
        return
    event = await edit_or_reply(event, "`wi8..! I am finding your song....`")
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    await catmusic(str(query), "128k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("yeah..! i found something wi8..🥰")
    else:
        await event.edit(f"Sorry..! i can't find anything with `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    await borg.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@borg.on(admin_cmd(pattern="song320( (.*)|$)"))
@borg.on(sudo_cmd(pattern="song320( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        event = await edit_or_reply(event, "`What I am Supposed to find `")
        return
    event = await edit_or_reply(event, "`wi8..! I am finding your song....`")
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    await catmusic(str(query), "320k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("yeah..! i found something wi8..🥰")
    else:
        await event.edit(f"Sorry..! i can't find anything with `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    await borg.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@borg.on(admin_cmd(pattern="vsong( (.*)|$)"))
@borg.on(sudo_cmd(pattern="vsong( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await edit_or_reply(event, "What I am Supposed to find")
        return
    event = await edit_or_reply(event, "wi8..! I am finding your videosong....")
    await catmusicvideo(query, event)
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    l = glob.glob(("./temp/*.mp4"))
    if l:
        await event.edit("yeah..! i found something wi8..🥰")
    else:
        await event.edit(f"Sorry..! i can't find anything with `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    await borg.send_file(
        event.chat_id,
        loa,
        thumb=catthumb,
        caption=query,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp4")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


CMD_HELP.update(
    {
        "getmusic": "`.song` query or `.song` reply to song name :\
    \nUSAGE:finds the song you entered in query and sends it"
    }
)
