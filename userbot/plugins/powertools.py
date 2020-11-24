import sys
from os import execl
from time import sleep

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, HEROKU_APP, bot


@bot.on(admin_cmd(pattern="restart$"))
@bot.on(sudo_cmd(pattern="restart$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    await edit_or_reply(
        event,
        "Restarted. `.ping` me or `.help` to check if I am online, actually it takes 1-2 min for restarting",
    )
    await bot.disconnect()
    execl(sys.executable, sys.executable, *sys.argv)


@bot.on(admin_cmd(pattern="shutdown$"))
@bot.on(sudo_cmd(pattern="shutdown$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if HEROKU_APP is not None:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down"
            )
        await edit_or_reply(event, "`Turning off bot now ...Manually turn me on later`")
        HEROKU_APP.process_formation()["userbot"].scale(0)
    else:
        await edit_or_reply(
            event,
            "`Set HEROKU_APP_NAME and HEROKU_API_KEY to work this function properly`",
        )
        await bot.disconnect()


@bot.on(admin_cmd(pattern="sleep( [0-9]+)?$"))
@bot.on(sudo_cmd(pattern="sleep( [0-9]+)?$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "Syntax: `.sleep time`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "You put the bot to sleep for " + str(counter) + " seconds",
        )
    event = await edit_or_reply(event, f"`ok, let me sleep for {counter} seconds`")
    sleep(counter)
    await event.edit("`OK, I'm awake now.`")


CMD_HELP.update(
    {
        "powertools": "**Plugin : **`powertools`\
        \n\n  •  **Syntax : **`.restart`\
        \n  •  **Function : **__Restarts the bot !!__\
        \n\n  •  **Syntax : **`.sleep <seconds>`\
        \n  •  **Function: **__Userbots get tired too. Let yours snooze for a few seconds.__\
        \n\n  •  **Syntax : **`.shutdown`\
        \n**  •  Function : **__To turn off the dyno of heroku. you cant turn on by bot you need to got to heroku and turn on or use__ @hk_heroku_bot"
    }
)
