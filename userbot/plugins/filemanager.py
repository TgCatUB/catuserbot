"""
By:- @Mrconfused & @sandy1709
idea from userage
"""
import io
import os
import time
from pathlib import Path

from ..utils import admin_cmd, edit_or_reply, humanbytes, sudo_cmd
from . import CMD_HELP, runcmd


@borg.on(admin_cmd(pattern="ls ?(.*)"))
@borg.on(sudo_cmd(pattern="ls ?(.*)", allow_sudo=True))
async def lst(event):
    cat = "".join(event.text.split(maxsplit=1)[1:])
    path = cat if cat else os.getcwd()
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"there is no such directory or file with the name `{cat}` check again",
        )
        return
    path = Path(cat) if cat else os.getcwd()
    if os.path.isdir(path):
        if cat:
            msg = "Folders and Files in `{}` :\n".format(path)
        else:
            msg = "Folders and Files in Current Directory :\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            catpath = os.path.join(path, contents)
            if not os.path.isdir(catpath):
                size = os.stat(catpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += "🎵" + f"`{contents}`\n"
                if str(contents).endswith((".opus")):
                    files += "🎙" + f"`{contents}`\n"
                elif str(contents).endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += "🎞" + f"`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += "🗜" + f"`{contents}`\n"
                elif str(contents).endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")
                ):
                    files += "🖼" + f"`{contents}`\n"
                else:
                    files += "📄" + f"`{contents}`\n"
            else:
                folders += f"📁`{contents}`\n"
        msg = msg + folders + files if files or folders else msg + "__empty path__"
    else:
        size = os.stat(path).st_size
        msg = f"The details of given file :\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵"
        if str(path).endswith((".opus")):
            mode = "🎙"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "🗜"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🖼"
        else:
            mode = "📄"
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location :** `{str(path)}`\n"
        msg += f"**icon :** `{mode}`\n"
        msg += f"**Size :** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"
    if len(msg) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path,
            )
            await event.delete()
    else:
        await edit_or_reply(event, msg)


@borg.on(admin_cmd(pattern="rem (.*)"))
@borg.on(sudo_cmd(pattern="rem (.*)", allow_sudo=True))
async def lst(event):
    cat = event.pattern_match.group(1)
    if cat:
        path = Path(cat)
    else:
        await edit_or_reply(event, "what should i delete")
        return
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"there is no such directory or file with the name `{cat}` check again",
        )
        return
    catcmd = f"rm -rf {path}"
    if os.path.isdir(path):
        await runcmd(catcmd)
        await edit_or_reply(event, f"Succesfully removed `{path}` directory")
    else:
        await runcmd(catcmd)
        await edit_or_reply(event, f"Succesfully removed `{path}` file")


CMD_HELP.update(
    {
        "filemanager": "**Plugin :**`filemanager`\
     \n\nList Files plugin for userbot \
     \n**Syntax :** `.ls`\
     \n**Usage :** will return files from current working directory\
     \n\n**Syntax :** .ls path\
     \n**Usage :** will return output according to path  \
     \n\n**Syntax :** .ls file path\
     \n**Usage :** will return file details\
     \n\nSimple Module for people who dont wanna use shell executor for listing files.\
     \n\n**Syntax :** `.rem path`\
     \n**Usage :** To delete the required item from the bot server\
"
    }
)
