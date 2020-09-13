import asyncio

from userbot import CMD_HELP
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="scam ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    input_str = event.pattern_match.group(1)
    action = "typing"
    if input_str:
        action = input_str
    async with borg.action(event.chat_id, action):
        await asyncio.sleep(86400)  # type for 10 seconds


CMD_HELP.update(
    {
        "scam": "__**PLUGIN NAME :** Scam__\
    \n\n📌** CMD ➥** `.scam` <action> \
    \n**USAGE   ➥  **Type .scam (action name) this shows the fake action in the group  the actions are `typing` ,`contact` ,`game`, `location`,`voice`,`round`, `video`,`photo`,`document`, `cancel`.\
    "
    }
)
