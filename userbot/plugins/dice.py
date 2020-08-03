#fix by @heyworld for OUB
#bug fixed by @d3athwarrior
#Edited by @Jisan7509

from telethon.tl.types import InputMediaDice
import requests 
import asyncio
from userbot import CMD_HELP, bot
from userbot.utils import admin_cmd, sudo_cmd



@borg.on(admin_cmd(pattern="dice ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(''))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(''))
        except:
            pass
        
@borg.on(admin_cmd(pattern="dart ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('🎯'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('🎯'))
        except:
            pass        

@borg.on(admin_cmd(pattern="basketball ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('🏀'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('🏀'))
        except:
            pass
        
@borg.on(admin_cmd(pattern="football ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('⚽️'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('⚽️'))
        except:
            pass
        
        

@borg.on(sudo_cmd(pattern="dice ?(.*)", allow_sudo = True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(''))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(''))
        except:
            pass
        
@borg.on(sudo_cmd(pattern="dart ?(.*)", allow_sudo = True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('🎯'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('🎯'))
        except:
            pass        

@borg.on(sudo_cmd(pattern="basketball ?(.*)", allow_sudo = True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('🏀'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('🏀'))
        except:
            pass
        
@borg.on(sudo_cmd(pattern="football ?(.*)", allow_sudo = True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('⚽️'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('⚽️'))
        except:
            pass
        
        
CMD_HELP.update({
    "dice":
    ".dice or .dice 1 to 6 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
})    

CMD_HELP.update({
    "basketball":
    ".basketball or .basketball 1 to 5 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
})    

CMD_HELP.update({
    "dart":
    ".dart or .dart 1 to 6 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
})    

CMD_HELP.update({
    "football":
    ".football or .football 1 to 6 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
})    
