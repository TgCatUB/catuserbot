# By MineisZarox https://t.me/IrisZarox (Demon)
import asyncio
import os
import time
from pathlib import Path

from telethon import Button, types
from telethon.events import CallbackQuery, InlineQuery
from userbot import catub

from ..Config import Config
from ..helpers.utils import _catutils
from . import humanbytes

CC = []
PATH = []  # using list method for some reason
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


def get_thumb(url):
    return types.InputWebDocument(url=url, size=0, mime_type="image/png", attributes=[])


# freaking selector
def add_s(msg, num: int):
    fmsg = ""
    msgs = msg.splitlines()
    leng = len(msgs)
    if num == 0:
        valv = leng - 1
        msgs[valv] = msgs[valv] + " ⭕️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    elif num == leng:
        valv = 1
        msgs[valv] = msgs[valv] + " ⭕️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    else:
        valv = num
        msgs[valv] = msgs[valv] + " ⭕️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    buttons = [
        [
            Button.inline(f"D", data=f"rem_{msgs[valv]}|{valv}"),
            Button.inline(f"X", data=f"cut_{msgs[valv]}|{valv}"),
            Button.inline(f"C", data=f"copy_{msgs[valv]}|{valv}"),
            Button.inline(f"V", data=f"paste_{valv}"),
        ],
        [
            Button.inline(f"⬅️", data=f"back"),
            Button.inline(f"⬆️", data=f"up_{valv}"),
            Button.inline(f"⬇️", data=f"down_{valv}"),
            Button.inline(f"➡️", data=f"forth_{msgs[valv]}"),
        ],
    ]
    return fmsg, buttons


def get_manager(path, num: int):
    if os.path.isdir(path):
        msg = "Folders and Files in `{}` :\n".format(path)
        lists = sorted(os.listdir(path))
        files = ""
        folders = ""
        for contents in sorted(lists):
            zpath = os.path.join(path, contents)
            if not os.path.isdir(zpath):
                size = os.stat(zpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎧`{contents}`\n"
                if str(contents).endswith((".opus")):
                    files += f"🎤`{contents}`\n"
                elif str(contents).endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += f"🎬`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += f"📚`{contents}`\n"
                elif str(contents).endswith((".py")):
                    files += f"🐍`{contents}`\n"
                elif str(contents).endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")
                ):
                    files += f"🏞`{contents}`\n"
                else:
                    files += f"📔`{contents}`\n"
            else:
                folders += f"📂`{contents}`\n"
        msg = msg + folders + files if files or folders else f"{msg}__empty path__"
        PATH.clear()
        PATH.append(path)
        msgs = add_s(msg, int(num))
    else:
        size = os.stat(path).st_size
        msg = "The details of given file :\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎧"
        if str(path).endswith((".opus")):
            mode = "🎤"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎬"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "📚"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🏞"
        elif str(path).endswith((".py")):
            mode = "🐍"
        else:
            mode = "📔"
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location :** `{path}`\n"
        msg += f"**icon :** `{mode}`\n"
        msg += f"**Size :** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"
        buttons = [
            [
                Button.inline(f"Rem", data=f"rem_File|{num}"),
                Button.inline(f"Send", data=f"send"),
                Button.inline(f"X", data=f"cut_File|{num}"),
                Button.inline(f"C", data=f"copy_File{num}"),
            ],
            [
                Button.inline(f"⬅️", data=f"back"),
                Button.inline(f"⬆️", data=f"up_File"),
                Button.inline(f"⬇️", data=f"down_File"),
                Button.inline(f"➡️", data=f"forth_File"),
            ],
        ]
        PATH.clear()
        PATH.append(path)
        msgs = (msg, buttons)
    return msgs


# BACK
@catub.tgbot.on(CallbackQuery(pattern="back"))
async def back(event):
    path = PATH[0]
    paths = path.split("/")
    if paths[-1] == "":
        paths.pop()
        paths.pop()
    else:
        paths.pop()
    npath = ""
    for ii in paths:
        npath += f"{ii}/"
    num = 1
    msg, buttons = get_manager(npath, num)
    await asyncio.sleep(1)
    await event.edit(msg, buttons=buttons)


# UP
@catub.tgbot.on(CallbackQuery(pattern="up_(.*)"))
async def up(event):
    num = event.pattern_match.group(1).decode("UTF-8")
    if num == "File":
        await event.answer("Its a File dummy!", alert=True)
    else:
        num1 = int(num) - 1
        path = PATH[0]
        msg, buttons = get_manager(path, num1)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)


# DOWN
@catub.tgbot.on(CallbackQuery(pattern="down_(.*)"))
async def down(event):
    num = event.pattern_match.group(1).decode("UTF-8")
    if num == "File":
        await event.answer("Its a file dummy!", alert=True)
    else:
        path = PATH[0]
        num1 = int(num) + 1
        msg, buttons = get_manager(path, num1)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)


# FORTH
@catub.tgbot.on(CallbackQuery(pattern="forth_(.*)"))
async def forth(event):
    npath = event.pattern_match.group(1).decode("UTF-8")
    if npath == "File":
        await event.answer("Its a file dummy!", alert=True)
    else:
        path = PATH[0]
        npath = npath[2:-4]
        rpath = f"{path}/{npath}"
        num = 1
        msg, buttons = get_manager(rpath, num)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)


# REMOVE
@catub.tgbot.on(CallbackQuery(pattern="rem_(.*)"))
async def remove(event):
    fn, num = (event.pattern_match.group(1).decode("UTF-8")).split("|", 1)
    path = PATH[0]
    if fn == "File":
        paths = path.split("/")
        if paths[-1] == "":
            paths.pop()
            paths.pop()
        else:
            paths.pop()
        npath = ""
        for ii in paths:
            npath += f"{ii}/"
        rpath = path
    else:
        n_path = fn[2:-4]
        rpath = f"{path}/{n_path}"
        npath = path
    msg, buttons = get_manager(npath, num)
    await asyncio.sleep(1)
    await event.edit(msg, buttons=buttons)
    await _catutils.runcmd(f"rm -rf '{rpath}'")
    await event.answer(f"{rpath} removed successfully...")


# SEND
@catub.tgbot.on(CallbackQuery(pattern="send"))
async def send(event):
    print(event)
    path = PATH[0]
    chat = -(int((await event.get_chat()).id)) + -1000000000000
    await catub.send_file(
        chat,
        file=path,
        thumb=thumb_image_path if os.path.exists(thumb_image_path) else None,
    )
    await event.answer(f"File {path} sent successfully...")


# CUT
@catub.tgbot.on(CallbackQuery(pattern="cut_(.*)"))
async def cut(event):
    f, n = (event.pattern_match.group(1).decode("UTF-8")).split("|", 1)
    if CC:
        return await event.answer(f"Paste {CC[1]} first")
    else:
        if f == "File":
            npath = PATH[0]
            paths = npath.split("/")
            if paths[-1] == "":
                paths.pop()
                paths.pop()
            else:
                paths.pop()
            path = ""
            for ii in paths:
                path += f"{ii}/"
            CC.append("cut")
            CC.append(npath)
            await event.answer(f"Moving {npath} ...")
        else:
            path = PATH[0]
            npath = f[2:-4]
            rpath = f"{path}/{npath}"
            CC.append("cut")
            CC.append(rpath)
            await event.answer(f"Moving {rpath} ...")
        msg, buttons = get_manager(path, n)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)


# COPY
@catub.tgbot.on(CallbackQuery(pattern="copy_(.*)"))
async def copy(event):
    f, n = (event.pattern_match.group(1).decode("UTF-8")).split("|", 1)
    if CC:
        return await event.answer(f"Paste {CC[1]} first")
    else:
        if f == "File":
            npath = PATH[0]
            paths = npath.split("/")
            if paths[-1] == "":
                paths.pop()
                paths.pop()
            else:
                paths.pop()
            path = ""
            for ii in paths:
                path += f"{ii}/"
            CC.append("copy")
            CC.append(npath)
            await event.answer(f"Copying {path} ...")
        else:
            path = PATH[0]
            npath = f[2:-4]
            rpath = f"{path}/{npath}"
            CC.append("copy")
            CC.append(rpath)
            await event.answer(f"Copying {rpath} ...")
        msg, buttons = get_manager(path, n)
        await asyncio.sleep(1)
        await event.edit(msg, buttons=buttons)


# PASTE
@catub.tgbot.on(CallbackQuery(pattern="paste_(.*)"))
async def paste(event):
    n = event.pattern_match.group(1).decode("UTF-8")
    path = PATH[0]
    if CC:
        if CC[0] == "cut":
            cmd = f"mv '{CC[1]}' '{path}'"
        else:
            cmd = f"cp '{CC[1]}' '{path}'"
        await _catutils.runcmd(cmd)
        msg, buttons = get_manager(path, n)
        await event.edit(msg, buttons=buttons)
        CC.clear
    else:
        await event.answer("You aint copied anything to paste")


@catub.tgbot.on(InlineQuery)
async def lsinline(event):

    if (
        event.query.user_id == Config.OWNER_ID
        or event.query.user_id in Config.SUDO_USERS
    ):
        try:
            ls, path_ = (event.text).split(" ", 1)
            path = Path(path_) if path_ else os.getcwd()
        except Exception:
            ls = event.text
            path = os.getcwd()
        if "ls" in ls:
            print(ls)
            if not os.path.exists(path):
                return
            num = 1
            msg, buttons = get_manager(path, num)
            result = []
            result.append(
                await event.builder.article(
                    title="Inline FM",
                    description="Inline file manager",
                    thumb=get_thumb(
                        "https://telegra.ph/file/95412625a79efe853bf9a.png"
                    ),
                    text=msg,
                    buttons=buttons,
                )
            )
            await event.answer(result)
