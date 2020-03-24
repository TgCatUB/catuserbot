"""
Memes Plugin for Userbot
usage = .meme someCharacter //default delay will be 3
By : - @Zero_cool7870

"""
from telethon import events
import asyncio
import os
import sys

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"meme", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.meme", outgoing=True))
async def meme(event):
    if event.fwd_from:
        return   
    memeVar = event.text
    sleepValue = 5
    memeVar = memeVar[6:] 
           
    await event.edit("-------------"+memeVar)
    await event.edit("------------"+memeVar+"-")
    await event.edit("-----------"+memeVar+"--")
    await event.edit("----------"+memeVar+"---")
    await event.edit("---------"+memeVar+"----")    
    await event.edit("--------"+memeVar+"-----")
    await event.edit("-------"+memeVar+"------")
    await event.edit("------"+memeVar+"-------")
    await event.edit("-----"+memeVar+"--------")
    await event.edit("----"+memeVar+"---------")
    await event.edit("---"+memeVar+"----------")
    await event.edit("--"+memeVar+"-----------")
    await event.edit("-"+memeVar+"------------")
    await event.edit(memeVar+"-------------")
    await event.edit("-------------"+memeVar)
    await event.edit("------------"+memeVar+"-")
    await event.edit("-----------"+memeVar+"--")
    await event.edit("----------"+memeVar+"---")
    await event.edit("---------"+memeVar+"----")    
    await event.edit("--------"+memeVar+"-----")
    await event.edit("-------"+memeVar+"------")
    await event.edit("------"+memeVar+"-------")
    await event.edit("-----"+memeVar+"--------")
    await event.edit("----"+memeVar+"---------")
    await event.edit("---"+memeVar+"----------")
    await event.edit("--"+memeVar+"-----------")
    await event.edit("-"+memeVar+"------------")
    await event.edit(memeVar+"-------------")
    await event.edit(memeVar)
    await asyncio.sleep(sleepValue)

"""
Bonus : Give Boquee Generater
usage:- .give

"""


@borg.on(admin_cmd(pattern=f"lp", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.lp", outgoing=True))
async def meme(event):
    if event.fwd_from:
        return   
    lp =" 🍭"
    sleepValue = 10
           
    await event.edit(lp+"        ")
    await event.edit(lp+lp+"       ")
    await event.edit(lp+lp+lp+"      ")
    await event.edit(lp+lp+lp+lp+"     ")
    await event.edit(lp+lp+lp+lp+lp+"    ")
    await event.edit(lp+lp+lp+lp+lp+lp+"   ")
    await event.edit(lp+lp+lp+lp+lp+lp+lp+"  ")
    await event.edit(lp+lp+lp+lp+lp+lp+lp+lp+" ")
    await event.edit(lp+lp+lp+lp+lp+lp+lp+lp+lp)
    await event.edit(lp+"        ")
    await event.edit(lp+lp+"       ")
    await event.edit(lp+lp+lp+"      ")
    await event.edit(lp+lp+lp+lp+"     ")
    await event.edit(lp+lp+lp+lp+lp+"    ")
    await event.edit(lp+lp+lp+lp+lp+lp+"   ")
    await event.edit(lp+lp+lp+lp+lp+lp+lp+"  ")
    await event.edit(lp+lp+lp+lp+lp+lp+lp+lp+" ")
    await event.edit(lp+lp+lp+lp+lp+lp+lp+lp+lp)
    await asyncio.sleep(sleepValue)
    


@borg.on(admin_cmd(pattern=f"give", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.give", outgoing=True))
async def meme(event):
    if event.fwd_from:
        return   
    memeVar = event.text
    sleepValue = 5
    memeVar = memeVar[6:]
           
    await event.edit(give+"        ")
    await event.edit(give+give+"       ")
    await event.edit(give+give+give+"      ")
    await event.edit(give+give+give+give+"     ")
    await event.edit(give+give+give+give+give+"    ")
    await event.edit(give+give+give+give+give+give+give+"   ")
    await event.edit(give+give+give+give+give+give+give+give+"  ")
    await event.edit(give+give+give+give+give+give+give+give+give+" ")
    await event.edit(give+give+give+give+give+give+give+give+give+give)
    await event.edit(give+"        ")
    await event.edit(give+give+"       ")
    await event.edit(give+give+give+"      ")
    await event.edit(give+give+give+give+"     ")
    await event.edit(give+give+give+give+give+"    ")
    await event.edit(give+give+give+give+give+give+give+"   ")
    await event.edit(give+give+give+give+give+give+give+give+"  ")
    await event.edit(give+give+give+give+give+give+give+give+give+" ")
    await event.edit(give+give+give+give+give+give+give+give+give+give)
    await asyncio.sleep(sleepValue)        
    
