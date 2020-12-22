# imported from uniborg credit goes to spechide
from telethon.tl.types import InputMediaDice

# EMOJI CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽️"
SLOT_E_MOJI = "🎰"
# EMOJI CONSTANTS


@bot.on(admin_cmd(pattern=f"({DART_E_MOJI}|dart)( ([1-6])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({DART_E_MOJI}|dart)( ([1-6])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "dart":
        emoticon = "🎯"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({DICE_E_MOJI}|dice)( ([1-6])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({DICE_E_MOJI}|dice)( ([1-6])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "dice":
        emoticon = "🎲"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({BALL_E_MOJI}|bb)( ([1-5])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({BALL_E_MOJI}|bb)( ([1-5])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "bb":
        emoticon = "🏀"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({FOOT_E_MOJI}|fb)( ([1-5])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({FOOT_E_MOJI}|fb)( ([1-5])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "fb":
        emoticon = "⚽️"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({SLOT_E_MOJI}|jp)( ([1-64])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({SLOT_E_MOJI}|jp)( ([1-64])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "jp":
        emoticon = "🎰"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


CMD_HELP.update(
    {
        "emojigames": "**Syntax :** `.🎯 [1-6]` or `.dart [1-6]`\
    \n**Usage : **each number shows different animation for dart\
    \n\n**Syntax : **`.🎲 [1-6]` or `.dice [1-6]`\
    \n**Usage : **each number shows different animation for dice\
    \n\n**Syntax : **`.🏀 [1-5]` or `.bb [1-5]`\
    \n**Usage : **each number shows different animation for basket ball\
    \n\n**Syntax : **`.⚽️ [1-5] `or `.fb [1-5]`\
    \n**Usage : **each number shows different animation for football\
    \n\n**Syntax : **`.🎰 [1-64] `or `.jp [1-64]`\
    \n**Usage : **each number shows different animation for slot machine(jackpot)\
    "
    }
)
