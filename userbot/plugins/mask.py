# credits to @mrconfused and @sandy1709

#    Copyright (C) 2020  sandeep.n(π.$)

import base64
import os

from telegraph import exceptions, upload_file
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import awooify, baguette, iphonex, lolice


@bot.on(admin_cmd("mask$", outgoing=True))
@bot.on(sudo_cmd(pattern="mask$", allow_sudo=True))
async def _(catbot):
    reply_message = await catbot.get_reply_message()
    if not reply_message.media or not reply_message:
        await edit_or_reply(catbot, "```reply to media message```")
        return
    chat = "@hazmat_suit_bot"
    if reply_message.sender.bot:
        await edit_or_reply(catbot, "```Reply to actual users message.```")
        return
    event = await catbot.edit("```Processing```")
    async with catbot.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=905164246)
            )
            await catbot.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("```Please unblock @hazmat_suit_bot and try again```")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await catbot.client.send_file(event.chat_id, response.message.media)
            await event.delete()


@bot.on(admin_cmd(pattern="awooify$"))
@bot.on(sudo_cmd(pattern="awooify$", allow_sudo=True))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catevent = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await catmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catevent.edit("generating image..")
    else:
        await catevent.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catevent.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await awooify(cat)
    await catevent.delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=replied)


@bot.on(admin_cmd(pattern="lolice$"))
@bot.on(sudo_cmd(pattern="lolice$", allow_sudo=True))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catevent = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await catmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catevent.edit("generating image..")
    else:
        await catevent.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catevent.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await lolice(cat)
    await catevent.delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=replied)


@bot.on(admin_cmd(pattern="bun$"))
@bot.on(sudo_cmd(pattern="bun$", allow_sudo=True))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catevent = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await catmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catevent.edit("generating image..")
    else:
        await catevent.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catevent.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await baguette(cat)
    await catevent.delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=replied)


@bot.on(admin_cmd(pattern="iphx$"))
@bot.on(sudo_cmd(pattern="iphx$", allow_sudo=True))
async def catbot(catmemes):
    replied = await catmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    if replied.media:
        catevent = await edit_or_reply(catmemes, "passing to telegraph...")
    else:
        await edit_or_reply(catmemes, "reply to a supported media file")
        return
    try:
        cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        cat = Get(cat)
        await catmemes.client(cat)
    except BaseException:
        pass
    download_location = await catmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await catevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await catevent.edit("generating image..")
    else:
        await catevent.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await catevent.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    cat = f"https://telegra.ph{response[0]}"
    cat = await iphonex(cat)
    await catevent.delete()
    await catmemes.client.send_file(catmemes.chat_id, cat, reply_to=replied)


CMD_HELP.update(
    {
        "mask": "`.mask` reply to any image file:\
      \nUSAGE:makes an image a different style try out your own.\
      "
    }
)
