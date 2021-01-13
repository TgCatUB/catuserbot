# pm and tagged messages logger for catuserbot by @mrconfused (@sandy1709)
import asyncio

from telethon import events

import userbot.plugins.sql_helper.no_log_pms_sql as no_log_pms_sql

from . import BOTLOG, BOTLOG_CHATID, LOGS

RECENT_USER = None
NEWPM = None
COUNT = 0


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    global RECENT_USER
    global NEWPM
    global COUNT
    if not Config.PM_LOGGR_BOT_API_ID:
        return
    sender = await event.get_sender()
    if Config.NO_LOG_P_M_S and not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if RECENT_USER != chat.id:
                RECENT_USER = chat.id
                if NEWPM:
                    if COUNT > 1:
                        await NEWPM.edit(
                            NEWPM.text.replace("new message", f"{COUNT} messages")
                        )
                    else:
                        await NEWPM.edit(
                            NEWPM.text.replace("new message", f"{COUNT} message")
                        )
                    COUNT = 0
                NEWPM = await event.client.send_message(
                    Config.PM_LOGGR_BOT_API_ID,
                    f"👤{_format.mentionuser(sender.first_name , sender.id)} has sent a new message \nId : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGR_BOT_API_ID, event.message, silent=True
                    )
                COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.mentioned))
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    if no_log_pms_sql.is_approved(hmm.id):
        return
    if not Config.PM_LOGGR_BOT_API_ID:
        return
    from .afk import USERAFK_ON

    if "on" in USERAFK_ON:
        return
    try:
        if (await event.get_sender()).bot:
            return
    except:
        pass
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except:
        pass
    messaget = media_type(event)
    resalt = f"#TAGS \n<b>Group : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += (
            f"\n<b>From : </b> 👤{_format.htmlmentionuser(full.first_name , full.id)}"
        )
    if messaget is not None:
        resalt += f"\n<b>Message type : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b>Message : </b>{event.message.message}"
    resalt += f"\n<b>Message link: </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>"
    await asyncio.sleep(3)
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGR_BOT_API_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@bot.on(admin_cmd(outgoing=True, pattern=r"save(?: |$)(.*)"))
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


@bot.on(admin_cmd(pattern="log$"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGR_BOT_API_ID is not None:
        chat = await event.get_chat()
        if no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.disapprove(chat.id)
            await edit_delete(
                event, "`logging of messages from this group has been started`", 5
            )


@bot.on(admin_cmd(pattern="nolog$"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGR_BOT_API_ID is not None:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.approve(chat.id)
            await edit_delete(
                event, "`Logging of messages from this chat has been stopped`", 5
            )


CMD_HELP.update(
    {
        "logchats": "**Plugin : **`logchats`\
        \n\n  •  **Syntax : **`.save` :\
        \n  •  **Function : **__Saves tagged message in private group .__\
        \n\n  •  **Syntax : **`.log`:\
        \n  •  **Function : **__By default will log all private chat messages if you use .nolog and want to log again then you need to use this__\
        \n\n  •  **Syntax : **`.nolog`:\
        \n  •  **Function : **__Stops logging from a private chat or group where you used__"
    }
)
