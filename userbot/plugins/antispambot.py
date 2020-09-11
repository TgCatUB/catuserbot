from telethon import events

from .. import LOGS
from ..utils import is_admin
from . import spamwatch

if Config.ANTISPAMBOT_BAN:

    @bot.on(events.ChatAction())
    async def _(event):
        chat = event.chat_id
        if event.user_joined:
            user = await event.get_user()
            catadmin = await is_admin(bot, chat, bot.uid)
            if not catadmin:
                return
            if spamwatch:
                ban = spamwatch.get_ban(user.id)
                if ban:
                    await event.reply(
                        f"This [{user.first_name}](tg://user?id={user.id}) was banned by spamwatch For the reason `{ban.reason}`"
                    )
                    try:
                        await bot.edit_permissions(chat, user.id, view_messages=False)
                    except Exception as e:
                        return LOGS.info(e)
