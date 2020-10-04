# pm and tagged messages logger for catuserbot by @mrconfused (@sandy1709)
import asyncio
import logging

from telethon import events

from ..utils import admin_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOGS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)

NO_PM_LOG_USERS = []


@borg.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if Config.NO_LOG_P_M_S and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != borg.uid:
            try:
                if Config.PM_LOGGR_BOT_API_ID and event.message:
                    e = await borg.get_entity(int(Config.PM_LOGGR_BOT_API_ID))
                    fwd_message = await borg.forward_messages(
                        e, event.message, silent=True
                    )
            except Exception as e:
                LOGS.warn(str(e))


@borg.on(events.NewMessage(incoming=True, func=lambda e: e.mentioned))
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    if hmm.id in NO_PM_LOG_USERS:
        return
    from .afk import USERAFK_ON

    if "on" in USERAFK_ON:
        return
    if not (await event.get_sender()).bot and Config.PM_LOGGR_BOT_API_ID:
        await asyncio.sleep(5)
        if not event.is_private:
            await event.client.send_message(
                Config.PM_LOGGR_BOT_API_ID,
                f"#TAGS \n<b>Group : </b><code>{hmm.title}</code>\
                        \n<b>Message : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>",
                parse_mode="html",
                link_preview=False,
            )


@borg.on(admin_cmd(outgoing=True, pattern=r"save(?: |$)([\s\S]*)"))
async def log(log_text):
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`What am I supposed to log?`")
            return
        await log_text.edit("`Logged Successfully`")
    else:
        await log_text.edit("`This feature requires Logging to be enabled!`")
    await asyncio.sleep(2)
    await log_text.delete()


@borg.on(admin_cmd(pattern="log$"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGR_BOT_API_ID is not None:
        chat = await event.get_chat()
        if chat.id in NO_PM_LOG_USERS:
            NO_PM_LOG_USERS.remove(chat.id)
            await event.edit("Will Log Messages from this chat")


@borg.on(admin_cmd(pattern="nolog$"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGR_BOT_API_ID is not None:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS:
            NO_PM_LOG_USERS.append(chat.id)
            await event.edit("Won't Log Messages from this chat")


CMD_HELP.update(
    {
        "log_chats": "**Plugin : **`log_chats`\
        \n\n**Syntax : **`.save` :\
        \n**Usage : ** saves taged message in private group .\
        \n\n**Syntax : **`.log`:\
        \n**Usage : **By default will log all private chat messages if you use .nolog and want to log again then you need to use this\
        \n\n**Syntax : **`.nolog`:\
        \n**Usage : **to stops logging from a private chat \
        \n\n**Note : **these resets after restart soon will try to add database so wont reset after restart"
    }
)
