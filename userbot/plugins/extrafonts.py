
import re
import time
import requests
from telethon import events
from userbot import CMD_HELP
from userbot.utils import admin_cmd
import asyncio
import random



ancientfont = ['ꍏ', 'ꌃ', 'ꉓ', 'ꀸ', 'ꍟ', 'ꎇ', 'ꁅ', 'ꃅ', 'ꀤ', 'ꀭ', 'ꀘ', '꒒', 'ꎭ', 'ꈤ', 'ꂦ', 'ᖘ', 'ꆰ', 'ꋪ', 'ꌗ', '꓄', 'ꀎ','ᐯ', 'ꅏ', 'ꊼ', 'ꌩ', 'ꁴ',
              'ꍏ', 'ꌃ', 'ꉓ', 'ꀸ', 'ꍟ', 'ꎇ', 'ꁅ', 'ꃅ', 'ꀤ', 'ꀭ', 'ꀘ', '꒒', 'ꎭ', 'ꈤ', 'ꂦ', 'ᖘ', 'ꆰ', 'ꋪ', 'ꌗ', '꓄', 'ꀎ', 'ᐯ', 'ꅏ', 'ꊼ', 'ꌩ','ꁴ',
              '0', '1', '2', '3', '4','5', '6', '7', '8', '9', '_', "'", ',', '\\', '/', '!', '?']

normalfont = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z',
              '0', '1', '2', '3', '4','5', '6', '7', '8', '9', '_', "'", ',', '\\', '/', '!', '?']

musicalfont = ['♬', 'ᖲ', '¢', 'ᖱ', '៩', '⨏', '❡', 'Ϧ', 'ɨ', 'ɉ', 'ƙ', 'ɭ', '៣', '⩎', '០', 'ᖰ', 'ᖳ', 'Ʀ', 'ន', 'Ƭ', '⩏','⩔', 'Ɯ', '✗', 'ƴ', 'Ȥ',
              '♬', 'ᖲ', '¢', 'ᖱ', '៩', '⨏', '❡', 'Ϧ', 'ɨ', 'ɉ', 'ƙ', 'ɭ', '៣', '⩎', '០', 'ᖰ', 'ᖳ', 'Ʀ', 'ន', 'Ƭ', '⩏', '⩔', 'Ɯ', '✗', 'ƴ','Ȥ',
              '0', '1', '2', '3', '4','5', '6', '7', '8', '9', '_', "'", ',', '\\', '/', '!', '?']

@borg.on(admin_cmd(pattern="fmusical ?(.*)"))
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
        if normalfontcharacter in normalfont:
            bubblescharacter = musicalfont[normalfont.index(normalfontcharacter)]
            string = string.replace(normalfontcharacter, bubblescharacter)
    await event.edit(string)                   
                  
@borg.on(admin_cmd(pattern="ancient ?(.*)"))
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
        if normalfontcharacter in normalfont:
            bubblescharacter = ancientfont[normalfont.index(normalfontcharacter)]
            string = string.replace(normalfontcharacter, bubblescharacter)
    await event.edit(string)               
    
    
    
    
    
