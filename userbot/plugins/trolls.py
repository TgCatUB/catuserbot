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

from telegraph import upload_file, exceptions
from userbot.utils import admin_cmd
from . import *
from userbot import CMD_HELP
import os
import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest as Get


@borg.on(admin_cmd(pattern="threats(?: |$)(.*)"))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await catmemes.edit("reply to a supported media file")
        return
    if replied.media:
        await catmemes.edit("passing to telegraph...")
    else:
        await catmemes.edit("reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemes.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await catmemes.edit("generating image..")
    else:
        await catmemes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await threats(cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


@borg.on(admin_cmd(pattern="trash(?: |$)(.*)"))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await catmemes.edit("reply to a supported media file")
        return
    if replied.media:
        await catmemes.edit("passing to telegraph...")
    else:
        await catmemes.edit("reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemes.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await catmemes.edit("generating image..")
    else:
        await catmemes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await trash(cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


@borg.on(admin_cmd(pattern="trap(?: |$)(.*)"))
async def catbot(catmemes):
    input_str = catmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        text1, text2 = input_str.split("|")
    else:
        await catmemes.edit("**Syntax :** reply to image or sticker with `.trap (name of the person to trap)|(trapper name)`")
        return
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await catmemes.edit("reply to a supported media file")
        return
    if replied.media:
        await catmemes.edit("passing to telegraph...")
    else:
        await catmemes.edit("reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemes.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await catmemes.edit("generating image..")
    else:
        await catmemes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await trap(text1, text2, cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)


@borg.on(admin_cmd(pattern="phub(?: |$)(.*)"))
async def catbot(catmemes):
    input_str = catmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        username, text = input_str.split("|")
    else:
        await catmemes.edit("**Syntax :** reply to image or sticker with `.phub (username)|(text in comment)`")
        return
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await catmemes.edit("reply to a supported media file")
        return
    if replied.media:
        await catmemes.edit("passing to telegraph...")
    else:
        await catmemes.edit("reply to a supported media file")
        return
    try:
        cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catmemes.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await catmemes.edit("generating image..")
    else:
        await catmemes.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await phcomment(cat, text, username)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id, cat, reply_to=replied)

CMD_HELP.update({"trolls":
                 "**TROLLS**\
      \n\n**Syntax :**`.threats` reply to image or sticker \
      \n**USAGE:**Changes the given pic to another pic which shows that pic content is threat to society as that of nuclear bomb .\
      \n\n**Syntax :**`.trash` reply to image or sticker\
      \n**USAGE : **Changes the given pic to another pic which shows that pic content is as equal as to trash(waste)\
      \n\n**Syntax :** reply to image or sticker with `.trap (name of the person to trap)|(trapper name)`\
      \n**USAGE :**Changes the given pic to another pic which shows that pic content is trapped in trap card\
      \n\n**Syntax :** reply to image or sticker with `.phub (username)|(text in comment)`\
      \n**USAGE :**Changes the given pic to another pic which shows that pic content as dp and shows a comment in phub with the given username\
      "
                 })
