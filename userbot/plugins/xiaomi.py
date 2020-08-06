#created by @eve_enryu

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.firmware(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@XiaomiGeeksBot"
    firmware = f"firmware"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await conv.send_message(f'/{firmware} {link}')
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @XiaomiGeeksBot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)

  
@register(outgoing=True, pattern="^.specs(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@XiaomiGeeksBot"
    specs = f"specs"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await conv.send_message(f'/{specs} {link}')
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @xiaomiGeeksBot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)
   
 
 
@register(outgoing=True, pattern="^.fastboot(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@XiaomiGeeksBot"
    fboot = f"fastboot"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await conv.send_message(f'/{fboot} {link}')
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @XiaomiGeeksBoot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)

 
@register(outgoing=True, pattern="^.recovery(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@XiaomiGeeksBot"
    recovery = f"recovery"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await conv.send_message(f'/{recovery} {link}')
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @XiaomiGeeksBot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.pb(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@XiaomiGeeksBot"
    pitch = f"pb"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await conv.send_message(f'/{pitch} {link}')
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @XiaomiGeeksBot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.of(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@XiaomiGeeksBot"
    ofox = f"of"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await conv.send_message(f'/{ofox} {link}')
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @XiaomiGeeksBot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)

CMD_HELP.update({
"xiaomi":
"For Xiaomeme devices only!\
\n\n`.firmware` (codename)\
     \nUsage : Get lastest Firmware\
\n\n`.pb` (codename)\
     \nUsage : Get latest PBRP\
\n\n`.specs` (codename)\
     \nUsage : Get quick spec information about device\
\n\n`.fastboot` (codename)\
     \nUsage : Get latest fastboot MIUI\
\n\n`.recovery` (codename)\
     \nUsage : Get latest recovery MIUI\
\n\n`.of` (codename)\
     \nUsage : Get latest ORangeFox Recovery"})
