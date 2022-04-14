# Random RGB Sticklet by @PhycoNinja13b
# modified by @UniBorg
# imported from ppe-remix by @heyworld & @DeletedUser420
# modified by @mrconfused


# RegEx by https://t.me/c/1220993104/500653 ( @SnapDragon7410 )
import io
import os
import random
import textwrap
import urllib

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import (
    clippy,
    convert_tosticker,
    deEmojify,
    hide_inlinebot,
    higlighted_text,
    waifutxt,
)
from ..helpers.utils import reply_id

plugin_category = "fun"


async def get_font_file(client, channel_id, search_kw=""):
    # first get the font messages
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        # this might cause FLOOD WAIT,
        # if used too many times
        limit=None,
        search=search_kw,
    )
    # get a random font from the list of fonts
    # https://docs.python.org/3/library/random.html#random.choice
    font_file_message = random.choice(font_file_message_s)
    # download and return the file path
    return await client.download_media(font_file_message)


@catub.cat_cmd(
    pattern="(?:st|sttxt)(?:\s|$)([\s\S]*)",
    command=("sttxt", plugin_category),
    info={
        "header": "Anime that makes your writing fun.",
        "usage": "{tr}sttxt <text>",
        "examples": "{tr}sttxt hello",
    },
)
async def waifu(animu):
    "Anime that makes your writing fun"
    text = animu.pattern_match.group(1)
    reply_to_id = await reply_id(animu)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            return await edit_or_reply(
                animu, "`You haven't written any article, Waifu is going away.`"
            )
    text = deEmojify(text)
    await animu.delete()
    await waifutxt(text, animu.chat_id, reply_to_id, animu.client)


# 12 21 28 30
@catub.cat_cmd(
    pattern="stcr ?(?:(.*?) ?; )?([\s\S]*)",
    command=("stcr", plugin_category),
    info={
        "header": "your text as sticker.",
        "usage": [
            "{tr}stcr <text>",
            "{tr}stcr <font file name> ; <text>",
        ],
        "examples": "{tr}stcr hello",
    },
)
async def sticklet(event):
    "your text as sticker"
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    reply_to_id = await reply_id(event)
    # get the input text
    # the text on which we would like to do the magic on
    font_file_name = event.pattern_match.group(1)
    if not font_file_name:
        font_file_name = ""
    sticktext = event.pattern_match.group(2)
    reply_message = await event.get_reply_message()
    if not sticktext:
        if event.reply_to_msg_id:
            sticktext = reply_message.message
        else:
            return await edit_or_reply(event, "need something, hmm")
    # delete the userbot command,
    # i don't know why this is required
    await event.delete()
    sticktext = deEmojify(sticktext)
    # https://docs.python.org/3/library/textwrap.html#textwrap.wrap
    sticktext = textwrap.wrap(sticktext, width=10)
    # converts back the list to a string
    sticktext = "\n".join(sticktext)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    FONT_FILE = await get_font_file(event.client, "@catfonts", font_file_name)
    font = ImageFont.truetype(FONT_FILE, size=fontsize)
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)
    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )
    image_stream = io.BytesIO()
    image_stream.name = "catuserbot.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    # finally, reply the sticker
    await event.client.send_file(
        event.chat_id,
        image_stream,
        caption="cat's Sticklet",
        reply_to=reply_to_id,
    )
    # cleanup
    try:
        os.remove(FONT_FILE)
    except BaseException:
        pass


@catub.cat_cmd(
    pattern="honk(?:\s|$)([\s\S]*)",
    command=("honk", plugin_category),
    info={
        "header": "Make honk say anything.",
        "usage": "{tr}honk <text/reply to msg>",
        "examples": "{tr}honk How you doing?",
    },
)
async def honk(event):
    "Make honk say anything."
    text = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    bot_name = "@honka_says_bot"
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edit_delete(
                event, "__What is honk supposed to say? Give some text.__"
            )
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(event.client, bot_name, text, event.chat_id, reply_to_id)


@catub.cat_cmd(
    pattern="twt(?:\s|$)([\s\S]*)",
    command=("twt", plugin_category),
    info={
        "header": "Make a cool tweet of your account",
        "usage": "{tr}twt <text/reply to msg>",
        "examples": "{tr}twt Catuserbot",
    },
)
async def twt(event):
    "Make a cool tweet of your account."
    text = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    bot_name = "@TwitterStatusBot"
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edit_delete(
                event, "__What am I supposed to Tweet? Give some text.__"
            )
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(event.client, bot_name, text, event.chat_id, reply_to_id)


@catub.cat_cmd(
    pattern="glax(|r)(?:\s|$)([\s\S]*)",
    command=("glax", plugin_category),
    info={
        "header": "Make glax the dragon scream your text.",
        "flags": {
            "r": "Reverse the face of the dragon",
        },
        "usage": [
            "{tr}glax <text/reply to msg>",
            "{tr}glaxr <text/reply to msg>",
        ],
        "examples": [
            "{tr}glax Die you",
            "{tr}glaxr Die you",
        ],
    },
)
async def glax(event):
    "Make glax the dragon scream your text."
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    bot_name = "@GlaxScremBot"
    c_lick = 1 if cmd == "r" else 0
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edit_delete(
                event, "What is glax supposed to scream? Give text.."
            )
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(
        event.client, bot_name, text, event.chat_id, reply_to_id, c_lick=c_lick
    )


@catub.cat_cmd(
    pattern="(|b)quby(?:\s|$)([\s\S]*)",
    command=("quby", plugin_category),
    info={
        "header": "Make doge say anything.",
        "flags": {
            "b": "Give the sticker on background.",
        },
        "usage": [
            "{tr}quby <text/reply to msg>",
            "{tr}bquby <text/reply to msg>",
        ],
        "examples": [
            "{tr}quby Gib money",
            "{tr}bquby Gib money",
        ],
    },
)
async def quby(event):
    "Make a cool quby text sticker"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edit_delete(
            event, "__What is quby supposed to say? Give some text.__"
        )
    await edit_delete(event, "`Wait, processing.....`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    temp_name = "./temp/quby_temp.png"
    file_name = "./temp/quby.png"
    templait = urllib.request.urlretrieve(
        "https://telegra.ph/file/09f4df5a129758a2e1c9c.jpg", temp_name
    )
    if len(text) < 40:
        font = 80
        wrap = 1.4
        position = (100, 0)
    else:
        font = 60
        wrap = 1.2
        position = (0, 0)
    text = deEmojify(text)
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace="+4",
        position=position,
    )
    if cmd == "b":
        cat = convert_tosticker(file_name)
        await event.client.send_file(
            event.chat_id, cat, reply_to=reply_to_id, force_document=False
        )
    else:
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await event.delete()
    for files in (temp_name, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="(|b)blob(?:\s|$)([\s\S]*)",
    command=("blob", plugin_category),
    info={
        "header": "Give the sticker on background.",
        "flags": {
            "b": "To create knife sticker transparent.",
        },
        "usage": [
            "{tr}blob <text/reply to msg>",
            "{tr}bblob <text/reply to msg>",
        ],
        "examples": [
            "{tr}blob Gib money",
            "{tr}bblob Gib money",
        ],
    },
)
async def knife(event):
    "Make a blob knife text sticker"
    cmd = event.pattern_match.group(1).lower
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edit_delete(
            event, "__What is knife supposed to say? Give some text.__"
        )
    await edit_delete(event, "`Wait, processing.....`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    temp_name = "./temp/knife_temp.png"
    file_name = "./temp/knife.png"
    templait = urllib.request.urlretrieve(
        "https://telegra.ph/file/2188367c8c5f43c36aa59.jpg", temp_name
    )
    if len(text) < 50:
        font = 90
        wrap = 2
        position = (250, -450)
    else:
        font = 60
        wrap = 1.4
        position = (150, 500)
    text = deEmojify(text)
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace="-5",
        position=position,
        direction="upwards",
    )
    if cmd == "b":
        cat = convert_tosticker(file_name)
        await event.client.send_file(
            event.chat_id, cat, reply_to=reply_to_id, force_document=False
        )
    else:
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await event.delete()
    for files in (temp_name, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="(|h)doge(?:\s|$)([\s\S]*)",
    command=("doge", plugin_category),
    info={
        "header": "Make doge say anything.",
        "flags": {
            "h": "To create doge sticker with highligted text.",
        },
        "usage": [
            "{tr}doge <text/reply to msg>",
            "{tr}tdoge <text/reply to msg>",
        ],
        "examples": [
            "{tr}doge Gib money",
            "{tr}hdoge Gib money",
        ],
    },
)
async def doge(event):
    "Make a cool doge text sticker"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edit_delete(
            event, "__What is doge supposed to say? Give some text.__"
        )
    await edit_delete(event, "`Wait, processing.....`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    temp_name = "./temp/doge_temp.jpg"
    file_name = "./temp/doge.jpg"
    templait = urllib.request.urlretrieve(
        "https://telegra.ph/file/6f621b9782d9c925bd6c4.jpg", temp_name
    )
    text = deEmojify(text)
    font, wrap = (90, 2) if len(text) < 90 else (70, 2.5)
    bg, fg, alpha, ls = (
        ("black", "white", 255, "5") if cmd == "h" else ("white", "black", 0, "-40")
    )
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace=ls,
        position=(0, 10),
        align="left",
        background=bg,
        foreground=fg,
        transparency=alpha,
    )
    cat = convert_tosticker(file_name)
    await event.client.send_file(
        event.chat_id, cat, reply_to=reply_to_id, force_document=False
    )
    await event.delete()
    for files in (temp_name, file_name):
        if files and os.path.exists(files):
            os.remove(files)
