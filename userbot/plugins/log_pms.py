"""Log PMs
Check https://t.me/tgbeta/3505"""
import asyncio
import logging
import os
import sys

from telethon import events
from telethon.tl import functions, types
from telethon.tl.types import Channel, Chat, User

from userbot.uniborgConfig import Config
from userbot.utils import admin_cmd

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARN)

global NO_PM_LOG_USERS
NO_PM_LOG_USERS = []


@borg.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if Config.NO_LOG_P_M_S and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != borg.uid:
            try:
                e = await borg.get_entity(int(Config.PM_LOGGR_BOT_API_ID))
                fwd_message = await borg.forward_messages(
                    e,
                    event.message,
                    silent=True
                )
            except Exception as e:
                # logger.warn(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e) 

@borg.on(admin_cmd(pattern=f"nolog", allow_sudo=True))
@borg.on(events.NewMessage(pattern="nolog ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if Config.NO_LOG_P_M_S:
        if event.is_private:
            if chat.id not in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.append(chat.id)
                await event.edit("Won't Log Messages from this chat")
                await asyncio.sleep(3)
                await event.delete()
