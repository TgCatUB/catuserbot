"""
Telegram Channel Media Downloader Plugin for userbot.
usage: .geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]
       .getc number_of_messsages channel_username  
By: @Zero_cool7870
"""
from telethon import events
import asyncio
import os
import subprocess
import sys
import time 
from userbot.utils import admin_cmd, humanbytes, progress, time_formatter
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern=r"getc(?: |$)(.*)"))
async def get_media(event):
    if event.fwd_from:
        return
    dir= "./temp/"
    try:
        os.makedirs("./temp/")
    except:
        pass
    catty = event.pattern_match.group(1)
    command = ['ls','temp','|','wc','-l' ]
    limit = int(catty.split(' ')[0])
    channel_username = str(catty.split(' ')[1])
    await event.edit("Downloading Media From this Channel.")
    msgs = await borg.get_messages(channel_username, limit=int(limit))
    with open('log.txt','w') as f:
        f.write(str(msgs))
    i = 0           
    for msg in msgs:
       if msg.media is not None:
            await borg.download_media(msg,dir)
            i +=1
            await event.edit(f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`")
    ps = subprocess.Popen(('ls', 'temp'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'"," ")
    output = output.replace("\\n'"," ")
    await event.edit("Downloaded "+output+" files.")
             
@borg.on(admin_cmd(pattern=r"geta(?: |$)(.*)"))
async def get_media(event):
    if event.fwd_from:
        return
    dir= "./temp/"
    try:
        os.makedirs("./temp/")
    except:
        pass
    channel_username = event.pattern_match.group(1)
    command = ['ls','temp','|','wc','-l' ]
    await event.edit("Downloading All Media From this Channel.")
    msgs = await borg.get_messages(channel_username,limit=3000)
    with open('log.txt','w') as f:
        f.write(str(msgs))
    i = 0
    for msg in msgs:
       if msg.media is not None:
           await borg.download_media(msg,dir)   
           i +=1
           await event.edit(f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`")
    ps = subprocess.Popen(('ls', 'temp'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'","")
    output = output.replace("\\n'","")
    await event.edit("Downloaded "+output+" files.")

CMD_HELP.update({"channel_download": "Telegram Channel Media Downloader Plugin for userbot.\
\n\n**usage :**\n .geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]\
\n .getc number_of_messsages channel_username" 
})  
