import os
from subprocess import PIPE, Popen

import aria2p
from requests import get

from .. import LOGS
from ..Config import Config

TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY


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
