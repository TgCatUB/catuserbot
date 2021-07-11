import html

from userbot import catub

from ..core.managers import edit_or_reply
from ..sql_helper import warns_sql as sql

plugin_category = "admin"


@catub.cat_cmd(
    pattern="warn(?:\s|$)([\s\S]*)",
    command=("warn", plugin_category),
    info={
        "header": "To warn a user.",
        "description": "will warn the replied user.",
        "usage": "{tr}warn <reason>",
    },
)
async def _(event):
    "To warn a user"
    warn_reason = event.pattern_match.group(1)
    if not warn_reason:
        warn_reason = "No reason"
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.sender_id, event.chat_id, warn_reason
    )
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            reply = "{} warnings, [user](tg://user?id={}) has to bee kicked!".format(
                limit, reply_message.sender_id
            )
        else:
            logger.info("TODO: ban user")
            reply = "{} warnings, [user](tg://user?id={}) has to bee banned!".format(
                limit, reply_message.sender_id
            )
    else:
        reply = "[user](tg://user?id={}) has {}/{} warnings... watch out!".format(
            reply_message.sender_id, num_warns, limit
        )
        if warn_reason:
            reply += "\nReason for last warn:\n{}".format(html.escape(warn_reason))
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="warns",
    command=("warns", plugin_category),
    info={
        "header": "To get users warns list.",
        "usage": "{tr}warns <reply>",
    },
)
async def _(event):
    "To get users warns list"
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_delete(event, "__Reply to user to get his warns.__")
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if not result or result[0] == 0:
        return await edit_or_reply(event, "this user hasn't got any warnings!")
    num_warns, reasons = result
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    if not reasons:
        return await edit_or_reply(
            event,
            "this user has {} / {} warning, but no reasons for any of them.".format(
                num_warns, limit
            ),
        )

    text = "This user has {}/{} warnings, for the following reasons:".format(
        num_warns, limit
    )
    text += "\r\n"
    text += reasons
    await event.edit(text)


@catub.cat_cmd(
    pattern="r(eset)?warns$",
    command=("resetwarns", plugin_category),
    info={
        "header": "To reset warns of the replied user",
        "usage": [
            "{tr}rwarns",
            "{tr}resetwarns",
        ],
    },
)
async def _(event):
    "To reset warns"
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await edit_or_reply(event, "__Warnings have been reset!__")
