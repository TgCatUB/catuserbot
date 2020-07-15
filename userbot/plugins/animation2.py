from telethon import events
from userbot.utils import admin_cmd
import random, re, asyncio
from userbot import CMD_HELP
from collections import deque

@borg.on(admin_cmd(pattern=r"lul$"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😂🤣😂🤣😂🤣"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

    
@borg.on(admin_cmd(pattern=r"nothappy$"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😁☹️😁☹️😁☹️😁"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(outgoing=True, pattern="clock$"))
async def _(event):
	    if event.fwd_from:
		    return
	    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
	    for _ in range(48):
		    await asyncio.sleep(0.1)
		    await event.edit("".join(deq))
		    deq.rotate(1)
        
@borg.on(admin_cmd(pattern=r"muah$"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("😗😙😚😚😘"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)	
    
@borg.on(admin_cmd(pattern="heart$"))		
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("❤️🧡💛💚💙💜🖤"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)        
        
		
@borg.on(admin_cmd(pattern="gym$", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@borg.on(admin_cmd(pattern=f"earth$", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@borg.on(admin_cmd(outgoing=True, pattern="moon$"))
async def _(event):
	    if event.fwd_from:
		    return
	    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
	    for _ in range(48):
		    await asyncio.sleep(0.1)
		    await event.edit("".join(deq))
		    deq.rotate(1)
			
@borg.on(admin_cmd(pattern=r"candy$"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🍦🍧🍩🍪🎂🍰🧁🍫🍬🍭"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)			
        
@borg.on(admin_cmd(pattern=f"smoon$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 101)
    await event.edit("smoon..")
    animation_chars = [

            "🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗",
            "🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘",    
            "🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑",
            "🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒",
            "🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓",
            "🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔",
            "🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕",
            "🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖"
        ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 8])
            
@borg.on(admin_cmd(pattern=f"tmoon$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 117)
    await event.edit("tmoon")
    animation_chars = [

            "🌗",
            "🌘",    
            "🌑",
            "🌒",
            "🌓",
            "🌔",
            "🌕",
            "🌖",
            "🌗",
            "🌘",    
            "🌑",
            "🌒",
            "🌓",
            "🌔",
            "🌕",
            "🌖",
            "🌗",
            "🌘",    
            "🌑",
            "🌒",
            "🌓",
            "🌔",
            "🌕",
            "🌖",
            "🌗",
            "🌘",    
            "🌑",
            "🌒",
            "🌓",
            "🌔",
            "🌕",
            "🌖"
        ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 32])

@borg.on(admin_cmd(pattern=f"clown$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.50
    animation_ttl = range(0, 16)
    animation_chars = [
        

            "COMMAND CREATE BY @Sur_vivor",
            "🤡️",
            "🤡🤡",
            "🤡🤡🤡",
            "🤡🤡🤡🤡",
            "🤡🤡🤡🤡🤡",
            "🤡🤡🤡🤡🤡🤡",    
            "🤡🤡🤡🤡🤡",
            "🤡🤡🤡🤡",
            "🤡🤡🤡",
            "🤡🤡",
            "🤡",
            "You",
            "You Are",
            "You Are A",
            "You Are A Clown 🤡"
        ]

    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 16])
