from telethon import events
from io import BytesIO
from PIL import Image
import asyncio
import datetime
from collections import defaultdict
import math
import os
import requests
import zipfile
from telethon.errors.rpcerrorlist import StickersetInvalidError
from telethon.errors import MessageNotModifiedError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputMediaUploadedDocument,
    InputPeerNotifySettings,
    InputStickerSetID,
    InputStickerSetShortName,
    MessageMediaPhoto
)
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="png ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a photo to add to my personal sticker pack.")
        return
    reply_message = await event.get_reply_message()
    sticker_emoji = "🔥"
    input_str = event.pattern_match.group(1)
    if input_str:
        sticker_emoji = input_str

    me = borg.me
    userid = event.from_id
    packname = f"{userid}'s @UniBorg Pack"
    packshortname = f"Uni_Borg_{userid}"  # format: Uni_Borg_userid

    is_a_s = is_it_animated_sticker(reply_message)
    file_ext_ns_ion = "@UniBorg_Sticker.png"
    file = await borg.download_file(reply_message.media)
    uploaded_sticker = None
    if is_a_s:
        file_ext_ns_ion = "AnimatedSticker.tgs"
        uploaded_sticker = await borg.upload_file(file, file_name=file_ext_ns_ion)
        packname = f"{userid}'s @AnimatedStickersGroup"
        if userid == 719877937:
            packshortname = "SnapDragon_Animated"
        else:
            packshortname = f"Uni_Borg_{userid}_as" # format: Uni_Borg_userid
    elif not is_message_image(reply_message):
        await event.edit("Invalid message type")
        return
    else:
        with BytesIO(file) as mem_file, BytesIO() as sticker:
            resize_image(mem_file, sticker)
            sticker.seek(0)
            uploaded_sticker = await borg.upload_file(sticker, file_name=file_ext_ns_ion)

    await event.edit("Processing this sticker. Please Wait!")

    async with borg.conversation("@Stickers") as bot_conv:
        now = datetime.datetime.now()
        dt = now + datetime.timedelta(minutes=1)
        if not await stickerset_exists(bot_conv, packshortname):
            await silently_send_message(bot_conv, "/cancel")
            if is_a_s:
                response = await silently_send_message(bot_conv, "/newanimated")
            else:
                response = await silently_send_message(bot_conv, "/newpack")
            if "Yay!" not in response.text:
                await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                return
            response = await silently_send_message(bot_conv, packname)
            if not response.text.startswith("Alright!"):
                await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                return
            w = await bot_conv.send_file(
                file=uploaded_sticker,
                allow_cache=False,
                force_document=True
            )
          #  response = await bot_conv.get_response()
          #  if "Sorry" in response.text:
           #    await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
            #    return
        #    await silently_send_message(bot_conv, sticker_emoji)
         #   await silently_send_message(bot_conv, "/publish")
          #  response = await silently_send_message(bot_conv, f"<{packname}>")
          #  await silently_send_message(bot_conv, "/skip")
           # response = await silently_send_message(bot_conv, packshortname)
           # if response.text == "Sorry, this short name is already taken.":
               # await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                #return
        #else:
            #await silently_send_message(bot_conv, "/cancel")
            #await silently_send_message(bot_conv, "/addsticker")
            #await silently_send_message(bot_conv, packshortname)
            await bot_conv.send_file(
                file=uploaded_sticker,
                allow_cache=False,
                force_document=True
            )
            response = await bot_conv.get_response()
            #if "Sorry" in response.text:
                #await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                #return
            #await silently_send_message(bot_conv, response)
            #await silently_send_message(bot_conv, sticker_emoji)
            #await silently_send_message(bot_conv, "/done")

    #await event.edit(f"R.I.P this sticker! This Sticker's Soul is [here](t.me/addstickers/{packshortname})")



# Helpers

def is_it_animated_sticker(message):
    try:
        if message.media and message.media.document:
            mime_type = message.media.document.mime_type
            if "tgsticker" in mime_type:
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


async def stickerset_exists(conv, setname):
    try:
        await borg(GetStickerSetRequest(InputStickerSetShortName(setname)))
        response = await silently_send_message(conv, "/addsticker")
        if response.text == "Invalid pack selected.":
            await silently_send_message(conv, "/cancel")
            return False
        await silently_send_message(conv, "/cancel")
        return True
    except StickersetInvalidError:
        return False


def resize_image(image, save_locaton):
    """ Copyright Rhyse Simpson:
        https://github.com/skittles9823/SkittBot/blob/master/tg_bot/modules/stickers.py
    """
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
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
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    im.save(save_locaton, "PNG")


def progress(current, total):
    logger.info("Uploaded: {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


def find_instance(items, class_or_tuple):
    for item in items:
        if isinstance(item, class_or_tuple):
            return item
    return None


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))
