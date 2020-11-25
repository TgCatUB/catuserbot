# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
# Thanks @rupansh
# modified and developed by @mrconfused

import io
import math
import random
import urllib.request
from os import remove

import emoji
import requests
from bs4 import BeautifulSoup as bs
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

combot_stickers_url = "https://combot.org/telegram/stickers?q="


@bot.on(admin_cmd(outgoing=True, pattern="kang ?(.*)"))
@bot.on(sudo_cmd(pattern="kang ?(.*)", allow_sudo=True))
async def kang(args):
    user = await args.client.get_me()
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
            photo = await args.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await args.client.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            await args.client.download_file(
                message.media.document, "AnimatedSticker.tgs"
            )

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await edit_delete(args, "`Unsupported File!`")
            return
    else:
        await edit_delete(args, "`I can't kang that...`")
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
        if Config.CUSTOM_STICKER_PACKNAME:
            packnick = f"{Config.CUSTOM_STICKER_PACKNAME} Vol.{pack}"
        else:
            packnick = f"@{user.username} Vol.{pack}"
        packname = f"{user.username}_{pack}"
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
            async with args.client.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while ("50" in x.text) or ("120" in x.text):
                    try:
                        val = int(pack)
                        pack = val + 1
                    except ValueError:
                        pack = 1
                    if Config.CUSTOM_STICKER_PACKNAME:
                        if is_anim:
                            packname = f"{user.username}_{pack}_anim"
                            packnick = f"{Config.CUSTOM_STICKER_PACKNAME} Vol.{pack} (Animated)"
                        else:
                            packname = f"{user.username}_{pack}"
                            packnick = f"{Config.CUSTOM_STICKER_PACKNAME} Vol.{pack}"
                    else:
                        if is_anim:
                            packname = f"{user.username}_{pack}_anim"
                            packnick = f"@{user.username} Vol.{pack} (Animated)"
                        else:
                            packname = f"{user.username}_{pack}"
                            packnick = f"@{user.username} Vol.{pack}"
                    await catevent.edit(
                        f"`Switching to Pack {str(pack)} due to insufficient space`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await args.client.send_read_acknowledge(conv.chat_id)
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
                            await args.client.send_read_acknowledge(conv.chat_id)
                            await args.edit(
                                f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp.txt}"
                            )
                            return
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await edit_delete(
                            catevent,
                            f"`Sticker added in a Different Pack !\
                            \nThis Pack is Newly created!\
                            \nYour pack can be found` [here](t.me/addstickers/{packname}) `and emoji of the sticker added is {emoji}`",
                            parse_mode="md",
                            time=7,
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
                    await args.client.send_read_acknowledge(conv.chat_id)
                    await catevent.edit(
                        f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp.text}"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
        else:
            await catevent.edit("`Brewing a new Pack...`")
            async with args.client.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
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
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await args.client.send_read_acknowledge(conv.chat_id)
        await edit_delete(
            catevent,
            f"`Sticker kanged successfully!\
            \nPack can be found` [here](t.me/addstickers/{packname}) `and emoji of the sticker is {emoji}`",
            parse_mode="md",
            time=7,
        )


@bot.on(admin_cmd(pattern="stkrinfo$", outgoing=True))
@bot.on(sudo_cmd(pattern="stkrinfo$", allow_sudo=True))
async def get_pack_info(event):
    if not event.is_reply:
        await edit_delete(event, "`I can't fetch info from nothing, can I ?!`", 5)
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await edit_delete(event, "`Reply to a sticker to get the pack details`", 5)
        return
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        catevent = await edit_or_reply(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await edit_delete(event, "`This is not a sticker. Reply to a sticker.`", 5)
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


@bot.on(admin_cmd(pattern="stickers ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="stickers ?(.*)", allow_sudo=True))
async def cb_sticker(event):
    split = event.pattern_match.group(1)
    if not split:
        await edit_delete(event, "`Provide some name to search for pack.`", 5)
        return
    catevent = await edit_or_reply(event, "`Searching sticker packs....`")
    text = requests.get(combot_stickers_url + split).text
    soup = bs(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        await edit_delete(catevent, "`No results found :(.`", 5)
        return
    reply = f"**Sticker packs found for {split} are :**"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            packid = (pack.button).get("data-popup")
            reply += f"\n **• ID: **`{packid}`\n [{packtitle}]({packlink})"
    await catevent.edit(reply)


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


CMD_HELP.update(
    {
        "stickers": "__**PLUGIN NAME :** Stickers__\
\n\n📌** CMD ➥** `.kang`\
\n**USAGE   ➥  **Reply .kang to a sticker or an image to kang it to your userbot pack.\
\n\n📌** CMD ➥** `.kang [emoji('s)]`\
\n**USAGE   ➥  **Works just like .kang but uses the emoji('s) you picked.\
\n\n📌** CMD ➥** `.kang [number]`\
\n**USAGE   ➥  **Kang's the sticker/image to the specified pack but uses 🤔 as emoji.\
\n\n📌** CMD ➥** `.kang [emoji('s)] [number]`\
\n**USAGE   ➥  **Kang's the sticker/image to the specified pack and uses the emoji('s) you picked.\
\n\n📌** CMD ➥** `.stickers name`\
\n**USAGE   ➥  **Shows you the list of non-animated sticker packs with that name.\
\n\n📌** CMD ➥** `.stkrinfo`\
\n**USAGE   ➥  **Gets info about the sticker pack."
    }
)
