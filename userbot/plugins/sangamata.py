import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd
import asyncio

@borg.on(admin_cmd(pattern=("sg ?(.*)")))
async def _(event):
   if event.fwd_from:
      return 
   if not event.reply_to_msg_id:
      await event.edit("```Reply to any user message.```")
      return
   reply_message = await event.get_reply_message() 
   if not reply_message.text:
      await event.edit("```reply to text message```")
      return
   chat = "@SangMataInfo_bot"
   sender = reply_message.sender
   if reply_message.sender.bot:
      await event.edit("```Reply to actual users message.```")
      return
   await event.edit("```Processing```")
   async with borg.conversation(chat) as conv:
         try:     
            response = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
            await borg.forward_messages(chat, reply_message)
            response = await response 
         except YouBlockedUserError: 
            await event.reply("```Please unblock @sangmatainfo_bot and try again```")
            return
         if response.text.startswith("Forward"):
            await event.edit("```can you kindly disable your forward privacy settings for good?```")
         else: 
            await event.edit(f"{response.message.message}")

@borg.on(admin_cmd(pattern=("fakemail ?(.*)")))
async def _(event):
   if event.fwd_from:
      return 
   chat = "@fakemailbot"
   command = "/generate"
   await event.edit("```Fakemail Creating, wait```")
   async with borg.conversation(chat) as conv:
      try:
         m = await event.client.send_message("@fakemailbot","/generate")     
         await asyncio.sleep(5)
         k = await event.client.get_messages(entity="@fakemailbot", limit=1, reverse=False) 
         mail = k[0].text
         # print(k[0].text)
      except YouBlockedUserError: 
         await event.reply("```Please unblock @fakemailbot and try again```")
         return
      await event.edit(mail)

@borg.on(admin_cmd(pattern=("mailid ?(.*)")))
async def _(event):
   if event.fwd_from:
      return 
   chat = "@fakemailbot"
   command = "/id"
   await event.edit("```Fakemail list getting```")
   async with borg.conversation(chat) as conv:
        try:
            m = await event.client.send_message("@fakemailbot","/id")     
            await asyncio.sleep(5)
            k = await event.client.get_messages(entity="@fakemailbot", limit=1, reverse=False) 
            mail = k[0].text
            # print(k[0].text)
        except YouBlockedUserError: 
            await event.reply("```Please unblock @fakemailbot and try again```")
            return
        await event.edit(mail)


@borg.on(admin_cmd(pattern=("ub ?(.*)")))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("```reply to text message```")
       return
    chat = "@uploadbot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit("```Processing```")
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=97342984))
              await borg.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock @uploadbot and try again```")
              return
          if response.text.startswith("Hi!,"):
             await event.edit("```can you kindly disable your forward privacy settings for good?```")
          else: 
             await event.edit(f"{response.message.message}")



@borg.on(admin_cmd(pattern=("gid ?(.*)")))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("```reply to text message```")
       return
    chat = "@getidsbot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit("```Processing```")
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=186675376))
              await borg.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```you blocked bot```")
              return
          if response.text.startswith("Hello,"):
             await event.edit("```can you kindly disable your forward privacy settings for good?```")
          else: 
             await event.edit(f"{response.message.message}")
