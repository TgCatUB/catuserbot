import requests
from bs4 import BeautifulSoup
from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
from userbot.utils import admin_cmd , sudo_cmd
import glob
import os  
from userbot import catdef, CMD_HELP

@borg.on(admin_cmd(pattern="song(?: |$)(.*)"))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("wi8..! I am finding your song....`")
    elif reply.message:
        query = reply.message
        await event.edit("wi8..! I am finding your song....`")
    else:
    	await event.edit("`What I am Supposed to find `")
    	return
    
    catdef.catmusic(str(query),"320k")
    l = glob.glob("*.mp3")
    loa = l[0]
    await event.edit("yeah..! i found something wi8..🥰")
    await borg.send_file(
                event.chat_id,
                loa,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to=reply_to_id
            )
    await event.delete()
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)		      
    
@borg.on(sudo_cmd(pattern="song(?: |$)(.*)", allow_sudo = True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        san = await event.reply("wi8..! I am finding your song....`")
    elif reply.message:
        query = reply.message
        san = await event.reply("wi8..! I am finding your song....`")
    else:
    	san = await event.reply("`What I am Supposed to find `")
    	return
    catdef.catmusic(str(query),"320k")
    l = glob.glob("*.mp3")
    loa = l[0]
    await event.edit("yeah..! i found something wi8..🥰")
    await borg.send_file(
                event.chat_id,
                loa,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to=reply_to_id
            )
    await san.delete()
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)
    
CMD_HELP.update({"getmusic":
    "`.song` query or `.song` reply to song name :\
    \nUSAGE:finds the song you entered in query and sends it"
})    
