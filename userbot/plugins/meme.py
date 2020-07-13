import asyncio
from userbot.utils import admin_cmd
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
import os
import sys

@borg.on(admin_cmd(pattern="session$"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**telethon.errors.rpcerrorlist.AuthKeyDuplicatedError: The authorization key (session file) was used under two different IP addresses simultaneously, and can no longer be used. Use the same session exclusively, or use different sessions (caused by GetMessagesRequest)**"
    await event.edit(mentions)

@borg.on(admin_cmd(pattern="ccry$"))
async def cry(e):
        await e.edit("(;´༎ຶД༎ຶ`)")

@borg.on(admin_cmd(pattern="fp$"))
async def facepalm(e):
        await e.edit("🤦‍♂")

@borg.on(admin_cmd(pattern=f"meme", outgoing=True))
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


@borg.on(admin_cmd(pattern=f"lp$", outgoing=True))
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
    


@borg.on(admin_cmd(pattern=f"give", outgoing=True))
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
    
@borg.on(admin_cmd(pattern="lcry$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 36)
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
        await event.edit(animation_chars[i % 36])
