# Copyright (C) 2019 Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import sleep

from telethon.tl.types import MessageEntityMentionName


from telethon import events
# from stdplugins.dbhelper import (add_chat_fban, add_chat_gban, get_fban,
#                                       get_gban, remove_chat_fban,
#                                       remove_chat_gban)
from userbot.uniborgConfig import Config
from userbot.utils import admin_cmd


from userbot.plugins.sql_helper.gmute_sql import is_gmuted, gmute, ungmute
from userbot.plugins.sql_helper.mute_sql import is_muted, mute ,unmute
from userbot.plugins.sql_helper.fban_sql_helper import is_fban,get_fban,add_chat_fban,remove_chat_fban
from userbot.plugins.sql_helper.gban_sql_helper import is_gban,get_gban,add_chat_gban,remove_chat_gban
from userbot.plugins.sql_helper.spam_mute_sql import is_muted,mute,unmute


# MONGOCLIENT = Config.MONGOCLIENT

@borg.on(admin_cmd(pattern=("gban ?(.*)")))
async def gban_all(msg):
    # if not is_mongo_alive():
    #     await msg.edit("`Database connections failing!`")
    #     return
    textx = await msg.get_reply_message()
    if textx:
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[1:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] gban"
    else:
        banid = msg.text.split(" ")[1]
        if banid.isnumeric():
            # if its a user id
            banid = int(banid)
        else:
            # deal wid the usernames
            if msg.message.entities is not None:
                probable_user_mention_entity = msg.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                banid = probable_user_mention_entity.user_id
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[2:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] fban"
    if not textx:
        await msg.edit(
            "Reply Message missing! Might fail on many bots! Still attempting Gban!"
        )
        # Ensure User Read the warning
        await sleep(1)
    x = get_gban()
    count = 0
    banlist = []
    for i in x:
        banlist.append(i["chat_id"])
    for banbot in banlist:
        async with bot.conversation(banbot) as conv:
            if textx:
                c = await msg.forward_to(banbot)
                await c.reply("/id")
            await conv.send_message(f"/gban {banid} {banreason}")
            await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            count += 1
            # We cant see if he actually Gbanned. Let this stay for now
            await msg.edit("`Gbanned on " + str(count) + " bots!`")
            await sleep(0.2)



@borg.on(admin_cmd(pattern=("fban ?(.*)")))
async def fedban_all(msg):
    # if not is_mongo_alive():
    #     await msg.edit("`Database connections failing!`")
    #     return
    textx = await msg.get_reply_message()
    if textx:
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[1:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] fban"
    else:
        banid = msg.text.split(" ")[1]
        if banid.isnumeric():
            # if its a user id
            banid = int(banid)
        else:
            # deal wid the usernames
            if msg.message.entities is not None:
                probable_user_mention_entity = msg.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                banid = probable_user_mention_entity.user_id
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[2:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] fban"
        if "spam" in banreason:
            spamwatch = True
        else:
            spamwatch = False
    failed = dict()
    count = 1
    fbanlist = []
    x = get_fban()
    for i in x:
        fbanlist.append(i["chat_id"])
    for bangroup in fbanlist:

        # Send to proof to Spamwatch in case it was spam
        # Spamwatch is a reputed fed fighting against spam on telegram

        if bangroup == -1001312712379:
            if spamwatch:
                if textx:
                    await textx.forward_to(-1001312712379)
                    # Tag him, coz we can't fban xd
                    await bot.send_message(-1001312712379, "@SitiSchu")
                else:
                    await msg.reply(
                        "`Spam message detected. But no reply message, can't forward to spamwatch`"
                    )
            continue
        async with bot.conversation(bangroup) as conv:
            await conv.send_message(f"!fban {banid} {banreason}")
            resp = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            if "Beginning federation ban " not in resp.text:
                failed[bangroup] = str(conv.chat_id)
            else:
                count += 1
                await msg.edit("`Fbanned on " + str(count) + " feds!`")
            # Sleep to avoid a floodwait.
            # Prevents floodwait if user is a fedadmin on too many feds
            await sleep(0.2)
    if failed:
        failedstr = ""
        for i in failed.keys():
            failedstr += failed[i]
            failedstr += " "
        await msg.reply(f"`Failed to fban in {failedstr}`")
    else:
        await msg.reply("`Fbanned in all feds!`")



@borg.on(admin_cmd(pattern=("addfban ?(.*)")))
async def add_to_fban(chat):
    # if not is_mongo_alive():
    #     await chat.edit("`Database connections failing!`")
    #     return
    add_chat_fban(chat.chat_id)
    await chat.edit("`Added this chat under the Fbanlist!`")



@borg.on(admin_cmd(pattern=("addgban ?(.*)")))
async def add_to_gban(chat):
    # if not is_mongo_alive():
    #     await chat.edit("`Database connections failing!`")
    #     return
    add_chat_gban(chat.chat_id)
    print(chat.chat_id)
    await chat.edit("`Added this bot under the Gbanlist!`")



@borg.on(admin_cmd(pattern=("removefban ?(.*)")))
async def remove_from_fban(chat):
    # if not is_mongo_alive():
    #     await chat.edit("`Database connections failing!`")
    #     return
    remove_chat_fban(chat.chat_id)
    await chat.edit("`Removed this chat from the Fbanlist!`")



@borg.on(admin_cmd(pattern=("removegban ?(.*)")))
async def remove_from_gban(chat):
    # if not is_mongo_alive():
    #     await chat.edit("`Database connections failing!`")
    #     return
    remove_chat_gban(chat.chat_id)
    await chat.edit("`Removed this bot from the Gbanlist!`")

