# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module for kanging stickers or making new ones. Thanks @rupansh"""
# modified by @mrconfused
import io
import math
import random
import urllib.request
from os import remove

import emoji
from PIL import Image
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
]


@bot.on(admin_cmd(outgoing=True, pattern="kang ?(.*)"))
@bot.on(sudo_cmd(pattern="kang ?(.*)", allow_sudo=True))
async def kang(args):
    """ For .kang command, kangs stickers or creates new ones. """
    user = await bot.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            user.username = user.first_name
        except UnicodeDecodeError:
            user.username = f"cat_{user.id}"
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            await bot.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await edit_or_reply(args, "`Unsupported File!`")
            return
    else:
        await edit_or_reply(args, "`I can't kang that...`")
        return
    if photo:
        splat = args.text.split()
        emoji = emoji if emojibypass else "😂"
        pack = 1
        if len(splat) == 3:
            if char_is_emoji(splat[1]):
                if char_is_emoji(splat[2]):
                    return await catevent.edit("check `.info stickers`")
                pack = splat[2]  # User sent both
                emoji = splat[1]
            elif char_is_emoji(splat[2]):
                pack = splat[1]  # User sent both
                emoji = splat[2]
            else:
                return await catevent.edit("check `.info stickers`")
        elif len(splat) == 2:
            if char_is_emoji(splat[1]):
                emoji = splat[1]
            else:
                pack = splat[1]
        packname = f"{user.username}_{pack}"
        packnick = f"@{user.username}'s_{pack}"
        cmd = "/newpack"
        file = io.BytesIO()
        if is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with bot.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while ("50" in x.text) or ("120" in x.text):
                    try:
                        val = int(pack)
                        pack = val + 1
                    except ValueError:
                        pack = 1
                    if is_anim:
                        packname = f"{user.username}_{pack}_anim"
                        packnick = f"@{user.username}'s_{pack} (Animated)"
                    else:
                        packname = f"{user.username}_{pack}"
                        packnick = f"@{user.username}'s_{pack}"
                    await catevent.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        rsp = await conv.get_response()
                        if (
                            "You can list several emoji in one message, but I recommend using no more than two per sticker"
                            not in rsp.text
                        ):
                            await bot.send_read_acknowledge(conv.chat_id)
                            await args.edit(
                                f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp.txt}"
                            )
                            return
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await catevent.edit(
                            f"Sticker added in a Different Pack !\
                            \nThis Pack is Newly created!\
                            \nYour pack can be found [here](t.me/addstickers/{packname}) and emoji of the sticker added is {emoji}",
                            parse_mode="md",
                        )
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if (
                    "You can list several emoji in one message, but I recommend using no more than two per sticker"
                    not in rsp.text
                ):
                    await bot.send_read_acknowledge(conv.chat_id)
                    await catevent.edit(
                        f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp.text}"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await catevent.edit("`Brewing a new Pack...`")
            async with bot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if (
                    "You can list several emoji in one message, but I recommend using no more than two per sticker"
                    not in rsp.text
                ):
                    await catevent.edit(
                        f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp}"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        await catevent.edit(
            f"Sticker kanged successfully!\
            \nPack can be found [here](t.me/addstickers/{packname}) and emoji of the sticker is {emoji}",
            parse_mode="md",
        )


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI


@bot.on(admin_cmd(pattern="stkrinfo$", outgoing=True))
@bot.on(sudo_cmd(pattern="stkrinfo$", allow_sudo=True))
async def get_pack_info(event):
    if not event.is_reply:
        await edit_or_reply(event, "`I can't fetch info from nothing, can I ?!`")
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await edit_or_reply(event, "`Reply to a sticker to get the pack details`")
        return
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        catevent = await edit_or_reply(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await edit_or_reply(event, "`This is not a sticker. Reply to a sticker.`")
        return
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await catevent.edit("`This is not a sticker. Reply to a sticker.`")
        return
    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = (
        f"**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"**Official:** `{get_stickerset.set.official}`\n"
        f"**Archived:** `{get_stickerset.set.archived}`\n"
        f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n"
        f"**Emojis In Pack:**\n{' '.join(pack_emojis)}"
    )
    await catevent.edit(OUTPUT)


CMD_HELP.update(
    {
        "stickers": "**Plugins : **`stickers`\
    \n\n**Syntax : **`.kang`\
\n**Function : **__Reply .kang to a sticker or an image to kang it to your userbot pack.__\
\n\n**Syntax : **`.kang [emoji('s)]`\
\n**Function : **__Works just like .kang but uses the emoji('s) you picked.__\
\n\n**Syntax : **`.kang [number]`\
\n**Function : **__Kang's the sticker/image to the specified pack but uses 🤔 as emoji.__\
\n\n**Syntax : **`.kang [emoji('s)] [number]`\
\n**Function : **__Kang's the sticker/image to the specified pack and uses the emoji('s) you picked.__\
\n\n**Syntax : **`.stkrinfo`\
\n**Function : **__Gets info about the sticker pack.__"
    }
)
