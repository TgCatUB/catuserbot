# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for purging unneeded messages(usually spam or ot). """

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import CMD_HELP
from userbot.utils import admin_cmd, errors_handler

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(outgoing=True, pattern="purge$"))
@errors_handler
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit(
            "`No message specified.`",
        )
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "Fast purge complete!\nPurged " + str(count) + " messages.",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "#PURGE \nPurge of " + str(count) + " messages done successfully.",
        )
    await sleep(2)
    await done.delete()


@borg.on(admin_cmd(outgoing=True, pattern="purgeme"))
@errors_handler
async def purgeme(delme):
    """ For .purgeme, delete x count of your latest message."""
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Purge complete!` Purged " + str(count) + " messages.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "#PURGEME \nPurge of " + str(count) + " messages done successfully.",
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@borg.on(admin_cmd(outgoing=True, pattern="del$"))
@errors_handler
async def delete_it(delme):
    """ For .del command, delete the replied message. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "#DEL \nDeletion of message was successful"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Well, I can't delete a message"
                )


@borg.on(admin_cmd(outgoing=True, pattern="edit"))
@errors_handler
async def editer(edit):
    """ For .editme command, edit your last message. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(
            BOTLOG_CHATID, "#EDIT \nEdit query was executed successfully"
        )


CMD_HELP.update(
    {
        "purge": "__**PLUGIN NAME :** Purge__\
    \n\n📌** CMD ➥** `.purge`\
    \n**USAGE   ➥  **Purges all messages starting from the reply.\
    \n\n📌** CMD ➥** `.purgeme` <x>\
    \n**USAGE   ➥  **Deletes x amount of your latest messages.\
    \n\n📌** CMD ➥** `.del`\
    \n**USAGE   ➥  **Deletes the message you replied to.\
    \n\n📌** CMD ➥** `.edit` <newmessage>\
    \n**USAGE   ➥  **Replace your last message with <newmessage>."
    }
)
