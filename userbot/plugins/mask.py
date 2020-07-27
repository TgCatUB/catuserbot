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

import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAlreadyParticipantError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from userbot.utils import admin_cmd , sudo_cmd
from userbot import CMD_HELP 
from telegraph import upload_file, exceptions
import os
from . import *
import pybase64

@borg.on(admin_cmd("mask ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```reply to media message```")
       return
    chat = "@hazmat_suit_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit("```Processing```")
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=905164246))
              await borg.send_message(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock @hazmat_suit_bot and try again```")
              return
          if response.text.startswith("Forward"):
             await event.edit("```can you kindly disable your forward privacy settings for good?```")
          else: 
             await borg.send_file(event.chat_id, response.message.media)  
                
@borg.on(admin_cmd(pattern = "awooify(?: |$)(.*)"))
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
    except:
        pass
    download_location = await borg.download_media(replied , Config.TMP_DOWNLOAD_DIRECTORY)
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
    cat = await awooify(cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id , cat,reply_to=replied)

@borg.on(admin_cmd(pattern = "lolice(?: |$)(.*)"))
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
    except:
        pass
    download_location = await borg.download_media(replied , Config.TMP_DOWNLOAD_DIRECTORY)
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
    cat = await lolice(cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id , cat,reply_to=replied)

@borg.on(admin_cmd(pattern = "bun(?: |$)(.*)"))
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
    except:
        pass
    download_location = await borg.download_media(replied , Config.TMP_DOWNLOAD_DIRECTORY)
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
    cat = await baguette(cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id , cat,reply_to=replied)

@borg.on(admin_cmd(pattern = "iphx(?: |$)(.*)"))
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
    except:
        pass
    download_location = await borg.download_media(replied , Config.TMP_DOWNLOAD_DIRECTORY)
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
    cat = await iphonex(cat)
    await catmemes.delete()
    await borg.send_file(catmemes.chat_id , cat,reply_to=replied)
                
@borg.on(sudo_cmd("mask ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.reply("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.reply("```reply to media message```")
       return
    chat = "@hazmat_suit_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.reply("```Reply to actual users message.```")
       return
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=905164246))
              await borg.send_message(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock @hazmat_suit_bot and try again```")
              return
          if response.text.startswith("Forward"):
             await event.edit("```can you kindly disable your forward privacy settings for good?```")
          else: 
             await borg.send_file(event.chat_id, response.message.media)  
                
                
CMD_HELP.update({"mask": "`.mask` reply to any image file:\
      \nUSAGE:makes an image a different style try out your own.\
      "
})             
