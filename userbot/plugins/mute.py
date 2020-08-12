'''Thakn You @pureindialover
'''
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
import asyncio
from uniborg.util import admin_cmd, sudo_cmd
from telethon.tl.functions.users import GetFullUserRequest
from userbot import CMD_HELP, bot
from userbot.uniborgConfig import Config

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
        
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

@borg.on(admin_cmd(pattern="mute ?(\d+)?"))
async def startmute(event):
        private = False
        if event.fwd_from:
          return
        if event.is_private:
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
        elif private:
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
        if event.is_private:
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
        
@borg.on(sudo_cmd(pattern=r"mute(?: |$)(.*)" ,allow_sudo = True))
@errors_handler
async def spider(spdr):
    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.reply(NO_ADMIN)
        return
    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return
    self_user = await spdr.client.get_me()
    if user.id == self_user.id:
        await spdr.reply(f"Sorry, I can't mute my self")
        return
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.reply(f"Error! User probably already muted.")
    try:
        await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))
        # Announce that the function is done
        if reason:
            await spdr.reply(f"{user.first_name} was muted in {spdr.chat.title}\n"f"`Reason:`{reason}")
        else:
            await spdr.reply(f"{user.first_name} was muted in {spdr.chat.title}")
        # Announce to logging group
        if BOTLOG:
            await spdr.client.send_message(
                    BOTLOG_CHATID, "#MUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)")
    except UserIdInvalidError:
            return await spdr.reply("`Uh oh my mute logic broke!`")


@borg.on(sudo_cmd(pattern=r"unmute(?: |$)(.*)" ,allow_sudo = True))
async def unmoot(unmot):
    """ For .unmute command, unmute the replied/tagged person """
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.reply(NO_ADMIN)
        return
    # If admin or creator, inform the user and start unmuting
    await unmot.edit('```Unmuting...```')
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return
    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.reply("`Error! User probably already unmuted.`")
    try:
       await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
       await unmot.reply("Unmuted Successfully")
    except UserIdInvalidError:
       await unmot.reply("`Uh oh my unmute logic broke!`")
       return
    if BOTLOG:
       await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)")        
