# ported from paperplaneExtended by avinashreddy3108 for media support

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from ..sql_helper.snip_sql import add_note, get_note, get_notes, rm_note
from . import BOTLOG, BOTLOG_CHATID, get_message_link

plugin_category = "utils"


@catub.cat_cmd(
    pattern="\#(\S+)",
)
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


@catub.cat_cmd(
    pattern="snips (\w*)",
    command=("snips", plugin_category),
    info={
        "header": "To save notes to the bot.",
        "description": "Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!. and get them by using #notename",
        "usage": "{tr}snips <keyword>",
    },
)
async def add_snip(event):
    "To save notes to bot."
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


@catub.cat_cmd(
    pattern="snipl$",
    command=("snipl", plugin_category),
    info={
        "header": "To list all notes in bot.",
        "usage": "{tr}snipl",
    },
)
async def on_snip_list(event):
    "To list all notes in bot."
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
            msglink = await get_message_link(BOTLOG_CHATID, note.f_mesg_id)
            message += f"  [preview]({msglink})\n"
        else:
            message += "  No preview\n"
    await edit_or_reply(event, message)


@catub.cat_cmd(
    pattern="snipd (\S+)",
    command=("snipd", plugin_category),
    info={
        "header": "To delete paticular note in bot.",
        "usage": "{tr}snipd <keyword>",
    },
)
async def on_snip_delete(event):
    "To delete paticular note in bot."
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
