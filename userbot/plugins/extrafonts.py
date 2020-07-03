import re
import time
import requests
from telethon import events
from userbot.utils import admin_cmd
import asyncio
import random
from userbot import CMD_HELP, fonts




@borg.on(admin_cmd(pattern="fmusical(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            musicalcharacter = fonts.musicalfont[fonts.normalfont.index(normalfontcharacter)]
            string = string.replace(normalfontcharacter, musicalcharacter)
    await event.edit(string)                   
                  
@borg.on(admin_cmd(pattern="ancient(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            ancientcharacter = fonts.ancientfont[fonts.normalfont.index(normalfontcharacter)]
            string = string.replace(normalfontcharacter, ancientcharacter)
    await event.edit(string)
