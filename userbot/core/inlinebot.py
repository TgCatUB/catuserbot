import json
import math
import os
import re
import time
from uuid import uuid4

from telethon import Button, types
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
from . import CMD_INFO, GRP_INFO, PLG_INFO, check_owner
from .logger import logging

LOGS = logging.getLogger(__name__)

CAT_IMG = Config.ALIVE_PIC or None
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
CATLOGO = "https://telegra.ph/file/493268c1f5ebedc967eba.jpg"
tr = Config.COMMAND_HAND_LER


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


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
        (
            Button.inline(
                f"{Config.EMOJI_TO_DISPLAY_IN_HELP} Check {Config.EMOJI_TO_DISPLAY_IN_HELP}",
                data="check",
            ),
        ),
        (
            Button.inline(
                f"👮‍♂️ Admin ({len(GRP_INFO['admin'])})",
                data=f"admin_menu",
            ),
            Button.inline(
                f"🤖 Bot ({len(GRP_INFO['bot'])})",
                data=f"bot_menu",
            ),
        ),
        (
            Button.inline(
                f"🎨 Fun ({len(GRP_INFO['fun'])})",
                data=f"fun_menu",
            ),
            Button.inline(
                f"🧩 Misc ({len(GRP_INFO['misc'])})",
                data=f"misc_menu",
            ),
        ),
        (
            Button.inline(
                f"🧰 Tools ({len(GRP_INFO['tools'])})",
                data=f"tools_menu",
            ),
            Button.inline(
                f"🗂 Utils ({len(GRP_INFO['utils'])})",
                data=f"utils_menu",
            ),
        ),
        (
            Button.inline(
                f"➕ Extra ({len(GRP_INFO['extra'])})",
                data=f"extra_menu",
            ),
            Button.inline(
                f"{Config.EMOJI_TO_DISPLAY_IN_HELP} Close Menu {Config.EMOJI_TO_DISPLAY_IN_HELP}",
                data=f"close",
            ),
        ),
    ]
    return text, buttons


def command_in_category(cname):
    cmds = 0
    for i in GRP_INFO[cname]:
        for _ in PLG_INFO[i]:
            cmds += 1
    return cmds


def paginate_help(
    page_number, loaded_plugins, prefix, plugins=True, category_plugins=None
):
    number_of_rows = Config.NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD
    number_of_cols = Config.NO_OF_COLOUMS_DISPLAYED_IN_H_ME_CMD
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    if plugins:
        modules = [
            Button.inline(
                f"{Config.EMOJI_TO_DISPLAY_IN_HELP} {x} {Config.EMOJI_TO_DISPLAY_IN_HELP}",
                data=f"{x}_prev(1)_command_{prefix}",
            )
            for x in helpable_plugins
        ]
    else:
        modules = [
            Button.inline(
                f"{Config.EMOJI_TO_DISPLAY_IN_HELP} {x} {Config.EMOJI_TO_DISPLAY_IN_HELP}",
                data=f"us_plugin_{x}",
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
                    Button.inline("Main Menu", data="mainmenu"),
                    Button.inline("⌦", data=f"{prefix}_next({modulo_page})_plugin"),
                )
            ]
        else:
            pairs = pairs + [(Button.inline("Main Menu", data="mainmenu"),)]
    else:
        if len(pairs) > number_of_rows:
            pairs = pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [
                (
                    Button.inline(
                        "⌫",
                        data=f"{prefix}_prev({modulo_page})_command_{category_plugins}",
                    ),
                    Button.inline(
                        "Back", data=f"back_{modulo_page}_{category_plugins}"
                    ),
                    Button.inline(
                        "⌦",
                        data=f"{prefix}_next({modulo_page})_command_{category_plugins}",
                    ),
                )
            ]
        else:
            pairs = pairs + [
                (Button.inline("Back", data=f"back_{modulo_page}_{category_plugins}"),)
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
        hmm = re.compile("secret (.*) (.*)")
        match = re.findall(hmm, query)
        if query.startswith("**Catuserbot"):
            buttons = [
                (
                    Button.inline("Stats", data="stats"),
                    Button.url("Repo", "https://github.com/sandy1709/catuserbot"),
                )
            ]
            if CAT_IMG and CAT_IMG.endswith((".jpg", ".png")):
                result = builder.photo(
                    CAT_IMG,
                    # title="Alive cat",
                    text=query,
                    buttons=buttons,
                )
            elif CAT_IMG:
                result = builder.document(
                    CAT_IMG,
                    title="Alive cat",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="Alive cat",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
        elif query.startswith("Inline buttons"):
            markdown_note = query[14:]
            prev = 0
            note_data = ""
            buttons = []
            for match in BTN_URL_REGEX.finditer(markdown_note):
                n_escapes = 0
                to_check = match.start(1) - 1
                while to_check > 0 and markdown_note[to_check] == "\\":
                    n_escapes += 1
                    to_check -= 1
                if n_escapes % 2 == 0:
                    buttons.append(
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
            message_text = note_data.strip()
            tl_ib_buttons = ibuild_keyboard(buttons)
            result = builder.article(
                title="Inline creator",
                text=message_text,
                buttons=tl_ib_buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
        elif match:
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
        elif query == "help":
            _result = main_menu()
            result = builder.article(
                title="© CatUserbot Help",
                description="Help menu for CatUserbot",
                text=_result[0],
                buttons=_result[1],
                link_preview=False,
            )
            await event.answer([result] if result else None)
        if str_y[0].lower() == "ytdl" and len(str_y) == 2:
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
            markup = event.client.build_reply_markup(buttons)
            photo = types.InputWebDocument(
                url=photo, size=0, mime_type="image/jpeg", attributes=[]
            )
            text, msg_entities = await event.client._parse_message_text(caption, "html")
            if found_:
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

            await event.answer([result] if result else None)
    else:
        buttons = [
            (
                Button.url("Source code", "https://github.com/sandy1709/catuserbot"),
                Button.url(
                    "Deploy",
                    "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FMr-confused%2Fcatpack&template=https%3A%2F%2Fgithub.com%2FMr-confused%2Fcatpack",
                ),
            )
        ]
        markup = event.client.build_reply_markup(buttons)
        photo = types.InputWebDocument(
            url=CATLOGO, size=0, mime_type="image/jpeg", attributes=[]
        )
        text, msg_entities = await event.client._parse_message_text(
            "𝗗𝗲𝗽𝗹𝗼𝘆 𝘆𝗼𝘂𝗿 𝗼𝘄𝗻 𝗖𝗮𝘁𝗨𝘀𝗲𝗿𝗯𝗼𝘁.", "md"
        )
        result = types.InputBotInlineResult(
            id=str(uuid4()),
            type="photo",
            title="𝘾𝙖𝙩𝙐𝙨𝙚𝙧𝙗𝙤𝙩",
            description="Deploy yourself",
            url="https://github.com/sandy1709/catuserbot",
            thumb=photo,
            content=photo,
            send_message=types.InputBotInlineMessageMediaAuto(
                reply_markup=markup, message=text, entities=msg_entities
            ),
        )
        await event.answer([result] if result else None)


@catub.tgbot.on(CallbackQuery(data=re.compile(b"close")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    await event.edit("menu closed")


@catub.tgbot.on(CallbackQuery(data=re.compile(b"check")))
@check_owner
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


@catub.tgbot.on(CallbackQuery(data=re.compile(b"back_(.*)_(.*)")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    pgno = int(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    buttons = paginate_help(pgno, GRP_INFO[category], category)
    text = f"**Category: **{category}\
        \n**Total plugins :** {len(GRP_INFO[category])}\
        \n**Total Commands:** {command_in_category(category)}"
    await event.edit(text, buttons=buttons)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"mainmenu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    _result = main_menu()
    await event.edit(_result[0], buttons=_result[1])


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"(.*)_prev\((.+?)\)_(.*)_?(.*)?")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = event.pattern_match.group(4)
    if category_plugins:
        category_plugins = str(category_plugins.decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number - 1, GRP_INFO[category], category)
    else:
        buttons = paginate_help(
            current_page_number - 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
        )
        text = f"**Plugin: **{category}\
                \n**Category: **{getkey(category)}\
                \n**Total Commands:** {len(PLG_INFO[category])}"
        try:
            return await event.edit(text, buttons=buttons)
        except Exception:
            pass
    await event.edit(buttons=buttons)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"(.*)_next\((.+?)\)_(.*)_?(.*)?")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = event.pattern_match.group(4)
    if category_plugins:
        category_plugins = str(category_plugins.decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number + 1, GRP_INFO[category], category)
    else:
        buttons = paginate_help(
            current_page_number + 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
        )
    await event.edit(buttons=buttons)
