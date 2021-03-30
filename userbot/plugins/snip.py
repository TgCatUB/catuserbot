# ported from paperplaneExtended by avinashreddy3108 for media support

from telethon import events

from . import BOTLOG, BOTLOG_CHATID, cat_users, get_message_link
from .sql_helper.snip_sql import add_note, get_note, get_notes, rm_note


@bot.on(events.NewMessage(pattern=r"\#(\S+)", from_users=cat_users))
async def incom_note(event):
    if not BOTLOG:
        return
    try:
        if not (await event.get_sender()).bot:
            notename = event.text[1:]
            notename = notename.lower()
            note = get_note(notename)
            message_id_to_reply = await reply_id(event)
            if note:
                if note.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(note.f_mesg_id)
                    )
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        msg_o,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
                elif note.reply:
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        note.reply,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
    except AttributeError:
        pass


@bot.on(admin_cmd(pattern=r"snips (\w*)"))
@bot.on(sudo_cmd(pattern=r"snips (\w*)", allow_sudo=True))
async def add_snip(event):
    if event.fwd_from:
        return
    if not BOTLOG:
        return await edit_delete(
            event, "`To save snip or notes you need to set PRIVATE_GROUP_BOT_API_ID`"
        )
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    keyword = keyword.lower()
    if msg and not string:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#NOTE\
            \n**Keyword :** `#{keyword}`\
            \n\nThe following message is saved as the snip in your bot , do NOT delete it !!",
        )
        msg_o = await event.client.forward_messages(
            entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
        )
        msg_id = msg_o.id
    elif msg:
        return await edit_delete(
            event,
            "`What should i save for your snip either do reply or give snip text along with keyword`",
        )
    if not msg:
        if string:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#NOTE\
            \n**Keyword :** `#{keyword}`\
            \n\nThe following message is saved as the snip in your bot , do NOT delete it !!",
            )
            msg_o = await event.client.send_message(BOTLOG_CHATID, string)
            msg_id = msg_o.id
            string = None
        else:
            return await edit_delete(event, "`what should i save for your snip`")
    success = "Note {} is successfully {}. Use` #{} `to get it"
    if add_note(keyword, string, msg_id) is False:
        rm_note(keyword)
        if add_note(keyword, string, msg_id) is False:
            return await edit_or_reply(
                event, f"Error in saving the given snip {keyword}"
            )
        return await edit_or_reply(event, success.format(keyword, "updated", keyword))
    return await edit_or_reply(event, success.format(keyword, "added", keyword))


@bot.on(admin_cmd(pattern="snipl$"))
@bot.on(sudo_cmd(pattern=r"snipl$", allow_sudo=True))
async def on_snip_list(event):
    message = "You havent saved any notes/snip"
    notes = get_notes()
    if not BOTLOG:
        return await edit_delete(
            event, "`For saving snip you must set PRIVATE_GROUP_BOT_API_ID`"
        )
    for note in notes:
        if message == "You havent saved any notes/snip":
            message = "Notes saved in your bot are\n\n"
        message += f"👉 `#{note.keyword}`"
        if note.f_mesg_id:
            msglink = await get_message_link(Config.PRIVATE_GROUP_ID, note.f_mesg_id)
            message += f"  [preview]({msglink})\n"
        else:
            message += "  No preview\n"
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
    await edit_or_reply(event, f"`snip #{name} deleted successfully`")


CMD_HELP.update(
    {
        "snip": "**Plugin :** `snip`\
\n\n•  **Syntax :** `#<snipname>`\
\n•  **Function :*** __Gets the specified note.__\
\n\n•  **Syntax :** `reply to note with .snips <notename>`\
\n•  **Function :*** __Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!)__\
\n\n•  **Syntax :** `.snipl`\
\n•  **Function :*** __Gets all saved notes in a chat.__\
\n\n•  **Syntax :** `.snipd <notename>`\
\n•  **Function :*** __Deletes the specified note.__\
"
    }
)
