import asyncio
import time
from asyncio import wait
from userbot.utils import admin_cmd
from telethon import events, utils

from userbot.events import register

@register(outgoing=True, pattern="^.sspam")
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        text = message.split()
        counter = int(text[1])
        spam_message = str(text[2])
      #  sm = ' '.join([str(elem) for elem in spam_message]) 
       # sm = ' '.join(map(str, spam_message)) 
        sleep2 = int(text[3])
        await e.delete()
        for i in range(counter):
            await asyncio.wait([ 
            e.respond(spam_message)])
            await asyncio.sleep(sleep2)
               
               
@borg.on(admin_cmd(pattern="tspam"))
async def tmeme(e):
     tspam = str(e.text[7:])
     message = tspam.replace(" ", "")
     for letter in message:
         await e.respond(letter)
     await e.delete()
