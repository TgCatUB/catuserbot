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
from telethon.tl.types import ChannelParticipantsAdmins, MessageEntityMentionName

from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, catmemes

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


async def get_user(event):
    # Get the user from argument or replied message.
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
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


@bot.on(admin_cmd(outgoing=True, pattern=r"(\w+)say (.*)"))
@bot.on(sudo_cmd(pattern="(\w+)say (.*)", allow_sudo=True))
async def univsaye(cowmsg):
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)
    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()
    await edit_or_reply(cowmsg, f"`{cheese.milk(text).replace('`', '´')}`")


@bot.on(admin_cmd(pattern="coin ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="coin ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    r = random.randint(1, 100)
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r % 2 == 1:
        if input_str == "heads":
            await edit_or_reply(
                event, "The coin landed on: **Heads**. \n You were correct."
            )
        elif input_str == "tails":
            await edit_or_reply(
                event,
                "The coin landed on: **Heads**. \n You weren't correct, try again ...",
            )
        else:
            await edit_or_reply(event, "The coin landed on: **Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await edit_or_reply(
                event, "The coin landed on: **Tails**. \n You were correct."
            )
        elif input_str == "heads":
            await edit_or_reply(
                event,
                "The coin landed on: **Tails**. \n You weren't correct, try again ...",
            )
        else:
            await edit_or_reply(event, "The coin landed on: **Tails**.")
    else:
        await edit_or_reply(event, r"¯\_(ツ)_/¯")


@bot.on(admin_cmd(pattern=r"slap(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="slap(?: |$)(.*)", allow_sudo=True))
async def who(event):
    replied_user = await get_user(event)
    caption = await catmemes.slap(replied_user, event, DEFAULTUSER)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await edit_or_reply(event, caption)
    except BaseException:
        await edit_or_reply(
            event, "`Can't slap this person, need to fetch some sticks and stones !!`"
        )


@bot.on(admin_cmd(outgoing=True, pattern="(yes|no|maybe|decide)$"))
@bot.on(sudo_cmd(pattern="(yes|no|maybe|decide)$", allow_sudo=True))
async def decide(event):
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id or None
    if decision != "decide":
        r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = requests.get(f"https://yesno.wtf/api").json()
    await event.delete()
    sandy = await event.client.send_message(
        event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"]
    )
    await _catutils.unsavegif(event, sandy)


@bot.on(admin_cmd(pattern=f"shout", outgoing=True))
@bot.on(sudo_cmd(pattern=f"shout", allow_sudo=True))
async def shout(args):
    msg = "```"
    messagestr = args.text
    messagestr = messagestr[7:]
    text = " ".join(messagestr)
    result = [" ".join([s for s in text])]
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + " " + "  " * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "\n" + result
    await edit_or_reply(args, "`" + msg + "`")


@bot.on(admin_cmd(outgoing=True, pattern="owo ?(.*)"))
@bot.on(sudo_cmd(pattern="owo ?(.*)", allow_sudo=True))
async def faces(owo):
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await edit_or_reply(owo, "` UwU no text given! `")
        return
    reply_text = re.sub(r"(r|l)", "w", message)
    reply_text = re.sub(r"(R|L)", "W", reply_text)
    reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = re.sub(r"\!+", " " + random.choice(catmemes.UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + random.choice(catmemes.UWUS)
    await edit_or_reply(owo, reply_text)


@bot.on(admin_cmd(outgoing=True, pattern="clap(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="clap(?: |$)(.*)", allow_sudo=True))
async def claptext(event):
    textx = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif textx.message:
        query = textx.message
    else:
        await edit_or_reply(event, "Hah, I don't clap pointlessly!")
        return
    reply_text = "👏 "
    reply_text += query.replace(" ", " 👏 ")
    reply_text += " 👏"
    await edit_or_reply(event, reply_text)


@bot.on(admin_cmd(outgoing=True, pattern="smk(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="smk(?: |$)(.*)", allow_sudo=True))
async def smrk(smk):
    textx = await smk.get_reply_message()
    if smk.pattern_match.group(1):
        message = smk.pattern_match.group(1)
    elif textx.message:
        message = textx.message
    else:
        await edit_or_reply(smk, "ツ")
        return
    if message == "dele":
        await edit_or_reply(smk, message + "te the hell" + "ツ")
    else:
        smirk = " ツ"
        reply_text = message + smirk
        await edit_or_reply(smk, reply_text)


@bot.on(admin_cmd(pattern="ftext (.*)"))
@bot.on(sudo_cmd(pattern="ftext (.*)", allow_sudo=True))
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
    await edit_or_reply(event, pay)


@bot.on(admin_cmd(pattern="wish ?(.*)"))
@bot.on(sudo_cmd(pattern="wish ?(.*)", allow_sudo=True))
async def wish_check(event):
    wishtxt = event.pattern_match.group(1)
    chance = random.randint(0, 100)
    if wishtxt:
        reslt = f"**Your wish **__{wishtxt}__ **has been cast.** ✨\
              \n\n__Chance of success :__ **{chance}%**"
    else:
        if event.is_reply:
            reslt = f"**Your wish has been cast. **✨\
                  \n\n__Chance of success :__ **{chance}%**"
        else:
            reslt = f"What's your Wish? Should I consider you as Idiot by default ? 😜"
    await edit_or_reply(event, reslt)


@bot.on(admin_cmd(outgoing=True, pattern="repo$"))
@bot.on(sudo_cmd(pattern="repo$", allow_sudo=True))
async def source(e):
    await edit_or_reply(
        e,
        "Click [here](https://github.com/sandy1709/catuserbot) to open this lit af repo.",
    )


@bot.on(admin_cmd(pattern="lfy ?(.*)"))
@bot.on(sudo_cmd(pattern="lfy ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`either reply to text message or give input to search`", 5
        )
    sample_url = f"https://da.gd/s?url=https://lmgtfy.com/?q={input_str.replace(' ', '+')}%26iie=1"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(
            event, f"[{input_str}]({response_api.rstrip()})\n`Thank me Later 🙃` "
        )
    else:
        return await edit_delete(
            event, "`something is wrong. please try again later.`", 5
        )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"LMGTFY query `{input_str}` was executed successfully",
        )


@bot.on(admin_cmd(pattern="gbun", outgoing=True))
@bot.on(sudo_cmd(pattern="gbun", allow_sudo=True))
async def gbun(event):
    if event.fwd_from:
        return
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n`"
    catevent = await edit_or_reply(event, "**Summoning out le Gungnir ❗️⚜️☠️**")
    await asyncio.sleep(3.5)
    chat = await event.get_input_chat()
    async for _ in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.sender_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.sender_id
        # make meself invulnerable cuz why not xD
        if idd == 1035034432:
            await catevent.edit(
                "`Wait a second, This is my master!`\n**How dare you threaten to ban my master nigger!**\n\n__Your account has been hacked! Pay 69$ to my master__ [π.$](tg://user?id=1035034432) __to release your account__😏"
            )
        else:
            jnl = (
                "`Warning!! `"
                "[{}](tg://user?id={})"
                "` 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n\n`"
                "**user's Name: ** __{}__\n"
                "**ID : ** `{}`\n"
            ).format(firstname, idd, firstname, idd)
            if usname is None:
                jnl += "**Victim Nigga's username: ** `Doesn't own a username!`\n"
            else:
                jnl += "**Victim Nigga's username** : @{}\n".format(usname)
            if len(gbunVar) > 0:
                gbunm = "`{}`".format(gbunVar)
                gbunr = "**Reason: **" + gbunm
                jnl += gbunr
            else:
                no_reason = "__Reason: Potential spammer. __"
                jnl += no_reason
            await catevent.edit(jnl)
    else:
        mention = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\nReason: Potential spammer. `"
        await catevent.edit(mention)


CMD_HELP.update(
    {
        "memes": "**Plugin : **`memes`\
        \n\n  •  **Syntax :** `.cowsay`\
        \n  •  **Function : **cow which says things.\
        \n\n  •  **Syntax :** `.coin <heads/tails>`\
        \n  •  **Function : **Flips a coin !!\
        \n\n  •  **Syntax :** `.slap`\
        \n  •  **Function : **reply to slap them with random objects !!\
        \n\n  •  **Syntax :** `.yes` ,`.no` , `.maybe` , `.decide`\
        \n  •  **Function : **Sends you the respectively gif of command u used\
        \n\n  •  **Syntax :** `.shout text`\
        \n  •  **Function : **shouts the text in a fun way\
        \n\n  •  **Syntax :** `.owo`\
        \n  •  **Function : **UwU\
        \n\n  •  **Syntax :** `.clap`\
        \n  •  **Function : **Praise people!\
        \n\n  •  **Syntax :** `.smk <text/reply>`\
        \n  •  **Function : **A shit module for ツ , who cares.\
        \n\n  •  **Syntax :** `.ftext <emoji/character>`\
        \n  •  **Function : **Pay Respects.\
        \n\n  •  **Syntax :** `.wish <reply/text>`\
        \n  •  **Function : **Shows the chance of your success inspired from @CalsiBot.\
        \n\n  •  **Syntax :** `.repo`\
        \n  •  **Function : **Shows to source code link of catuserbot.\
        \n\n  •  **Syntax :** `.lfy <query>`\
        \n  •  **Function : **Let me Google that for you real quick !!\
        \n\n  •  **Syntax :** `.gbun <reason>`\
        \n  •  **Function : **Fake gban action !!\
"
    }
)
