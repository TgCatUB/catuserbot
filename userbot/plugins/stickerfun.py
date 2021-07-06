# Random RGB Sticklet by @PhycoNinja13b
# modified by @UniBorg
# imported from ppe-remix by @heyworld & @DeletedUser420
# modified by @mrconfused


# RegEx by https://t.me/c/1220993104/500653 ( @SnapDragon7410 )
import io
import os
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.functions import deEmojify, hide_inlinebot, waifutxt
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
    pattern="sttxt(?:\s|$)([\s\S]*)",
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
    pattern="doge(?:\s|$)([\s\S]*)",
    command=("doge", plugin_category),
    info={
        "header": "Make doge say anything.",
        "usage": "{tr}doge <text/reply to msg>",
        "examples": "{tr}doge Gib money",
    },
)
async def doge(event):
    "Make a cool doge text sticker"
    text = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    bot_name = "@DogeStickerBot"
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edit_delete(
                event, "__What is doge supposed to say? Give some text.__"
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
