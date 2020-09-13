""".admin Plugin for @UniBorg"""
import html

import userbot.plugins.sql_helper.warns_sql as sql

from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="warn (.*)"))
@borg.on(sudo_cmd(pattern="warn (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    warn_reason = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.from_id, event.chat_id, warn_reason
    )
    if num_warns >= limit:
        sql.reset_warns(reply_message.from_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            reply = "{} warnings, [user](tg://user?id={}) has to bee kicked!".format(
                limit, reply_message.from_id
            )
        else:
            logger.info("TODO: ban user")
            reply = "{} warnings, [user](tg://user?id={}) has to bee banned!".format(
                limit, reply_message.from_id
            )
    else:
        reply = "[user](tg://user?id={}) has {}/{} warnings... watch out!".format(
            reply_message.from_id, num_warns, limit
        )
        if warn_reason:
            reply += "\nReason for last warn:\n{}".format(html.escape(warn_reason))
    await edit_or_reply(event, reply)


@borg.on(admin_cmd(pattern="get_warns$"))
@borg.on(sudo_cmd(pattern="get_warns$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.from_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(
                num_warns, limit
            )
            text += "\r\n"
            text += reasons
            await event.edit(text)
        else:
            await edit_or_reply(
                event,
                "this user has {} / {} warning, but no reasons for any of them.".format(
                    num_warns, limit
                ),
            )
    else:
        await edit_or_reply(event, "this user hasn't got any warnings!")


@borg.on(admin_cmd(pattern="reset_warns$"))
@borg.on(sudo_cmd(pattern="reset_warns$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.from_id, event.chat_id)
    await edit_or_reply(event, "Warnings have been reset!")
