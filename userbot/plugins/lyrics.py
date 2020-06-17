"@s_a_i_k_r_i_s_h_n_a idea"
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="lyrics ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    chat = "@sarah_robot"
    await event.edit("Checking...")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1103306594))
              await event.client.send_message(chat, "/lyrics {}".format(input_str))
              response = await response 
          except YouBlockedUserError: 
              await event.reply("unblock @sarah_robot and try")
              return
          if response.text.startswith("song not found"):
             await event.edit("😐Song Not Found. Try other😐\n\n👇")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
            
            
CMD_HELP.update({
    "lyrics":
    ".lyrics songname\
    \n USAGE: sends you song lyrics of required song "
})            
