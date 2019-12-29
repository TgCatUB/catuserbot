# base by: @r4v4n4
# created by: @A_Dark_Princ3
# if you change these, you gay
# some things from kang.py from Spechide's fork of Uniborg
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd
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

@borg.on(admin_cmd("mmf ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Syntax: reply to an image with .mmf` 'text on top' ; 'text on bottom' ")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```reply to a media```")
       return
    chat = "@MemeAutobot"
    sender = reply_message.sender
    file_ext_ns_ion = "@memetime.png"
    file = await borg.download_file(reply_message.media)
    uploaded_sticker = None
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    else:
     await event.edit("```Transfiguration Time! Mwahaha memifying this image! (」ﾟﾛﾟ)｣ ```")
    
    async with borg.conversation("@MemeAutobot") as bot_conv:
          try:
            memeVar = event.pattern_match.group(1)
            await silently_send_message(bot_conv, "/start")
            await asyncio.sleep(1)
            await silently_send_message(bot_conv, memeVar)
            await borg.send_file(chat, reply_message.media)
            response = await bot_conv.get_response()
          except YouBlockedUserError: 
              await event.reply("```Please unblock @MemeAutobot and try again```")
              return
          if response.text.startswith("Forward"):
              await event.edit("```can you kindly disable your forward privacy settings for good nibba?```")
          if "Okay..." in response.text:
            await event.edit("```NANI?! This is a sticker! This will take sum tym owo```")
            with BytesIO(file) as mem_file, BytesIO() as sticker:
                resize_image(mem_file, sticker)
                sticker.seek(0)
                uploaded_sticker = await borg.upload_file(sticker, file_name=file_ext_ns_ion)
            await bot_conv.send_file(
                file=uploaded_sticker,
                allow_cache=False,
                force_document=False
            )
            response = await bot_conv.get_response()
            await borg.send_file(event.chat_id, response.media)
            await borg.send_message(event.chat_id, "` 10 points to Griffindor! `")
          elif not is_message_image(reply_message):
            await event.edit("Invalid message type.")
            return
          else: 
               await borg.send_file(event.chat_id, response.media)
               await borg.send_message(event.chat_id, "` 10 points to Griffindor! `")

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
