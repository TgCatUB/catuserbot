import asyncio
import time
from telethon import events
from userbot.utils import admin_cmd

# {user_id: expiration timestamp}
add_auths = {}
AUTH_TIME = 60 * 10

@borg.on(events.ChatAction(func=lambda e: e.user_added or e.created))
async def on_added(e):
    am = e.action_message
    if am.from_id == borg.uid:
        return
    if borg.uid not in am.action.users:
        return
    if add_auths.get(am.from_id, 0) >= time.time():
        logger.info(f'Removing temporary auth for {am.from_id}')
        del add_auths[am.from_id]
        return
    logger.info(f'Leaving {am.to_id} (added by {am.from_id})')
    await borg.kick_participant(am.to_id, 'me')

@borg.on(admin_cmd(pattern=f".auth", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.auth", outgoing=True, func=lambda e: e.is_private))
async def on_auth(e):
    logger.info(f'Adding temporary auth for {e.chat_id}')
    add_auths[e.chat_id] = time.time() + AUTH_TIME
    await e.delete()
