import os
import re

import pygments
import requests
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.utils import get_extension
from urlextract import URLExtract

from userbot import catub

from ..Config import Config
from ..core.events import MessageEdited
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import pastetext, reply_id

plugin_category = "utils"

extractor = URLExtract()

LOGS = logging.getLogger(__name__)

pastebins = {
    "Pasty": "p",
    "Neko": "n",
    "Spacebin": "s",
    "Dog": "d",
}


def get_key(val):
    for key, value in pastebins.items():
        if val == value:
            return key


@catub.cat_cmd(
    pattern="pcode(?:\s|$)([\s\S]*)",
    command=("pcode", plugin_category),
    info={
        "header": "Will paste the entire text on the blank white image.",
        "flags": {
            "f": "Use this flag to send it as file rather than image",
        },
        "usage": ["{tr}pcode <reply>", "{tr}pcode text"],
    },
)
async def paste_img(event):
    "To paste text to image."
    reply_to = await reply_id(event)
    d_file_name = None
    catevent = await edit_or_reply(event, "`Pasting the text on image`")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    ext = re.findall(r"-f", input_str)
    extension = None
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    text_to_print = input_str or ""
    if text_to_print == "" and reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply and reply.text:
            text_to_print = reply.raw_text
        else:
            return await edit_delete(
                catevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    pygments.highlight(
        text_to_print,
        Python3Lexer(),
        ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
        "out.png",
    )
    try:
        await event.client.send_file(
            event.chat_id,
            "out.png",
            force_document=bool(extension),
            reply_to=reply_to,
        )
        await catevent.delete()
        os.remove("out.png")
        if d_file_name is not None:
            os.remove(d_file_name)
    except Exception as e:
        await edit_delete(catevent, f"**Error:**\n`{e}`", time=10)


@catub.cat_cmd(
    pattern="(d|p|s|n)?(paste|neko)(?:\s|$)([\S\s]*)",
    command=("paste", plugin_category),
    info={
        "header": "To paste text to a paste bin.",
        "description": "Uploads the given text to website so that you can share text/code with others easily. If no flag is used then it will use p as default",
        "flags": {
            "d": "Will paste text to dog.bin",
            "p": "Will paste text to pasty.lus.pm",
            "s": "Will paste text to spaceb.in (language extension not there at present.)",
        },
        "usage": [
            "{tr}{flags}paste <reply/text>",
            "{tr}{flags}paste {extension} <reply/text>",
        ],
        "examples": [
            "{tr}spaste <reply/text>",
            "{tr}ppaste -py await event.client.send_message(chat,'Hello! testing123 123')",
        ],
    },
)
async def paste_bin(event):
    "To paste text to a paste bin."
    catevent = await edit_or_reply(event, "`pasting text to paste bin....`")
    input_str = event.pattern_match.group(3)
    reply = await event.get_reply_message()
    ext = re.findall(r"-\w+", input_str)
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    if event.pattern_match.group(2) == "neko":
        pastetype = "n"
    else:
        pastetype = event.pattern_match.group(1) or "p"
    text_to_print = input_str or ""
    if text_to_print == "" and reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            if extension is None:
                extension = get_extension(reply.document)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply and reply.text:
            text_to_print = reply.raw_text
        else:
            return await edit_delete(
                catevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    if extension and extension.startswith("."):
        extension = extension[1:]
    try:
        response = await pastetext(text_to_print, pastetype, extension)
        if "error" in response:
            return await edit_delete(
                catevent,
                "**Error while pasting text:**\n`Unable to process your request may be pastebins are down.`",
            )

        result = ""
        if pastebins[response["bin"]] != pastetype:
            result += f"<b>{get_key(pastetype)} is down, So </b>"
        result += f"<b>Pasted to: <a href={response['url']}>{response['bin']}</a></b>"
        if response["raw"] != "":
            result += f"\n<b>Raw link: <a href={response['raw']}>Raw</a></b>"
        await catevent.edit(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await edit_delete(catevent, f"**Error while pasting text:**\n`{e}`")


@catub.cat_cmd(
    command=("neko", plugin_category),
    info={
        "header": "To paste text to a neko bin.",
        "description": "Uploads the given text to nekobin so that you can share text/code with others easily.",
        "usage": ["{tr}neko <reply/text>", "{tr}neko {extension} <reply/text>"],
        "examples": [
            "{tr}neko <reply/text>",
            "{tr}neko -py await event.client.send_message(chat,'Hello! testing123 123')",
        ],
    },
)
async def _(event):
    "To paste text to a neko bin."
    # just to show in help menu as seperate


@catub.cat_cmd(
    pattern="g(et)?paste(?:\s|$)([\s\S]*)",
    command=("getpaste", plugin_category),
    info={
        "header": "To paste text into telegram from pastebin link.",
        "description": "Gets the content of a pastebin. You can provide link along with cmd or reply to link.",
        "Support bins": ["pasty", "spacebin", "nekobin", "dogbin"],
        "usage": ["{tr}getpaste <link>", "{tr}gpaste <link>"],
    },
)
async def get_dogbin_content(event):
    "To paste text into telegram from del dog link."
    textx = await event.get_reply_message()
    url = event.pattern_match.group(2)
    if not url and textx.text:
        urls = extractor.find_urls(textx.text)
        for iurl in urls:
            if (
                ("pasty" in iurl)
                or ("spaceb" in iurl)
                or ("nekobin" in iurl)
                or ("catbin" in iurl)
            ):
                url = iurl
                break
    if not url:
        return await edit_delete(event, "__I can't find any pastebin link.__")
    catevent = await edit_or_reply(event, "`Getting Contents of pastebin.....`")
    rawurl = None
    if "raw" in url:
        rawurl = url
    if rawurl is None:
        fid = os.path.splitext((os.path.basename(url)))
        if "pasty" in url:
            rawurl = f"https://pasty.lus.pm/{fid[0]}/raw"
        elif "spaceb" in url:
            rawurl = f"https://spaceb.in/api/v1/documents/{fid[0]}/raw"
        elif "nekobin" in url:
            rawurl = f"nekobin.com/raw/{fid[0]}"
        elif "catbin" in url:
            rawurl = f"http://catbin.up.railway.app/raw/{fid[0]}"
        else:
            return await edit_delete(event, "__This pastebin is not supported.__")
    resp = requests.get(rawurl)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as HTTPErr:
        return await catevent.edit(
            f"**Request returned an unsuccessful status code.**\n\n__{str(HTTPErr)}__"
        )
    except requests.exceptions.Timeout as TimeoutErr:
        return await catevent.edit(f"**Request timed out.**__{str(TimeoutErr)}__")
    except requests.exceptions.TooManyRedirects as RedirectsErr:
        return await catevent.edit(
            (
                f"**Request exceeded the configured number of maximum redirections.**__{str(RedirectsErr)}__"
            )
        )
    reply_text = f"**Fetched dogbin URL content successfully!**\n\n**Content:** \n```{resp.text}```"
    await edit_or_reply(catevent, reply_text)


@catub.cat_cmd(
    pattern="paster(?:\s|$)([\s\S]*)",
    command=("paster", plugin_category),
    info={
        "header": "Create a instant view or a paste it in telegraph file.",
        "usage": ["{tr}paster <reply>", "{tr}paster text"],
    },
)
async def _(event):
    "Create a instant view or a paste it in telegraph file."
    catevent = await edit_or_reply(event, "`pasting text to paste bin....`")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    pastetype = "d"
    text_to_print = input_str or ""
    if text_to_print == "" and reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply and reply.text:
            text_to_print = reply.raw_text
        else:
            return await edit_delete(
                catevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    try:
        response = await pastetext(text_to_print, pastetype, extension="txt")
        if "error" in response:
            return await edit_delete(
                catevent,
                "**Error while pasting text:**\n`Unable to process your request may be pastebins are down.`",
            )

    except Exception as e:
        return await edit_delete(catevent, f"**Error while pasting text:**\n`{e}`")
    url = response["url"]
    chat = "@CorsaBot"
    await catevent.edit("`Making instant view...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                MessageEdited(incoming=True, from_users=conv.chat_id), timeout=10
            )
            await event.client.send_message(chat, url)
            response = await response
        except YouBlockedUserError:
            return await catevent.edit("```Please unblock me (@CorsaBot) and try```")
        result = ""
        if response:
            await event.client.send_read_acknowledge(conv.chat_id)
            urls = extractor.find_urls(response.text)
            if urls:
                result = f"The instant preview is [here]({urls[0]})"
        if result == "":
            result = "I can't make it as instant view"
        await catevent.edit(result, link_preview=True)
