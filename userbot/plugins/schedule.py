""" Schedule message to anytime or in loop """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot import BOTLOG_CHATID, catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper import schedule_sql as sql

logging.getLogger("apscheduler").setLevel(logging.WARNING)

plugin_category = "tools"


@catub.cat_cmd(
    pattern="(auto|)schedule(?:\s|$)([\s\S]*)",
    command=("schedule", plugin_category),
)
async def autoschedule(event):
    "Schedule message"
    cmd = event.pattern_match.group(1)
    commands = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    try:
        user, daytime = commands.split(">")
        if cmd == "auto":
            scheduled_time, error = sql.get_scdule_from_day(daytime)
            if not scheduled_time:
                return await edit_delete(event, error, 30)
        elif cmd == "":
            scheduled_time = datetime.strptime(daytime.strip(), "%Y-%m-%d %H:%M")
            current_time = datetime.now().replace(second=0, microsecond=0)
            daytime = None
            if scheduled_time < current_time:
                return await edit_delete(
                    event, "**ಠ∀ಠ Its not a time machine to send message in the past**"
                )
        if not reply:
            return await edit_delete(event, "**ಠ∀ಠ Reply to a message**")

        logged = await catub.send_message(BOTLOG_CHATID, reply)
        message = {"chat": logged.chat_id, "msg_id": logged.id}
        sql.add_message_to_database(user.split(), message, scheduled_time, daytime)
        await edit_delete(event, "**ಠ∀ಠ Added to database**")
    except Exception as err:
        await edit_delete(event, f"**Error:** {err}", 30)


@catub.cat_cmd(
    pattern="myschedule(?:\s|$)([\s\S]*)",
    command=("myschedule", plugin_category),
)
async def schedulelist(event):
    "Schedule list"
    cmd = event.pattern_match.group(1)
    schedules = sql.get_all_messages()
    if not schedules:
        return await edit_delete(event, "**No scheduled task found.**")
    if cmd and "-d" in cmd:
        task = cmd.replace("-d", "").strip()
        if not task:
            return await edit_delete(
                event, "**Reply with a task id, or `all` if want to delete all tasks.**"
            )
        elif task == "all":
            sql.delete_all_messages()
            await edit_delete(event, "**All tasks deleted successfully.**")
        else:
            res = sql.delete_message_by_id(int(task))
            await edit_delete(event, res)
    else:
        string = ""
        for item in schedules:
            string += f'<b>Task ID:</b>  <code>{item.id}</code>\n<b>Message:  <a href="https://t.me/c/{str(item.message["chat"])[4:]}/{item.message["msg_id"]}">Scheduled Message</a></b>\n<b>Time:</b>  <code>{item.scheduled_time} seconds</code>'
            if item.day_of_week:
                string += f" (<code>{item.day_of_week}</code>)"
            string += "\n\n"
        await edit_or_reply(event, string, parse_mode="html")


scheduler = AsyncIOScheduler()
scheduler.add_job(sql.send_scheduled_messages, "interval", seconds=60)
scheduler.start()
