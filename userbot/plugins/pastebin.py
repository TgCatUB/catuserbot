"""IX.IO pastebin like site
Syntax: .paste"""

"""IX.IO pastebin like site
Syntax: .npaste"""


"""iffuci.tk pastebin site
Code written by @loxxi {iffuci}
Syntax: .iffuci"""

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





def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@borg.on(admin_cmd("paste ?(.*)"))
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

        
        
@borg.on(admin_cmd(pattern="npaste ?(.*)"))
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
                # message += m.decode("UTF-8") + "\r\n"
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
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

# data = "tets sgdfgklj kdgjld"

# key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')

# url = f'https://nekobin.com/{key}'

# reply_text = f'Nekofied to *Nekobin* : {url}'
 
    
    
    
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
    
