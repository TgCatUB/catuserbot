# For @UniBorg

"""Countdown Commands

.wchar"""



from telethon import events

from datetime import datetime

import importlib.util

import asyncio

import random

import importlib.util




from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"wchar", allow_sudo=True))

async def timer_blankx(e):

 txt=e.text[7:] + '\n\n`Tesla Wireless Charging (beta) Started...\nDevice Detected: Nokia 1100\nBattery Percentage:` '

 j=10

 k=j

 for j in range(j):

  await e.edit(txt + str(k))

  k=k+10

  await asyncio.sleep(1)

 if e.pattern_match.group(1) == '100':

  await e.edit("`Tesla Wireless Charging (beta) Completed...\nDevice Detected: Nokia 1100 (Space Grey Varient)\nBattery Percentage:` [100%](https://telegra.ph/file/a45aa7450c8eefed599d9.mp4) ", link_preview=True)


