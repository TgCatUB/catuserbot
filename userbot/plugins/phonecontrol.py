#New Qoute module by @r4v4n4 😉

import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="battery ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.reply("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.reply("```Reply to text message```")
       return
    chat = "@batterylevelbot"
    sender = reply_message.sender 

    if reply_message.sender.bot:
       await event.reply("```Reply to actual users message.```")
       return

    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=830109936))
              message = await event.client.forward_messages(chat, reply_message)
              await message.reply("🔋 Battery")

              await asyncio.sleep(4)
              response = await response

          except YouBlockedUserError: 
              await event.reply("```Please unblock me u Nigga```")
              return

          if response.text.startswith("Hello"):
             await event.reply("```Can you kindly disable your forward privacy settings for good?```")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message, reply_to=event.message.reply_to_msg_id)




@borg.on(admin_cmd(pattern="pmute ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.reply("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.reply("```Reply to text message```")
       return
    chat = "@batterylevelbot"
    sender = reply_message.sender 

    if reply_message.sender.bot:
       await event.reply("```Reply to actual users message.```")
       return

    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=830109936))
              message = await event.client.forward_messages(chat, reply_message)
              await message.reply("/ring_mode silent")

              await asyncio.sleep(4)
              response = await response

          except YouBlockedUserError: 
              await event.reply("```Please unblock me u Nigga```")
              return

          if response.text.startswith("Hello"):
             await event.reply("```Can you kindly disable your forward privacy settings for good?```")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message, reply_to=event.message.reply_to_msg_id)




@borg.on(admin_cmd(pattern="pring ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.reply("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.reply("```Reply to text message```")
       return
    chat = "@batterylevelbot"
    sender = reply_message.sender 

    if reply_message.sender.bot:
       await event.reply("```Reply to actual users message.```")
       return

    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=830109936))
              message = await event.client.forward_messages(chat, reply_message)
              await message.reply("/ring_mode normal")

              await asyncio.sleep(4)
              response = await response

          except YouBlockedUserError: 
              await event.reply("```Please unblock me u Nigga```")
              return

          if response.text.startswith("Hello"):
             await event.reply("```Can you kindly disable your forward privacy settings for good?```")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message, reply_to=event.message.reply_to_msg_id)




@borg.on(admin_cmd(pattern="pvibrate ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.reply("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.reply("```Reply to text message```")
       return
    chat = "@batterylevelbot"
    sender = reply_message.sender 

    if reply_message.sender.bot:
       await event.reply("```Reply to actual users message.```")
       return

    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=830109936))
              message = await event.client.forward_messages(chat, reply_message)
              await message.reply("/ring_mode vibrate")

              await asyncio.sleep(4)
              response = await response

          except YouBlockedUserError: 
              await event.reply("```Please unblock me u Nigga```")
              return

          if response.text.startswith("Hello"):
             await event.reply("```Can you kindly disable your forward privacy settings for good?```")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message, reply_to=event.message.reply_to_msg_id)

