import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from userbot import BOTLOG_CHATID, catub

from ..core.managers import edit_delete
from ..sql_helper import schedule_sql as sql

logging.getLogger("apscheduler").setLevel(logging.WARNING)

plugin_category = "tools"


@catub.cat_cmd(
    pattern="sc(?: |$)(.*)",
    command=("sc", plugin_category),
)
async def schedule(event):
    "Schedule message"
    commands = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    try:
        user, scheduled_time = commands.split(">")
        scheduled_time = datetime.strptime(scheduled_time.strip(), "%Y-%m-%d %H:%M")
        current_time = datetime.now().replace(second=0, microsecond=0)
        if scheduled_time < current_time:
            return await edit_delete(
                event, "**ಠ∀ಠ Its not a time machine to send message in the past**"
            )
        if not reply:
            return await edit_delete(event, "**ಠ∀ಠ Reply to a message**")
        logged = await catub.send_message(BOTLOG_CHATID, reply)
        message = {"chat": logged.chat_id, "msg_id": logged.id}
        sql.add_message_to_database(user.split(), message, scheduled_time)
        await edit_delete(event, "**ಠ∀ಠ Added to database**")
    except Exception as err:
        await edit_delete(event, f"**Error:** {err}", 30)


@catub.cat_cmd(
    pattern="asc(?: |$)(.*)",
    command=("asc", plugin_category),
)
async def autoschedule(event):
    "Auto Schedule message"
    commands = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    try:
        user, daytime = commands.split(">")
        scheduled_time, error = sql.get_scdule_from_day(daytime)
        if not scheduled_time:
            return await edit_delete(event, error, 30)
        if not reply:
            return await edit_delete(event, "**ಠ∀ಠ Reply to a message**")
        logged = await catub.send_message(BOTLOG_CHATID, reply)
        message = {"chat": logged.chat_id, "msg_id": logged.id}
        sql.add_message_to_database(user.split(), message, scheduled_time, daytime)
        await edit_delete(event, "**ಠ∀ಠ Added to database**")
    except Exception as err:
        await edit_delete(event, f"**Error:** {err}", 30)


scheduler = AsyncIOScheduler()
scheduler.add_job(sql.send_scheduled_messages, "interval", seconds=60)
scheduler.start()
