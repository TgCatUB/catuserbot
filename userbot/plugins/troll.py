"""
Created by @Jisan7509
plugin for Cat_Userbot
☝☝☝
You remove this, you gay.
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import bot


@bot.on(admin_cmd(pattern="fox ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="fox ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    sf = f"sf"
    cat = await edit_or_reply(event, "```Fox is on your way...```")
    async with event.client.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=740813545)
            )
            await conv.send_message(f"/{sf} {jisan}")
            response = await response
        except YouBlockedUserError:
            await cat.edit("```Unblock @themememakerbot plox```")
            return
        else:
            await cat.delete()
            await event.client.send_message(event.chat_id, response.message)
            await event.client.send_read_acknowledge(conv.chat_id)


@bot.on(admin_cmd(pattern="talkme ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="talkme ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    ttm = f"ttm"
    cat = await edit_or_reply(event, "```Wait making your hardcore meme...```")
    async with event.client.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=740813545)
            )
            await conv.send_message(f"/{ttm} {jisan}")
            response = await response
        except YouBlockedUserError:
            await cat.edit("```Unblock @themememakerbot plox```")
            return
        else:
            await cat.delete()
            await event.client.send_message(event.chat_id, response.message)
            await event.client.send_read_acknowledge(conv.chat_id)


@bot.on(admin_cmd(pattern="brnsay ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="brnsay ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    bbs = f"bbs"
    cat = await edit_or_reply(event, "```You can't stop your brain...```")
    async with event.client.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=740813545)
            )
            await conv.send_message(f"/{bbs} {jisan}")
            response = await response
        except YouBlockedUserError:
            await cat.edit("```Unblock @themememakerbot plox```")
            return
        else:
            await cat.delete()
            await event.client.send_message(event.chat_id, response.message)
            await event.client.send_read_acknowledge(conv.chat_id)


@bot.on(admin_cmd(pattern="sbob ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="sbob ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    sp = f"sp"
    cat = await edit_or_reply(event, "```Yaah wait for spongebob...```")
    async with event.client.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=740813545)
            )
            await conv.send_message(f"/{sp} {jisan}")
            response = await response
        except YouBlockedUserError:
            await cat.edit("```Unblock @themememakerbot plox```")
            return
        else:
            await cat.delete()
            await event.client.send_message(event.chat_id, response.message)
            await event.client.send_read_acknowledge(conv.chat_id)


@bot.on(admin_cmd(pattern="child ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="child ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    jisan = event.pattern_match.group(1)
    love = f"love"
    cat = await edit_or_reply(event, "```Wait for your son...```")
    async with bot.conversation("@themememakerbot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=740813545)
            )
            await conv.send_message(f"/{love} {jisan}")
            response = await response
        except YouBlockedUserError:
            await cat.edit("```Unblock @themememakerbot plox```")
            return
        else:
            await cat.delete()
            await event.client.send_message(event.chat_id, response.message)
            await event.client.send_read_acknowledge(conv.chat_id)


CMD_HELP.update(
    {
        "troll": "__**PLUGIN NAME :** Troll__\
\n\n📌** CMD ➥** `.fox` <your text>\
\n**USAGE   ➥  **Send sneeky fox troll \
\n\n📌** CMD ➥** `.talkme` <your text>\
\n**USAGE   ➥  **Send you a hardcore meme.\
\n\n📌** CMD ➥** `.brnsay` <your text>\
\n**USAGE   ➥  **Send you a sleeping brain meme.\
\n\n📌** CMD ➥** `.sbob` <your text>\
\n**USAGE   ➥  **Send you spongebob meme.\
\n\n📌** CMD ➥** `.child` <your text>\
\n**USAGE   ➥  **Send you child in trash meme."
    }
)
