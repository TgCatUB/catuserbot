import asyncio
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="purl ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("**Reply to any document.**")
       return
    reply_message = await event.get_reply_message() 
    chat = "@FiletolinkTGbot"
    sender = reply_message.sender
    await event.edit("**Making public url...**")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1011636686))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@FiletolinkTGbot) u Nigga```")
              return
          await event.delete()
          await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)

@borg.on(admin_cmd(pattern="sgm ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("**Reply to an user message.**")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("**Reply to a message.**")
       return
    chat = "@sangmatainfo_bot"
    sender = reply_message.sender
    await event.edit("**Getting user's name history..**")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@SangMataInfo_bot) u Nigga```")
              return
          await event.delete()
          await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)

@borg.on(admin_cmd(pattern="reader ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("**Reply to a URL.**")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("**Reply to a url message.**")
       return
    chat = "@chotamreaderbot"
    sender = reply_message.sender
    await event.edit("**Making instant view...**")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=272572121))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@chotamreaderbot) u Nigga```")
              return
          await event.delete()
          await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)
        
@borg.on(admin_cmd(pattern="audiodl ?(.*)"))
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
    chat = "@audiotubebot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit("```Processing```")
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=507379365))
              await borg.send_message(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock @AudioTubeBot and try again```")
              return
          await event.delete()
          await borg.send_file(event.chat_id, response.message.media)

@borg.on(admin_cmd(pattern="instadl ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    chat = "@Regrambot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=274562699))
              await event.client.send_message(chat, "{}".format(input_str))
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Unblock @Regrambot```")
              return
          if response.text.startswith("I can't find that"):
             await event.edit("😐")
          else: 
             await event.delete()
             await event.client.send_file(event.chat_id, response.message)
