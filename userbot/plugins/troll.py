"""
Created by @Jisan7509
plugin for Cat_Userbot

☝☝☝
You remove this, you gay.
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot, CMD_HELP
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="fox ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    sf = f"sf"
    await event.edit("```Fox is on your way...```")
    async with bot.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=740813545))
            await conv.send_message(f'/{sf} {jisan}')
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @themememakerbot plox```")
            return
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="talkme ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    ttm = f"ttm"
    await event.edit("```Wait making your hardcore meme...```")
    async with bot.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=740813545))
            await conv.send_message(f'/{ttm} {jisan}')
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @themememakerbot plox```")
            return
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="brnsay ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    bbs = f"bbs"
    await event.edit("```You can't stop your brain...```")
    async with bot.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=740813545))
            await conv.send_message(f'/{bbs} {jisan}')
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @themememakerbot plox```")
            return
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="sbob ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    sp = f"sp"
    await event.edit("```Yaah wait for spongebob...```")
    async with bot.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=740813545))
            await conv.send_message(f'/{sp} {jisan}')
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @themememakerbot plox```")
            return
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="child ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    love = f"love"
    await event.edit("```Wait for your son...```")
    async with bot.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=740813545))
            await conv.send_message(f'/{love} {jisan}')
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @themememakerbot plox```")
            return
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


CMD_HELP.update({
    "troll":
    "`.fox` <your text>\
\n**Usage:** Send sneeky fox troll \
\n\n`.talkme` <your text>\
\n**Usage:** Send you a hardcore meme.\
\n\n`.brnsay` <your text>\
\n**Usage:** Send you a sleeping brain meme.\
\n\n`.sbob` <your text>\
\n**Usage:** Send you spongebob meme.\
\n\n`.child` <your text>\
\n**Usage:** Send you child in trash meme."
})
