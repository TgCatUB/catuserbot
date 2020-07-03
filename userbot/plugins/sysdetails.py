"""Get the info your system. Using .neofetch then .sysd"""
from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from telethon import events
import asyncio
from collections import deque
from userbot.utils import admin_cmd
from os import remove
from telethon import version
from userbot import CMD_HELP, ALIVE_NAME
from datetime import datetime
from userbot import StartTime
import time

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
# ============================================


@borg.on(admin_cmd(pattern=f"sysd", outgoing=True))
async def sysdetails(sysd):
    """ a. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
            fetch = await asyncrunapp(
                neo,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await sysd.edit("Neofetch Result: `" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Hello, on catuserbot  install .neofetch first kthx`")

#uptime idea and credits was from @Sur_vivor
@borg.on(admin_cmd(pattern="uptime$"))
async def _(event):
    uptime = get_readable_time((time.time() - StartTime))
    OUTPUT = f"**[Cat's](tg://need_update_for_some_feature/) CPU UPTIME:**\n{uptime}"
    await event.edit(OUTPUT)

@borg.on(admin_cmd(outgoing=True, pattern="botver$"))
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await event.edit("`Userbot Version: "
                         f"{verout}"
                         "` \n"
                         "`Revision: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            "Shame that you don't have git, You're running 9.0 - 'Extended' anyway"
        )





CMD_HELP.update(
    {"sysdetails": 
     ".sysd\
    \nUsage: Shows system information using neofetch.\
    \n\n.botver\
    \nUsage: Shows the userbot version. \
    \n\n.pip <module(s)>\
    \nUsage: Does a search of pip modules(s).\
    "
    })

