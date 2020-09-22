import asyncio
import io

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

from .. import ALIVE_NAME, CMD_HELP
from ..utils import admin_cmd
from . import check
from .sql_helper import pmpermit_sql as pmpermit_sql

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
CACHE = {}
PMPERMIT_PIC = Config.PMPERMIT_PIC
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USER_BOT_WARN_ZERO = "`You were spamming my peru master's inbox, henceforth you are blocked by my master's userbot.` **Now GTFO, i'm playing minecraft** "

if Var.PRIVATE_GROUP_ID is not None:

    @borg.on(admin_cmd(pattern="approve ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        reason = event.pattern_match.group(1)
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            chat = await event.get_chat()
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                pmpermit_sql.approve(chat.id, reason)
                await event.edit(
                    "Approved to pm [{}](tg://user?id={})".format(firstname, chat.id)
                )
                await asyncio.sleep(3)
                await event.delete()
            else:
                await event.edit(
                    "[{}](tg://user?id={}) is already in approved list".format(
                        firstname, chat.id
                    )
                )
                await asyncio.sleep(3)
                await event.delete()
            return
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            replied_user = await event.client.get_entity(reply.from_id)
            chat = replied_user.id
            firstname = str(replied_user.first_name)
            if not pmpermit_sql.is_approved(chat):
                if chat in PM_WARNS:
                    del PM_WARNS[chat]
                if chat in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat].delete()
                    del PREV_REPLY_MESSAGE[chat]
                pmpermit_sql.approve(chat, reason)
                await event.edit(
                    "Approved to pm [{}](tg://user?id={})".format(firstname, chat)
                )
                await asyncio.sleep(3)
                await event.delete()
            else:
                await event.edit(
                    "[{}](tg://user?id={}) is already in approved list".format(
                        firstname, chat
                    )
                )
                await asyncio.sleep(3)
                await event.delete()

    @bot.on(events.NewMessage(outgoing=True))
    async def you_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.text.startswith((".bloack", ".disapprove")):
            return
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id not in PM_WARNS:
                    pmpermit_sql.approve(chat.id, "outgoing")

    @borg.on(admin_cmd(pattern="disapprove ?(.*)"))
    async def disapprove_p_m(event):
        if event.fwd_from:
            return
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            chat = await event.get_chat()
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "disapproved to pm [{}](tg://user?id={})".format(firstname, chat.id)
                )
            else:
                await event.edit(
                    "[{}](tg://user?id={}) is not yet approved".format(
                        firstname, chat.id
                    )
                )
            return
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            chat = await event.client.get_entity(reply.from_id)
            firstname = str(chat.first_name)
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "disapproved to pm [{}](tg://user?id={})".format(firstname, chat.id)
                )
            else:
                await event.edit(
                    "[{}](tg://user?id={}) is not yet approved".format(
                        firstname, chat.id
                    )
                )

    @borg.on(admin_cmd(pattern="block$"))
    async def block_p_m(event):
        if event.fwd_from:
            return
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            chat = await event.get_chat()
            await event.edit(
                " ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\nYou have been blocked. Now You Can't Message Me..[{}](tg://user?id={})".format(
                    firstname, chat.id
                )
            )
            await event.client(functions.contacts.BlockRequest(chat.id))
            return
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            chat = await event.client.get_entity(reply.from_id)
            firstname = str(chat.first_name)
            await event.edit(
                " ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\nYou have been blocked. Now You Can't Message Me..[{}](tg://user?id={})".format(
                    firstname, chat.id
                )
            )
            await event.client(functions.contacts.BlockRequest(chat.id))

    @borg.on(admin_cmd(pattern="unblock$"))
    async def unblock_pm(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            chat = await event.client.get_entity(reply.from_id)
            firstname = str(chat.first_name)
            await event.client(functions.contacts.UnblockRequest(chat.id))
            await event.edit(
                "You have been unblocked. Now You Can Message Me..[{}](tg://user?id={})".format(
                    firstname, chat.id
                )
            )

    @borg.on(admin_cmd(pattern="listapproved$"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += (
                        f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)

    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.from_id == bot.uid:
            return
        if Var.PRIVATE_GROUP_ID is None:
            return
        if not event.is_private:
            return
        message_text = event.message.message
        chat_id = event.from_id
        catid = chat_id
        message_text.lower()
        USER_BOT_NO_WARN = (
            f"[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id={catid})\n\n"
            "This is auto generated message from cat security service\n\n"
            f"Hi buddy my master {DEFAULTUSER} haven't approved you yet. so ,"
            "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years.\n\n"
            "**Send** `/start` ** so that my master can decide why you're here.**"
        )
        if USER_BOT_NO_WARN == message_text:
            # userbot's should not reply to other userbot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        if event.from_id in CACHE:
            sender = CACHE[event.from_id]
        else:
            sender = await bot.get_entity(event.from_id)
            CACHE[event.from_id] = sender
        if chat_id == bot.uid:
            # don't log Saved Messages
            return
        if sender.bot:
            # don't log bots
            return
        if sender.verified:
            # don't log verified accounts
            return
        if len(event.raw_text) == 1:
            if check(event.raw_text):
                return
        if not pmpermit_sql.is_approved(chat_id):
            # pm permit
            await do_pm_permit_action(chat_id, event)

    async def do_pm_permit_action(chat_id, event):
        if chat_id not in PM_WARNS:
            PM_WARNS.update({chat_id: 0})
        if PM_WARNS[chat_id] == Config.MAX_FLOOD_IN_P_M_s:
            r = await event.reply(USER_BOT_WARN_ZERO)
            await asyncio.sleep(1)
            await event.client(functions.contacts.BlockRequest(chat_id))
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r
            the_message = ""
            the_message += "#BLOCKED_PMs\n\n"
            the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
            the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
            # the_message += f"Media: {message_media}"
            try:
                await event.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True,
                )
                return
            except BaseException:
                return
        catid = chat_id
        if PMPERMIT_PIC:
            if Config.CUSTOM_PMPERMIT_TEXT:
                USER_BOT_NO_WARN = (
                    Config.CUSTOM_PMPERMIT_TEXT
                    + "\n\n"
                    + "**Send** `/start` ** so that my master can decide why you're here.**"
                )
            else:
                USER_BOT_NO_WARN = (
                    "This is auto generated message from cat security service\n\n"
                    f"Hi buddy my master {DEFAULTUSER} haven't approved you yet. so ,"
                    "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years.\n\n"
                    "**Send** `/start` ** so that my master can decide why you're here.**"
                )
            r = await event.reply(USER_BOT_NO_WARN, file=PMPERMIT_PIC)
        else:
            if Config.CUSTOM_PMPERMIT_TEXT:
                USER_BOT_NO_WARN = (
                    Config.CUSTOM_PMPERMIT_TEXT
                    + "\n\n"
                    + "**Send** `/start` ** so that my master can decide why you're here.**"
                )
            else:
                USER_BOT_NO_WARN = (
                    f"[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id={catid})\n\n"
                    "This is auto generated message from cat security service\n\n"
                    f"Hi buddy my master {DEFAULTUSER} haven't approved you yet. so ,"
                    "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years.\n\n"
                    "**Send** `/start` ** so that my master can decide why you're here.**"
                )
            r = await event.reply(USER_BOT_NO_WARN)
        PM_WARNS[chat_id] += 1
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r


CMD_HELP.update(
    {
        "pmpermit": ".approve\
\nUsage: Approves the mentioned/replied person to PM.\
.disapprove\
\nUsage: dispproves the mentioned/replied person to PM.\
\n\n.block\
\nUsage: Blocks the person.\
\n\n.unblock\
\nUsage: unBlocks the person.\
\n\n.listapproved\
\nUsage: To list the all approved users.\
"
    }
)
