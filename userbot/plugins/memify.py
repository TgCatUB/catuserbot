# base by: @r4v4n4
# created by: @A_Dark_Princ3
# if you change these, you gay
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd
import asyncio

@borg.on(admin_cmd("mmf ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Syntax: reply to an image with .mmf` 'text on top' ; 'text on bottom' ")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```reply to an image")
       return
    chat = "@MemeAutobot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit("```Transfiguration Time! Mwahaha memifying this image! (」ﾟﾛﾟ)｣ ```")
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=225462430))
              memeVar = event.pattern_match.group(1)
              await borg.send_message(chat, "/start")
              await borg.send_message(chat, memeVar)
              await asyncio.sleep(1)
              await borg.send_file(chat, reply_message.media)
              responded = await response
          except YouBlockedUserError: 
              await event.reply("```Please unblock @MemeAutobot and try again```")
              return
          if responded.text.startswith("Forward"):
              await event.edit("```can you kindly disable your forward privacy settings for good nibba?```")
          else: 
               await borg.send_file(event.chat_id, responded.message.media)
               await borg.send_message(event.chat_id, "` 10 points to Griffindor! `")
