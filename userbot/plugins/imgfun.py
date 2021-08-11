# by @mrconfused (@sandy1709)
import io
import os
from io import BytesIO

from PIL import Image, ImageFilter, ImageOps

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.functions import dotify
from ..helpers.utils import _cattools

plugin_category = "fun"


@catub.cat_cmd(
    pattern="imirror(s)? ?(-)?(l|r|u|b)?$",
    command=("imirror", plugin_category),
    info={
        "header": "gives to reflected  image of one part on other part.",
        "description": "Additionaly use along with cmd i.e, imirrors to gib out put as sticker.",
        "flags": {
            "-l": "Right half will be reflection of left half.",
            "-r": "Left half will be reflection of right half.",
            "-u": "bottom half will be reflection of upper half.",
            "-b": "upper half will be reflection of bottom half.",
        },
        "usage": [
            "{tr}imirror <flag> - gives output as image",
            "{tr}imirrors <flag> - gives output as sticker",
        ],
        "examples": [
            "{tr}imirror -l",
            "{tr}imirrors -u",
        ],
    },
)
async def imirror(event):  # sourcery no-metrics
    "imgae refelection fun."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(event, "__Reply to photo or sticker to make mirror.__")
    catevent = await event.edit("__Reflecting the image....__")
    args = event.pattern_match.group(1)
    if args:
        filename = "catuserbot.webp"
        f_format = "webp"
    else:
        filename = "catuserbot.jpg"
        f_format = "jpeg"
    try:
        imag = await _cattools.media_to_pic(catevent, reply, noedits=True)
        if imag[1] is None:
            return await edit_delete(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        image = Image.open(imag[1])
    except Exception as e:
        return await edit_delete(catevent, f"**Error in identifying image:**\n__{e}__")
    flag = event.pattern_match.group(3) or "r"
    w, h = image.size
    if w % 2 != 0 and flag in ["r", "l"] or h % 2 != 0 and flag in ["u", "b"]:
        image = image.resize((w + 1, h + 1))
        h, w = image.size
    if flag == "l":
        left = 0
        upper = 0
        right = w // 2
        lower = h
        nw = right
        nh = left
    elif flag == "r":
        left = w // 2
        upper = 0
        right = w
        lower = h
        nw = upper
        nh = upper
    elif flag == "u":
        left = 0
        upper = 0
        right = w
        lower = h // 2
        nw = left
        nh = lower
    elif flag == "b":
        left = 0
        upper = h // 2
        right = w
        lower = h
        nw = left
        nh = left
    temp = image.crop((left, upper, right, lower))
    temp = ImageOps.mirror(temp) if flag in ["l", "r"] else ImageOps.flip(temp)
    image.paste(temp, (nw, nh))
    img = BytesIO()
    img.name = filename
    image.save(img, f_format)
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await catevent.delete()


@catub.cat_cmd(
    pattern="irotate(?: |$)(\d+)$",
    command=("irotate", plugin_category),
    info={
        "header": "To rotate the replied image or sticker",
        "usage": [
            "{tr}irotate <angle>",
        ],
    },
)
async def irotate(event):
    "To convert replied image or sticker to gif"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(
            event, "__Reply to photo or sticker to rotate it with given angle.__"
        )
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edit_delete(
            event,
            "__Reply to photo or sticker to rotate it with given angle. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "__Rotating the replied media...__")
    imag = await _cattools.media_to_pic(catevent, reply, noedits=True)
    if imag[1] is None:
        return await edit_delete(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    image = Image.open(imag[1])
    try:
        image = image.rotate(int(args), expand=True)
    except Exception as e:
        return await edit_delete(event, "**Error**\n" + str(e))
    await event.delete()
    img = io.BytesIO()
    img.name = "CatUserbot.png"
    image.save(img, "PNG")
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await catevent.delete()


@catub.cat_cmd(
    pattern="iresize(?:\s|$)([\s\S]*)$",
    command=("iresize", plugin_category),
    info={
        "header": "To resize the replied image/sticker",
        "usage": [
            "{tr}iresize <dimension> will send square image of that dimension",
            "{tr}iresize <width> <height> will send square image of that dimension",
        ],
        "examples": ["{tr}iresize 250", "{tr}iresize 500 250"],
    },
)
async def iresize(event):
    "To resize the replied image/sticker"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(event, "__Reply to photo or sticker to resize it.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edit_delete(
            event,
            "__Reply to photo or sticker to resize it. Animated sticker is not supported__",
        )
    args = (event.pattern_match.group(1)).split()
    catevent = await edit_or_reply(event, "__Resizeing the replied media...__")
    imag = await _cattools.media_to_pic(catevent, reply, noedits=True)
    if imag[1] is None:
        return await edit_delete(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    image = Image.open(imag[1])
    w, h = image.size
    nw, nh = None, None
    if len(args) == 1:
        try:
            nw, nh = int(args[0]), int(args[0])
        except ValueError:
            return await edit_delete(catevent, "**Error:**\n__Invalid dimension.__")
    else:
        try:
            nw = int(args[0])
        except ValueError:
            return await edit_delete(catevent, "**Error:**\n__Invalid width.__")
        try:
            nh = int(args[1])
        except ValueError:
            return await edit_delete(catevent, "**Error:**\n__Invalid height.__")
    try:
        image = image.resize((nw, nh))
    except Exception as e:
        return await edit_delete(catevent, f"**Error:** __While resizing.\n{e}__")
    await event.delete()
    img = io.BytesIO()
    img.name = "CatUserbot.png"
    image.save(img, "PNG")
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await catevent.delete()


@catub.cat_cmd(
    pattern="square$",
    command=("square", plugin_category),
    info={
        "header": "Converts replied image to square image.",
        "usage": "{tr}square",
    },
)
async def square_cmd(event):
    "Converts replied image to square image."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo"]:
        return await edit_delete(event, "__Reply to photo to make it square image.__")
    catevent = await event.edit("__Adding borders to make it square....__")
    try:
        imag = await _cattools.media_to_pic(catevent, reply, noedits=True)
        if imag[1] is None:
            return await edit_delete(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        img = Image.open(imag[1])
    except Exception as e:
        return await edit_delete(catevent, f"**Error in identifying image:**\n__{e}__")
    w, h = img.size
    if w == h:
        return await edit_delete(event, "__The replied image is already in 1:1 ratio__")
    _min, _max = min(w, h), max(w, h)
    bg = img.crop(((w - _min) // 2, (h - _min) // 2, (w + _min) // 2, (h + _min) // 2))
    bg = bg.filter(ImageFilter.GaussianBlur(5))
    bg = bg.resize((_max, _max))
    bg.paste(img, ((_max - w) // 2, (_max - h) // 2))
    img = io.BytesIO()
    img.name = "img.jpg"
    bg.save(img)
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await catevent.delete()


@catub.cat_cmd(
    pattern="dotify(?: |$)(\d+)?$",
    command=("dotify", plugin_category),
    info={
        "header": "To convert image into doted image",
        "usage": [
            "{tr}dotify <number>",
        ],
    },
)
async def pic_gifcmd(event):
    "To convert image into doted image"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(
            event, "__Reply to photo or sticker to make it doted image.__"
        )
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edit_delete(
            event,
            "__Reply to photo or sticker to make it doted image. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    if args:
        if args.isdigit():
            pix = int(args) if int(args) > 0 else 100
    else:
        pix = 100
    catevent = await edit_or_reply(event, "__🎞Dotifying image...__")
    imag = await _cattools.media_to_pic(catevent, reply, noedits=True)
    if imag[1] is None:
        return await edit_delete(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    result = await dotify(imag[1], pix, True)
    await event.client.send_file(event.chat_id, result, reply_to=reply)
    await catevent.delete()
    for i in [imag[1]]:
        if os.path.exists(i):
            os.remove(i)
