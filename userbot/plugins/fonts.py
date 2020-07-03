import re
import time
import requests
from telethon import events
from userbot import CMD_HELP, fonts
from userbot.utils import admin_cmd
import asyncio
import random


@borg.on(admin_cmd(pattern="vapor(?: |$)(.*)"))
async def vapor(vpr):
        reply_text = list()
        textx = await vpr.get_reply_message()
        message = vpr.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await vpr.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
            return

        for charac in message:
            if 0x21 <= ord(charac) <= 0x7F:
                reply_text.append(chr(ord(charac) + 0xFEE0))
            elif ord(charac) == 0x20:
                reply_text.append(chr(0x3000))
            else:
                reply_text.append(charac)

        await vpr.edit("".join(reply_text))

@borg.on(admin_cmd(pattern="smallcaps(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            smallcapscharacter = fonts.smallcapsfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, smallcapscharacter)
    await event.edit(string) 
          


@borg.on(admin_cmd(pattern="blackbf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            bubblesblackcharacter = fonts.bubblesblackfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, bubblesblackcharacter)
    await event.edit(string)  
 
@borg.on(admin_cmd(pattern="bubbles(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            bubblescharacter = fonts.bubblesfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, bubblescharacter)
    await event.edit(string) 


@borg.on(admin_cmd(pattern="tanf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            tantextcharacter = fonts.tantextfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, tantextcharacter)
    await event.edit(string) 

@borg.on(admin_cmd(pattern="boxf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            littleboxtextcharacter = fonts.littleboxtextfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, littleboxtextcharacter)
    await event.edit(string) 


@borg.on(admin_cmd(pattern="smothtext(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text 
    if not args:    
        await event.edit("What I am Supposed to change give text")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            smothtextcharacter = fonts.smothtextfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, smothtextcharacter)
    await event.edit(string)     
    
    
CMD_HELP.update({
    "fonts": ".vapor (text) or .vapor reply to message \
\nUsage: Vaporize the given text. \
"
})
