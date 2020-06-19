#created by @Mr_Hops
"""Gps: Avaible commands: .gps <location>
"""


import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="gps ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    chat = "@Thepgirlbot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1097028858))
              await event.client.send_message(chat, "/gps {}".format(input_str))
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Unblock @Thepgirlbot```")
              return
          if response.text.startswith("I can't find that"):
             await event.edit("😐**Place Not Found**😐\n\n👇👇👇👇👇👇👇👇👇\n 👉👉Enter a valid place👈👈\n👆👆👆👆👆👆👆👆👆")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)