#Fban Userlist by @Sur_vivor
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from userbot.utils import admin_cmd
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)


BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
                                          
@borg.on(admin_cmd(pattern=r"plist ?(.*)", outgoing=True))
async def get_users(show):
    await show.delete()
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "id,reason"
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
                    else:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(show.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
                    else:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await bot.send_message(BOTLOG_CHATID, mentions)
        except MessageTooLongError:
            file = open("userslist.csv", "w+")
            file.write(mentions)
            file.close()
            await show.client.send_file(
                BOTLOG_CHATID,
                "userslist.csv",
                caption='Group Members in {}'.format(title),
                reply_to=show.id,
            )
            


@borg.on(admin_cmd(pattern=r"blist ?(.*)", outgoing=True))
async def get_users(show):
    await show.delete()
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "id,reason"
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
                    else:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(show.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
                    else:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await bot.send_message(BOTLOG_CHATID, mentions)
        except MessageTooLongError:
            file = open("userslist.csv", "w+")
            file.write(mentions)
            file.close()
            await show.client.send_file(
                BOTLOG_CHATID,
                "userslist.csv",
                caption='Group members in {}'.format(title),
                reply_to=show.id,
            )
