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

@borg.on(admin_cmd(pattern=r"\.meme", outgoing=True))
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
Bonus : Flower Boquee Generater
usage:- .flower

"""
@borg.on(admin_cmd(pattern=r"\.lp", outgoing=True))
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
    
    
@borg.on(admin_cmd(pattern=r"\.flower", outgoing=True))
async def meme(event):
    if event.fwd_from:
        return   
    flower =" 🌹"
    sleepValue = 10
           
    await event.edit(flower+"        ")
    await event.edit(flower+flower+"       ")
    await event.edit(flower+flower+flower+"      ")
    await event.edit(flower+flower+flower+flower+"     ")
    await event.edit(flower+flower+flower+flower+flower+"    ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+"   ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+flower+"  ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+flower+flower+" ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+flower+flower+flower)
    await event.edit(flower+"        ")
    await event.edit(flower+flower+"       ")
    await event.edit(flower+flower+flower+"      ")
    await event.edit(flower+flower+flower+flower+"     ")
    await event.edit(flower+flower+flower+flower+flower+"    ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+"   ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+flower+"  ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+flower+flower+" ")
    await event.edit(flower+flower+flower+flower+flower+flower+flower+flower+flower+flower)
    await asyncio.sleep(sleepValue)        
    
