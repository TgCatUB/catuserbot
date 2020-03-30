"""@RollADie
Syntax: .dice"""
from telethon.tl.types import InputMediaDice
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="dice ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice())
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice())
        except:
            pass
