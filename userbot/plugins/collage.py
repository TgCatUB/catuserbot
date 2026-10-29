import math
import os
import shlex

from userbot import Convert, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _catutils, meme_type, reply_id

plugin_category = "utils"


@catub.cat_cmd(
    pattern=r"collage(?:\s|$)([\s\S]*)",
    command=("collage", plugin_category),
    info={
        "header": "To create collage from still images extracted from video/gif.",
        "description": "Shows you the grid image of images extracted from video/gif. you can customize the Grid size by giving integer between 1 to 9 to cmd by default it is 3",
        "usage": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "To create collage from still images extracted from video/gif."
    catinput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    catid = await reply_id(event)
    if not (reply and (reply.media)):
        return await edit_delete(event, "`Reply to a media file..`")
    mediacheck = await meme_type(reply)
    if mediacheck not in [
        "Round Video",
        "Gif",
        "Video Sticker",
        "Animated Sticker",
        "Video",
    ]:
        return await edit_delete(event, "`The replied message media type is not supported.`")
    if catinput:
        if not catinput.isdigit():
            return await edit_delete(event, "`You input is invalid, check help`")

        catinput = int(catinput)
        if not 0 < catinput < 10:
            await edit_or_reply(
                event,
                "__Why big grid you cant see images, use size of grid between 1 to 9\nAnyways changing value to max 9__",
            )
            catinput = 9
    else:
        catinput = 3
    await edit_or_reply(event, "```Collaging this may take several minutes..... 😁```")
    if mediacheck in ["Round Video", "Gif", "Video Sticker", "Video"]:
        if not os.path.isdir("./temp/"):
            os.mkdir("./temp/")
        catsticker = await reply.download_media(file="./temp/")
        collagefile = catsticker
    else:
        collage_file = await Convert.to_gif(event, reply, file="collage.mp4", noedits=True)
        collagefile = collage_file[1]
    if not collagefile:
        return await edit_or_reply(event, "**Error:-** __Unable to process the replied media__")
    endfile = "./temp/collage.png"
    probe_cmd = shlex.join(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            collagefile,
        ]
    )
    duration_text, _, probe_status, _ = await _catutils.runcmd(probe_cmd)
    try:
        duration = float(duration_text)
    except ValueError:
        duration = 0
    if probe_status or not math.isfinite(duration) or duration <= 0:
        if os.path.exists(collagefile):
            os.remove(collagefile)
        return await edit_delete(event, "`Media is not supported, or try with smaller grid size`")

    frame_count = catinput * catinput
    frame_rate = frame_count / duration
    filters = (
        f"fps={frame_rate:.8f},"
        "scale=320:180:force_original_aspect_ratio=decrease,"
        "pad=320:180:(ow-iw)/2:(oh-ih)/2,"
        f"tile={catinput}x{catinput}:nb_frames={frame_count}:padding=8:margin=8:color=black"
    )
    ffmpeg_cmd = shlex.join(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            collagefile,
            "-vf",
            filters,
            "-frames:v",
            "1",
            "-y",
            endfile,
        ]
    )
    _, _, ffmpeg_status, _ = await _catutils.runcmd(ffmpeg_cmd)
    if ffmpeg_status or not os.path.exists(endfile):
        if os.path.exists(collagefile):
            os.remove(collagefile)
        return await edit_delete(event, "`Media is not supported, or try with smaller grid size`")
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=catid,
    )
    await event.delete()
    for files in (collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)
