"""
Created by @Jisan7509
#catuserbot
"""

import os
import random
import re
from io import BytesIO

import PIL
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from telegraph import upload_file

from userbot import Convert, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import clippy
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import hmention, reply_id

# ======================================================================================================================================================================================

vars_list = {
    "lbg": "LOGO_BACKGROUND",
    "lfc": "LOGO_FONT_COLOR",
    "lfs": "LOGO_FONT_SIZE",
    "lfh": "LOGO_FONT_HEIGHT",
    "lfw": "LOGO_FONT_WIDTH",
    "lfsw": "LOGO_FONT_STROKE_WIDTH",
    "lfsc": "LOGO_FONT_STROKE_COLOR",
    "lf": "LOGO_FONT",
}

rand_bg = ["total random", "anime", "frame", "mcu/dcu", "neon"]
# ======================================================================================================================================================================================

plugin_category = "extra"


def random_checker(Font, Color, Background):
    if Font == "Random":
        return True
    if Color == "Random":
        return True
    if Background in rand_bg:
        return True
    return False


def random_loader(Font, Color, Background, collection):
    bg = []
    if Font == "Random":
        Font = random.choice(collection["fonts"])
    if Color == "Random":
        Color = random.choice(collection["colors"])
    if Background in rand_bg:
        if Background == "total random":
            for i in collection["backgronds"]:
                bg += collection["backgronds"][i]
            Background = random.choice(bg)
        else:
            Background = random.choice(collection["backgronds"][Background])
    return Font, Color, Background


@catub.cat_cmd(
    pattern="(|f|s)logo(?: |$)([\s\S]*)",
    command=("logo", plugin_category),
    info={
        "header": "Make a logo in image or sticker",
        "description": "Just a fun purpose plugin to create logo in image or in sticker.",
        "flags": {
            "s": "To create a logo in sticker instade of image.",
            "f": "To create a logo image and send as documnent",
        },
        "note": "To create multiple logo at once you can use count value from 1 to 7.\nThis only work if any random option is selected.",
        "usage": [
            "{tr}logo <text/reply>",
            "{tr}logo count ; <text/reply>",
            "{tr}flogo <text/reply>",
            "{tr}flogo count ; <text/reply>",
            "{tr}slogo <text/reply>",
        ],
        "examples": [
            "{tr}logo CatUserbot",
            "{tr}logo 10;CatUserbot",
            "{tr}flogo CatUserBot",
            "{tr}flogo 5; CatUserbot",
            "{tr}slogo CatUserBot",
        ],
    },
)
async def very(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "To create a logo"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    if text and ";" in text:
        count, text = text.split(";")
    else:
        count = 1
    count = min(int(count), 7)
    reply = await event.get_reply_message()
    if not text and reply:
        text = reply.text
    if not text:
        return await edit_delete(event, "**ಠ∀ಠ Gimmi text to make logo**")
    catevent = await edit_or_reply(event, "Processing...")
    reply_to_id = await reply_id(event)
    LOGO_FONT_SIZE = gvarstatus("LOGO_FONT_SIZE") or 200
    LOGO_FONT_WIDTH = gvarstatus("LOGO_FONT_WIDTH") or 2
    LOGO_FONT_HEIGHT = gvarstatus("LOGO_FONT_HEIGHT") or 2
    LOGO_FONT_COLOR = loader1 = gvarstatus("LOGO_FONT_COLOR") or "red"
    LOGO_FONT_STROKE_WIDTH = gvarstatus("LOGO_FONT_STROKE_WIDTH") or 0
    LOGO_FONT_STROKE_COLOR = gvarstatus("LOGO_FONT_STROKE_COLOR") or None
    LOGO_BACKGROUND = loader2 = (
        gvarstatus("LOGO_BACKGROUND")
        or "https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Logo/Background/black.jpg"
    )
    LOGO_FONT = loader3 = (
        gvarstatus("LOGO_FONT")
        or "https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Logo/Fonts/Streamster.ttf?raw=true"
    )
    rcheck = random_checker(LOGO_FONT, LOGO_FONT_COLOR, LOGO_BACKGROUND)
    if rcheck:
        rjson = requests.get(
            "https://raw.githubusercontent.com/TgCatUB/CatUserbot-Resources/master/Resources/Logo/resources.txt"
        ).json()
    if count > 1 and not rcheck:
        count = 1
        catevent = await edit_or_reply(
            event, "Not using random value,Changing limit to 1.."
        )
    output = []
    captionlist = []
    for i in range(count):
        if rcheck:
            LOGO_FONT, LOGO_FONT_COLOR, LOGO_BACKGROUND = random_loader(
                LOGO_FONT, LOGO_FONT_COLOR, LOGO_BACKGROUND, rjson
            )
        try:
            template = requests.get(LOGO_BACKGROUND)
            temp_img = Image.open(BytesIO(template.content))
        except Exception as e:
            await edit_or_reply(catevent, f"**Bad Url:** {LOGO_BACKGROUND}\n\n{e}")
        raw_width, raw_height = temp_img.size
        resized_width, resized_height = (
            (1024, int(1024 * raw_height / raw_width))
            if raw_width > raw_height
            else (int(1024 * raw_width / raw_height), 1024)
        )
        img = temp_img.convert("RGBA").resize((resized_width, resized_height))
        draw = ImageDraw.Draw(img)
        logo = requests.get(LOGO_FONT)
        fontsize = int(LOGO_FONT_SIZE)
        font = ImageFont.truetype(BytesIO(logo.content), fontsize)
        while font.getsize(max(text.splitlines(), key=len))[0] > 0.70 * resized_width:
            fontsize -= 1
            font = ImageFont.truetype(BytesIO(logo.content), fontsize)
        image_widthz, image_heightz = img.size
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        try:
            draw.text(
                (
                    (image_widthz - w) / float(LOGO_FONT_WIDTH),
                    (image_heightz - h) / float(LOGO_FONT_HEIGHT),
                ),
                text,
                font=font,
                fill=LOGO_FONT_COLOR,
                stroke_width=int(LOGO_FONT_STROKE_WIDTH),
                stroke_fill=LOGO_FONT_STROKE_COLOR,
            )
        except OSError:
            draw.text(
                (
                    (image_widthz - w) / float(LOGO_FONT_WIDTH),
                    (image_heightz - h) / float(LOGO_FONT_HEIGHT),
                ),
                text,
                font=font,
                fill=LOGO_FONT_COLOR,
                stroke_width=0,
                stroke_fill=None,
            )
        file_name = f"badcat{i}.png"
        img.save(file_name, "png")
        output.append(file_name)
        captionlist.append("")
        LOGO_FONT_COLOR, LOGO_BACKGROUND, LOGO_FONT = loader1, loader2, loader3
    captionlist[-1] = f"<b><i>➥ Logo generated by :- {hmention}</i></b>"
    if cmd == "":
        await event.client.send_file(
            event.chat_id,
            output,
            reply_to=reply_to_id,
        )
    elif cmd == "f":
        await event.client.send_file(
            event.chat_id,
            output,
            caption=captionlist,
            reply_to=reply_to_id,
            force_document=True,
            parse_mode="html",
        )
    else:
        await clippy(event.client, output[0], event.chat_id, reply_to_id)
    await catevent.delete()
    for i in output:
        os.remove(i)


@catub.cat_cmd(
    pattern="(|c)lbg(?:\s|$)([\s\S]*)",
    command=("lbg", plugin_category),
    info={
        "header": "Change the background of logo",
        "description": "To change the background on which logo will created, in **bg** there few built-in backgrounds.",
        "flags": {
            "c": "Custom background for logo, can set by giving a telegraph link or reply to media.",
        },
        "usage": [
            "{tr}lbg <background color code>",
            "{tr}clbg <telegraph link / reply to media>",
        ],
        "examples": [
            "{tr}lbg red",
            "{tr}clbg https://telegra.ph/blablabla.jpg",
        ],
    },
)
async def bad(event):
    "To change background of logo"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    bg_name = ["black", "blue", "purple", "red", "white"] + rand_bg
    if cmd == "c":
        reply_message = await event.get_reply_message()
        if not input_str and event.reply_to_msg_id and reply_message.media:
            output = await Convert.to_image(
                event, reply_message, dirct="./temp", file="lbg.png", noedits=True
            )
            myphoto_urls = upload_file(output[1])
            input_str = f"https://telegra.ph{myphoto_urls[0]}"
            os.remove(output[1])
        if not input_str.startswith("https://t"):
            return await edit_delete(
                event, "Give a valid Telegraph picture link, Or reply to a media."
            )
        addgvar("LOGO_BACKGROUND", input_str)
        return await edit_delete(
            event, f"**Background for logo changed to :-** `{input_str}`"
        )
    if not input_str or input_str not in bg_name:
        lbg_list = "**Available background names are here:-**\n\n**1.** `black`\n**2.** `blue`\n**3.** `purple`\n**4.** `red`\n**5.** `white`\n\n**Random Backgrounds:**\n**1.** `total random`\n**2.** `anime`\n**3.** `frame`\n**4.** `mcu/dcu`\n**5.** `neon`\n"
        return await edit_delete(event, lbg_list, 60)
    string = (
        input_str
        if input_str in rand_bg
        else f"https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Logo/Background/{input_str}.jpg"
    )
    addgvar("LOGO_BACKGROUND", string)
    await edit_delete(event, f"**Background for logo changed to :-** `{input_str}`", 10)


@catub.cat_cmd(
    pattern="lf(|c|s|h|w|sc|sw)(?:\s|$)([\s\S]*)",
    command=("lf", plugin_category),
    info={
        "header": "Change text style for logo.",
        "description": "Customise logo font, font size, font position like text hight or width.",
        "flags": {
            "c": "To change color of logo font.",
            "s": "To change size of logo font.",
            "h": "To change hight of logo font.",
            "w": "To change width of logo font.",
            "sw": "To change stroke width of logo font.",
            "sc": "To change stroke color of logo font.",
        },
        "usage": [
            "{tr}lf <font name>",
            "{tr}lfc <logo font color>",
            "{tr}lfs <1-1000>",
            "{tr}lfh <10-100>",
            "{tr}lfw <10-100>",
            "{tr}lfsw <10-100>",
            "{tr}lfsc <logo font stroke color>",
        ],
        "examples": [
            "{tr}lf genau-font.ttf",
            "{tr}lfc white",
            "{tr}lfs 120",
            "{tr}lfh 1",
            "{tr}lfw 8",
            "{tr}lfsw 5",
            "{tr}lfsc white",
        ],
    },
)
async def pussy(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "To customise logo font"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    if cmd == "":
        source = requests.get(
            "https://github.com/TgCatUB/CatUserbot-Resources/tree/master/Resources/Logo/Fonts"
        )
        soup = BeautifulSoup(source.text, features="html.parser")
        links = soup.find_all("a", class_="js-navigation-open Link--primary")
        logo_font = []
        font_name = "**Available font names are here:-**\n\n**0.** `Random`\n\n"
        for i, each in enumerate(links, start=1):
            cat = os.path.splitext(each.text)[0]
            logo_font.append(cat)
            font_name += f"**{i}.**  `{cat}`\n"
        logo_font.append("Random")
        if not input_str or input_str not in logo_font:
            return await edit_delete(event, font_name, 80)
        string = input_str
        if input_str != "Random":
            if " " in input_str:
                input_str = str(input_str).replace(" ", "%20")
            string = f"https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Logo/Fonts/{input_str}.ttf?raw=true"
        addgvar("LOGO_FONT", string)
        return await edit_delete(
            event, f"**Font for logo changed to :-** `{input_str}`", 10
        )
    elif cmd in ["c", "sc"]:
        fg_name = []
        for name, code in PIL.ImageColor.colormap.items():
            fg_name.append(name)
            fg_list = str(fg_name).replace("'", "`")
        rfg_name = fg_name + ["Random"]
        if cmd == "c":
            if not input_str or input_str not in rfg_name:
                return await edit_delete(
                    event,
                    f"**Available font color names are here:-**\n\n[`Random`]\n\n{fg_list}",
                    80,
                )
            addgvar("LOGO_FONT_COLOR", input_str)
            return await edit_delete(
                event, f"**Font color for logo changed to :-** `{input_str}`", 10
            )
        if not input_str or input_str not in fg_name:
            return await edit_delete(
                event, f"**Available stroke color names are here:-**\n\n{fg_list}", 80
            )
        addgvar("LOGO_FONT_STROKE_COLOR", input_str)
        return await edit_delete(
            event, f"**Stroke color for logo changed to :-** `{input_str}`", 10
        )
    cat = re.compile(r"^\-?[1-9][0-9]*\.?[0-9]*")
    isint = re.match(cat, input_str)
    if not input_str or not isint:
        return await edit_delete(event, "**Give an integer value to set**", 10)
    if cmd == "s":
        input_str = int(input_str)
        if input_str > 0 and input_str <= 1000:
            addgvar("LOGO_FONT_SIZE", input_str)
            return await edit_delete(
                event, f"**Font size is changed to :-** `{input_str}`", 10
            )
        await edit_delete(
            event,
            f"**Font size is between 0 - 1000, You can't set limit to :** `{input_str}`",
            10,
        )
    elif cmd == "w":
        input_str = float(input_str)
        if input_str > 0 and input_str <= 100:
            addgvar("LOGO_FONT_WIDTH", input_str)
            return await edit_delete(
                event, f"**Font width is changed to :-** `{input_str}`", 10
            )
        await edit_delete(
            event,
            f"**Font width is between 0 - 100, You can't set limit to {input_str}",
            10,
        )
    elif cmd == "h":
        input_str = float(input_str)
        if input_str > 0 and input_str <= 100:
            addgvar("LOGO_FONT_HEIGHT", input_str)
            return await edit_delete(
                event, f"**Font hight is changed to :-** `{input_str}`", 10
            )
        await edit_delete(
            event,
            f"**Font hight is between 0 - 100, You can't set limit to {input_str}",
            10,
        )
    elif cmd == "sw":
        input_str = int(input_str)
        if input_str > 0 and input_str <= 100:
            addgvar("LOGO_FONT_STROKE_WIDTH", input_str)
            return await edit_delete(
                event, f"**Font stroke width is changed to :-** `{input_str}`", 10
            )
        await edit_delete(
            event,
            f"**Font stroke width size is between 0 - 100, You can't set limit to :** `{input_str}`",
            10,
        )


@catub.cat_cmd(
    pattern="(g|d|r)lvar(?:\s|$)([\s\S]*)",
    command=("lvar", plugin_category),
    info={
        "header": "Manage values which set for logo",
        "description": "To see which value have been set, or to delete a value , or to reset all values.",
        "flags": {
            "g": "Gets the value of the var which you set manually for logo.",
            "d": "Delete the value of the var which you set manually for logo.",
            "r": "Delete all the values of the vars which you set manually for logo & reset all changes.",
        },
        "usage": [
            "{tr}glvar <var code>",
            "{tr}dlvar <var code>",
            "{tr}rlvar",
        ],
        "examples": [
            "{tr}glvar lbg",
            "{tr}dlvar lfc",
        ],
    },
)
async def cat(event):
    "Manage all values of logo"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    if input_str in vars_list.keys():
        var = vars_list[input_str]
        if cmd == "g":
            var_data = gvarstatus(var)
            await edit_delete(event, f"📑 Value of **{var}** is  `{var_data}`", time=60)
        elif cmd == "d":
            delgvar(var)
            await edit_delete(
                event, f"📑 Value of **{var}** is now deleted & set to default.", time=60
            )
    elif not input_str and cmd == "r":
        delgvar("LOGO_BACKGROUND")
        delgvar("LOGO_FONT_COLOR")
        delgvar("LOGO_FONT")
        delgvar("LOGO_FONT_SIZE")
        delgvar("LOGO_FONT_HEIGHT")
        delgvar("LOGO_FONT_WIDTH")
        delgvar("LOGO_FONT_STROKE_COLOR")
        delgvar("LOGO_FONT_STROKE_WIDTH")
        await edit_delete(
            event,
            "📑 Values for all vars deleted successfully & all settings reset.",
            time=20,
        )
    else:
        await edit_delete(
            event,
            f"**📑 Give correct vars name :**\n__Correct Vars code list is :__\n\n1. `lbg` : **LOGO_BACKGROUND**\n2. `lfc` : **LOGO_FONT_COLOR**\n3. `lf` : **LOGO_FONT**\n4. `lfs` : **LOGO_FONT_SIZE**\n5. `lfh` : **LOGO_FONT_HEIGHT**\n6. `lfw` : **LOGO_FONT_WIDTH**",
            time=60,
        )
