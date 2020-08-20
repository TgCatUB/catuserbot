"""DA.GD helpers in @UniBorg
Available Commands:
.isup URL
.dns google.com
.url <long url>
.unshort <short url>"""

import os
import json
import requests
from telethon import events
from userbot import CMD_HELP
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

@borg.on(admin_cmd(pattern="dns (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event ,"DNS records of {} are \n{}".format(input_str, response_api))
    else:
        await edit_or_reply(event ,"i can't seem to find {} on the internet".format(input_str))

@borg.on(admin_cmd(pattern="url (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event ,"Generated {} for {}.".format(response_api, input_str))
    else:
        await edit_or_reply(event ,"something is wrong. please try again later.")

@borg.on(admin_cmd(pattern="unshort (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith('3'):
        await edit_or_reply(event ,"Input URL: {}\nReDirected URL: {}".format(input_str, r.headers["Location"]))
    else:
        await edit_or_reply(event ,"Input URL {} returned status_code {}".format(input_str, r.status_code))
        
CMD_HELP.update({
    "ping":
    "**SYNTAX :** `.dns link`\
    \n**USAGE : **Shows you Domain Name System(dns) of the given link . example `.dns google.com` or `.dns github.cm`\
    \n\n**SYNTAX : **`.url link`\
    \n**USAGE : **shortens the given link\
    \n\n**SYNTAX : **`.unshort link`\
    \n**USAGE : **unshortens the given short link\
    "
})               
