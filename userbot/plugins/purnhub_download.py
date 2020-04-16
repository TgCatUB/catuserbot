"""
Pornhub downloader by @anubisxx
Syntax: .phd link
"""
import datetime
import asyncio
import requests
from bs4 import BeautifulSoup
import os
from pySmartDL import SmartDL
from telethon import events 
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAlreadyParticipantError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from userbot.utils import admin_cmd, LESS_SPAMMY

@borg.on(admin_cmd("phd ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    bot = "@phsavebot"
    r = requests.get(d_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    temporary_variable = soup.find("span", {"class": "inlineFree"})
    title = temporary_variable.text
    temp = soup.find("div", {"class": "thumbnail"})
    view = soup.find("span", {"class": "count"})
    views = view.text
    temporary_variable_to_use = temp.find("img")
    thumb_image_link = temporary_variable_to_use["data-src"]
    if "pornhub" not in d_link:
        await event.edit("` I need a link to download something pro.`**(._.)**")
    else:
        await event.edit("**💦Preparing to upload Video💦 **\n**Title**:  `{}`\n**Total Views**: `{}`".format(title, views))
    downloaded_file_name = "userbot/original_pic.jpg"
    downloader = SmartDL(thumb_image_link, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    photo_thumb = "userbot/original_pic.jpg"
    await asyncio.sleep(2)
    

    async with event.client.conversation("@phsavebot") as conv:
          try:
              await conv.send_message("/start")
              oop = await conv.get_response()
              if "language" in oop.text:
                  await borg.send_message(event.chat_id, "**Please go to** @phsavebot **and select your language**")
              await asyncio.sleep(2)
              me = await borg.get_me()
              my_id = me.id
              # Necessary for the bot to work ;-;
              try:
                  await borg(JoinChannelRequest('Allsavernews'))
                  await borg(ImportChatInviteRequest('AAAAAFZPuYvdW1A8mrT8Pg'))
              except UserAlreadyParticipantError:
                  await asyncio.sleep(0.00000069420)
              await conv.send_message(d_link)
              response = await conv.get_response()
              if "Downloading" in response.text:
                  video_hehe = await conv.get_response()
                  await borg.send_file(event.chat_id, video_hehe, caption="`🤤 Video Uploaded!🤤 `\n**Title:** `{}`".format(title), thumb=photo_thumb)
              elif "Unfortunately" in response.text:
                  await event.edit("`Woops, Incorrect link!`\n**Please check and try again.**")
              elif "correct" in response.text:
                  await borg.send_message(event.chat_id, response.text)
          except YouBlockedUserError: 
              await event.reply("**Please unblock** @phsavebot **and try again**")
              return

