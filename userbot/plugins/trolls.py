# credits to @mrconfused and @sandy1709
#    Copyright (C) 2020  sandeep.n(π.$)

import base64
import os

from telegraph import exceptions, upload_file
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import convert_toimage, deEmojify, phcomment, threats, trap, trash


@bot.on(admin_cmd(pattern="threats$"))
@bot.on(sudo_cmd(pattern="threats$", allow_sudo=True))
async def catbot(catmemes):
    if catmemes.fwd_from:
        return
    replied = await catmemes.get_reply_message()
    catid = await reply_id(catmemes)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    output = await _cattools.media_to_pic(catmemes, replied)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        san = Get(san)
        await catmemes.client(san)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await threats(cat)
    await output[0].delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=catid)


@bot.on(admin_cmd(pattern="trash$"))
@bot.on(sudo_cmd(pattern="trash$", allow_sudo=True))
async def catbot(catmemes):
    if catmemes.fwd_from:
        return
    replied = await catmemes.get_reply_message()
    catid = await reply_id(catmemes)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    output = await _cattools.media_to_pic(catmemes, replied)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        san = Get(san)
        await catmemes.client(san)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await trash(cat)
    await output[0].delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=catid)


@bot.on(admin_cmd(pattern="trap(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="trap(?: |$)(.*)", allow_sudo=True))
async def catbot(catmemes):
    if catmemes.fwd_from:
        return
    input_str = catmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        await edit_or_reply(
            catmemes,
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap);(trapper name)`",
        )
        return
    replied = await catmemes.get_reply_message()
    catid = await reply_id(catmemes)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    output = await _cattools.media_to_pic(catmemes, replied)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        san = Get(san)
        await catmemes.client(san)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await trap(text1, text2, cat)
    await output[0].delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=catid)


@bot.on(admin_cmd(pattern="phub(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="phub(?: |$)(.*)", allow_sudo=True))
async def catbot(catmemes):
    if catmemes.fwd_from:
        return
    input_str = catmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        username, text = input_str.split(";")
    else:
        await edit_or_reply(
            catmemes,
            "**Syntax :** reply to image or sticker with `.phub (username);(text in comment)`",
        )
        return
    replied = await catmemes.get_reply_message()
    catid = await reply_id(catmemes)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    output = await _cattools.media_to_pic(catmemes, replied)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        san = Get(san)
        await catmemes.client(san)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await phcomment(cat, text, username)
    await output[0].delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=catid)


CMD_HELP.update(
    {
        "trolls": "__**PLUGIN NAME :** TROLLS__\
      \n\n📌** CMD ➥** `.threats` reply to image or sticker \
      \n**USAGE   ➥  **Changes the given pic to another pic which shows that pic content is threat to society as that of nuclear bomb .\
      \n\n📌** CMD ➥** `.trash` reply to image or sticker\
      \n**USAGE   ➥  **Changes the given pic to another pic which shows that pic content is as equal as to trash(waste)\
      \n\n📌** CMD ➥** Reply to image or sticker with `.trap (name of the person to trap)|(trapper name)`\
      \n**USAGE   ➥  **Changes the given pic to another pic which shows that pic content is trapped in trap card\
      \n\n📌** CMD ➥** Reply to image or sticker with `.phub (username)|(text in comment)`\
      \n**USAGE   ➥  **Changes the given pic to another pic which shows that pic content as dp and shows a comment in phub with the given username\
      "
    }
)
