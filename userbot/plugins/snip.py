# ported from paperplaneExtended by avinashreddy3108 for media support

from telethon import events

from . import BOTLOG, BOTLOG_CHATID, cat_users
from .sql_helper.snip_sql import add_note, get_note, get_notes, rm_note


@bot.on(events.NewMessage(pattern=r"\#(\S+)", from_users=cat_users))
async def incom_note(getnt):
    try:
        if not (await getnt.get_sender()).bot:
            notename = getnt.text[1:]
            notename = notename.lower()
            note = get_note(notename)
            message_id_to_reply = getnt.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note:
                if note.f_mesg_id:
                    msg_o = await bot.get_messages(
                        entity=BOTLOG_CHATID, ids=int(note.f_mesg_id)
                    )
                    await getnt.delete()
                    await bot.send_message(
                        getnt.chat_id,
                        msg_o,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
                elif note.reply:
                    await getnt.delete()
                    await bot.send_message(
                        getnt.chat_id,
                        note.reply,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
    except AttributeError:
        pass


@bot.on(admin_cmd(pattern=r"snips (\w*)"))
@bot.on(sudo_cmd(pattern=r"snips (\w*)", allow_sudo=True))
async def add_snip(fltr):
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    keyword = keyword.lower()
    if msg and msg.media and not string:
        if BOTLOG:
            await bot.send_message(
                BOTLOG_CHATID,
                f"#NOTE\
                  \nKEYWORD: `#{keyword}`\
                  \n\nThe following message is saved as the snip in your bot , do NOT delete it !!",
            )
            msg_o = await bot.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=fltr.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                fltr,
                "Saving media as data for the note requires the `PRIVATE_GROUP_BOT_API_ID` to be set.",
            )
            return
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    success = "Note {} is successfully {}. Use` #{} `to get it"
    if add_note(keyword, string, msg_id) is False:
        rm_note(keyword)
        if add_note(keyword, string, msg_id) is False:
            return await edit_or_reply(
                fltr, f"Error in saving the given snip {keyword}"
            )
        return await edit_or_reply(fltr, success.format(keyword, "updated", keyword))
    return await edit_or_reply(fltr, success.format(keyword, "added", keyword))


@bot.on(admin_cmd(pattern="snipl$"))
@bot.on(sudo_cmd(pattern=r"snipl$", allow_sudo=True))
async def on_snip_list(event):
    message = "There are no saved notes in this chat"
    notes = get_notes()
    for note in notes:
        if message == "There are no saved notes in this chat":
            message = "Notes saved in this chat:\n"
        message += "👉 `#{}`\n".format(note.keyword)
    await edit_or_reply(event, message)


@bot.on(admin_cmd(pattern=r"snipd (\S+)"))
@bot.on(sudo_cmd(pattern=r"snipd (\S+)", allow_sudo=True))
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    name = name.lower()
    catsnip = get_note(name)
    if catsnip:
        rm_note(name)
    else:
        return await edit_or_reply(
            event, f"Are you sure that #{name} is saved as snip?"
        )
    await edit_or_reply(event, "snip #{} deleted successfully".format(name))


CMD_HELP.update(
    {
        "snip": "**Plugin :** `snip`\
\n\n•  **Syntax :** #<snipname>\
\n•  **Function :*** Gets the specified note.\
\n\n•  **Syntax :** `reply to a message with .snips <notename>`\
\n•  **Function :*** Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!)\
\n\n•  **Syntax :** `.snipl`\
\n•  **Function :*** Gets all saved notes in a chat.\
\n\n•  **Syntax :** `.snipd <notename>`\
\n•  **Function :*** Deletes the specified note.\
"
    }
)
