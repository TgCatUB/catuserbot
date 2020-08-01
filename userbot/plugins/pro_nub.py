"""Available Commands:
.unoob
.menoob
.upro
.mepro
@arnab431"""

from telethon import events
from userbot import CMD_HELP 
import asyncio
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="unoob$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 9)
    await event.edit("unnoob")
    animation_chars = [
            "EvErYbOdY",
            "iZ",
            "BiGGeSt",
            "NoOoB" ,
            "uNtiL",
            "YoU",
            "aRriVe",
            "😈",
            "EvErYbOdY iZ BiGGeSt NoOoB uNtiL YoU aRriVe 😈"
        ]
    for i in animation_ttl:
            await event.edit(animation_chars[i % 9])
            await asyncio.sleep(animation_interval)

@borg.on(admin_cmd(pattern="menoob$"))           
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 9)
    await event.edit("menoob")
    animation_chars = [
            "EvErYbOdY",
            "iZ",
            "BiGGeSt",
            "NoOoB" ,
            "uNtiL",
            "i",
            "aRriVe",
            "😈",
            "EvErYbOdY iZ BiGGeSt NoOoB uNtiL i aRriVe 😈"
        ]
    for i in animation_ttl:
            await event.edit(animation_chars[i % 9])
            await asyncio.sleep(animation_interval) 
           
@borg.on(admin_cmd(pattern="upro$"))            
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 8)
    await event.edit("upro")
    animation_chars = [
            "EvErYbOdY",
            "iZ",
            "PeRu" ,
            "uNtiL",
            "YoU",
            "aRriVe",
            "😈",
            "EvErYbOdY iZ PeRu uNtiL YoU aRriVe 😈"
        ]
    for i in animation_ttl:
            await event.edit(animation_chars[i % 8])
            await asyncio.sleep(animation_interval)  
            
@borg.on(admin_cmd(pattern="mepro$"))            
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 8)
    await event.edit("mepro")
    animation_chars = [
            "EvErYbOdY",
            "iZ",
            "PeRu" ,
            "uNtiL",
            "i",
            "aRriVe",
            "😈",
            "EvErYbOdY iZ PeRu uNtiL i aRriVe 😈"
        ]
    for i in animation_ttl:
            await event.edit(animation_chars[i % 8])
            await asyncio.sleep(animation_interval)                                
