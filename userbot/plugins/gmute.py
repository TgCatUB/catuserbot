from userbot import CMD_HELP 
from userbot.uniborgConfig import Config
from telethon.tl.functions.users import GetFullUserRequest
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
import asyncio
from userbot.utils import sudo_cmd

BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

@command(outgoing=True, pattern=r"^.gmute ?(\d+)?")
async def startgmute(event):
    if any([x in event.raw_text for x in ("/gmute", "!gmute", "agmute", "bgmute", "cgmute", "dgmute", 
                                          "egmute", "fgmute", "ggmute", "hgmute", "igmute", "jgmute",
                                          "kgmute", "lgmute", "mgmute", "ngmute", "ogmute", "pgmute", 
                                          "qgmute", "rgmute", "sgmute", "tgmute", "ugmute", "vgmute", 
                                          "wgmute", "xgmute", "ygmute", "zgmute" , "1gmute", "2gmute", 
                                          "3gmute", "4gmute", "5gmute", "6gmute", "7gmute", "8gmute", 
                                          "9gmute", "0gmute", "Agmute", "Bgmute", "Cgmute", "Dgmute", 
                                          "Egmute", "Fgmute", "Ggmute", "Hgmute", "Igmute", "Jgmute", 
                                          "Kgmute", "Lgmute", "Mgmute", "Ngmute", "Ogmute", "Pgmute",
                                          "Qgmute", "Rgmute", "Sgmute", "Tgmute", "Ugmute", "Vgmute", 
                                          "Wgmute", "Xgmute", "Ygmute", "Zgmute",)]):
        return
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
        return await event.edit("Please reply to a user or add their into the command to gmute them.")
    replied_user = await event.client(GetFullUserRequest(userid))
    chat_id = event.chat_id
    chat = await event.get_chat()
    if is_muted(userid, "gmute"):
        return await event.edit("This user is already gmuted")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.edit("Error occured!\nError is " + str(e))
    else:
        await event.edit("Successfully gmuted that person")
    if BOTLOG:
      await event.client.send_message(
                    BOTLOG_CHATID, "#GMUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")    

@command(outgoing=True, pattern=r"^.ungmute ?(\d+)?")
async def endgmute(event):
    if any([x in event.raw_text for x in ("/ungmute", "!ungmute", "aungmute", "bungmute", "cungmute", "dungmute", 
                                          "eungmute", "fungmute", "gungmute", "hungmute", "iungmute", "jungmute",
                                          "kungmute", "lungmute", "mungmute", "nungmute", "oungmute", "pungmute", 
                                          "qungmute", "rungmute", "sungmute", "tungmute", "uungmute", "vungmute", 
                                          "wungmute", "xungmute", "yungmute", "zungmute" , "1ungmute", "2ungmute", 
                                          "3ungmute", "4ungmute", "5ungmute", "6ungmute", "7ungmute", "8ungmute", 
                                          "9ungmute", "0ungmute", "Aungmute", "Bungmute", "Cungmute", "Dungmute", 
                                          "Eungmute", "Fungmute", "Gungmute", "Hungmute", "Iungmute", "Jungmute", 
                                          "Kungmute", "Lungmute", "Mungmute", "Nungmute", "Oungmute", "Pungmute",
                                          "Qungmute", "Rungmute", "Sungmute", "Tungmute", "Uungmute", "Vungmute", 
                                          "Wungmute", "Xungmute", "Yungmute", "Zungmute",)]):
        return
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
        return await event.edit("Please reply to a user or add their into the command to ungmute them.")
    chat_id = event.chat_id
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await event.edit("This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.edit("Error occured!\nError is " + str(e))
    else:
        await event.edit("Successfully ungmuted that person")
    if BOTLOG:
      await event.client.send_message(
                    BOTLOG_CHATID, "#UNGMUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")         


@borg.on(sudo_cmd(pattern=r"gmute ?(\d+)?", allow_sudo=True))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
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
        return await event.reply("Please reply to a user or add their into the command to gmute them.")
    chat_id = event.chat_id
    replied_user = await event.client(GetFullUserRequest(userid))
    chat = await event.get_chat()
    if is_muted(userid, "gmute"):
        return await event.reply("This user is already gmuted")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully gmuted that person")
    if BOTLOG:
      await event.client.send_message(
                    BOTLOG_CHATID, "#GMUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")    
        

@borg.on(sudo_cmd(pattern=r"ungmute ?(\d+)?", allow_sudo=True))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
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
        return await event.reply("Please reply to a user or add their into the command to ungmute them.")
    chat_id = event.chat_id
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await event.reply("This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully ungmuted that person")
    if BOTLOG:
      await event.client.send_message(
                    BOTLOG_CHATID, "#UNGMUTE\n"
                    f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)")          

@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()
        
   
        
CMD_HELP.update({
    "gmute":
    ".gmute <username/reply> <reason (optional)>\
\nUsage: Mutes the person in all groups you have in common with them.\
\n\n.ungmute <username/reply>\
\nUsage: Reply someone's message with .ungmute to remove them from the gmuted list."
})
