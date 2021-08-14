import asyncio
import os
import re
from io import BytesIO
from random import choice, randint
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
from requests import get
from telethon.utils import get_display_name

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.utils import get_user_from_event, reply_id
from . import ALIVE_NAME

plugin_category = "extra"


async def amongus_gen(text: str, clr: int) -> str:
    url = "https://github.com/sandy1709/CatUserbot-Resources/raw/master/Resources/Amongus/"
    font = ImageFont.truetype(
        BytesIO(
            get(
                "https://github.com/sandy1709/CatUserbot-Resources/raw/master/Resources/fonts/bold.ttf"
            ).content
        ),
        60,
    )
    imposter = Image.open(BytesIO(get(f"{url}{clr}.png").content))
    text_ = "\n".join("\n".join(wrap(part, 30)) for part in text.split("\n"))
    w, h = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textsize(
        text_, font, stroke_width=2
    )
    text = Image.new("RGBA", (w + 30, h + 30))
    ImageDraw.Draw(text).multiline_text(
        (15, 15), text_, "#FFF", font, stroke_width=2, stroke_fill="#000"
    )
    w = imposter.width + text.width + 10
    h = max(imposter.height, text.height)
    image = Image.new("RGBA", (w, h))
    image.paste(imposter, (0, h - imposter.height), imposter)
    image.paste(text, (w - text.width, 0), text)
    image.thumbnail((512, 512))
    output = BytesIO()
    output.name = "imposter.webp"
    webp_file = os.path.join(Config.TEMP_DIR, output.name)
    image.save(webp_file, "WebP")
    return webp_file


async def get_imposter_img(text: str) -> str:
    background = get(
        f"https://github.com/sandy1709/CatUserbot-Resources/raw/master/Resources/imposter/impostor{randint(1,22)}.png"
    ).content
    font = get(
        "https://github.com/sandy1709/CatUserbot-Resources/raw/master/Resources/fonts/roboto_regular.ttf"
    ).content
    font = BytesIO(font)
    font = ImageFont.truetype(font, 30)
    image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    w, h = draw.multiline_textsize(text=text, font=font)
    image = Image.open(BytesIO(background))
    x, y = image.size
    draw = ImageDraw.Draw(image)
    draw.multiline_text(
        ((x - w) // 2, (y - h) // 2), text=text, font=font, fill="white", align="center"
    )
    output = BytesIO()
    output.name = "impostor.png"
    webp_file = os.path.join(Config.TEMP_DIR, output.name)
    image.save(webp_file, "png")
    return webp_file


@catub.cat_cmd(
    pattern="amongus(?:\s|$)([\s\S]*)",
    command=("amongus", plugin_category),
    info={
        "header": "Create a Sticker based on the popular game Among Us",
        "flags": {
            "1": "red",
            "2": "lime",
            "3": "green",
            "4": "blue",
            "5": "cyan",
            "6": "brown",
            "7": "purple",
            "8": "pink",
            "9": "orange",
            "10": "yellow",
            "11": "white",
            "12": "black",
        },
        "usage": [
            "{tr}amongus <text/reply>",
            "{tr}amongus -c<colur number> <text/reply>",
        ],
        "examples": [
            "{tr}amongus gather around",
            "{tr}amongus -c3 gather around",
        ],
    },
)
async def sayliecmd(event):
    text = event.pattern_match.group(1)
    reply_to = await reply_id(event)
    reply = await event.get_reply_message()
    if not text and reply:
        text = reply.raw_text
    clr = re.findall(r"-c\d+", text)
    try:
        clr = clr[0]
        clr = clr.replace("-c", "")
        text = text.replace("-c" + clr, "")
        clr = int(clr)
        if clr > 12 or clr < 1:
            clr = randint(1, 12)
    except IndexError:
        clr = randint(1, 12)
    if not text:
        if not reply:
            return await edit_or_reply(event, f"{mention} Was a traitor!")
        if not reply.text:
            return await edit_or_reply(
                event,
                f"{_format.mentionuser(get_display_name(reply.sender) ,reply.sender.id)} Was a traitor!",
            )
    imposter_file = await amongus_gen(text, clr)
    await event.delete()
    await event.client.send_file(event.chat_id, imposter_file, reply_to=reply_to)


@catub.cat_cmd(
    pattern="imposter(?:\s|$)([\s\S]*)",
    command=("imposter", plugin_category),
    info={
        "header": "Fun images for imposter ",
        "usage": "{tr}imposter <username/userid/reply>",
    },
)
async def procces_img(event):
    "Fun images for imposter"
    remain = randint(1, 2)
    imps = ["wasn`t the impostor", "was the impostor"]
    text2 = f"\n{remain} impostor(s) remain."
    reply_to = await reply_id(event)
    user, reason = await get_user_from_event(event, noedits=True)
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    if not user:
        try:
            if args or reply:
                user = await event.client.get_entity(args or reply.sender_id)
            else:
                user = await event.client.get_me()
            text = f"{get_display_name(user)} {choice(imps)}."
            text += text2
        except Exception:
            text = args
    else:
        text = f"{get_display_name(user)} {choice(imps)}."
        text += text2
    imposter_file = await get_imposter_img(text)
    await event.delete()
    await event.client.send_file(event.chat_id, imposter_file, reply_to=reply_to)


@catub.cat_cmd(
    pattern="imp(|n) ([\s\S]*)",
    command=("imp", plugin_category),
    info={
        "header": "Find imposter with stickers animation.",
        "description": "Imp for imposter impn for not imposter",
        "usage": ["{tr}imp <name>", "{tr}impn <name>"],
        "examples": ["{tr}imp blabla", "{tr}impn blabla"],
    },
)
async def _(event):
    "Find imposter with stickers animation."
    USERNAME = f"tg://user?id={event.client.uid}"
    name = event.pattern_match.group(2)
    cmd = event.pattern_match.group(1).lower()
    text1 = await edit_or_reply(event, "Uhmm... Something is wrong here!!")
    await asyncio.sleep(2)
    await text1.delete()
    stcr1 = await event.client.send_file(
        event.chat_id, "CAADAQADRwADnjOcH98isYD5RJTwAg"
    )
    text2 = await event.reply(
        f"**[{ALIVE_NAME}]({USERNAME}) :** I have to call discussion"
    )
    await asyncio.sleep(3)
    await stcr1.delete()
    await text2.delete()
    stcr2 = await event.client.send_file(
        event.chat_id, "CAADAQADRgADnjOcH9odHIXtfgmvAg"
    )
    text3 = await event.reply(
        f"**[{ALIVE_NAME}]({USERNAME}) :** We have to eject the imposter or will lose "
    )
    await asyncio.sleep(3)
    await stcr2.delete()
    await text3.delete()
    stcr3 = await event.client.send_file(
        event.chat_id, "CAADAQADOwADnjOcH77v3Ap51R7gAg"
    )
    text4 = await event.reply("**Others :** Where??? ")
    await asyncio.sleep(2)
    await text4.edit("**Others :** Who?? ")
    await asyncio.sleep(2)
    await text4.edit(
        f"**[{ALIVE_NAME}]({USERNAME}) :** Its {name} , I saw {name}  using vent,"
    )
    await asyncio.sleep(3)
    await text4.edit(f"**Others :**Okay.. Vote {name} ")
    await asyncio.sleep(2)
    await stcr3.delete()
    await text4.delete()
    stcr4 = await event.client.send_file(
        event.chat_id, "CAADAQADLwADnjOcH-wxu-ehy6NRAg"
    )
    catevent = await event.reply(f"{name} is ejected.......")
    await asyncio.sleep(2)
    await catevent.edit("ඞㅤㅤㅤㅤ ㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤඞㅤㅤㅤㅤ ㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤ ඞㅤㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤ ඞㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤ ඞㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤ ඞㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤ ඞㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤ ඞㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ඞ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ")
    await asyncio.sleep(0.2)
    await stcr4.delete()
    if cmd == "":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ{name} was an Imposter.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         0 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
        await asyncio.sleep(4)
        await catevent.delete()
        await event.client.send_file(event.chat_id, "CAADAQADLQADnjOcH39IqwyR6Q_0Ag")
    elif cmd == "n":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ{name} was not an Imposter.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         1 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
        await asyncio.sleep(4)
        await catevent.delete()
        await event.client.send_file(event.chat_id, "CAADAQADQAADnjOcH-WOkB8DEctJAg")


@catub.cat_cmd(
    pattern="timp(|n) ([\s\S]*)",
    command=("timp", plugin_category),
    info={
        "header": "Find imposter with text animation.",
        "description": "timp for imposter timpn for not imposter",
        "usage": ["{tr}timp <name>", "{tr}timpn <name>"],
        "examples": ["{tr}timp blabla", "{tr}timpn blabla"],
    },
)
async def _(event):
    "Find imposter with text animation."
    name = event.pattern_match.group(2)
    cmd = event.pattern_match.group(1).lower()
    catevent = await edit_or_reply(event, f"{name} is ejected.......")
    await asyncio.sleep(2)
    await catevent.edit("ඞㅤㅤㅤㅤ ㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤඞㅤㅤㅤㅤ ㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤ ඞㅤㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤ ඞㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤ ඞㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤ ඞㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤ ඞㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤ ඞㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ඞ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ")
    await asyncio.sleep(0.2)
    if cmd == "":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ {name} was an Imposter.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         0 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
    elif cmd == "n":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ {name} was not an Imposter.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         1 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
