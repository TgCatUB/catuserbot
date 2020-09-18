"""AFK Plugin for @UniBorg
Syntax: .afk REASON"""
import asyncio
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from ..utils import admin_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP

global USERAFK_ON
global afk_time
global last_afk_message
global afk_start
global afk_end
USERAFK_ON = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@borg.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if "afk" not in current_message and "on" in USERAFK_ON:
        shite = await borg.send_message(
            event.chat_id,
            "__Back alive!__\n**No Longer afk.**\n `Was afk for:``"
            + total_afk_time
            + "`",
        )
        if BOTLOG:
            await borg.send_message(
                BOTLOG_CHATID,
                "#AFKFALSE \nSet AFK mode to False\n"
                + "__Back alive!__\n**No Longer afk.**\n `Was afk for:``"
                + total_afk_time
                + "`",
            )
        await asyncio.sleep(5)
        await shite.delete()
        USERAFK_ON = {}
        afk_time = None


@borg.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USERAFK_ON and not (await event.get_sender()).bot:
        msg = None
        message_to_reply = (
            f"__My Master Has Been In afk For__ `{total_afk_time}`\nWhere He Is: ONLY GOD KNOWS "
            + f"\n\n__I promise He'll back in a few light years__\n**REASON**: {reason}"
            if reason
            else f"**Heya!**\n__I am currently unavailable. Since when, you ask? For {total_afk_time} I guess.__\n\nWhen will I be back? Soon __Whenever I feel like it__**( ಠ ʖ̯ ಠ)**  "
        )
        if not (event.chat_id in Config.UB_BLACK_LIST_CHAT):
            msg = await event.reply(message_to_reply)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg
        await asyncio.sleep(5)
        hmm = await event.get_chat()
        if Config.PM_LOGGR_BOT_API_ID:
            if not event.is_private:
                await bot.send_message(
                    Config.PM_LOGGR_BOT_API_ID,
                    f"#AFK_TAGS \nhttps://t.me/c/{hmm.id}/{event.message.id}",
                )


@borg.on(admin_cmd(pattern=r"afk ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    USERAFK_ON = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    if not USERAFK_ON:
        last_seen_status = await borg(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.now()
        USERAFK_ON = f"on: {reason}"
        if reason:
            await borg.send_message(
                event.chat_id, f"**I shall be Going afk!** __because ~ {reason}__"
            )
        else:
            await borg.send_message(event.chat_id, f"**I am Going afk!**")
        await asyncio.sleep(5)
        await event.delete()
        if BOTLOG:
            await borg.send_message(
                BOTLOG_CHATID,
                f"#AFKTRUE \nSet AFK mode to True, and Reason is {reason}",
            )


CMD_HELP.update(
    {
        "afk": ".afk [Optional Reason]\
\n**Usage : **Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
\nafk means away from keyboard/keypad.\
"
    }
)
