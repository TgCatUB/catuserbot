
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="ctg ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to a Link.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("```Reply to a Link```")
       return
    chat = "@chotamreaderbot"
    sender = reply_message.sender
    await event.edit("```Processing```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=272572121))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("`RIP Check Your Blacklist Boss`")
              return
          if response.text.startswith(""):
             await event.edit("Am I Dumb Or Am I Dumb?")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
