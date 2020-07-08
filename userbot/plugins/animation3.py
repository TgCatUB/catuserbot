from userbot import CMD_HELP
from telethon import events
import asyncio
from userbot.utils import admin_cmd
from userbot import ALIVE_NAME
import random, re
from collections import deque
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Cat"

@borg.on(admin_cmd(pattern=r"star$", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🦋✨🦋✨🦋✨🦋✨"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(pattern=r"boxs"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🟥🟧🟨🟩🟦🟪🟫⬛⬜"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
		
@borg.on(admin_cmd(pattern=f"rain$", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌬☁️🌩🌨🌧🌦🌥⛅🌤"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

@borg.on(admin_cmd(pattern=r"clol$"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🤔🧐🤨🤔🧐🤨"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)		

@borg.on(admin_cmd(pattern=r"odra$"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🚶🏃🚶🏃🚶🏃🚶🏃"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)		
		
@borg.on(admin_cmd(pattern=r"deploy$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 3
    animation_ttl = range(0, 12)
    await event.edit("Deploying...")
    animation_chars = [
        
            "**Heroku Connecting To Latest Github Build **",
            f"**Build started by user** ** {DEFAULTUSER} **",
            f"**Deploy** `535a74f0` **by user** ** {DEFAULTUSER} **",
            "**Restarting Heroku Server...**",
            "**State changed from up to starting**",    
            "**Stopping all processes with SIGTERM**",
            "**Process exited with** `status 143`",
            "**Starting process with command** `python3 -m stdborg`",
            "**State changed from starting to up**",
            "__INFO:Userbot:Logged in as 557667062__",
            "__INFO:Userbot:Successfully loaded all plugins__",
            "**Build Succeeded**"
 ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 12])       


@borg.on(admin_cmd(pattern="dump ?(.*)"))
async def _(message):
    try:
        obj = message.pattern_match.group(1)
        if len(obj) != 3:
            raise IndexError
        inp = ' '.join(obj)
    except IndexError:
        inp = "🥞 🎂 🍫"
    u, t, g, o, s, n = inp.split(), '🗑', '<(^_^ <)', '(> ^_^)>', '⠀ ', '\n'
    h = [(u[0], u[1], u[2]), (u[0], u[1], ''), (u[0], '', '')]
    for something in reversed([y for y in ([''.join(x) for x in (
    f + (s, g, s + s * f.count(''), t), f + (g, s * 2 + s * f.count(''), t),
    f[:i] + (o, f[i], s * 2 + s * f.count(''), t), f[:i] + (s + s * f.count(''), o, f[i], s, t),
    f[:i] + (s * 2 + s * f.count(''), o, f[i], t), f[:i] + (s * 3 + s * f.count(''), o, t),
    f[:i] + (s * 3 + s * f.count(''), g, t))] for i, f in enumerate(reversed(h)))]):
        for something_else in something:
            await asyncio.sleep(0.3)
            try:
                await message.edit(something_else)
            except errors.MessageIdInvalidError:
                return
	
@borg.on(admin_cmd(pattern="fleaveme$"))
async def _(event):
    animation_interval = 1
    animation_ttl = range(0, 10)
    animation_chars = [
        
            "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
            "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
            "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
            "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
            "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",    
            "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
            "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
            "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
            "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
            "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️"
 ]
    if event.fwd_from:
        return
    await event.edit("fleaveme....")
    await asyncio.sleep(2)
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 10])
		
@borg.on(admin_cmd(pattern="loveu", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.5
    animation_ttl = range(0, 70)
    await event.edit("loveu")
    animation_chars = [
            "😀",
            "👩‍🎨",
            "😁",    
            "😂",
            "🤣",
            "😃",
            "😄",
            "😅",
            "😊",
            "☺",
            "🙂",    
            "🤔",
            "🤨",
            "😐",
            "😑",
            "😶",
            "😣",
            "😥",
            "😮",    
            "🤐",
            "😯",
            "😴",
            "😔",
            "😕",
            "☹",
            "🙁",
            "😖",    
            "😞",
            "😟",
            "😢",
            "😭",
            "🤯",
            "💔",
            "❤",
            "i Love You❤",   
        ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 35])
            
@borg.on(admin_cmd(pattern=f"plane", outgoing=True))
async def _(event):
    if event.fwd_from:
        retun
    await event.edit("✈-------------")
    await event.edit("-✈------------")
    await event.edit("--✈-----------")
    await event.edit("---✈----------")
    await event.edit("----✈---------")
    await event.edit("-----✈--------")
    await event.edit("------✈-------")
    await event.edit("-------✈------")
    await event.edit("--------✈-----") 
    await event.edit("---------✈----")
    await event.edit("----------✈---")
    await event.edit("-----------✈--")
    await event.edit("------------✈-")
    await event.edit("-------------✈")
    await asyncio.sleep(3)
    await event.delete()           
    
    
@borg.on(admin_cmd(pattern=r"police"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 12)
    await event.edit("Police")
    animation_chars = [
        
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",    
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            f"{DEFAULTUSER} **Police iz Here**"

 ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])    

	
@borg.on(admin_cmd(pattern=f"jio$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 19)
    await event.edit("jio network boosting...")
    animation_chars = [
            "`Connecting To JIO NETWORK ....`",
            "`█ ▇ ▆ ▅ ▄ ▂ ▁`",
            "`▒ ▇ ▆ ▅ ▄ ▂ ▁`",
            "`▒ ▒ ▆ ▅ ▄ ▂ ▁`",
            "`▒ ▒ ▒ ▅ ▄ ▂ ▁`",    
            "`▒ ▒ ▒ ▒ ▄ ▂ ▁`",
            "`▒ ▒ ▒ ▒ ▒ ▂ ▁`",
            "`▒ ▒ ▒ ▒ ▒ ▒ ▁`",
            "`▒ ▒ ▒ ▒ ▒ ▒ ▒`",
            "*Optimising JIO NETWORK...*",
            "`▒ ▒ ▒ ▒ ▒ ▒ ▒`",
            "`▁ ▒ ▒ ▒ ▒ ▒ ▒`",           
            "`▁ ▂ ▒ ▒ ▒ ▒ ▒`",
            "`▁ ▂ ▄ ▒ ▒ ▒ ▒`",
            "`▁ ▂ ▄ ▅ ▒ ▒ ▒`",
            "`▁ ▂ ▄ ▅ ▆ ▒ ▒`",
            "`▁ ▂ ▄ ▅ ▆ ▇ ▒`",
            "`▁ ▂ ▄ ▅ ▆ ▇ █`",
            "**JIO NETWORK Boosted....**"
 ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 19])                
                    
            
@borg.on(admin_cmd(pattern=f"solarsystem", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 80)
    await event.edit("solarsystem")
    animation_chars = [
            "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️🌎◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
            "`◼️◼️◼️◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️◼️◼️◼️`",
            "`◼️🌕◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️☀◼️`",
            "`◼️◼️◼️🌕◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️☀◼️◼️◼️`",
            "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️🌎◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",    
            "`◼️◼️◼️◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️◼️◼️◼️`",
            "`◼️☀◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️🌕◼️`",
            "`◼️◼️◼️☀◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️🌕◼️◼️◼️`",
            ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 8])
