# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#AvinashReddy
""" Userbot module for purging unneeded messages(usually spam or ot).
`.ipurg`
"""

from asyncio import sleep
from telethon.errors import rpcbaseerrors
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="ipurg ?(.*)"))
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await purg.get_input_chat()
    msgs = []
    count = purg.pattern_match.group(1)
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
        await purg.edit("`I Need a Mesasge to Start Purging From.`")
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
        done = await purg.client.send_message(
        purg.chat_id, f"`Fast purge complete!`\
        \nPurged {str(count)} messages") 
        
    await sleep(1)
    await done.delete()


