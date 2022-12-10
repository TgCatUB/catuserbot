import os
import random
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
from ..helpers.utils import headers, pastetext, reply_id
from ..sql_helper.globals import addgvar, gvarstatus
from . import hmention

plugin_category = "utils"

extractor = URLExtract()

LOGS = logging.getLogger(__name__)

pastebins = {
    "Pasty": "p",
    "Neko": "n",
    "Spacebin": "s",
    "Dog": "d",
}

THEMES = [
    "breeze",
    "candy",
    "crimson",
    "falcon",
    "meadow",
    "midnight",
    "raindrop",
    "sunset",
]

MODES = ["mode-day", "mode-night"]


def get_key(val):
    for key, value in pastebins.items():
        if val == value:
            return key


def text_chunk_list(query, bits=29900):
    text_list = []
    string = query
    checker = len(query)
    if checker > bits:
        limit = int(checker / (int(checker / bits) + 1))
        string = ""

        for item in query.split(" "):
            string += f"{item} "
            if len(string) > limit:
                string = string.replace(item, "")
                text_list.append(string)
                string = ""
    if string != "":
        text_list.append(string)
    return text_list


@catub.cat_cmd(
    pattern="rayso(?:\s|$)([\s\S]*)",
    command=("rayso", plugin_category),
    info={
        "header": "Create beautiful images of your code",
        "Themes": "`breeze` | `candy` | `crimson` | `falcon` | `meadow` | `midnight` | `raindrop` | `random` | `sunset` |",
        "Modes": "`Mode-Day` | `Mode-Night` |",
        "examples": [
            "{tr}rayso -l",
            "{tr}rayso breeze",
            "{tr}rayso Cat is op",
            "{tr}rayso <reply>",
        ],
        "usage": [
            "{tr}rayso -l (get list of themes & modes)",
            "{tr}rayso <theme> (change the theme)",
            "{tr}rayso <text/reply> (generate)",
            "{tr}rayso <theme> <text/reply>(generate with the theme)",
        ],
    },
)
async def rayso_by_pro_odi(event):  # By @feelded
    "To paste text or file into image."
    checker = None
    files = []
    captions = []
    reply_to_id = await reply_id(event)
    query = event.pattern_match.group(1)
    rquery = await event.get_reply_message()
    catevent = await edit_or_reply(event, "**⏳ Processing ...**")
    if query:
        checker = query.split(maxsplit=1)

    # Add Theme
    if checker and (checker[0].lower() in THEMES or checker[0].lower() == "random"):
        addgvar("RAYSO_THEME", checker[0].lower())
        if checker[0] == query and not rquery:
            return await edit_delete(catevent, f"`Theme changed to {query.title()}.`")
        query = checker[1] if len(checker) > 1 else None

    # Add Mode
    if checker and checker[0].lower() in MODES:
        addgvar("RAYSO_MODES", checker[0].lower())
        if checker[0] == query and not rquery:
            return await edit_delete(
                catevent, f"`Theme Mode changed to {query.title()}.`"
            )
        query = checker[1] if len(checker) > 1 else None

    # Themes List
    if query == "-l":
        ALLTHEME = "**🎈Modes:**\n**1.**  `Mode-Day`\n**2.**  `Mode-Night`\n\n**🎈Themes:**\n**1.**  `Random`"
        for i, each in enumerate(THEMES, start=2):
            ALLTHEME += f"\n**{i}.**  `{each.title()}`"
        return await edit_delete(catevent, ALLTHEME, 60)

    # Get Theme
    theme = gvarstatus("RAYSO_THEME") or "random"
    if theme == "random":
        theme = random.choice(THEMES)

    # Get Mode
    mode = gvarstatus("RAYSO_MODES") or "mode-night"
    darkMode = True if mode == "mode-night" else False

    if query:
        text = query
    elif rquery:
        if rquery.file and rquery.file.mime_type.startswith("text"):
            filename = await rquery.download_media()
            with open(filename, "r") as f:
                text = str(f.read())
            os.remove(filename)
        elif rquery.text:
            text = rquery.raw_text
        else:
            return await edit_delete(catevent, "`Unsupported.`")
    else:
        return await edit_delete(catevent, "`What should I do?`")

    # // Max size 30000 byte but that breaks thumb so making on 28000 byte
    text_list = text_chunk_list(text, 28000)
    for i, text in enumerate(text_list, start=1):
        await edit_or_reply(catevent, f"**⏳ Pasting on image : {i}/{len(text_list)} **")
        r = requests.post(
            "https://rayso-cat.herokuapp.com/api",
            json={
                "code": str(text),
                "title": (await catub.get_me()).first_name,
                "theme": theme,
                "language": "python",
                "darkMode": darkMode,
            },
            headers=headers,
        )
        name = f"rayso{i}.png"
        with open(name, "wb") as f:
            f.write(r.content)
        files.append(name)
        captions.append("")
    await edit_or_reply(catevent, f"**📎 Uploading... **")
    captions[-1] = f"<i>➥ Generated by : <b>{hmention}</b></i>"
    await catub.send_file(
        event.chat_id,
        files,
        reply_to=reply_to_id,
        force_document=True,
        caption=captions,
        parse_mode="html",
    )
    await catevent.delete()
    for name in files:
        os.remove(name)


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
        mediatype = await media_type(reply)
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
        mediatype = await media_type(reply)
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
    rawurl = url if "raw" in url else None
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
        mediatype = await media_type(reply)
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
            if urls := extractor.find_urls(response.text):
                result = f"The instant preview is [here]({urls[0]})"
        if result == "":
            result = "I can't make it as instant view"
        await catevent.edit(result, link_preview=True)
