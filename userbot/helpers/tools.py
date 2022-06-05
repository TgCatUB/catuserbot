import contextlib
import json
import os

from .utils.utils import runcmd


async def meme_type(message):
    if message:
        try:
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
                if mime == "application/x-tgsticker":
                    return "Animated Sticker"
                return "Document"
        except AttributeError:
            return await file_type(message)
    return None


async def media_type(message):
    if message:
        try:
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
        except AttributeError:
            media = await file_type(message)
            if media and media in [
                "Video Sticker",
                "Animated Sticker",
                "Static Sticker",
            ]:
                return "Sticker"
            return media
    return None


async def fileinfo(file):
    x, y, z, s = await runcmd(f"mediainfo '{file}' --Output=JSON")
    cat_json = json.loads(x)["media"]["track"]
    dic = {
        "path": file,
        "size": int(cat_json[0]["FileSize"]),
        "extension": cat_json[0]["FileExtension"],
        "type": "None",
        "format": "None",
        "audio": "None",
    }
    with contextlib.suppress(IndexError, KeyError):
        dic["format"] = cat_json[0]["Format"]
        dic["type"] = cat_json[1]["@type"]
        if "ImageCount" not in cat_json[0]:
            dic["duration"] = int(float(cat_json[0]["Duration"]))
            dic["bitrate"] = int(cat_json[0]["OverallBitRate"]) // 1000
        dic["height"] = int(cat_json[1]["Height"])
        dic["width"] = int(cat_json[1]["Width"])
        dic["audio"] = "Present" if cat_json[0]["AudioCount"] else "None"
    return dic


async def file_type(message):
    if not os.path.exists(message):
        return None
    media = await fileinfo(message)
    if media["type"] == "Image":
        if media["format"] == "GIF":
            return "Gif"
        if media["format"] == "WebP":
            return "Static Sticker"
        return "Photo"
    elif media["type"] == "Video":
        if media["audio"] == "None":
            return "Video Sticker" if media["format"] == "WebM" else "Gif"
        return "Video"
    elif media["type"] == "Audio":
        return "Voice" if media["format"] == "Ogg" else "Audio"
    elif media["extension"] == "tgs":
        return "Animated Sticker"
    return "Document"
