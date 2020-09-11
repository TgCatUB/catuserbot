from telethon import events

from userbot.uniborgConfig import Config

from .. import LOGS
from ..utils import is_admin
from . import spamwatch
from .gadmin import BANNED_RIGHTS

if Config.SPAMWATCH_BAN and spamwatch:

    @bot.on(events.ChatAction())
    async def _(event):
        chat = event.chat_id
        if event.user_joined:
            user = await event.get_user()
            catadmin = await is_admin(bot, chat, bot.uid)
            if not catadmin:
                return
            ban = spamwatch.get_ban(user.id)
            if ban:
                await event.reply(
                    f"This [{user.first_name}](tg://user?id={user.id}) was banned by spamwatch For the reason `{ban.reason}`"
                )
                try:
                    await bot(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                except Exception as e:
                    return LOGS.info(e)
