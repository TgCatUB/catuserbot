# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# From UniBorg by @Spechide
""" Userbot module containing commands for keeping global notes. """

from userbot.utils import register, errors_handler
from userbot import CMD_HELP, BOTLOG_CHATID


@register(outgoing=True, pattern=r"\$\.*", ignore_unsafe=True)
@errors_handler
async def on_snip(event):
    """ Snips logic. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    if snip:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(snip.f_mesg_id))
        message_id_to_reply = event.message.reply_to_msg_id
        if not message_id_to_reply:
            message_id_to_reply = None
        await event.client.send_message(event.chat_id,
                                        msg_o.message,
                                        reply_to=message_id_to_reply,
                                        file=msg_o.media)
        await event.delete()


@register(outgoing=True, pattern="^.snip (.*)")
@errors_handler
async def on_snip_save(event):
    """ For .snip command, saves snips for future use. """
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if not msg:
        await event.edit("`I need something to save as a snip.`")
        return
    elif BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID, f"#SNIP\
        \nKEYWORD: {name}\
        \nThe following message is saved as the data for the snip, please do NOT delete it !!"
        )
        msg_o = await event.client.forward_messages(entity=BOTLOG_CHATID,
                                                    messages=msg,
                                                    from_peer=event.chat_id,
                                                    silent=True)
        success = "`Snip {} successfully. Use` **${}** `anywhere to get it`"
        if add_snip(name, msg_o.id) is False:
            await event.edit(success.format('updated', name))
        else:
            await event.edit(success.format('saved', name))
    else:
        await event.edit(
            "`This feature requires the BOTLOG_CHATID to be set up.`")
        return


@register(outgoing=True, pattern="^.snips$")
@errors_handler
async def on_snip_list(event):
    """ For .snips command, lists snips saved by you. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return

    message = "`No snips available right now.`"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "`No snips available right now.`":
            message = "Available snips:\n"
            message += f"`${a_snip.snip}`\n"
        else:
            message += f"`${a_snip.snip}`\n"

    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (.*)")
@errors_handler
async def on_snip_delete(event):
    """ For .remsnip command, deletes a snip. """
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"`Successfully deleted snip:` **{name}**")
    else:
        await event.edit(f"`Couldn't find snip:` **{name}**")


CMD_HELP.update({
    "snips":
    "\
$<snip_name>\
\nUsage: Gets the specified snip.\
\n\n.snip <name>\
\nUsage: Saves the replied message as a snip with the name. (Works with pics, docs, and stickers too!)\
\n\n.snips\
\nUsage: Gets all saved snips.\
\n\n.remsnip <snip_name>\
\nUsage: Deletes the specified snip.\
"
})
