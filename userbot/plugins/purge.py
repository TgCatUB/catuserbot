# Userbot module for purging unneeded messages(usually spam or ot).
import re
from asyncio import sleep

from telethon.errors import rpcbaseerrors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterEmpty,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"


purgelist = {}

purgetype = {
    "a": InputMessagesFilterVoice,
    "f": InputMessagesFilterDocument,
    "g": InputMessagesFilterGif,
    "i": InputMessagesFilterPhotos,
    "l": InputMessagesFilterGeo,
    "m": InputMessagesFilterMusic,
    "r": InputMessagesFilterRoundVideo,
    "t": InputMessagesFilterEmpty,
    "u": InputMessagesFilterUrl,
    "v": InputMessagesFilterVideo,
    # "s": search
}


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
    elif not input_str:
        await event.delete()


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
        await edit_delete(event, f"**Error**\n`{e}`")


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


# TODO: only sticker messages.
@catub.cat_cmd(
    pattern="purge(?:\s|$)([\s\S]*)",
    command=("purge", plugin_category),
    info={
        "header": "To purge messages from the replied message.",
        "description": "•  Deletes the x(count) amount of messages from the replied message\
        \n•  If you don't use count then deletes all messages from the replied messages\
        \n•  If you haven't replied to any message and used count then deletes recent x messages.\
        \n•  If you haven't replied to any message or havent mentioned any flag or count then doesnt do anything\
        \n•  If flag is used then selects that type of messages else will select all types\
        \n•  You can use multiple flags like -gi 10 (It will delete 10 images and 10 gifs but not 10 messages of combination images and gifs.)\
        ",
        "flags": {
            "a": "To delete Voice messages.",
            "f": "To delete documents.",
            "g": "To delete gif's.",
            "i": "To delete images/photos.",
            "l": "To delete locations/gps.",
            "m": "To delete Audio files(music files).",
            "r": "To delete Round video messages.",
            "t": "To delete stickers and text messages.",
            "u": "To delete url/links.",
            "v": "To delete Video messages.",
            "s": "To search paticular message and delete",
        },
        "usage": [
            "{tr}purge <flag(optional)> <count(x)> <reply> - to delete x flagged messages after reply",
            "{tr}purge <flag> <count(x)> - to delete recent x messages",
        ],
        "examples": [
            "{tr}purge 10",
            "{tr}purge -f 10",
            "{tr}purge -gi 10",
        ],
    },
)
async def fastpurger(event):  # sourcery no-metrics
    "To purge messages from the replied message"
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            if p_type is not None:
                for ty in p_type:
                    if ty in purgetype:
                        async for msg in event.client.iter_messages(
                            event.chat_id,
                            limit=int(input_str),
                            offset_id=reply.id - 1,
                            reverse=True,
                            filter=purgetype[ty],
                        ):
                            count += 1
                            msgs.append(msg)
                            if len(msgs) == 50:
                                await event.client.delete_messages(chat, msgs)
                                msgs = []
                        if msgs:
                            await event.client.delete_messages(chat, msgs)
                    elif ty == "s":
                        error += "\n• __You can't use s flag along with otherflags.__"
                    else:
                        error += f"\n• `{ty}` __is Invalid flag.__"
            else:
                count += 1
                async for msg in event.client.iter_messages(
                    event.chat_id,
                    limit=(int(input_str) - 1),
                    offset_id=reply.id,
                    reverse=True,
                ):
                    msgs.append(msg)
                    count += 1
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
        elif input_str and p_type is not None:
            if p_type == "s":
                try:
                    cont, inputstr = input_str.split(" ")
                except ValueError:
                    cont = "error"
                    inputstr = input_str
                cont = cont.strip()
                inputstr = inputstr.strip()
                if cont.isnumeric():
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        limit=int(cont),
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=inputstr,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                else:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=input_str,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            else:
                error += f"\n• `{ty}` __is Invalid flag.__"
        elif input_str:
            error += f"\n• `.purge {input_str}` __is invalid syntax try again by reading__ `.help -c purge`"
        elif p_type is not None:
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        filter=purgetype[ty],
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                else:
                    error += f"\n• `{ty}` __is Invalid flag.__"
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id - 1
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
    elif p_type is not None and input_str:
        if p_type != "s" and input_str.isnumeric():
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id, limit=int(input_str), filter=purgetype[ty]
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                elif ty == "s":
                    error += "\n• __You can't use s with other flags or you haven't given search query.__"

                else:
                    error += f"\n• `{ty}` __is Invalid flag.__"
        elif p_type == "s":
            try:
                cont, inputstr = input_str.split(" ")
            except ValueError:
                cont = "error"
                inputstr = input_str
            cont = cont.strip()
            inputstr = inputstr.strip()
            if cont.isnumeric():
                async for msg in event.client.iter_messages(
                    event.chat_id, limit=int(cont), search=inputstr
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            else:
                async for msg in event.client.iter_messages(
                    event.chat_id, search=input_str
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
        else:
            error += f"\n• `{ty}` __is Invalid flag.__"
    elif p_type is not None:
        for ty in p_type:
            if ty in purgetype:
                async for msg in event.client.iter_messages(
                    event.chat_id, filter=purgetype[ty]
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            elif ty == "s":
                error += "\n• __You can't use s with other flags or you haven't given search query.__"

            else:
                error += f"\n• `{ty}` __is Invalid flag.__"
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(chat, limit=int(input_str) + 1):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
    else:
        error += "\n•  __Nothing is specified Recheck the help__ (`.help -c purge`)"
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "__Fast purge complete!\nPurged __`" + str(count) + "` __messages.__"
    if error != "":
        result += f"\n\n**Error:**{error}"
    if result == "":
        result += "__There are no messages to purge.__"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PURGE \n{result}",
        )
    await sleep(5)
    await hi.delete()


@catub.cat_cmd(
    pattern="upurge( -a)?(?:\s|$)([\s\S]*)",
    command=("upurge", plugin_category),
    info={
        "header": "To purge messages from the replied message of replied user.",
        "description": "•  Deletes the x(count) amount of messages from the replied message of replied user\
        \n•  If you don't use count then deletes all messages from the replied messages of replied user\
        \n•  Use -a flag to delete all his messages or mention x to delete x recent messages of his\
        \n•  Use -s flag to delete all his messages which contatins given word.\
        \n•  You cann't use both flags at a time\
        ",
        "flags": {
            "a": "To delete all messages of replied user.",
            "s": "To delete all messages of replied user with the given query.",
        },
        "usage": [
            "{tr}upurge <count> <reply>",
            "{tr}upurge -a <count(optional)> <reply>",
            "{tr}upurge -s <query> <reply>",
        ],
        "examples": [
            "{tr}upurge 10",
            "{tr}upurge -s fuck",
            "{tr}upurge -a",
        ],
    },
)
async def fast_purger(event):  # sourcery no-metrics
    "To purge messages from the replied message of replied user."
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if not reply or reply.sender_id is None:
        return await edit_delete(
            event, "**Error**\n__This cmd Works only if you reply to user message.__"
        )
    if not flag:
        if input_str and p_type == "s":
            async for msg in event.client.iter_messages(
                event.chat_id,
                search=input_str,
                from_user=reply.sender_id,
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str and input_str.isnumeric():
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=int(input_str),
                offset_id=reply.id - 1,
                reverse=True,
                from_user=reply.sender_id,
            ):
                msgs.append(msg)
                count += 1
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            error += f"\n• `.upurge {input_str}` __is invalid syntax try again by reading__ `.help -c purge`"
        else:
            async for msg in event.client.iter_messages(
                chat,
                min_id=event.reply_to_msg_id - 1,
                from_user=reply.sender_id,
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(
            chat,
            limit=int(input_str),
            from_user=reply.sender_id,
        ):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    else:
        async for msg in event.client.iter_messages(
            chat,
            from_user=reply.sender_id,
        ):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "__Fast purge completed!\nPurged __`" + str(count) + "` __messages.__"
    if error != "":
        result += f"\n\n**Error:**{error}"
    if result == "":
        result += "__There are no messages to purge.__"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#UPURGE \n{result}",
        )
    await sleep(5)
    await hi.delete()
