# (c) @UniBorg

from telethon import events
import asyncio
from collections import deque
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=r"lul"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😂🤣😂🤣😂🤣"))
	for _ in range(999):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(pattern=r"candy"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🍦🍧🍩🍪🎂🍰🧁🍫🍬🍭"))
	for _ in range(999):
		await asyncio.sleep(0.4)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@borg.on(admin_cmd(pattern=r"nothappy"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😁☹️😁☹️😁☹️😁"))
	for _ in range(999):
		await asyncio.sleep(0.4)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(pattern=r"tlol"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🤔🧐🤨🤔🧐🤨"))
	for _ in range(999):
		await asyncio.sleep(0.4)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(pattern=r"blk"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🟥🟧🟨🟩🟦🟪🟫⬛⬜"))
	for _ in range(999):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(pattern="ccry$"))
async def cry(e):
        await e.edit("(;´༎ຶД༎ຶ)")

@borg.on(admin_cmd(pattern="heart$"))		
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("❤️🧡💛💚💙💜🖤"))
	for _ in range(32):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
