"""
imported from nicegrill
modified by @mrconfused
QuotLy: Avaible commands: .qbot
"""

import io
import os
import re
import textwrap
from textwrap import wrap

import requests
from PIL import Image, ImageDraw, ImageFont
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.utils import get_display_name

from userbot import Convert, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import file_check, fontTest, media_type, process, soft_deEmojify
from ..helpers.utils import get_user_from_event, reply_id

plugin_category = "fun"


class Forward_Lock:
    def __init__(self, name):
        self.first_name = name
        self.last_name = None
        self.photo = None


def get_warp_length(width):
    return int((20.0 / 1024.0) * (width + 0.0))


@catub.cat_cmd(
    pattern="qpic(?:\s|$)([\s\S]*)",
    command=("qpic", plugin_category),
    info={
        "header": "Makes quote pic.",
        "flags": {
            "-b": "To get black and white output.",
            "-s": "To output file as sticker",
        },
        "usage": "{tr}qpic <flag> <input/reply to text msg>",
        "examples": ["{tr}qpic CatUserbot.", "{tr}qpic -b CatUserbot."],
    },
)
async def q_pic(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    args = event.pattern_match.group(1)
    black = re.findall(r"-b", args)
    sticker = re.findall(r"-s", args)
    args = args.replace("-b", "")
    args = args.replace("-s", "")
    input_str = args.strip()
    pfp = None
    reply_to = await reply_id(event)
    reply = await event.get_reply_message()
    if reply and input_str or not reply and input_str:
        text = input_str
    elif reply and reply.raw_text:
        text = reply.raw_text
    else:
        return await edit_delete(
            event, "__Provide input along with cmd or reply to text message.__"
        )
    text = soft_deEmojify(text)
    catevent = await edit_or_reply(event, "__Making Quote pic....__")
    file_check(re=False, me=False, mo=False, it=False)
    mediatype = await media_type(reply)
    if (
        (not reply)
        or (not mediatype)
        or (mediatype not in ["Photo", "Sticker"])
        or (
            mediatype == "Sticker"
            and reply.document.mime_type == "application/i-tgsticker"
        )
    ):
        user = reply.sender_id if reply else event.client.uid
        pfp = await event.client.download_profile_photo(user)
    else:
        imag = await Convert.to_image(
            event, reply, dirct="./temp", file="quotly.png", noedits=True
        )
        if imag[1] is None:
            return await edit_delete(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        user = event.client.uid
        pfp = imag[1]
    try:
        user = await event.client.get_entity(user)
    except Exception as e:
        LOGS.info(str(e))
        user = None
    if not pfp:
        pfp = "profilepic.jpg"
        with open(pfp, "wb") as f:
            f.write(
                requests.get(
                    "https://telegra.ph/file/1fd74fa4a4dbf1655f3ec.jpg"
                ).content
            )
    text = "\n".join(textwrap.wrap(text, 25))
    text = f"“{text}„"
    textf = (
        "./temp/ArialUnicodeMS.ttf" if await fontTest(text[0]) else "./temp/Quivira.otf"
    )
    textfont = ImageFont.truetype(textf, 50)
    img = Image.open(pfp)
    if black:
        img = img.convert("L")
    img = img.convert("RGBA").resize((1024, 1024))
    w, h = img.size
    nw, nh = 20 * (w // 100), 20 * (h // 100)
    nimg = Image.new("RGBA", (w - nw, h - nh), (0, 0, 0))
    nimg.putalpha(150)
    img.paste(nimg, (nw // 2, nh // 2), nimg)
    draw = ImageDraw.Draw(img)
    tw, th = draw.textsize(text=text, font=textfont)
    x, y = (w - tw) // 2, (h - th) // 2
    draw.text((x, y), text=text, font=textfont, fill="#ffffff", align="center")
    if user is not None:
        usrname = get_display_name(user)
        namef = (
            "./temp/ArialUnicodeMS.ttf"
            if await fontTest(usrname[0])
            else "./temp/Quivira.otf"
        )
        namefont = ImageFont.truetype(namef, 50)
        credit = "\n".join(wrap(f"by {usrname}", int(get_warp_length(w / 2.5))))
        tw, th = draw.textsize(text=credit, font=namefont)
        draw.text(
            ((w - nw + tw) // 1.6, (h - nh - th)),
            text=credit,
            font=namefont,
            fill="#ffffff",
            align="left",
        )
    output = io.BytesIO()
    if sticker:
        output.name = "CatUserbot.Webp"
        img.save(output, "webp")
    else:
        output.name = "CatUserbot.png"
        img.save(output, "PNG")
    output.seek(0)
    await event.client.send_file(event.chat_id, output, reply_to=reply_to)
    await catevent.delete()
    for i in [pfp]:
        if os.path.lexists(i):
            os.remove(i)


@catub.cat_cmd(
    pattern="(q|rq|fq|frq)(?:\s|$)([\s\S]*)",
    command=("q", plugin_category),
    info={
        "header": "Makes your message as sticker quote.",
        "flags": {
            "r": "use r infront of q to include the previous replied message",
            "f": "use f infront of q to create fake quote with given user",
        },
        "usage": [
            "{tr}q",
            "{tr}rq",
            "{tr}fq <user/reply> <text>",
            "{tr}frq <user/reply> <text>",
        ],
        "examples": ["{tr}fq @jisan7509 hello bad boys and girls"],
    },
)
async def stickerchat(catquotes):
    "Makes your message as sticker quote"
    reply = await catquotes.get_reply_message()
    cmd = catquotes.pattern_match.group(1)
    mediatype = None
    if cmd in ["rq", "q", "frq"]:
        if not reply:
            return await edit_or_reply(
                catquotes, "`I cant quote the message . reply to a message`"
            )
        fetchmsg = reply.message
        mediatype = await media_type(reply)
    if cmd == "rq":
        repliedreply = await reply.get_reply_message()
    elif cmd == "frq":
        repliedreply = reply
    else:
        repliedreply = None
    if mediatype and mediatype in ["Photo", "Round Video", "Gif"]:
        return await edit_or_reply(catquotes, "`Replied message is not supported now`")
    catevent = await edit_or_reply(catquotes, "`Making quote...`")
    if cmd in ["rq", "q"]:
        try:
            user = (
                await catquotes.client.get_entity(reply.forward.sender)
                if reply.fwd_from
                else reply.sender
            )
        except TypeError:
            user = Forward_Lock(reply.fwd_from.from_name)
    else:
        user, rank = await get_user_from_event(catquotes, secondgroup=True)
        if not user:
            return
        fetchmsg = rank
        if not fetchmsg and reply:
            fetchmsg = reply.message
        if not fetchmsg:
            return await edit_or_reply(
                catquotes, "`I cant quote the message . no text is given`"
            )
    res, catmsg = await process(
        fetchmsg, user, catquotes.client, reply, catquotes, repliedreply
    )
    if not res:
        return
    outfi = os.path.join("./temp", "sticker.png")
    catmsg.save(outfi)
    endfi = await Convert.to_sticker(
        catquotes, outfi, file="stickerchat.webp", noedits=True
    )
    await catquotes.client.send_file(catquotes.chat_id, endfi[1], reply_to=reply)
    await catevent.delete()
    os.remove(endfi[1])


@catub.cat_cmd(
    pattern="qbot(?:\s|$)([\s\S]*)",
    command=("qbot", plugin_category),
    info={
        "header": "Makes your message as sticker quote by @quotlybot",
        "usage": "{tr}qbot",
    },
)
async def _(event):
    "Makes your message as sticker quote by @quotlybot"
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    message = ""
    messages_id = []
    if reply:
        if input_str and input_str.isnumeric():
            messages_id.append(reply.id)
            async for message in event.client.iter_messages(
                event.chat_id,
                limit=(int(input_str) - 1),
                offset_id=reply.id,
                reverse=True,
            ):
                if message.id != event.id:
                    messages_id.append(message.id)
        elif input_str:
            message = input_str
        else:
            messages_id.append(reply.id)
    elif input_str:
        message = input_str
    else:
        return await edit_delete(
            event, "`Either reply to message or give input to function properly`"
        )
    chat = "@QuotLyBot"
    catevent = await edit_or_reply(event, "```Making a Quote```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            if messages_id != []:
                await event.client.forward_messages(chat, messages_id, event.chat_id)
            elif message != "":
                await event.client.send_message(conv.chat_id, message)
            else:
                return await edit_delete(
                    catevent, "`I guess you have used a invalid syntax`"
                )
            response = await response
        except YouBlockedUserError:
            return await catevent.edit("```Please unblock me (@QuotLyBot) u Nigga```")
        await event.client.send_read_acknowledge(conv.chat_id)
        await catevent.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_to
        )
