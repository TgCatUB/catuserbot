from asyncio import sleep

from userbot import catub

plugin_category = "utils"


@catub.cat_cmd(
    pattern="schd (\d*) ([\s\S]*)",
    command=("schd", plugin_category),
    info={
        "header": "To schedule a message after given time(in seconds).",
        "usage": "{tr}schd <time_in_seconds>  <message to send>",
        "examples": "{tr}schd 120 hello",
    },
)
async def _(event):
    "To schedule a message after given time"
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)
