# (c) @UniBorg
# Original written by @UniBorg edit by @I_m_Rock

from telethon import events
import asyncio
from collections import deque


from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"rain", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.rain", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌬☁️🌩🌨🌧🌦🌥⛅🌤"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
