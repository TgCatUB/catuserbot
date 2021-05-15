from telethon.errors import FloodWaitError, MessageNotModidied
from ..Config import Config
from telethon.events import CallbackQuery
import asyncio

def check_owner(func):
    async def wrapper(_, c_q: CallbackQuery):
        if c_q.from_user and (
            c_q.from_user.id == Config.OWNER_ID or c_q.from_user.id in Config.SUDO_USERS
        ):
            try:
                await func(c_q)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds + 5)
            except MessageNotModified:
                pass
        else:
            await c_q.answer(
                "Only My Master can Access This !!\n\nDeploy your own Catuserbot.",
                show_alert=True,
            )

    return wrapper
