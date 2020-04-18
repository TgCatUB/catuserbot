"""
HeadPat Module for Userbot (http://headp.at)
cmd:- .pat username or reply to msg
By:- git: jaskaranSM tg: @Zero_cool7870




"""




from userbot.utils import admin_cmd
from random import choice
from urllib import parse
from os import remove
import requests
import asyncio








BASE_URL = "https://headp.at/pats/{}"
PAT_IMAGE = "pat.jpg"




@borg.on(admin_cmd(pattern="pat ?(.*)", outgoing =True))
async def lastfm(event):
    if event.fwd_from:
        return
    username = event.pattern_match.group(1)
    if not username and not event.reply_to_msg_id:
        await event.edit("`Reply to a message or provide username`")
        return 




    resp = requests.get("http://headp.at/js/pats.json")
    pats = resp.json()
    pat = BASE_URL.format(parse.quote(choice(pats)))
    await event.delete()
    with open(PAT_IMAGE,'wb') as f:
        f.write(requests.get(pat).content)
    if username:
        await borg.send_file(event.chat_id,PAT_IMAGE,caption=username)
    else:
        await borg.send_file(event.chat_id,PAT_IMAGE,reply_to=event.reply_to_msg_id) 
    remove(PAT_IMAGE)