"""
by  @sandy1709 ( https://t.me/mrconfused  )
"""
# songs finder for catuserbot

import os
from pathlib import Path

import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import (
    ALIVE_NAME,
    CMD_HELP,
    name_dl,
    runcmd,
    song_dl,
    thumb_dl,
    video_dl,
    yt_search,
)

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USERNAME = str(Config.LIVE_USERNAME) if Config.LIVE_USERNAME else "@Jisan7509"


@bot.on(admin_cmd(pattern="(song|song320)($| (.*))"))
@bot.on(sudo_cmd(pattern="(song|song320)($| (.*))", allow_sudo=True))
async def _(event):
    reply_to_id = None
    if event.from_id != bot.uid:
        reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        await edit_or_reply(event, "`What I am Supposed to find `")
        return
    cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    cmd = event.pattern_match.group(1)
    if cmd == "song":
        q = "128k"
    elif cmd == "song320":
        q = "320k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    stderr = (await runcmd(song_cmd))[1]
    if stderr:
        return await catevent.edit(f"**Error :** `{stderr}`")
    catname, stderr = (await runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**Error :** `{stderr}`")
    stderr = (await runcmd(thumb_cmd))[1]
    catname = os.path.splitext(catname)[0]
    if stderr:
        return await catevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{catname}.mp3")
    if not os.path.exists(song_file):
        return await catevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await catevent.edit("`yeah..! i found something wi8..🥰`")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None

    await borg.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"➥ __**Song :- {query}**__\n__**➥ Uploaded by :-**__ [{DEFAULTUSER}]({USERNAME})",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="vsong( (.*)|$)"))
@bot.on(sudo_cmd(pattern="vsong( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = None
    if event.from_id != bot.uid:
        reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await edit_or_reply(event, "What I am Supposed to find")
        return
    cat = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await runcmd(video_cmd))[1]
    if stderr:
        return await catevent.edit(f"**Error :** `{stderr}`")
    catname, stderr = (await runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**Error :** `{stderr}`")
    stderr = (await runcmd(thumb_cmd))[1]
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    if stderr:
        return await catevent.edit(f"**Error :** `{stderr}`")
    catname = os.path.splitext(catname)[0]
    vsong_file = Path(f"{catname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await catevent.edit("`yeah..! i found something wi8..🥰`")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    await borg.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=f"➥ __**Song :- {query}**__\n__**➥ Uploaded by :-**__ [{DEFAULTUSER}]({USERNAME})",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "getsongs": "__**PLUGIN NAME :** Get Songs__\
        \n\n📌** CMD ➥** `.song` <query> or `.song reply to song name`\
        \n**USAGE   ➥  **Searches the song you entered in query and sends it quality of it is 128k\
        \n\n📌** CMD ➥** `.song320` <query> or `.song320 reply to song name`\
        \n**USAGE   ➥  **Searches the song you entered in query and sends it quality of it is 320k\
        \n\n📌** CMD ➥** .vsong` <query> or `.vsong reply to song name`\
        \n**USAGE   ➥  **Searches the video song you entered in query and sends it"
    }
)
