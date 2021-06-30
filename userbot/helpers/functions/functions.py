import os
import zipfile
from random import choice
from textwrap import wrap
from uuid import uuid4

import requests

from ..utils.extdl import install_pip

try:
    from imdb import IMDb
except ModuleNotFoundError:
    install_pip("IMDbPY")
    from imdb import IMDb

from PIL import Image, ImageColor, ImageDraw, ImageFont
from telethon.errors.rpcerrorlist import YouBlockedUserError

from ...Config import Config
from ...sql_helper.globals import gvarstatus
from ..resources.states import states

imdb = IMDb()

mov_titles = [
    "long imdb title",
    "long imdb canonical title",
    "smart long imdb canonical title",
    "smart canonical title",
    "canonical title",
    "localized title",
]


async def get_cast(casttype, movie):
    mov_casttype = ""
    if casttype in list(movie.keys()):
        i = 0
        for j in movie[casttype]:
            if i < 1:
                mov_casttype += str(j)
            elif i < 5:
                mov_casttype += ", " + str(j)
            else:
                break
            i += 1
    else:
        mov_casttype += "Not Data"
    return mov_casttype


async def get_moviecollections(movie):
    result = ""
    if "box office" in movie.keys():
        for i in movie["box office"].keys():
            result += f"\n•  <b>{i}:</b> <code>{movie['box office'][i]}</code>"
    else:
        result = "<code>No Data</code>"
    return result


def rand_key():
    return str(uuid4())[:8]


async def age_verification(event, reply_to_id):
    ALLOW_NSFW = gvarstatus("ALLOW_NSFW") or "False"
    if ALLOW_NSFW.lower() == "true":
        return False
    results = await event.client.inline_query(
        Config.TG_BOT_USERNAME, "age_verification_alert"
    )
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()
    return True


def reddit_thumb_link(preview, thumb=None):
    for i in preview:
        if "width=216" in i:
            thumb = i
            break
    if not thumb:
        thumb = preview.pop()
    return thumb.replace("\u0026", "&")


def higlighted_text(
    input_img,
    text,
    output_img,
    background="black",
    foreground="white",
    transparency=255,
    align="center",
    direction=None,
    text_wrap=2,
    font_name=None,
    font_size=60,
    linespace="+2",
    rad=20,
    position=(0, 0),
):
    templait = Image.open(input_img)
    # resize image
    source_img = templait.convert("RGBA").resize((1024, 1024))
    w, h = source_img.size
    if font_name is None:
        font_name = "userbot/helpers/styles/impact.ttf"
    font = ImageFont.truetype(font_name, font_size)
    ew, eh = position
    # get text size
    tw, th = font.getsize(text)
    width = 50 + ew
    hight = 30 + eh
    # wrap the text & save in a list
    mask_size = int((w / text_wrap) + 50)
    input_text = "\n".join(wrap(text, int((40.0 / w) * mask_size)))
    list_text = input_text.splitlines()
    # create image with correct size and black background
    if direction == "upwards":
        list_text.reverse()
        operator = "-"
        hight = h - (th + int(th / 1.2)) + eh
    else:
        operator = "+"
    for i, items in enumerate(list_text):
        x, y = (font.getsize(list_text[i])[0] + 50, int(th * 2 - (th / 2)))
        # align masks on the image....left,right & center
        if align == "right":
            width_align = "(mask_size-x)"
        if align == "left":
            width_align = "0"
        if align == "center":
            width_align = "((mask_size-x)/2)"
        clr = ImageColor.getcolor(background, "RGBA")
        if transparency == 0:
            mask_img = Image.new(
                "RGBA", (x, y), (clr[0], clr[1], clr[2], 0)
            )  # background
            mask_draw = ImageDraw.Draw(mask_img)
            mask_draw.text((25, 8), list_text[i], foreground, font=font)
        else:
            mask_img = Image.new(
                "RGBA", (x, y), (clr[0], clr[1], clr[2], transparency)
            )  # background
            # put text on mask
            mask_draw = ImageDraw.Draw(mask_img)
            mask_draw.text((25, 8), list_text[i], foreground, font=font)
            # remove corner (source- https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi)
            circle = Image.new("L", (rad * 2, rad * 2), 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, rad * 2, rad * 2), transparency)
            alpha = Image.new("L", mask_img.size, transparency)
            mw, mh = mask_img.size
            alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
            alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, mh - rad))
            alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (mw - rad, 0))
            alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (mw - rad, mh - rad))
            mask_img.putalpha(alpha)
        # put mask_img on source image & trans remove the corner white
        trans = Image.new("RGBA", source_img.size)
        trans.paste(
            mask_img,
            (
                (int(width) + int(eval(f"{width_align}"))),
                (eval(f"{hight} {operator}({y*i}+({int(linespace)*i}))")),
            ),
        )
        source_img = Image.alpha_composite(source_img, trans)
    source_img.save(output_img, "png")


async def clippy(borg, msg, chat_id, reply_to_id):
    chat = "@clippy"
    async with borg.conversation(chat) as conv:
        try:
            msg = await conv.send_file(msg)
            pic = await conv.get_response()
            await borg.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kakashi.edit("Please unblock @clippy and try again")
            return
        await borg.send_file(
            chat_id,
            pic,
            reply_to=reply_to_id,
        )
    await borg.delete_messages(conv.chat_id, [msg.id, pic.id])


# https://www.tutorialspoint.com/How-do-you-split-a-list-into-evenly-sized-chunks-in-Python
def sublists(input_list: list, width: int = 3):
    return [input_list[x : x + width] for x in range(0, len(input_list), width)]


async def sanga_seperator(sanga_list):
    for i in sanga_list:
        if i.startswith("🔗"):
            sanga_list.remove(i)
    s = 0
    for i in sanga_list:
        if i.startswith("Username History"):
            break
        s += 1
    usernames = sanga_list[s:]
    names = sanga_list[:s]
    return names, usernames


# unziping file
async def unzip(downloaded_file_name):
    with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
        zip_ref.extractall("./temp")
    downloaded_file_name = os.path.splitext(downloaded_file_name)[0]
    return f"{downloaded_file_name}.gif"


# covid india data


async def covidindia(state):
    url = "https://www.mohfw.gov.in/data/datanew.json"
    req = requests.get(url).json()
    for i in states:
        if i == state:
            return req[states.index(i)]
    return None


async def hide_inlinebot(borg, bot_name, text, chat_id, reply_to_id, c_lick=0):
    sticcers = await borg.inline_query(bot_name, f"{text}.")
    cat = await sticcers[c_lick].click("me", hide_via=True)
    if cat:
        await borg.send_file(int(chat_id), cat, reply_to=reply_to_id)
        await cat.delete()


# for stickertxt
async def waifutxt(text, chat_id, reply_to_id, bot):
    animus = [
        0,
        1,
        2,
        3,
        4,
        9,
        15,
        20,
        22,
        27,
        29,
        32,
        33,
        34,
        37,
        38,
        41,
        42,
        44,
        45,
        47,
        48,
        51,
        52,
        53,
        55,
        56,
        57,
        58,
        61,
        62,
        63,
    ]
    sticcers = await bot.inline_query("stickerizerbot", f"#{choice(animus)}{text}")
    cat = await sticcers[0].click("me", hide_via=True)
    if cat:
        await bot.send_file(int(chat_id), cat, reply_to=reply_to_id)
        await cat.delete()
