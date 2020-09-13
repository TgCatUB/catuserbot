# ported from paperplaneExtended by avinashreddy3108 for media support
from telethon import events
from telethon.tl import types

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from .sql_helper.snip_sql import add_note, get_note, get_notes, rm_note
from .sql_helper.snips_sql import get_all_snips, get_snips, remove_snip

TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(events.NewMessage(pattern=r"\#(\S+)", outgoing=True))
async def on_snip(event):
    name = event.pattern_match.group(1)
    snip = get_snips(name)
    if snip:
        if snip.snip_type == TYPE_PHOTO:
            media = types.InputPhoto(
                int(snip.media_id),
                int(snip.media_access_hash),
                snip.media_file_reference,
            )
        elif snip.snip_type == TYPE_DOCUMENT:
            media = types.InputDocument(
                int(snip.media_id),
                int(snip.media_access_hash),
                snip.media_file_reference,
            )
        else:
            media = None
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        await borg.send_message(
            event.chat_id, snip.reply, reply_to=message_id, file=media
        )
        await event.delete()


@borg.on(events.NewMessage(pattern=r"\#(\S+)", outgoing=True))
async def incom_note(getnt):
    try:
        if not (await getnt.get_sender()).bot:
            notename = getnt.text[1:]
            note = get_note(notename)
            message_id_to_reply = getnt.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note and note.f_mesg_id:
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
            elif note and note.reply:
                await getnt.delete()
                await bot.send_message(
                    getnt.chat_id,
                    note.reply,
                    reply_to=message_id_to_reply,
                    link_preview=False,
                )
    except AttributeError:
        pass


@borg.on(admin_cmd(pattern=r"snips (\w*)"))
@borg.on(sudo_cmd(pattern=r"snips (\w*)", allow_sudo=True))
async def add_snip(fltr):
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
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
    success = "Note {}  is successfully saved. Use` #{} `to get it"
    if add_note(keyword, string, msg_id) is False:
        rm_note(keyword)
        if add_note(keyword, string, msg_id) is False:
            return await edit_or_reply(
                fltr, f"Error in saving the given snip {keyword}"
            )
        return await edit_or_reply(fltr, success.format("updated", keyword))
    return await edit_or_reply(fltr, success.format("added", keyword))


@borg.on(admin_cmd(pattern="snipl$"))
@borg.on(sudo_cmd(pattern=r"snipl$", allow_sudo=True))
async def on_snip_list(event):
    message = "There are no saved notes in this chat"
    notes = get_notes()
    all_snips = get_all_snips()
    for note in notes:
        if message == "There are no saved notes in this chat":
            message = "Notes saved in this chat:\n"
            message += "👉 `#{}`\n".format(note.keyword)
        else:
            message += "👉 `#{}`\n".format(note.keyword)
    for a_snip in all_snips:
        if message == "There are no saved notes in this chat":
            message = "Notes saved in this chat:\n"
            message += "👉 `#{}`\n".format(a_snip.snip)
        else:
            message += "👉 `#{}`\n".format(a_snip.snip)
    if len(message) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(message)) as out_file:
            out_file.name = "snips.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Snips",
                reply_to=event,
            )
            await event.delete()
    else:
        await edit_or_reply(event, message)


@borg.on(admin_cmd(pattern=r"snipd (\S+)"))
@borg.on(sudo_cmd(pattern=r"snipd (\S+)", allow_sudo=True))
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    snip = get_snips(name)
    catsnip = get_note(name)
    if snip:
        remove_snip(name)
    elif catsnip:
        rm_note(name)
    else:
        return await edit_or_reply(
            event, f"Are you sure that #{name} is saved as snip?"
        )
    await edit_or_reply(event, "snip #{} deleted successfully".format(name))


CMD_HELP.update(
    {
        "snip": "__**PLUGIN NAME :** Snip__\
\n\n📌** CMD ➥**  #<snipname>\
\n**USAGE   ➥  **Gets the specified note.\
\n\n📌** CMD ➥** `.snips`: reply to a message with `.snips <notename>`\
\n**USAGE   ➥  **Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!)\
\n\n📌** CMD ➥** `.snipl`\
\n**USAGE   ➥  **Gets all saved notes in a chat.\
\n\n📌** CMD ➥** `.snipd <notename>`\
\n**USAGE   ➥  **Deletes the specified note.\
"
    }
)
