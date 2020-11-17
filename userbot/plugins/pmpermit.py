import asyncio
import io

from telethon import events, functions

from ..utils import admin_cmd
from . import ALIVE_NAME, CMD_HELP, PM_START, PMMENU, check, get_user_from_event
from .sql_helper import pmpermit_sql as pmpermit_sql

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
CACHE = {}
PMPERMIT_PIC = Config.PMPERMIT_PIC
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USER_BOT_WARN_ZERO = "You were spamming my peru master's inbox, henceforth you are blocked by my master's userbot. **Now GTFO, i'm playing minecraft** "

if Config.PRIVATE_GROUP_ID is not None:

    @bot.on(admin_cmd(outgoing=True))
    async def you_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.text.startswith((".block", ".disapprove")):
            return
        if (
            event.is_private
            and not pmpermit_sql.is_approved(chat.id)
            and chat.id not in PM_WARNS
        ):
            pmpermit_sql.approve(chat.id, "outgoing")

    @bot.on(admin_cmd(pattern="(a|approve) ?(.*)"))
    async def approve_p_m(event):
        if event.is_private:
            user = await event.get_chat()
            reason = event.pattern_match.group(1)
        else:
            user, reason = await get_user_from_event(event)
            if not user:
                return await edit_delete(event, "`Couldn't Fectch user`", 5)
            if not reason:
                reason = "Not mentioned"
        if not pmpermit_sql.is_approved(user.id):
            if user.id in PM_WARNS:
                del PM_WARNS[user.id]
            if user.id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[user.id].delete()
                del PREV_REPLY_MESSAGE[user.id]
            if user.id in PM_START:
                PM_START.remove(user.id)
            pmpermit_sql.approve(user.id, reason)
            await edit_delete(
                event, f"Approved to pm [{user.first_name}](tg://user?id={user.id})", 5
            )
        else:
            await edit_delete(
                event,
                f"[{user.first_name}](tg://user?id={user.id}) is already in approved list",
                5,
            )

    @bot.on(admin_cmd(pattern="(da|disapprove)$"))
    async def disapprove_p_m(event):
        if event.is_private:
            user = await event.get_chat()
        else:
            user, reason = await get_user_from_event(event)
            if not user:
                return await edit_delete(event, "`Couldn't Fectch user`", 5)
        if user.id in PM_START:
            PM_START.remove(user.id)
        if pmpermit_sql.is_approved(user.id):
            pmpermit_sql.disapprove(user.id)
            await edit_delete(
                event,
                f"disapproved to pm [{user.first_name}](tg://user?id={user.id})",
                5,
            )
        else:
            await edit_delete(
                event,
                f"[{user.first_name}](tg://user?id={user.id}) is not yet approved",
                5,
            )

    @bot.on(admin_cmd(pattern="block$"))
    async def block_p_m(event):
        if event.is_private:
            user = await event.get_chat()
        else:
            user, reason = await get_user_from_event(event)
            if not user:
                return await edit_delete(event, "`Couldn't Fectch user`", 5)
        if user.id in PM_START:
            PM_START.remove(user.id)
        await event.edit(
            f"`You are blocked Now .You Can't Message Me from now..`[{user.first_name}](tg://user?id={user.id})"
        )
        await event.client(functions.contacts.BlockRequest(user.id))

    @bot.on(admin_cmd(pattern="unblock$"))
    async def unblock_pm(event):
        if event.is_private:
            user = await event.get_chat()
        else:
            user, reason = await get_user_from_event(event)
            if not user:
                return await edit_delete(event, "`Couldn't Fectch user`", 5)
        await event.client(functions.contacts.UnblockRequest(user.id))
        await asyncio.sleep(2)
        await event.edit(
            f"`You are Unblocked Now .You Can Message Me From now..`[{user.first_name}](tg://user?id={user.id})"
        )

    @bot.on(admin_cmd(pattern="listapproved$"))
    async def approve_p_m(event):
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
                out_file.name = "approvedpms.text"
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

    if PMMENU:

        @bot.on(events.NewMessage(incoming=True))
        async def on_new_private_message(event):
            if event.sender_id == event.client.uid:
                return
            if Config.PRIVATE_GROUP_ID is None:
                return
            if not event.is_private:
                return
            message_text = event.message.message
            chat_id = event.sender_id
            USER_BOT_NO_WARN = (
                f"My master {DEFAULTUSER} haven't approved you yet. Don't spam his inbox "
                "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years.\n\n"
                "**Send** `/start` ** so that my master can decide why you're here.**"
            )
            if USER_BOT_NO_WARN == message_text:
                # userbot's should not reply to other userbot's
                # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
                return
            if chat_id in CACHE:
                sender = CACHE[chat_id]
            else:
                sender = await event.client.get_entity(chat_id)
                CACHE[chat_id] = sender
            if chat_id == bot.uid:  # don't log Saved Messages
                return
            if sender.bot:  # don't log bots
                return
            if sender.verified:  # don't log verified accounts
                return
            if event.raw_text == "/start":
                if chat_id not in PM_START:
                    PM_START.append(chat_id)
                return
            if len(event.raw_text) == 1 and check(event.raw_text):
                return
            if chat_id in PM_START:
                return
            if not pmpermit_sql.is_approved(chat_id):
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
                if chat_id in PM_START:
                    PM_START.remove(chat_id)
                PREV_REPLY_MESSAGE[chat_id] = r
                the_message = ""
                the_message += "#BLOCKED_PMs\n\n"
                the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
                the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
                try:
                    await event.client.send_message(
                        entity=Config.PRIVATE_GROUP_ID,
                        message=the_message,
                    )
                    return
                except BaseException:
                    return
            if Config.CUSTOM_PMPERMIT_TEXT:
                USER_BOT_NO_WARN = (
                    Config.CUSTOM_PMPERMIT_TEXT
                    + "\n\n"
                    + "**Send** `/start` ** so that my master can decide why you're here.**"
                )
            else:
                USER_BOT_NO_WARN = (
                    f"My master {DEFAULTUSER} haven't approved you yet. Don't spam his inbox "
                    "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years.\n\n"
                    "**Send** `/start` ** so that my master can decide why you're here.**"
                )
            if PMPERMIT_PIC:
                r = await event.reply(USER_BOT_NO_WARN, file=PMPERMIT_PIC)
            else:
                r = await event.reply(USER_BOT_NO_WARN)
            PM_WARNS[chat_id] += 1
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r

    else:

        @bot.on(events.NewMessage(incoming=True))
        async def on_new_private_message(event):
            if event.sender_id == event.client.uid:
                return
            if Config.PRIVATE_GROUP_ID is None:
                return
            if not event.is_private:
                return
            message_text = event.message.message
            chat_id = event.sender_id
            USER_BOT_NO_WARN = (
                f"My master {DEFAULTUSER} haven't approved you yet. Don't spam his inbox "
                "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years.\n\n"
                "**Send** `/start` ** so that my master can decide why you're here.**"
            )
            if USER_BOT_NO_WARN == message_text:
                # userbot's should not reply to other userbot's
                # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
                return
            if chat_id in CACHE:
                sender = CACHE[chat_id]
            else:
                sender = await event.client.get_entity(chat_id)
                CACHE[chat_id] = sender
            if chat_id == bot.uid:  # don't log Saved Messages
                return
            if sender.bot:  # don't log bots
                return
            if sender.verified:  # don't log verified accounts
                return
            if not pmpermit_sql.is_approved(chat_id):
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
                if chat_id in PM_START:
                    PM_START.remove(chat_id)
                PREV_REPLY_MESSAGE[chat_id] = r
                the_message = ""
                the_message += "#BLOCKED_PMs\n\n"
                the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
                the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
                try:
                    await event.client.send_message(
                        entity=Config.PRIVATE_GROUP_ID,
                        message=the_message,
                    )
                    return
                except BaseException:
                    return
            if Config.CUSTOM_PMPERMIT_TEXT:
                USER_BOT_NO_WARN = Config.CUSTOM_PMPERMIT_TEXT
            else:
                USER_BOT_NO_WARN = (
                    f"My master {DEFAULTUSER} haven't approved you yet. Don't spam his inbox "
                    "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years."
                )
            if PMPERMIT_PIC:
                r = await event.reply(USER_BOT_NO_WARN, file=PMPERMIT_PIC)
            else:
                r = await event.reply(USER_BOT_NO_WARN)
            PM_WARNS[chat_id] += 1
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r


CMD_HELP.update(
    {
        "pmpermit": "**Plugin : **`pmpermit`\
        \n\n  •  **Syntax : **`.approve or .a`\
        \n  •  **Function : **__Approves the mentioned/replied person to PM.__\
        \n\n  •  **Syntax : **`.disapprove or .da`\
        \n  •  **Function : **__dispproves the mentioned/replied person to PM.__\
        \n\n  •  **Syntax : **`.block`\
        \n  •  **Function : **__Blocks the person.__\
        \n\n  •  **Syntax : **`.unblock`\
        \n  •  **Function : **__Unblocks the person.__\
        \n\n  •  **Syntax : **`.listapproved`\
        \n  •  **Function : **__To list the all approved users.__\
"
    }
)
