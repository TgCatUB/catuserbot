import os
import sys
import asyncio
import random
import logging
from telethon import events
from userbot.utils import admin_cmd

@borg.on(admin_cmd("bigoof"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 7)
    await event.edit("┏━━━┓╋╋╋╋┏━━━┓ \n┃┏━┓┃╋╋╋╋┃┏━┓┃ \n┃┃╋┃┣┓┏┓┏┫┃╋┃┃ \n┃┃╋┃┃┗┛┗┛┃┃╋┃┃ \n┃┗━┛┣┓┏┓┏┫┗━┛┃ \n┗━━━┛┗┛┗┛┗━━━┛")
    animation_chars = [
            "╭━━━╮╱╱╱╭━╮ \n┃╭━╮┃╱╱╱┃╭╯ \n┃┃╱┃┣━━┳╯╰╮ \n┃┃╱┃┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃┃┃ \n╰━━━┻━━╯╰╯ ",
            "╭━━━╮╱╱╱╱╱╱╭━╮ \n┃╭━╮┃╱╱╱╱╱╱┃╭╯ \n┃┃╱┃┣━━┳━━┳╯╰╮ \n┃┃╱┃┃╭╮┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃╰╯┃┃┃ \n ╰━━━┻━━┻━━╯╰╯",
            "╭━━━╮╱╱╱╱╱╱╱╱╱╭━╮ \n┃╭━╮┃╱╱╱╱╱╱╱╱╱┃╭╯ \n┃┃╱┃┣━━┳━━┳━━┳╯╰╮ \n┃┃╱┃┃╭╮┃╭╮┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃╰╯┃╰╯┃┃┃ \n╰━━━┻━━┻━━┻━━╯╰╯",
            "╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭━╮ \n┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃╭╯ \n┃┃╱┃┣━━┳━━┳━━┳━━┳╯╰╮ \n┃┃╱┃┃╭╮┃╭╮┃╭╮┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃╰╯┃╰╯┃╰╯┃┃┃ \n╰━━━┻━━┻━━┻━━┻━━╯╰╯",
            "╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╮ \n┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃╭╯ \n┃┃╱┃┣━━┳━━┳━━┳━━┳━━┳╯╰╮ \n┃┃╱┃┃╭╮┃╭╮┃╭╮┃╭╮┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃╰╯┃╰╯┃╰╯┃╰╯┃┃┃ \n╰━━━┻━━┻━━┻━━┻━━┻━━╯╰╯",
            "╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭━╮ \n┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃╭╯ \n┃┃╱┃┣━━┳━━┳━━┳━━┳╯╰╮ \n┃┃╱┃┃╭╮┃╭╮┃╭╮┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃╰╯┃╰╯┃╰╯┃┃┃ \n╰━━━┻━━┻━━┻━━┻━━╯╰╯",
            "╭━━━╮╱╱╱╱╱╱╱╱╱╭━╮ \n┃╭━╮┃╱╱╱╱╱╱╱╱╱┃╭╯ \n┃┃╱┃┣━━┳━━┳━━┳╯╰╮ \n┃┃╱┃┃╭╮┃╭╮┃╭╮┣╮╭╯ \n┃╰━╯┃╰╯┃╰╯┃╰╯┃┃┃ \n╰━━━┻━━┻━━┻━━╯╰╯"
         ]
          
    for i in animation_ttl:        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 7])

@borg.on(admin_cmd(pattern="g1 ?(.*)"))
async def payf(event):
    paytext=event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1,paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1, paytext*1)
    await event.edit(pay)

@borg.on(admin_cmd(pattern="uff ?(.*)"))      
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1    
    animation_ttl = range(0, 13)    
    animation_chars = [
            "U",
            "Uf",    
            "Uff",
            "Ufffff",
            "Uffffff",
            "Ufffffff",
            "Uffffffff",
            "Ufffffffff",
            "Uffffffffff",    
            "Ufffffffffff",
            "Uffffffffffff",
            "Ufffffffffffff",
            "Uffffffffffffff"
        ]
    for i in animation_ttl:        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 13])

@borg.on(admin_cmd(pattern="ctext ?(.*)"))
async def payf(event):
    paytext=event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*8, paytext*8, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2, paytext*8, paytext*8)
    await event.edit(pay)
      
@borg.on(admin_cmd(pattern="ftext ?(.*)"))
async def payf(event):
    paytext=event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*8, paytext*8, paytext*2, paytext*2, paytext*2, paytext*6, paytext*6, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2)
    await event.edit(pay)      

@borg.on(admin_cmd(outgoing=True, pattern="kf$(.*)"))
async def _(event):                             
                 r = random.randint(0, 3)
                 logger.debug(r)
                 if r == 0:
                     await event.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")
                 else:
                     r == 1            
                     await event.edit("╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯")    

@borg.on(admin_cmd(pattern="f (.*)"))
async def payf(e):
        paytext = e.pattern_match.group(1)
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*5, paytext*1,paytext*1, paytext*4, paytext*1, paytext*1, paytext*1)
        await e.edit(pay)
