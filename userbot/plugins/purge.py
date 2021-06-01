# Userbot module for purging unneeded messages(usually spam or ot).
from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"


purgelist = {}


@catub.cat_cmd(
    pattern="purge(?: |$)(.*)",
    command=("purge", plugin_category),
    info={
        "header": "To purge messages from the replied message.",
        "description": "Deletes the x(count) amount of messages from the replied message if you don't use count then deletes all messages from there",
        "usage": [
            "{tr}purge <count> <reply>",
            "{tr}purge <reply>",
        ],
        "examples": "{tr}purge 10",
    },
)
async def fastpurger(event):
    "To purge messages from the replied message"
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            count += 1
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=(int(input_str) - 1),
                offset_id=reply.id,
                reverse=True,
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            return await edit_or_reply(
                event, f"**Error**\n`{input_str} is not an integer. Use proper syntax.`"
            )
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    else:
        await edit_or_reply(
            event,
            "`No message specified.`",
        )
        return
    if msgs:
        await event.client.delete_messages(chat, msgs)
    await event.delete()
    hi = await event.client.send_message(
        event.chat_id,
        "`Fast purge complete!\nPurged " + str(count) + " messages.`",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PURGE \n`Purge of " + str(count) + " messages done successfully.`",
        )
    await sleep(5)
    await hi.delete()


@catub.cat_cmd(
    pattern="purgefrom$",
    command=("purgefrom", plugin_category),
    info={
        "header": "To mark the replied message as starting message of purge list.",
        "description": "After using this u must use purgeto command also so that the messages in between this will delete.",
        "usage": "{tr}purgefrom",
    },
)
async def purge_from(event):
    "To mark the message for purging"
    reply = await event.get_reply_message()
    if reply:
        reply_message = await reply_id(event)
        purgelist[event.chat_id] = reply_message
        await edit_delete(
            event,
            "`This Message marked for deletion. Reply to another message with purgeto to delete all messages in between.`",
        )
    else:
        await edit_delete(event, "`Reply to a message to let me know what to delete.`")


@catub.cat_cmd(
    pattern="purgeto$",
    command=("purgeto", plugin_category),
    info={
        "header": "To mark the replied message as end message of purge list.",
        "description": "U need to use purgefrom command before using this command to function this.",
        "usage": "{tr}purgeto",
    },
)
async def purge_to(event):
    "To mark the message for purging"
    chat = await event.get_input_chat()
    reply = await event.get_reply_message()
    try:
        from_message = purgelist[event.chat_id]
    except KeyError:
        return await edit_delete(
            event,
            "`First mark the messsage with purgefrom and then mark purgeto .So, I can delete in between Messages`",
        )
    if not reply or not from_message:
        return await edit_delete(
            event,
            "`First mark the messsage with purgefrom and then mark purgeto .So, I can delete in between Messages`",
        )
    try:
        to_message = await reply_id(event)
        msgs = []
        count = 0
        async for msg in event.client.iter_messages(
            event.chat_id, min_id=(from_message - 1), max_id=(to_message + 1)
        ):
            msgs.append(msg)
            count += 1
            msgs.append(event.reply_to_msg_id)
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
        await edit_delete(
            event,
            "`Fast purge complete!\nPurged " + str(count) + " messages.`",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PURGE \n`Purge of " + str(count) + " messages done successfully.`",
            )
    except Exception as e:
        await edit_delete(event, f"**Error**\n`{str(e)}`")


@catub.cat_cmd(
    pattern="purgeme",
    command=("purgeme", plugin_category),
    info={
        "header": "To purge your latest messages.",
        "description": "Deletes x(count) amount of your latest messages.",
        "usage": "{tr}purgeme <count>",
        "examples": "{tr}purgeme 2",
    },
)
async def purgeme(event):
    "To purge your latest messages."
    message = event.text
    count = int(message[9:])
    i = 1
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        "**Purge complete!**` Purged " + str(count) + " messages.`",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PURGEME \n`Purge of " + str(count) + " messages done successfully.`",
        )
    await sleep(5)
    await smsg.delete()


@catub.cat_cmd(
    pattern="del(\s*| \d+)$",
    command=("del", plugin_category),
    info={
        "header": "To delete replied message.",
        "description": "Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately",
        "usage": ["{tr}del <time in seconds>", "{tr}del"],
        "examples": "{tr}del 2",
    },
)
async def delete_it(event):
    "To delete replied message."
    input_str = event.pattern_match.group(1).strip()
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#DEL \n`Deletion of message was successful`"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "`Well, I can't delete a message. I am not an admin`",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "`Well the time you mentioned is invalid.`")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#DEL \n`Deletion of message was successful`"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "`Well, I can't delete a message`")
    else:
        if not input_str:
            await event.delete()
