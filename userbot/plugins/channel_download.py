"""
Telegram Channel Media Downloader Plugin for userbot.
usage: .geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]
       .getc number_of_messsages channel_username
By: @Zero_cool7870
"""
import os
import subprocess

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern=r"getc(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="getc(?: |$)(.*)", allow_sudo=True))
async def get_media(event):
    if event.fwd_from:
        return
    tempdir = Config.TMP_DOWNLOAD_DIRECTORY
    try:
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    except BaseException:
        pass
    catty = event.pattern_match.group(1)
    limit = int(catty.split(" ")[0])
    channel_username = str(catty.split(" ")[1])
    event = await edit_or_reply(event, "Downloading Media From this Channel.")
    msgs = await borg.get_messages(channel_username, limit=int(limit))
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    i = 0
    for msg in msgs:
        if msg.media is not None:
            await borg.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", "temp"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", " ")
    output = output.replace("\\n'", " ")
    await event.edit("Downloaded " + output + " files.")


@borg.on(admin_cmd(pattern="geta(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="geta(?: |$)(.*)", allow_sudo=True))
async def get_media(event):
    if event.fwd_from:
        return
    tempdir = Config.TMP_DOWNLOAD_DIRECTORY
    try:
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    except BaseException:
        pass
    channel_username = event.pattern_match.group(1)
    event = await edit_or_reply(event, "Downloading All Media From this Channel.")
    msgs = await borg.get_messages(channel_username, limit=3000)
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    i = 0
    for msg in msgs:
        if msg.media is not None:
            await borg.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", "temp"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\\n'", "")
    await event.edit("Downloaded " + output + " files.")


CMD_HELP.update(
    {
        "channel_download": "Telegram Channel Media Downloader Plugin for userbot.\
\n\n**USAGE :**\n .geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]\
\n\n.getc number_of_messsages channel_username"
    }
)
