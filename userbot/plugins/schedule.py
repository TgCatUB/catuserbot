from asyncio import sleep

from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd


@bot.on(admin_cmd(pattern="schd (\d*) (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="schd (\d*) (.*)", allow_sudo=True))
async def _(event):
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    try:
        await event.delete()
    except:
        pass
    await sleep(ttl)
    await event.respond(message)


CMD_HELP.update(
    {
        "schedule": "**Plugin : **`schedule`\
    \n\n**Syntax : **`.schd <time_in_seconds>  <message to send>`\
    \n**Function : **Send you the given message after that particular time\
    "
    }
)
