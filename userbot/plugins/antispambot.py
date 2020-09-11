from telethon import events

from .. import LOGS
from ..utils import is_admin
from . import spamwatch
from .gadmin import BANNED_RIGHTS

if Config.SPAMWATCH_BAN:

    @bot.on(events.ChatAction)
    async def _(event):
        chat = event.chat_id
        if event.user_joined:
            user = await event.get_user()
            if not is_admin(bot, chat, user.id):
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
