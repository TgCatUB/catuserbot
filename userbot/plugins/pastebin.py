"""IX.IO pastebin like site
Syntax: .paste
Syntax: .npaste
Syntax: .paster
Syntax: .iffuci
"""

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import asyncio
import os
from datetime import datetime
import requests
from telethon import events
from userbot.utils import admin_cmd
from userbot.uniborgConfig import Config  
from telethon.errors.rpcerrorlist import YouBlockedUserError
from requests import exceptions, get, post

def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))
    
from userbot import CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

DOGBIN_URL = "https://del.dog/"

BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
BOTLOG = True

@borg.on(admin_cmd(pattern="paste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.edit("Dogged to {} in {} seconds. GoTo Original URL: {}".format(url, ms, nurl))
    else:
        await event.edit("Dogged to {} in {} seconds".format(url, ms))
        

@register(outgoing=True, pattern="^\.getpaste(?: |$)(.*)")
async def get_dogbin_content(dog_url):
    """ For .getpaste command, fetches the content of a dogbin URL. """
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit("`Getting dogbin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f'{DOGBIN_URL}'
    format_view = f'{DOGBIN_URL}v/'

    if message.startswith(format_view):
        message = message[len(format_view):]
    elif message.startswith(format_normal):
        message = message[len(format_normal):]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/"):]
    else:
        await dog_url.edit("`Is that even a dogbin url?`")
        return

    resp = get(f'{DOGBIN_URL}raw/{message}')

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await dog_url.edit(
            "Request returned an unsuccessful status code.\n\n" + str(HTTPErr))
        return
    except exceptions.Timeout as TimeoutErr:
        await dog_url.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await dog_url.edit(
            "Request exceeded the configured number of maximum redirections." +
            str(RedirectsErr))
        return

    reply_text = "`Fetched dogbin URL content successfully!`\n\n`Content:` " + resp.text

    await dog_url.edit(reply_text)
    if BOTLOG:
        await dog_url.client.send_message(
            BOTLOG_CHATID,
            "Get dogbin content query was executed successfully",
        )


      
        
@borg.on(admin_cmd(pattern="npaste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.npaste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                # message += m.decode("UTF-8") + "\r\n"
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.npaste <long text to include>`"
    py_file =  ""
    if downloaded_file_name.endswith(".py"):
        py_file += ".py"
        data = message
        key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}{py_file}'
        reply_text = f'Nekofied to *Nekobin* : {url}'
        await event.edit(reply_text)
    else:
        data = message
        key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}'
        reply_text = f'Nekofied to *Nekobin* : {url}'
        await event.edit(reply_text)


 
    
    
    
@borg.on(admin_cmd(pattern="iffuci ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.iffuci <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.iffuci <long text to include>`"
    url = "https://www.iffuci.tk/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://iffuci.tk/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://iffuci.tk/v/{r['key']}"
        await event.edit("code is pasted to {} in {} seconds. GoTo Original URL: {}".format(url, ms, nurl))
    else:
        await event.edit("code is pasted to {} in {} seconds".format(url, ms))



@borg.on(admin_cmd(pattern="paster ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    reply_message = await event.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    chat = "@chotamreaderbot"
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.edit("Dogged to {} in {} seconds. GoTo Original URL: {}".format(url, ms, nurl))
    #This module is modded by @ViperAdnan #KeepCredit
    else:
      await event.edit("**Making instant view...**")
      async with event.client.conversation(chat) as conv:
            try:     
                response = conv.wait_event(events.NewMessage(incoming=True,from_users=272572121))
                await event.client.send_message(chat, url)
                response = await response 
            except YouBlockedUserError: 
                await event.reply("```Please unblock me (@chotamreaderbot) u Nigga```")
                return
            await event.delete()
            await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)

CMD_HELP.update({
    "pastebin":
    ".paste <text/reply>\
\nUsage: Create a paste or a shortened url using dogbin (https://del.dog/)\
\n\n.getpaste\
\nUsage: Gets the content of a paste or shortened url from dogbin (https://del.dog/)\
\n\n.npaste <text/reply>\
\nUsage: Create a paste or a shortened url using nekobin (https://nekobin.com)\
\n\n.iffuci <text/reply>\
\nUsage: Create a paste or a shortened url using iffuci (https://www.iffuci.tk)\
\n\n.paster <text/reply>\
\nUsage: Create a instant view or a paste it in telegraph file\
  "
})  
