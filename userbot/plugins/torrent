# ported from ProjectBish by @sandy1709
# credits to ProjectBish
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

import math
import os
from asyncio import sleep
from subprocess import PIPE, Popen

import aria2p
from requests import get

from ..utils import admin_cmd, humanbytes
from . import CMD_HELP, LOGS, TMP_DOWNLOAD_DIRECTORY, bot


def subprocess_run(cmd):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        return
    return talk


# Get best trackers for improved download speeds, thanks K-E-N-W-A-Y.
trackers_list = get(
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
).text.replace("\n\n", ",")
trackers = f"[{trackers_list}]"

cmd = f"aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800 --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --max-upload-limit=5K --max-concurrent-downloads=5 --min-split-size=10M --follow-torrent=mem --split=10 --bt-tracker={trackers} --daemon=true --allow-overwrite=true"
EDIT_SLEEP_TIME_OUT = 5

aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))

subprocess_run(cmd)

if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(TMP_DOWNLOAD_DIRECTORY)

download_path = os.getcwd() + TMP_DOWNLOAD_DIRECTORY.strip(".")

aria2.set_global_options({"dir": download_path})


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    LOGS.info("Changing GID " + gid + " to" + new_gid)
    return new_gid


@bot.on(admin_cmd(pattern=r"fromurl(?: |$)(.*)"))
async def aurl_download(event):
    uri = [event.pattern_match.group(1)]
    try:  # Add URL Into Queue
        download = aria2.add_uris(uri, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        return await event.edit("Error :\n`{}`".format(str(e)))
    gid = download.gid
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, event=event, previous=None)
    else:
        await check_progress_for_dl(gid=gid, event=event, previous=None)


@bot.on(admin_cmd(pattern=r"magnet(?: |$)(.*)"))
async def magnet_download(event):
    magnet_uri = event.pattern_match.group(1)
    # Add Magnet URI Into Queue
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        return await event.edit("Error:\n`" + str(e) + "`")
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    await sleep(5)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=event, previous=None)


@bot.on(admin_cmd(pattern=r"tor(?: |$)(.*)"))
async def torrent_download(event):
    torrent_file_path = event.pattern_match.group(1)
    # Add Torrent Into Queue
    try:
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None
        )
    except Exception as e:
        return await event.edit(str(e))
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)


@bot.on(admin_cmd(pattern=r"aclear$"))
async def remove_all(event):
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except Exception:
        pass
    if not removed:  # If API returns False Try to Remove Through System Call.
        subprocess_run("aria2p remove-all")
    await event.edit("`Clearing on-going downloads... `")
    await sleep(2.5)
    await event.edit("`Successfully cleared all downloads.`")
    await sleep(2.5)


@bot.on(admin_cmd(pattern="apause$"))
async def pause_all(event):
    # Pause ALL Currently Running Downloads.
    await event.edit("`Pausing downloads...`")
    aria2.pause_all(force=True)
    await sleep(2.5)
    await event.edit("`Successfully paused on-going downloads.`")
    await sleep(2.5)


@bot.on(admin_cmd(pattern="aresume$"))
async def resume_all(event):
    await event.edit("`Resuming downloads...`")
    aria2.resume_all()
    await sleep(1)
    await event.edit("`Downloads resumed.`")
    await sleep(2.5)
    await event.delete()


@bot.on(admin_cmd(pattern=r"ashow$"))
async def show_all(event):
    output = "output.txt"
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = (
            msg
            + "File: `"
            + str(download.name)
            + "`\nSpeed: "
            + str(download.download_speed_string())
            + "\nProgress: "
            + str(download.progress_string())
            + "\nTotal Size: "
            + str(download.total_length_string())
            + "\nStatus: "
            + str(download.status)
            + "\nETA:  "
            + str(download.eta_string())
            + "\n\n"
        )
    if len(msg) <= 4096:
        await event.edit("`On-going Downloads: `\n" + msg)
    else:
        await event.edit("`Output is too big, sending it as a file...`")
        with open(output, "w") as f:
            f.write(msg)
        await sleep(2)
        await event.delete()
        await event.client.send_file(
            event.chat_id,
            output,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
        )


async def check_progress_for_dl(gid, event, previous):
    file = aria2.get_download(gid)
    complete = file.is_complete
    try:
        if not complete:
            if not file.error_message:
                percentage = int(file.progress)
                downloaded = percentage * int(file.total_length) / 100
                prog_str = "**Downloading : **`[{0}{1}] {2}`".format(
                    "".join(["▰" for i in range(math.floor(percentage / 10))]),
                    "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
                    file.progress_string(),
                )
                msg = (
                    f"**Name : **`{file.name}`\n"
                    f"**Status : **`{file.status.capitalize()}`\n"
                    f"{prog_str}\n"
                    f"`{humanbytes(downloaded)} of {file.total_length_string()}"
                    f" @ {file.download_speed_string()}`\n"
                    f"**ETA** -> `{file.eta_string()}`\n"
                )
                if msg != previous:
                    await event.edit(msg)
                    msg = previous

                await sleep(3)
                await check_progress_for_dl(gid, event, previous)
            else:
                await event.edit("Error : `{}`".format(str(file.error_message)))
                return
        else:
            return await event.edit(
                f"**Name : **`{file.name}`\n"
                f"**Size : **`{file.total_length_string()}`\n"
                f"**Path : **`{TMP_DOWNLOAD_DIRECTORY + file.name}`\n"
                "**Resp : **`OK - Successfully downloaded...`"
            )
    except Exception as e:
        if " not found" in str(e) or "'file'" in str(e):
            await event.edit("Download Canceled :\n`{}`".format(file.name))
            await sleep(2.5)
            return await event.delete()
        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await event.edit(
                "Download Auto Canceled :\n`{}`\nYour Torrent/Link is Dead.".format(
                    file.name
                )
            )


CMD_HELP.update(
    {
        "torrent": "**Plugin : **`torrent`"
        "\n\n**Syntax : **`.fromurl [URL]` (or) >`.magnet [Magnet Link]` (or) >`.tor [path to torrent file]`"
        "\n**Usage :** Downloads the file into your userbot server storage."
        "\n\n**Syntax : **`.apause (or) .aresume`"
        "\n**Usage : **Pauses/resumes on-going downloads."
        "\n\n**Syntax :**`.aclear`"
        "\n**Usage : **Clears the download queue, deleting all on-going downloads."
        "\n\n**Syntax : **`.ashow`"
        "\n**Usage : **Shows progress of the on-going downloads."
    }
)
