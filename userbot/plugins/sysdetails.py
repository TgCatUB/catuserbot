"""Get the info your system. Using .neofetch then .sysd"""
from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
import asyncio
from userbot.utils import admin_cmd
from userbot import CMD_HELP, ALIVE_NAME, catdef, StartTime
import time
# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
# ============================================


@borg.on(admin_cmd(pattern="cpu$"))
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
#    dirname = event.pattern_match.group(1)
#    tempdir = "localdir"
    cmd = "cat /proc/cpuinfo | grep 'model name'"
#    if dirname == tempdir:

    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Cat's](tg://need_update_for_some_feature/) CPU Model:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        await event.edit(OUTPUT)


@borg.on(admin_cmd(pattern="neofetch$"))
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
#    dirname = event.pattern_match.group(1)
#    tempdir = "localdir"
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
#    if dirname == tempdir:

    event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    stdout.decode()
    OUTPUT = f"Neofetch Installed, Use `.sysd`"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "neofetch.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(OUTPUT)


@borg.on(admin_cmd(pattern=f"sysd$", outgoing=True))
async def sysdetails(sysd):
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

# uptime idea and credits was from @Sur_vivor


@borg.on(admin_cmd(pattern="uptime$"))
async def _(event):
    uptime = await catdef.get_readable_time((time.time() - StartTime))
    OUTPUT = f"**[Cat's](tg://need_update_for_some_feature/) CPU UPTIME:**\n{uptime}"
    await event.edit(OUTPUT)


CMD_HELP.update(
    {"sysdetails":
     ".sysd\
    \nUsage: Shows system information using neofetch.\
    \n\n`.uptime`\
    \nUsage:shows the uptime of your cpu\
    "
     })
