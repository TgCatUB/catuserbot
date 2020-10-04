# created by @eve_enryu

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import admin_cmd


@borg.on(admin_cmd(pattern="firmware(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        firmware = f"firmware"
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{firmware} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="specs(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        specs = f"specs"
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{specs} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @xiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="fastboot(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        fboot = f"fastboot"
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{fboot} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBoot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="recovery(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        recovery = f"recovery"
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{recovery} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="pb(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        pitch = f"pb"
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{pitch} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="of(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        ofox = f"of"
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{ofox} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
        await bot.send_read_acknowledge(conv.chat_id)


CMD_HELP.update(
    {
        "xiaomi": "**Plugin :** `Xiaomi`\
        \n\n__**For Xiaomeme devices only!**__\
        \n\n**Syntax :** `.firmware` (codename)\
        \n**Usage : **Get lastest Firmware\
        \n\n**Syntax :** `.pb` (codename)\
        \n**Usage : **Get latest PBRP\
        \n\n**Syntax :** `.specs` (codename)\
        \n**Usage : **Get quick spec information about device\
        \n\n**Syntax :** `.fastboot` (codename)\
        \n**Usage : **Get latest fastboot MIUI\
        \n\n**Syntax :** `.recovery` (codename)\
        \n**Usage : **Get latest recovery MIUI\
        \n\n**Syntax :** `.of` (codename)\
        \n**Usage : **Get latest ORangeFox Recovery"
    }
)
