import contextlib
import json

from .utils.utils import runcmd


def meme_type(message):
    if message:
        if message.photo:
            return "Photo"
        if message.audio:
            return "Audio"
        if message.voice:
            return "Voice"
        if message.video_note:
            return "Round Video"
        if message.gif:
            return "Gif"
        if message.sticker:
            mime = message.document.mime_type
            if mime == "application/x-tgsticker":
                return "Animated Sticker"
            if mime == "video/webm":
                return "Video Sticker"
            return "Static Sticker"
        if message.video:
            return "Video"
        if message.document:
            mime = message.document.mime_type
            if mime != "image/gif" and mime.split("/")[0] == "image":
                return "Photo"
            if mime == "image/gif":
                return "Gif"
            if mime.split("/")[0] == "video":
                return "Video"
            return "Document"
    return None


def media_type(message):
    if message:
        if message.photo:
            return "Photo"
        if message.audio:
            return "Audio"
        if message.voice:
            return "Voice"
        if message.video_note:
            return "Round Video"
        if message.gif:
            return "Gif"
        if message.sticker:
            return "Sticker"
        if message.video:
            return "Video"
        if message.document:
            return "Document"
    return None


async def fileinfo(file):
    x, y, z, s = await runcmd(f"mediainfo '{file}' --Output=JSON")
    cat_json = json.loads(x)["media"]["track"]
    dic = {
        "path": file,
        "size": int(cat_json[0]["FileSize"]),
        "extension": cat_json[0]["FileExtension"],
    }
    with contextlib.suppress(IndexError, KeyError):
        dic["format"] = cat_json[0]["Format"]
        dic["type"] = cat_json[1]["@type"]
        if "ImageCount" not in cat_json[0]:
            dic["duration"] = int(float(cat_json[0]["Duration"]))
            dic["bitrate"] = int(cat_json[0]["OverallBitRate"]) // 1000
        dic["height"] = int(cat_json[1]["Height"])
        dic["width"] = int(cat_json[1]["Width"])
    return dic
