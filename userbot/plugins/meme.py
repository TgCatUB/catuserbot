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
async def give(event):
    if event.fwd_from:
        return   
    giveVar = event.text
    sleepValue = 5
    giveVar = giveVar[6:]
           
    await event.edit(giveVar+"        ")
    await event.edit(giveVar+giveVar+"       ")
    await event.edit(giveVar+giveVar+giveVar+"      ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+"     ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+"    ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+"   ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+"  ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+" ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar)
    await event.edit(giveVar+"        ")
    await event.edit(giveVar+giveVar+"       ")
    await event.edit(giveVar+giveVar+giveVar+"      ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+"     ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+"    ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+"   ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+"  ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+" ")
    await event.edit(giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar+giveVar)
    await asyncio.sleep(sleepValue)        
    
@borg.on(admin_cmd(pattern="lcry"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 103)
    await event.edit("crying")
    animation_chars = [

            ";__",
            ";___",
            ";____",
            ";_____",
            ";______",
            ";_______",
            ";________",
            ";__________",
            ";____________",
            ";______________",
            ";________________",
            ";__________________",
            ";____________________",
            ";______________________",
            ";________________________",
            ";_________________________",
            ";_________________________",
            ";________________________",
            ";_______________________",
            ";______________________",
            ";_____________________",
            ";____________________",
            ";___________________",
            ";__________________",
            ";_________________",
            ";________________",
            ";_______________",
            ";_____________",
            ";___________",
            ";_________",
            ";_______",
            ";_____",
            ";____",
            ";___",
            ";__",
            ";You made me `CRY`"
        ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])
