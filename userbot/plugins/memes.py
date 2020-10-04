# catUserbot module for having some fun with people.

# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.

import asyncio
import random
import re

import requests
from cowpy import cow
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from ..utils import admin_cmd, register
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, CMD_HELP, memes

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


@borg.on(admin_cmd(outgoing=True, pattern=r"(\w+)say (.*)"))
async def univsaye(cowmsg):
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)
    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()
    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$")
async def kek(keks):
    """ Check yourself ;)"""
    if not keks.text[0].isalpha() and keks.text[0] not in ("/", "#", "@", "!"):
        uio = ["/", "\\"]
        for i in range(1, 15):
            await asyncio.sleep(0.3)
            await keks.edit(":" + uio[i % 2])


@borg.on(admin_cmd(pattern="coin ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    r = random.randint(1, 100)
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r % 2 == 1:
        if input_str == "heads":
            await event.edit("The coin landed on: **Heads**. \n You were correct.")
        elif input_str == "tails":
            await event.edit(
                "The coin landed on: **Heads**. \n You weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await event.edit("The coin landed on: **Tails**. \n You were correct.")
        elif input_str == "heads":
            await event.edit(
                "The coin landed on: **Tails**. \n You weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Tails**.")
    else:
        await event.edit(r"¯\_(ツ)_/¯")


@borg.on(admin_cmd(pattern=r"slap(?: |$)(.*)", outgoing=True))
async def who(event):
    if event.fwd_from:
        return
    replied_user = await get_user(event)
    caption = await slap(replied_user, event)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await event.edit(caption)
    except BaseException:
        await event.edit(
            "`Can't slap this person, need to fetch some sticks and stones !!`"
        )


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap aliens, they ugly AF !!`")
            return None

    return replied_user


async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username
    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"
    temp = random.choice(memes.SLAP_TEMPLATES)
    item = random.choice(memes.ITEMS)
    hit = random.choice(memes.HIT)
    throw = random.choice(memes.THROW)
    where = random.choice(memes.WHERE)
    return "..." + temp.format(
        user1=DEFAULTUSER,
        victim=slapped,
        item=item,
        hits=hit,
        throws=throw,
        where=where,
    )


@register(outgoing=True, pattern="^-_-$")
async def lol(lel):
    """ Ok... """
    if not lel.text[0].isalpha() and lel.text[0] not in ("/", "#", "@", "!"):
        okay = "-_-"
        for _ in range(10):
            okay = okay[:-1] + "_-"
            await lel.edit(okay)


@borg.on(admin_cmd(outgoing=True, pattern="(yes|no|maybe|decide)$"))
async def decide(event):
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id if event.reply_to_msg_id else None
    if decision != "decide":
        r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = requests.get(f"https://yesno.wtf/api").json()
    await event.delete()
    await event.client.send_message(
        event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"]
    )


@register(outgoing=True, pattern="^;_;")
async def fun(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        t = ";__;"
        for _ in range(10):
            t = t[:-1] + "_;"
            await e.edit(t)


@borg.on(admin_cmd(outgoing=True, pattern="insult$"))
async def insult(e):
    await e.edit(random.choice(memes.INSULT_STRINGS))


@borg.on(admin_cmd(outgoing=True, pattern="repo$"))
async def source(e):
    await e.edit(
        "Click [here](https://github.com/Jisan09/catuserbot) to open this lit af repo."
    )


@borg.on(admin_cmd(outgoing=True, pattern="hey$"))
async def hoi(hello):
    await hello.edit(random.choice(memes.HELLOSTR))


@borg.on(admin_cmd(outgoing=True, pattern="rape$"))
async def raping(raped):
    index = random.randint(0, len(memes.RAPE_STRINGS) - 1)
    reply_text = memes.RAPE_STRINGS[index]
    await raped.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="pro$"))
async def proo(pros):
    index = random.randint(0, len(memes.PRO_STRINGS) - 1)
    reply_text = memes.PRO_STRINGS[index]
    await pros.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="fuck$"))
async def chutiya(fuks):
    index = random.randint(0, len(memes.CHU_STRINGS) - 1)
    reply_text = memes.FUK_STRINGS[index]
    await fuks.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="thanos$"))
async def thanos(thanos):
    index = random.randint(0, len(memes.THANOS_STRINGS) - 1)
    reply_text = memes.THANOS_STRINGS[index]
    await thanos.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="abusehard$"))
async def fuckedd(abusehard):
    index = random.randint(0, len(memes.ABUSEHARD_STRING) - 1)
    reply_text = memes.ABUSEHARD_STRING[index]
    await abusehard.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="abuse$"))
async def abusing(abused):
    index = random.randint(0, len(memes.ABUSE_STRINGS) - 1)
    reply_text = memes.ABUSE_STRINGS[index]
    await abused.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="owo (.*)"))
async def faces(owo):
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU no text given! `")
        return

    reply_text = re.sub(r"(r|l)", "w", message)
    reply_text = re.sub(r"(R|L)", "W", reply_text)
    reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = re.sub(r"\!+", " " + random.choice(memes.UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + random.choice(memes.UWUS)
    await owo.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="shg$"))
async def shrugger(shg):
    await shg.edit(random.choice(memes.SHGS))


@borg.on(admin_cmd(outgoing=True, pattern="runs$"))
async def runner_lol(run):
    await run.edit(random.choice(memes.RUNSREACTS))


@borg.on(admin_cmd(outgoing=True, pattern="noob$"))
async def metoo(hahayes):
    await hahayes.edit(random.choice(memes.NOOBSTR))


@borg.on(admin_cmd(outgoing=True, pattern="rendi$"))
async def metoo(hahayes):
    await hahayes.edit(random.choice(memes.RENDISTR))


@borg.on(admin_cmd(outgoing=True, pattern="oof$"))
async def Oof(e):
    t = "Oof"
    for _ in range(15):
        t = t[:-1] + "of"
        await e.edit(t)


@borg.on(admin_cmd(outgoing=True, pattern="10iq$"))
async def iqless(e):
    await e.edit("♿")


@borg.on(admin_cmd(outgoing=True, pattern="clap(?: |$)(.*)"))
async def claptext(event):
    textx = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif textx.message:
        query = textx.message
    else:
        await event.edit("Hah, I don't clap pointlessly!")
        return
    reply_text = "👏 "
    reply_text += query.replace(" ", " 👏 ")
    reply_text += " 👏"
    await event.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="smk(?: |$)(.*)"))
async def smrk(smk):
    textx = await smk.get_reply_message()
    if smk.pattern_match.group(1):
        message = smk.pattern_match.group(1)
    elif textx.message:
        message = textx.message
    else:
        await smk.edit("ツ")
        return
    if message == "dele":
        await smk.edit(message + "te the hell" + "ツ")
        await smk.edit("ツ")
    else:
        smirk = " ツ"
        reply_text = message + smirk
        await smk.edit(reply_text)


@borg.on(admin_cmd(pattern="ftext ?(.*)"))
async def payf(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8,
        paytext * 8,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 6,
        paytext * 6,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
    )
    await event.edit(pay)


@borg.on(admin_cmd(pattern=f"react ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str in "happy":
        emoticons = [
            "( ͡° ͜ʖ ͡°)",
            "(ʘ‿ʘ)",
            "(✿´‿`)",
            "=͟͟͞͞٩(๑☉ᴗ☉)੭ु⁾⁾",
            "(*⌒▽⌒*)θ～♪",
            "°˖✧◝(⁰▿⁰)◜✧˖°",
            "✌(-‿-)✌",
            "⌒°(❛ᴗ❛)°⌒",
            "(ﾟ<|＼(･ω･)／|>ﾟ)",
            "ヾ(o✪‿✪o)ｼ",
        ]
    elif input_str in "think":
        emoticons = [
            "(҂⌣̀_⌣́)",
            "（；¬＿¬)",
            "(-｡-;",
            "┌[ O ʖ̯ O ]┐",
            "〳 ͡° Ĺ̯ ͡° 〵",
        ]
    elif input_str in "wave":
        emoticons = [
            "(ノ^∇^)",
            "(;-_-)/",
            "@(o・ェ・)@ノ",
            "ヾ(＾-＾)ノ",
            "ヾ(◍’౪`◍)ﾉﾞ♡",
            "(ό‿ὸ)ﾉ",
            "(ヾ(´・ω・｀)",
        ]
    elif input_str in "wtf":
        emoticons = [
            "༎ຶ‿༎ຶ",
            "(‿ˠ‿)",
            "╰U╯☜(◉ɷ◉ )",
            "(;´༎ຶ益༎ຶ`)♡",
            "╭∩╮(︶ε︶*)chu",
            "( ＾◡＾)っ (‿|‿)",
        ]
    elif input_str in "love":
        emoticons = [
            "乂❤‿❤乂",
            "(｡♥‿♥｡)",
            "( ͡~ ͜ʖ ͡°)",
            "໒( ♥ ◡ ♥ )७",
            "༼♥ل͜♥༽",
        ]
    elif input_str in "confused":
        emoticons = [
            "(・_・ヾ",
            "｢(ﾟﾍﾟ)",
            "﴾͡๏̯͡๏﴿",
            "(￣■￣;)!?",
            "▐ ˵ ͠° (oo) °͠ ˵ ▐",
            "(-_-)ゞ゛",
        ]
    elif input_str in "dead":
        emoticons = [
            "(✖╭╮✖)",
            "✖‿✖",
            "(+_+)",
            "(✖﹏✖)",
            "∑(✘Д✘๑)",
        ]
    elif input_str in "sad":
        emoticons = [
            "(＠´＿｀＠)",
            "⊙︿⊙",
            "(▰˘︹˘▰)",
            "●︿●",
            "(　´_ﾉ` )",
            "彡(-_-;)彡",
        ]
    elif input_str in "dog":
        emoticons = [
            "-ᄒᴥᄒ-",
            "◖⚆ᴥ⚆◗",
        ]
    else:
        emoticons = [
            "( ͡° ͜ʖ ͡°)",
            r"¯\_(ツ)_/¯",
            "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
            "ʕ•ᴥ•ʔ",
            "(▀̿Ĺ̯▀̿ ̿)",
            "(ง ͠° ͟ل͜ ͡°)ง",
            "༼ つ ◕_◕ ༽つ",
            "ಠ_ಠ",
            "(☞ ͡° ͜ʖ ͡°)☞",
            r"¯\_༼ ି ~ ି ༽_/¯",
            "c༼ ͡° ͜ʖ ͡° ༽⊃",
        ]
    index = random.randint(0, len(emoticons))
    output_str = emoticons[index]
    await event.edit(output_str)


@borg.on(admin_cmd(outgoing=True, pattern="bt$"))
async def bluetext(bt_e):
    """ Believe me, you will find this useful. """
    if bt_e.is_group:
        await bt_e.edit(
            "/BLUETEXT /MUST /CLICK.\n"
            "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS?"
        )


@borg.on(admin_cmd(pattern="ggl (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit(
            "[{}]({})\n`Thank me Later 🙃` ".format(input_str, response_api.rstrip())
        )
    else:
        await event.edit("something is wrong. please try again later.")
    if BOTLOG:
        await bot.send_message(
            BOTLOG_CHATID,
            "LMGTFY query `" + input_str + "` was executed successfully",
        )


@borg.on(admin_cmd(pattern="type (.*)"))
async def typewriter(typew):
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("`Give a text to type!`")
        return
    sleep_time = 0.1
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)


CMD_HELP.update(
    {
        "memes": "__**PLUGIN NAME :** Memes__\
\n\n📌** CMD ➥** `.cowsay`\
\n**USAGE   ➥  **cow which says things.\
\n\n📌** CMD ➥** `.milksay`\
\n**USAGE   ➥  **Weird Milk that can speak\
\n\n📌** CMD ➥** `:/` or `-_-` or `;_;` \
\n**USAGE   ➥  **Check yourself ;)\
\n\n📌** CMD ➥** `.10iq`\
\nUsage: You retard !!\
\n\n📌** CMD ➥** `.oof`\
\n**USAGE   ➥  **Ooooof\
\n\n📌** CMD ➥** `.hey`\
\n**USAGE   ➥  **Greet everyone!\
\n\n📌** CMD ➥** `.coinflip` <heads/tails>\
\n**USAGE   ➥  **Flip a coin !!\
\n\n📌** CMD ➥** `.owo` <text> \
\n**USAGE   ➥  **UwU\
\n\n📌** CMD ➥** `.react` <type>\
\n**USAGE   ➥  **Make your userbot react. types are <happy ,think ,wave ,wtf ,love ,confused,dead, sad,dog>\
\n\n📌** CMD ➥** `.slap`\
\n**USAGE   ➥  **reply to slap them with random objects !!\
\n\n📌** CMD ➥** `.shg`\
\n**USAGE   ➥  **Shrug at it !!\
\n\n📌** CMD ➥** `.runs`\
\n**USAGE   ➥  **Run, run, RUNNN! [`.disable runs`: disable | `.enable runs`: enable]\
\n\n📌** CMD ➥** `.clap`\
\n**USAGE   ➥  **Praise people!\
\n\n📌** CMD ➥** `.ftext` <emoji/character>\
\n**USAGE   ➥  **Pay Respects.\
\n\n📌** CMD ➥** `.bt`\
\n**USAGE   ➥  **Believe me, you will find this useful.\
\n\n📌** CMD ➥** `.smk` <text/reply>\
\n**USAGE   ➥  **A shit module for ツ , who cares.\
\n\n📌** CMD ➥** `.type`\
\n**USAGE   ➥  **Just a small command to make your keyboard become a typewriter!\
\n\n📌** CMD ➥** `.ggl` <query>\
\n**USAGE   ➥  **Let me Google that for you real quick !!\
\n\n📌** CMD ➥** `.decide`\
\n**USAGE   ➥  **Make a quick decision.\
\n\n📌** CMD ➥** `.abusehard`\
\n**USAGE   ➥  **You already got that! Ain't?.\
\n\n📌** CMD ➥** `.thanos`\
\n**USAGE   ➥  **Try and then Snap.\
\n\n📌** CMD ➥** `.noob`\
\n**USAGE   ➥  **Whadya want to know? Are you a NOOB?\
\n\n📌** CMD ➥** `.pro`\
\n**USAGE   ➥  **If you think you're pro, try this.\
\n\n📌** CMD ➥** `.abuse`\
\n**USAGE   ➥  **Protects you from unwanted peeps.\
"
    }
)
