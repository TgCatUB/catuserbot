# Lots of lub to @r4v4n4 for gibing the base <3
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd,register
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="scan ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```reply to a media message```")
       return
    chat = "@DrWebBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit(" `Sliding my tip, of fingers over it`")
    async with borg.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
              await borg.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock @sangmatainfo_bot and try again```")
              return
          if response.text.startswith("Forward"):
             await event.edit("```can you kindly disable your forward privacy settings for good?```")
          else:
          	if response.text.startswith("Select"):
          		await event.edit("`Please go to` @DrWebBot `and select your language.`") 
          	else: 
          			await event.edit(f"**Antivirus scan was completed. I got dem final results.**\n {response.message.message}")

CMD_HELP.update({
    "antivirus":
    ".scan reply to media or file\
    \n USEAGE: it scans the media or file and checks either any virus is in the file or media\
"
})      
