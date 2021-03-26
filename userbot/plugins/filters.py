# ported from paperplaneExtended by avinashreddy3108 for media support
import re

from . import BOTLOG, BOTLOG_CHATID
from .sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)


@bot.on(admin_cmd(incoming=True))
async def filter_incoming_handler(handler):
    try:
        if (
            not (await handler.get_sender()).bot
            and (handler.sender_id) != handler.client.uid
        ):
            name = handler.raw_text
            filters = get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    if trigger.f_mesg_id:
                        msg_o = await handler.client.get_messages(
                            entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                        )
                        await handler.reply(msg_o.message, file=msg_o.media)
                    elif trigger.reply:
                        await handler.reply(trigger.reply)
    except AttributeError:
        pass


@bot.on(admin_cmd(pattern="filter (.*)"))
@bot.on(sudo_cmd(pattern="filter (.*)", allow_sudo=True))
async def add_new_filter(new_handler):
    if new_handler.fwd_from:
        return
    keyword = new_handler.pattern_match.group(1)
    string = new_handler.text.partition(keyword)[2]
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await new_handler.client.send_message(
                BOTLOG_CHATID,
                f"#FILTER\
            \nCHAT ID: {new_handler.chat_id}\
            \nTRIGGER: {keyword}\
            \n\nThe following message is saved as the filter's reply data for the chat, please do NOT delete it !!",
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                new_handler,
                "`Saving media as reply to the filter requires the PRIVATE_GROUP_BOT_API_ID to be set.`",
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "`Filter` **{}** `{} successfully`"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "added"))
    remove_filter(str(new_handler.chat_id), keyword)
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "Updated"))
    await edit_or_reply(new_handler, f"Error while setting filter for {keyword}")


@bot.on(admin_cmd(pattern="filters$"))
@bot.on(sudo_cmd(pattern="filters$", allow_sudo=True))
async def on_snip_list(event):
    if event.fwd_from:
        return
    OUT_STR = "There are no filters in this chat."
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "There are no filters in this chat.":
            OUT_STR = "Active filters in this chat:\n"
        OUT_STR += "👉 `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="Available Filters in the Current Chat",
        file_name="filters.text",
    )


@bot.on(admin_cmd(pattern="stop (.*)"))
@bot.on(sudo_cmd(pattern="stop (.*)", allow_sudo=True))
async def remove_a_filter(r_handler):
    if r_handler.fwd_from:
        return
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("Filter` {} `doesn't exist.".format(filt))
    else:
        await r_handler.edit("Filter `{} `was deleted successfully".format(filt))


@bot.on(admin_cmd(pattern="rmfilters$"))
@bot.on(sudo_cmd(pattern="rmfilters$", allow_sudo=True))
async def on_all_snip_delete(event):
    if event.fwd_from:
        return
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, f"filters in current chat deleted successfully")
    else:
        await edit_or_reply(event, f"There are no filters in this group")


CMD_HELP.update(
    {
        "filters": "**Plugin :**`filters`\
    \n\n•  **Syntax :** `.filters`\
    \n•  **Function : **Lists all active (of your userbot) filters in a chat.\
    \n\n•  **Syntax :** `.filter`  reply to a message with .filter <keyword>\
    \n•  **Function : **Saves the replied message as a reply to the 'keyword'.\
    \nThe bot will reply to the message whenever 'keyword' is mentioned. Works with everything from files to stickers.\
    \n\n•  **Syntax :** `.stop <keyword>`\
    \n•  **Function : **Stops the specified keyword.\
    \n\n•  **Syntax :** `.rmfilters` \
    \n•  **Function : **Removes all filters of your userbot in the chat."
    }
)
