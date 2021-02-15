import math
import os
from asyncio import sleep
from subprocess import PIPE, Popen

try:
    import appdirs
except:
    install_pip("appdirs")
    import appdirs
    
try:
    import aria2p
except:
    install_pip("aria2p")
    import aria2p

from requests import get

from . import LOGS, humanbytes


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

cmd = f"aria2c \
--enable-rpc \
--rpc-listen-all=false \
--rpc-listen-port 8210 \
--max-connection-per-server=10 \
--rpc-max-request-size=1024M \
--seed-time=0.01 \
--max-upload-limit=5K \
--max-concurrent-downloads=5 \
--min-split-size=10M \
--follow-torrent=mem \
--split=10 \
--bt-tracker={trackers} \
--daemon=true \
--allow-overwrite=true"

subprocess_run(cmd)
TEMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
    os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
download_path = os.getcwd() + TEMP_DOWNLOAD_DIRECTORY.strip(".")

aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=8210, secret=""))

aria2.set_global_options({"dir": download_path})


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    LOGS.info("Changing GID " + gid + " to" + new_gid)
    return new_gid


async def check_progress_for_dl(gid, event, previous):
    complete = None
    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            if not complete and not file.error_message:
                percentage = int(file.progress)
                downloaded = percentage * int(file.total_length) / 100
                prog_str = "`Downloading` | [{0}{1}] `{2}`".format(
                    "".join(["▰" for i in range(math.floor(percentage / 10))]),
                    "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
                    file.progress_string(),
                )
                msg = (
                    f"**Name**: `{file.name}`\n"
                    f"**Status** -> `{file.status.capitalize()}`\n"
                    f"{prog_str}\n"
                    f"`{humanbytes(downloaded)} of {file.total_length_string()}"
                    f" @ {file.download_speed_string()}`\n"
                    f"**ETA** -> {file.eta_string()}\n"
                )
                if msg != previous:
                    await event.edit(msg)
                    msg = previous
            else:
                await event.edit(f"`{msg}`")
            await sleep(5)
            await check_progress_for_dl(gid, event, previous)
            file = aria2.get_download(gid)
            complete = file.is_complete
            if complete:
                return await event.edit(
                    f"**Name :** `{file.name}`\n"
                    f"**Size :** `{file.total_length_string()}`\n"
                    f"**Path :** `{TEMP_DOWNLOAD_DIRECTORY + file.name}`\n"
                    "**Response :** __OK - Successfully downloaded...__"
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
