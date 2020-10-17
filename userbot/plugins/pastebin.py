# pastebin for catuserbot

import logging
import os

import requests
from requests import exceptions, get
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


DOGBIN_URL = "https://del.dog/"


@bot.on(admin_cmd(pattern="paste( (.*)|$)", outgoing=True))
@bot.on(sudo_cmd(pattern="paste( (.*)|$)", allow_sudo=True))
async def _(event):
    catevent = await edit_or_reply(event, "`pasting to del dog.....`")
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TEMP_DIR,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            try:
                for m in m_list:
                    message += m.decode("UTF-8")
            except:
                message = "Usage : .paste <long text to include/reply to text file>"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "Usage : .paste <long text to include/reply to text file>"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await catevent.edit(
            "**Pasted to dogbin : **[dog]({}).\n**GoTo Original URL: **[link]({})".format(
                nurl, url
            )
        )
    else:
        await catevent.edit("**Pasted to dogbin : **[dog]({})".format(url))


@bot.on(admin_cmd(pattern="neko( (.*)|$)", outgoing=True))
@bot.on(sudo_cmd(pattern="neko( (.*)|$)", allow_sudo=True))
async def _(event):
    catevent = await edit_or_reply(event, "`pasting to neko bin.....`")
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    if input_str:
        message = input_str
        downloaded_file_name = None
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TEMP_DIR,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            try:
                for m in m_list:
                    message += m.decode("UTF-8")
            except:
                message = (
                    "**Usage : **`.neko <long text to include/reply to text file>`"
                )
            os.remove(downloaded_file_name)
        else:
            downloaded_file_name = None
            message = previous_message.message
    else:
        downloaded_file_name = None
        message = "**Usage : **`.neko <long text to include/reply to text file>`"
    if downloaded_file_name and downloaded_file_name.endswith(".py"):
        py_file = ".py"
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}{py_file}"
    else:
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}"
    reply_text = f"**Pasted to Nekobin : **[neko]({url})"
    await catevent.edit(reply_text)


@bot.on(admin_cmd(pattern="iffuci( (.*)|$)", outgoing=True))
@bot.on(sudo_cmd(pattern="iffuci( (.*)|$)", allow_sudo=True))
async def _(event):
    catevent = await edit_or_reply(event, "`pasting to del dog.....`")
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TEMP_DIR,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            try:
                for m in m_list:
                    message += m.decode("UTF-8")
            except:
                message = "Usage : .paste <long text to include/reply to text file>"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "Usage : .paste <long text to include/reply to text file>"
    url = "https://www.iffuci.tk/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://iffuci.tk/{r['key']}"
    if r["isUrl"]:
        nurl = f"https://iffuci.tk/v/{r['key']}"
        await catevent.edit(
            "code is pasted to {}. GoTo Original URL: {}".format(nurl, url)
        )
    else:
        await catevent.edit("code is pasted to {}".format(url))


@bot.on(admin_cmd(outgoing=True, pattern="getpaste( (.*)|$)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="getpaste( (.*)|$)"))
async def get_dogbin_content(dog_url):
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    catevent = await edit_or_reply(dog_url, "`Getting dogbin content...`")
    if not message and textx:
        message = str(textx.message)
    format_normal = f"{DOGBIN_URL}"
    format_view = f"{DOGBIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view) :]
    elif message.startswith(format_normal):
        message = message[len(format_normal) :]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/") :]
    else:
        await catevent.edit("`Is that even a dogbin url?`")
        return
    resp = get(f"{DOGBIN_URL}raw/{message}")
    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await catevent.edit(
            "Request returned an unsuccessful status code.\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await catevent.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await catevent.edit(
            "Request exceeded the configured number of maximum redirections."
            + str(RedirectsErr)
        )
        return
    reply_text = "`Fetched dogbin URL content successfully!`\n\n`Content:` " + resp.text
    await catevent.edit(reply_text)


@bot.on(admin_cmd(pattern="paster( (.*)|$)", outgoing=True))
@bot.on(sudo_cmd(pattern="paster( (.*)|$)", allow_sudo=True))
async def _(event):
    catevent = await edit_or_reply(event, "`pasting to del dog.....`")
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    previous_message = None
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TEMP_DIR,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            try:
                for m in m_list:
                    message += m.decode("UTF-8")
            except:
                message = "Usage : .paste <long text to include/reply to text file>"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "Usage : .paste <long text to include/reply to text file>"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    chat = "@chotamreaderbot"
    # This module is modded by @ViperAdnan #KeepCredit
    await catevent.edit("**Making instant view...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=272572121)
            )
            await event.client.send_message(chat, url)
            response = await response
        except YouBlockedUserError:
            await catevent.edit("```Please unblock me (@chotamreaderbot) u Nigga```")
            return
        await catevent.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=previous_message
        )


CMD_HELP.update(
    {
        "pastebin": "**Plugin : **`pastebin`\
        \n\n**Syntax : **`.paste <text/reply>`\
        \n**Function : **Create a paste or a shortened url using dogbin `https://del.dog/`\
        \n\n**Syntax : **`.neko <text/reply>`\
        \n**Function : **Create a paste or a shortened url using nekobin `https://nekobin.com`\
        \n\n**Syntax : **`.iffuci <text/reply>`\
        \n**Function : **Create a paste or a shortened url using iffuci `https://www.iffuci.tk`\
        \n\n**Syntax : **`.getpaste`\
        \n**Function : **Gets the content of a paste or shortened url from dogbin `https://del.dog/`\
        \n\n**Syntax : **`.paster <text/reply>`\
        \n**Function : **Create a instant view or a paste it in telegraph file\
  "
    }
)
