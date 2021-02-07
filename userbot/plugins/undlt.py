import asyncio

from userbot.utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot.cmdhelp import CmdHelp


@bot.on(admin_cmd(pattern="undlt"))
@bot.on(sudo_cmd(pattern="undlt", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await borg.get_admin_log(
            event.chat_id, limit=5, search="", edit=False, delete=True
        )
        for i in a:
            await event.reply(i.original.action.message)
    else:
        await edit_or_reply(event, "You need administrative permissions in order to do this command"
        )
        await asyncio.sleep(3)
        await event.delete()

CmdHelp("undlt").add_command(
  "undlt", None, "Sends 5 recently deleted message from that group. Requires admin position"
).add()