""" Schedule message to anytime or in loop """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot import BOTLOG_CHATID, catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper import broadcast_sql as bcast
from ..sql_helper import schedule_sql as sql

logging.getLogger("apscheduler").setLevel(logging.WARNING)

plugin_category = "tools"


@catub.cat_cmd(
    pattern="(auto|)schedule(?:\s|$)([\s\S]*)",
    command=("schedule", plugin_category),
    info={
        "header": "Schedule message to a perticulater day and time.",
        "description": "It will save your replied message in botlogger & send to then user when time is matched. Don't delete the message of bot logger or tast wouldn't complete",
        "flags": {"b": "To use broadcast list. For more info check broadcast plugin."},
        "usage": [
            "{tr}schedule <user> > <time: YYYY-MM-DD HH:MM> <Reply to a Message>",
            "  ",
            "{tr}schedule <user1> <user2> <user3> > <time: YYYY-MM-DD HH:MM> <Reply to a Message>",
            "  ",
            "{tr}myschedule -b <broadcast list> > <time: YYYY-MM-DD HH:MM> <Reply to a Message>",
        ],
        "examples": [
            "{tr}schedule @cat > 2069-01-30 20:30",
            "{tr}schedule @cat 25465845 -1005554825 > 2069-01-30 20:30",
            "{tr}schedule -b catlist > 2069-01-30 20:30",
        ],
        "Note": "Set `TZ` in config with your timezone, default it is Asia/Kolkata.",
    },
)
async def schedule(event):
    "Schedule message to a perticulater datetime"
    cmd = event.pattern_match.group(1)
    commands = event.pattern_match.group(2).lower()
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "__Reply to a message to schedule...__")
    try:
        user, daytime = commands.split(">")
        user_list = []
        if "-b" in user:
            user = user.replace("-b", "").strip()
            if bcast.num_broadcastlist_chat(user) == 0:
                return await edit_delete(
                    event,
                    f"__There is no category with name **{user}**. Check `.listall` in broadcast plugin__",
                )
            user_list = list(bcast.get_chat_broadcastlist(user))
        else:
            for item in user.split():
                with contextlib.suppress(ValueError):
                    item = int(item)
                with contextlib.suppress(ValueError, IndexError):
                    user = await catub.get_entity(item)
                    user_list.append(user.id)
        if not user_list:
            return await edit_delete(
                event, "__Didn't found any users to schedule message...__"
            )
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
                    event, "__Its not a time machine to send message in the past__"
                )
        logged = await catub.send_message(BOTLOG_CHATID, reply)
        message = {"chat": logged.chat_id, "msg_id": logged.id}
        sql.add_message_to_database(user_list, message, scheduled_time, daytime)
        await edit_delete(event, "__Task added to database__")
    except Exception as err:
        await edit_delete(event, f"**Error:** `{err}`", 30)


@catub.cat_cmd(
    pattern="autoschedule$",
    command=("autoschedule", plugin_category),
    info={
        "header": "Schedule message in loop everyday.",
        "description": "It will save your replied message in botlogger & send to then user when time is matched. Don't delete the message of bot logger or tast wouldn't complete",
        "flags": {"b": "To use broadcast list. For more info check broadcast plugin."},
        "usage": [
            "{tr}autoschedule <user> > <time: Day of Week HH:MM> <Reply to a Message>",
            "  ",
            "{tr}autoschedule <user1> <user2> <user3> > <time: Day of Week HH:MM> <Reply to a Message>",
            "  ",
            "{tr}autoschedule -b <broadcast list> > <time: Day of Week HH:MM> <Reply to a Message>",
        ],
        "examples": [
            "{tr}autoschedule @cat > sunday 20:30",
            "{tr}autoschedule @cat 25465845 -1005554825 > sunday 20:30",
            "{tr}autoschedule -b catlist > sunday 20:30",
        ],
        "Note": "Set `TZ` in config with your timezone, default it is Asia/Kolkata.",
    },
)
async def autoschedule(event):
    "Autoschedule message in loop"


@catub.cat_cmd(
    pattern="myschedule(?:\s|$)([\s\S]*)",
    command=("myschedule", plugin_category),
    info={
        "header": "Get all active schedule tasks list.",
        "description": "View your existing task list or delete tasks. You can delete all tasks using `all`",
        "flags": {"d": "To delete the task"},
        "usage": [
            "{tr}myschedule",
            "{tr}myschedule -d < task id >",
        ],
        "examples": ["{tr}myschedule", "{tr}myschedule -d 5", "{tr}myschedule -d all"],
    },
)
async def schedulelist(event):
    "Manage schedule list"
    cmd = event.pattern_match.group(1)
    schedules = sql.get_all_messages()
    if not schedules:
        return await edit_delete(event, "__No scheduled task found.__")
    if cmd and "-d" in cmd:
        task = cmd.replace("-d", "").strip()
        if not task:
            return await edit_delete(
                event, "__Reply with a task id, or `all` if want to delete all tasks.__"
            )
        elif task == "all":
            sql.delete_all_messages()
            await edit_delete(event, "__All tasks deleted successfully.__")
        else:
            res = sql.delete_message_by_id(int(task))
            await edit_delete(event, res)
    else:
        string = ""
        for item in schedules:
            string += f'<b>Task ID:</b>  <code>{item.id}</code>\n<b>Message:  <a href="https://t.me/c/{str(item.message["chat"])[4:]}/{item.message["msg_id"]}">Scheduled Message</a></b>\n<b>Time:</b>  <code>{item.scheduled_time} seconds</code>\n'
            if item.day_of_week:
                string += f"<b>Repeat:</b>  <i>Every {item.day_of_week}</i>"
            string += "\n\n"
        await edit_or_reply(event, string, parse_mode="html")


scheduler = AsyncIOScheduler()
scheduler.add_job(sql.send_scheduled_messages, "interval", seconds=60)
scheduler.start()
