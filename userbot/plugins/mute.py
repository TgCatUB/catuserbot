'''Thakn You @pureindialover
'''
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
import asyncio
from uniborg.util import admin_cmd
from telethon.tl.functions.users import GetFullUserRequest
from userbot import CMD_HELP, bot
from userbot.uniborgConfig import Config

BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

@borg.on(admin_cmd(pattern="mute ?(\d+)?"))
async def startmute(event):
        private = False
        if event.fwd_from:
          return
        elif event.is_private:
          await event.edit("Unexpected issues or ugly errors may occur!")
          await asyncio.sleep(3)
          private = True           
        reply = await event.get_reply_message()
        if event.pattern_match.group(1) is not None:
            userid = event.pattern_match.group(1)
        elif reply is not None:
            userid = reply.sender_id
        elif private is True:
            userid = event.chat_id
        else:
            return await event.edit("Please reply to a user or add their userid into the command to mute them.")
        chat_id = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat = await event.get_chat()
        if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None: 
            if chat.admin_rights.delete_messages is True:
                pass
            else:
                return await event.edit("`You can't mute a person if you dont have delete messages permission. ಥ﹏ಥ`")
        elif "creator" in vars(chat):
            pass
        elif private == True:
            pass
        else:
            return await event.edit("`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  ")
        if is_muted(userid, chat_id):
            return await event.edit("This user is already muted in this chat ~~lmfao sed rip~~")
        try:
            mute(userid, chat_id)
        except Exception as e:
            await event.edit("Error occured!\nError is " + str(e))
        else:
            await event.edit("Successfully muted that person.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **")           
        # Announce to logging group    
        if BOTLOG:
          await event.client.send_message(
                    BOTLOG_CHATID, "#MUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")     

@borg.on(admin_cmd(pattern="unmute ?(\d+)?"))
async def endmute(event):
        private = False
        if event.fwd_from:
          return
        elif event.is_private:
          await event.edit("Unexpected issues or ugly errors may occur!")
          await asyncio.sleep(3)
          private = True            
        reply = await event.get_reply_message()
        if event.pattern_match.group(1) is not None:
            userid = event.pattern_match.group(1)
        elif reply is not None:
            userid = reply.sender_id
        elif private is True:
            userid = event.chat_id
        else:
            return await event.edit("Please reply to a user or add their userid into the command to unmute them.")
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if not is_muted(userid, chat_id):
            return await event.edit("__This user is not muted in this chat__\n（ ^_^）o自自o（^_^ ）")
        try:
            unmute(userid, chat_id)
        except Exception as e:
            await event.edit("Error occured!\nError is " + str(e))
        else:
            await event.edit("Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍")        
        # Announce to logging group    
        if BOTLOG:
           await event.client.send_message(
                    BOTLOG_CHATID, "#UNMUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")

@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()
