"""
Pulls Up A Random Chant From Harry Potter Series...
Syntax: .hp
    orginal author : AlenPaulVarghese(@STARKTM1)
"""
from telethon import events
import asyncio
import os
import sys
import random

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"hps", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.hps", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    x=(random.randrange(1,40)) 
    if (x==1):
      await event.edit("**Aberto**")
    if (x==2):
      await event.edit("**Accio**")
    if (x==3):
      await event.edit("**Aguamenti**")
    if (x==4):
      await event.edit("**Alohomora**")
    if (x==5):
      await event.edit("**Avada Kedavra**")
    if (x==6):
      await event.edit("**Colloportus**")
    if (x==7):
      await event.edit("**Confringo**")
    if (x==8):
      await event.edit("**Confundo**")
    if (x==9):
      await event.edit("**Crucio**")
    if (x==10):
      await event.edit("**Descendo**")
    if (x==11):
      await event.edit("**Diffindo**")
    if (x==12):
      await event.edit("**Engorgio**")
    if (x==13):
      await event.edit("**Episkey**")
    if (x==14):
      await event.edit("**Evanesco**")
    if (x==15):
      await event.edit("**Expecto Patronum**")
    if (x==16):
      await event.edit("**Expelliarmus**")
    if (x==17):
      await event.edit("**Finestra**")
    if (x==18):
      await event.edit("**Homenum Revelio**")
    if (x==19):
      await event.edit("**Impedimenta**")
    if (x==20):
      await event.edit("**Imperio**")
    if (x==21):
      await event.edit("**Impervius**")
    if (x==22):
      await event.edit("**Incendio**")
    if (x==23):
      await event.edit("**Levicorpus**")
    if (x==24):
      await event.edit("**Lumos**")
    if (x==25):
      await event.edit("**Muffliato**")
    if (x==26):
      await event.edit("**Obliviate**")
    if (x==27):
      await event.edit("**Petrificus Totalus**")
    if (x==28):
      await event.edit("**Priori Incantato**")
    if (x==29):
      await event.edit("**Protego**")
    if (x==30):
      await event.edit("**Reducto**")
    if (x==31):
      await event.edit("**Rennervate**")
    if (x==32):
      await event.edit("**Revelio**")
    if (x==33):
      await event.edit("**Rictusempra**")
    if (x==34):
      await event.edit("**Riddikulus**")
    if (x==35):
      await event.edit("**Scourgify**")
    if (x==36):
      await event.edit("**Sectumsempra**")
    if (x==37):
      await event.edit("**Silencio**")
    if (x==37):
      await event.edit("**Stupefy**")
    if (x==38):
      await event.edit("**Tergeo**")
    if (x==39):
      await event.edit("**Wingardium Leviosa**")





