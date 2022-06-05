import json
import math
import os
import random
import re
import time
from uuid import uuid4

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from youtubesearchpython import VideosSearch

from userbot import catub

from ..Config import Config
from ..helpers.functions import rand_key
from ..helpers.functions.utube import (
    download_button,
    get_yt_video_id,
    get_ytthumb,
    result_formatter,
    ytsearch_data,
)
from ..plugins import mention
from ..sql_helper.globals import gvarstatus
from . import CMD_INFO, GRP_INFO, PLG_INFO, check_owner
from .logger import logging

LOGS = logging.getLogger(__name__)

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
MEDIA_PATH_REGEX = re.compile(r"(:?\<\bmedia:(:?(?:.*?)+)\>)")
tr = Config.COMMAND_HAND_LER


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


def get_thumb(name):
    url = f"https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Inline/{name}.png?raw=true"
    return types.InputWebDocument(url=url, size=0, mime_type="image/png", attributes=[])


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


def main_menu():
    text = f"𝗖𝗮𝘁𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗛𝗲𝗹𝗽𝗲𝗿\
        \n𝗣𝗿𝗼𝘃𝗶𝗱𝗲𝗱 𝗯𝘆 {mention}"
    buttons = [
        (Button.inline("ℹ️ Info", data="check"),),
        (
            Button.inline(f"👮‍♂️ Admin ({len(GRP_INFO['admin'])})", data="admin_menu"),
            Button.inline(f"🤖 Bot ({len(GRP_INFO['bot'])})", data="bot_menu"),
        ),
        (
            Button.inline(f"🎨 Fun ({len(GRP_INFO['fun'])})", data="fun_menu"),
            Button.inline(f"🧩 Misc ({len(GRP_INFO['misc'])})", data="misc_menu"),
        ),
        (
            Button.inline(f"🧰 Tools ({len(GRP_INFO['tools'])})", data="tools_menu"),
            Button.inline(f"🗂 Utils ({len(GRP_INFO['utils'])})", data="utils_menu"),
        ),
        (
            Button.inline(f"➕ Extra ({len(GRP_INFO['extra'])})", data="extra_menu"),
            Button.inline("🔒 Close Menu", data="close"),
        ),
    ]
    if Config.BADCAT:
        switch_button = [
            (
                Button.inline(f"➕ Extra ({len(GRP_INFO['extra'])})", data="extra_menu"),
                Button.inline(
                    f"⚰️ Useless ({len(GRP_INFO['useless'])})", data="useless_menu"
                ),
            ),
            (Button.inline("🔒 Close Menu", data="close"),),
        ]
        buttons = buttons[:-1] + switch_button

    return text, buttons


async def article_builder(event, method):
    media = thumb = photo = None
    link_preview = False
    builder = event.builder
    title = "Cat Userbot"
    description = "Button menu for CatUserbot"
    if method == "help":
        help_info = main_menu()
        title = "Help Menu"
        description = "Help menu for CatUserbot"
        thumb = get_thumb("help")
        query = help_info[0]
        buttons = help_info[1]

    elif method == "deploy":
        media = "https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Inline/catlogo.png"
        title = "𝘾𝙖𝙩𝙐𝙨𝙚𝙧𝙗𝙤𝙩"
        description = "Deploy yourself"
        query = "𝗗𝗲𝗽𝗹𝗼𝘆 𝘆𝗼𝘂𝗿 𝗼𝘄𝗻 𝗖𝗮𝘁𝗨𝘀𝗲𝗿𝗯𝗼𝘁."
        buttons = [
            (
                Button.url("Source code", "https://github.com/TgCatUB/catuserbot"),
                Button.url("Deploy", "https://github.com/TgCatUB/nekopack"),
            )
        ]

    elif method == "pmpermit":
        query = gvarstatus("pmpermit_text")
        buttons = [Button.inline(text="Show Options.", data="show_pmpermit_options")]
        PM_PIC = gvarstatus("pmpermit_pic")
        if PM_PIC:
            CAT = [x for x in PM_PIC.split()]
            PIC = list(CAT)
            media = random.choice(PIC)

    elif method == "ialive":
        thumb = get_thumb("alive")
        buttons = [
            (
                Button.inline("Stats", data="stats"),
                Button.url("Repo", "https://github.com/TgCatUB/catuserbot"),
            )
        ]
        try:
            from userbot.plugins.alive import catalive_text

            query = catalive_text()
        except:
            return None
        title = "Cat Alive"
        description = "Alive menu for CatUserbot"
        ALIVE_PIC = gvarstatus("ALIVE_PIC")
        IALIVE_PIC = gvarstatus("IALIVE_PIC")
        if IALIVE_PIC:
            CAT = [x for x in IALIVE_PIC.split()]
            PIC = list(CAT)
            media = random.choice(PIC)
        if not IALIVE_PIC and ALIVE_PIC:
            CAT = [x for x in ALIVE_PIC.split()]
            PIC = list(CAT)
            media = random.choice(PIC)

    elif method == "spotify":
        try:
            from userbot.plugins.spotify import SP_DATABASE, get_spotify, sp_data

            title = "Spotify"
            description = "Get currently playing song"
            media = "https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Inline/spotify_off.png"
            if (
                not (Config.SPOTIFY_CLIENT_ID and Config.SPOTIFY_CLIENT_SECRET)
                or SP_DATABASE is None
            ):
                query = "__Spotify not setup properly. \nDo `.help spsetup` and follow the tutorial.__"
                buttons = [
                    Button.url(
                        "Tutorial",
                        "https://telegra.ph/Steps-of-setting-Spotify-Vars-in-Catuserbot-04-24-2",
                    )
                ]
            else:
                response = sp_data(
                    "https://api.spotify.com/v1/me/player/currently-playing"
                )
                if response.status_code == 204:
                    query = "__Currently not listening any music on spotify...__"
                    buttons = [Button.url("Open Spotify", "https://open.spotify.com/")]
                else:
                    media, tittle, dic, lyrics, symbol = await get_spotify(
                        event, response
                    )
                    thumb = get_thumb("spotify_on")
                    query = f'**🎶 Track :- ** `{tittle}`\n**🎤 Artist :- ** `{dic["interpret"]}`'
                    buttons = [
                        (
                            Button.url("🎧 Spotify", dic["link"]),
                            Button.url(f"{symbol} Lyrics", lyrics),
                        )
                    ]
        except:
            return None

    elif method.startswith("Inline buttons"):
        markdown_note = method[14:]
        prev = 0
        note_data = ""
        buttons_list = []
        catmedia = MEDIA_PATH_REGEX.search(markdown_note)
        if catmedia:
            media = catmedia.group(2)
            markdown_note = markdown_note.replace(catmedia.group(0), "")
        for match in BTN_URL_REGEX.finditer(markdown_note):
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and markdown_note[to_check] == "\\":
                n_escapes += 1
                to_check -= 1
            if n_escapes % 2 == 0:
                buttons_list.append(
                    (match.group(2), match.group(3), bool(match.group(4)))
                )
                note_data += markdown_note[prev : match.start(1)]
                prev = match.end(1)
            elif n_escapes % 2 == 1:
                note_data += markdown_note[prev:to_check]
                prev = match.start(1) - 1
            else:
                break
        else:
            note_data += markdown_note[prev:]
        query = note_data.strip()
        buttons = ibuild_keyboard(buttons_list)
    if media and not media.endswith((".jpg", ".jpeg", ".png")):
        result = builder.document(
            media,
            title=title,
            thumb=thumb,
            description=description,
            text=query,
            buttons=buttons,
        )
    else:
        type = "article"
        if media and media.endswith((".jpg", ".jpeg", ".png")):
            photo = types.InputWebDocument(
                url=media, size=0, mime_type="image/jpeg", attributes=[]
            )
            type = "photo"
        result = builder.article(
            title=title,
            description=description,
            type=type,
            file=media,
            thumb=thumb if thumb else photo,
            content=photo,
            text=query,
            buttons=buttons,
            link_preview=link_preview,
        )
    return result


def command_in_category(cname):
    cmds = 0
    for i in GRP_INFO[cname]:
        for _ in PLG_INFO[i]:
            cmds += 1
    return cmds


def paginate_help(
    page_number,
    loaded_plugins,
    prefix,
    plugins=True,
    category_plugins=None,
    category_pgno=0,
):  # sourcery no-metrics  # sourcery skip: low-code-quality
    try:
        number_of_rows = int(gvarstatus("NO_OF_ROWS_IN_HELP") or 5)
    except (ValueError, TypeError):
        number_of_rows = 5
    try:
        number_of_cols = int(gvarstatus("NO_OF_COLUMNS_IN_HELP") or 2)
    except (ValueError, TypeError):
        number_of_cols = 2
    HELP_EMOJI = gvarstatus("HELP_EMOJI") or " "
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    if len(HELP_EMOJI) == 2:
        if plugins:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_prev(1)_command_{prefix}_{page_number}",
                )
                for x in helpable_plugins
            ]
        else:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
                )
                for x in helpable_plugins
            ]
    elif plugins:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_prev(1)_command_{prefix}_{page_number}",
            )
            for x in helpable_plugins
        ]
    else:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
            )
            for x in helpable_plugins
        ]
    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    elif len(modules) % number_of_cols == 2:
        pairs.append((modules[-2], modules[-1]))
    max_num_pages = math.ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if plugins:
        if len(pairs) > number_of_rows:

            pairs = pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [
                (
                    Button.inline("⌫", data=f"{prefix}_prev({modulo_page})_plugin"),
                    Button.inline("⚙️ Main Menu", data="mainmenu"),
                    Button.inline("⌦", data=f"{prefix}_next({modulo_page})_plugin"),
                )
            ]
        else:
            pairs = pairs + [(Button.inline("⚙️ Main Menu", data="mainmenu"),)]
    elif len(pairs) > number_of_rows:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "⌫",
                    data=f"{prefix}_prev({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "⬅️ Back ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "⌦",
                    data=f"{prefix}_next({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
            )
        ]
    else:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs + [
            (
                Button.inline(
                    "⬅️ Back ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
            )
        ]
    return pairs


@catub.tgbot.on(InlineQuery)
async def inline_handler(event):  # sourcery no-metrics
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        hmm = re.compile("troll (.*) (.*)")
        match = re.findall(hmm, query)
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        hid = re.compile("hide (.*)")
        match3 = re.findall(hid, query)
        if string == "ialive":
            result = await article_builder(event, string)
            await event.answer([result] if result else None)
        elif query.startswith("Inline buttons"):
            result = await article_builder(event, query)
            await event.answer([result] if result else None)
        elif match:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            troll = os.path.join("./userbot", "troll.txt")
            try:
                jsondata = json.load(open(troll))
            except Exception:
                jsondata = False
            try:
                # if u is user id
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        sandy = f"@{u.username}"
                    else:
                        sandy = f"[{u.first_name}](tg://user?id={u.id})"
                    u = int(u.id)
                except ValueError:
                    # ValueError: Could not find the input entity
                    sandy = f"[user](tg://user?id={u})"
            except ValueError:
                # if u is username
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    sandy = f"@{u.username}"
                else:
                    sandy = f"[{u.first_name}](tg://user?id={u.id})"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time.time() * 2)
            newtroll = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline("show message 🔐", data=f"troll_{timestamp}")]
            result = builder.article(
                title="Troll Message",
                text=f"Only {sandy} cannot access this message!",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newtroll)
                json.dump(jsondata, open(troll, "w"))
            else:
                json.dump(newtroll, open(troll, "w"))
        elif match2:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            secret = os.path.join("./userbot", "secrets.txt")
            try:
                jsondata = json.load(open(secret))
            except Exception:
                jsondata = False
            try:
                # if u is user id
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        sandy = f"@{u.username}"
                    else:
                        sandy = f"[{u.first_name}](tg://user?id={u.id})"
                    u = int(u.id)
                except ValueError:
                    # ValueError: Could not find the input entity
                    sandy = f"[user](tg://user?id={u})"
            except ValueError:
                # if u is username
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    sandy = f"@{u.username}"
                else:
                    sandy = f"[{u.first_name}](tg://user?id={u.id})"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time.time() * 2)
            newsecret = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline("show message 🔐", data=f"secret_{timestamp}")]
            result = builder.article(
                title="secret message",
                text=f"🔒 A whisper message to {sandy}, Only he/she can open it.",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newsecret)
                json.dump(jsondata, open(secret, "w"))
            else:
                json.dump(newsecret, open(secret, "w"))
        elif match3:
            query = query[5:]
            builder = event.builder
            hide = os.path.join("./userbot", "hide.txt")
            try:
                jsondata = json.load(open(hide))
            except Exception:
                jsondata = False
            timestamp = int(time.time() * 2)
            newhide = {str(timestamp): {"text": query}}

            buttons = [Button.inline("Read Message ", data=f"hide_{timestamp}")]
            result = builder.article(
                title="Hidden Message",
                text=f"✖✖✖",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newhide)
                json.dump(jsondata, open(hide, "w"))
            else:
                json.dump(newhide, open(hide, "w"))
        elif string == "help":
            result = await article_builder(event, string)
            await event.answer([result] if result else None)
        elif string == "spotify":
            result = await article_builder(event, string)
            await event.answer([result] if result else None)
        elif str_y[0].lower() == "ytdl" and len(str_y) == 2:
            link = get_yt_video_id(str_y[1].strip())
            found_ = True
            if link is None:
                search = VideosSearch(str_y[1].strip(), limit=15)
                resp = (search.result()).get("result")
                if len(resp) == 0:
                    found_ = False
                else:
                    outdata = await result_formatter(resp)
                    key_ = rand_key()
                    ytsearch_data.store_(key_, outdata)
                    buttons = [
                        Button.inline(
                            f"1 / {len(outdata)}",
                            data=f"ytdl_next_{key_}_1",
                        ),
                        Button.inline(
                            "📜  List all",
                            data=f"ytdl_listall_{key_}_1",
                        ),
                        Button.inline(
                            "⬇️  Download",
                            data=f'ytdl_download_{outdata[1]["video_id"]}_0',
                        ),
                    ]
                    caption = outdata[1]["message"]
                    photo = await get_ytthumb(outdata[1]["video_id"])
            else:
                caption, buttons = await download_button(link, body=True)
                photo = await get_ytthumb(link)
            if found_:
                markup = event.client.build_reply_markup(buttons)
                photo = types.InputWebDocument(
                    url=photo, size=0, mime_type="image/jpeg", attributes=[]
                )
                text, msg_entities = await event.client._parse_message_text(
                    caption, "html"
                )
                result = types.InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=link,
                    description="⬇️ Click to Download",
                    thumb=photo,
                    content=photo,
                    send_message=types.InputBotInlineMessageMediaAuto(
                        reply_markup=markup, message=text, entities=msg_entities
                    ),
                )
            else:
                result = builder.article(
                    title="Not Found",
                    text=f"No Results found for `{str_y[1]}`",
                    description="INVALID",
                )
            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="Not Found",
                            text=f"No Results found for `{str_y[1]}`",
                            description="INVALID",
                        )
                    ]
                )
        elif string == "age_verification_alert":
            buttons = [
                Button.inline(text="Yes I'm 18+", data="age_verification_true"),
                Button.inline(text="No I'm Not", data="age_verification_false"),
            ]
            markup = event.client.build_reply_markup(buttons)
            photo = types.InputWebDocument(
                url="https://i.imgur.com/Zg58iXc.jpg",
                size=0,
                mime_type="image/jpeg",
                attributes=[],
            )
            text, msg_entities = await event.client._parse_message_text(
                "<b>ARE YOU OLD ENOUGH FOR THIS ?</b>", "html"
            )
            result = types.InputBotInlineResult(
                id=str(uuid4()),
                type="photo",
                title="Age verification",
                thumb=photo,
                content=photo,
                send_message=types.InputBotInlineMessageMediaAuto(
                    reply_markup=markup, message=text, entities=msg_entities
                ),
            )
            await event.answer([result] if result else None)
        elif string == "pmpermit":
            result = await article_builder(event, string)
            await event.answer([result] if result else None)
        elif string == "":
            results = []
            alive_menu = await article_builder(event, "ialive")
            results.append(alive_menu) if alive_menu else None
            help_menu = await article_builder(event, "help")
            results.append(help_menu) if help_menu else None
            spotify_menu = await article_builder(event, "spotify")
            results.append(spotify_menu) if spotify_menu else None
            results.append(
                builder.article(
                    title="Secret",
                    description="Send secret message to your friends",
                    text="__Send secret message which only you & the reciver can see..__",
                    thumb=get_thumb("secret"),
                    buttons=[
                        Button.switch_inline(
                            "Secret Text", query="secret @username Text", same_peer=True
                        )
                    ],
                ),
            )
            results.append(
                builder.article(
                    title="Troll",
                    description="Send troll message to your friends",
                    text="__Send troll message which everyone can see except the reciver..__",
                    thumb=get_thumb("troll"),
                    buttons=[
                        Button.switch_inline(
                            "Troll Text", query="troll @username Text", same_peer=True
                        )
                    ],
                ),
            )
            results.append(
                builder.article(
                    title="Hide",
                    description="Send hidden text in chat",
                    text="__Send hidded message to save from being quote..__",
                    thumb=get_thumb("hide"),
                    buttons=[
                        Button.switch_inline(
                            "Hidden Text", query="hide Text", same_peer=True
                        )
                    ],
                ),
            )
            results.append(
                builder.article(
                    title="Youtube Download",
                    description="Download videos from YouTube",
                    text="__Download videos or audio from YouTube with different option of resolution..__",
                    thumb=get_thumb("youtube"),
                    buttons=[
                        Button.switch_inline(
                            "Youtube-dl", query="ytdl perfect", same_peer=True
                        )
                    ],
                ),
            )
            await event.answer(results)
    else:
        result = await article_builder(event, "deploy")
        await event.answer([result] if result else None)


@catub.tgbot.on(CallbackQuery(data=re.compile(b"close")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    buttons = [
        (Button.inline("Open Menu", data="mainmenu"),),
    ]
    await event.edit("Menu Closed", buttons=buttons)


@catub.tgbot.on(CallbackQuery(data=re.compile(b"check")))
async def on_plugin_callback_query_handler(event):
    text = f"𝙿𝚕𝚞𝚐𝚒𝚗𝚜: {len(PLG_INFO)}\
        \n𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜: {len(CMD_INFO)}\
        \n\n{tr}𝚑𝚎𝚕𝚙 <𝚙𝚕𝚞𝚐𝚒𝚗> : 𝙵𝚘𝚛 𝚜𝚙𝚎𝚌𝚒𝚏𝚒𝚌 𝚙𝚕𝚞𝚐𝚒𝚗 𝚒𝚗𝚏𝚘.\
        \n{tr}𝚑𝚎𝚕𝚙 -𝚌 <𝚌𝚘𝚖𝚖𝚊𝚗𝚍> : 𝙵𝚘𝚛 𝚊𝚗𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚒𝚗𝚏𝚘.\
        \n{tr}𝚜 <𝚚𝚞𝚎𝚛𝚢> : 𝚃𝚘 𝚜𝚎𝚊𝚛𝚌𝚑 𝚊𝚗𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜.\
        "
    await event.answer(text, cache_time=0, alert=True)


@catub.tgbot.on(CallbackQuery(data=re.compile(b"(.*)_menu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    buttons = paginate_help(0, GRP_INFO[category], category)
    text = f"**Category: **{category}\
        \n**Total plugins :** {len(GRP_INFO[category])}\
        \n**Total Commands:** {command_in_category(category)}"
    await event.edit(text, buttons=buttons)


@catub.tgbot.on(
    CallbackQuery(
        data=re.compile(b"back_([a-z]+)_([a-z_1-9]+)_([0-9]+)_?([a-z1-9]+)?_?([0-9]+)?")
    )
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    mtype = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    if mtype == "plugin":
        buttons = paginate_help(pgno, GRP_INFO[category], category)
        text = f"**Category: **`{category}`\
            \n**Total plugins :** __{len(GRP_INFO[category])}__\
            \n**Total Commands:** __{command_in_category(category)}__"
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            pgno,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**Plugin: **`{category}`\
                \n**Category: **__{getkey(category)}__\
                \n**Total Commands:** __{len(PLG_INFO[category])}__"
    await event.edit(text, buttons=buttons)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"mainmenu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    _result = main_menu()
    await event.edit(_result[0], buttons=_result[1])


@catub.tgbot.on(
    CallbackQuery(data=re.compile(rb"(.*)_prev\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number - 1, GRP_INFO[category], category)
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            current_page_number - 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**Plugin: **`{category}`\
                \n**Category: **__{getkey(category)}__\
                \n**Total Commands:** __{len(PLG_INFO[category])}__"
        try:
            return await event.edit(text, buttons=buttons)
        except Exception as e:
            LOGS.error(str(e))
    await event.edit(buttons=buttons)


@catub.tgbot.on(
    CallbackQuery(data=re.compile(rb"(.*)_next\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = event.pattern_match.group(4)
    if category_plugins:
        category_plugins = str(category_plugins.decode("UTF-8"))
    category_pgno = event.pattern_match.group(5)
    if category_pgno:
        category_pgno = int(category_pgno.decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number + 1, GRP_INFO[category], category)
    else:
        buttons = paginate_help(
            current_page_number + 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
    await event.edit(buttons=buttons)


@catub.tgbot.on(
    CallbackQuery(
        data=re.compile(b"(.*)_cmdhelp_([a-z_1-9]+)_([0-9]+)_([a-z]+)_([0-9]+)")
    )
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    cmd = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
    category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
    buttons = [
        (
            Button.inline(
                "⬅️ Back ",
                data=f"back_command_{category}_{pgno}_{category_plugins}_{category_pgno}",
            ),
            Button.inline("⚙️ Main Menu", data="mainmenu"),
        )
    ]
    text = f"**Command :** `{tr}{cmd}`\
        \n**Plugin :** `{category}`\
        \n**Category :** `{category_plugins}`\
        \n\n**✘ Intro :**\n{CMD_INFO[cmd][0]}"
    await event.edit(text, buttons=buttons)
