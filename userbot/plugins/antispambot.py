from requests import get
from telethon import events

from .. import LOGS
from ..utils import is_admin
from . import spamwatch

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

if Config.ANTISPAMBOT_BAN:

    @bot.on(events.ChatAction())
    async def _(event):
        chat = event.chat_id
        if event.user_joined:
            user = await event.get_user()
            catadmin = await is_admin(bot, chat, bot.uid)
            if not catadmin:
                return
            catbanned = None
            if spamwatch:
                ban = spamwatch.get_ban(user.id)
                if ban:
                    hmm = await event.reply(
                        f"This [{user.first_name}](tg://user?id={user.id}) was banned by spamwatch For the reason `{ban.reason}`"
                    )
                    try:
                        await bot.edit_permissions(chat, user.id, view_messages=False)
                        catbanned = True
                    except Exception as e:
                        LOGS.info(e)
                if not catbanned:
                    try:
                        casurl = "https://api.cas.chat/check?user_id={}".format(user.id)
                        data = get(casurl).json()
                    except Exception as e:
                        LOGS.info(e)
                        data = None
                    if data and data["ok"]:
                        reason = f"[Banned by Combot Anti Spam](https://cas.chat/query?u={user.id})"
                        hmm = await event.reply(
                            f"This [{user.first_name}](tg://user?id={user.id}) was banned by Combat anti-spam service(CAS) For the reason check {reason}"
                        )
                        try:
                            await bot.edit_permissions(
                                chat, user.id, view_messages=False
                            )
                            catbanned = True
                        except Exception as e:
                            LOGS.info(e)
                if BOTLOG and catbanned:
                    await bot.send_message(
                        BOTLOG_CHATID,
                        "#ANTISPAMBOT\n"
                        f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                        f"**Chat :** {event.chat.title} (`{event.chat_id}`)\n"
                        f"**Reason :** {hmm.text}",
                    )
