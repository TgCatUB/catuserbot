# imported from uniborg credit goes to spechide
from telethon.tl.types import InputMediaDice

from . import catub

plugin_category = "fun"

# EMOJI CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽️"
SLOT_E_MOJI = "🎰"
BOWL_E_MOJI = "🎳"
# EMOJI CONSTANTS


@catub.cat_cmd(
    pattern=f"({DART_E_MOJI}|dart)( ([1-6])|$)",
    command=("dart", plugin_category),
    info={
        "header": "To get specific dart animation.",
        "description": "will send and delete the dart emoji animation until the selected outcome comes.",
        "usage": [
            "{tr}dart [1-6]",
            "{tr}🎯 [1-6]",
        ],
        "examples": ["{tr}dart 3", "{tr}🎯 4"],
    },
    groups_only=True,
)
async def _(event):
    "To get specific dart emoji animation"
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


@catub.cat_cmd(
    pattern=f"({DICE_E_MOJI}|dice)( ([1-6])|$)",
    command=("dice", plugin_category),
    info={
        "header": "To get specific dice animation.",
        "description": "will send and delete the dice emoji animation until the selected outcome comes.",
        "usage": [
            "{tr}dice [1-6]",
            "{tr}🎲 [1-6]",
        ],
        "examples": ["{tr}dice 3", "{tr}🎲 4"],
    },
    groups_only=True,
)
async def _(event):
    "To get specific dice emoji animation"
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


@catub.cat_cmd(
    pattern=f"({BALL_E_MOJI}|bb)( ([1-5])|$)",
    command=("bb", plugin_category),
    info={
        "header": "To get specific basket ball animation.",
        "description": "will send and delete the basket ball emoji animation until the selected outcome comes.",
        "usage": [
            "{tr}bb [1-5]",
            "{tr}🏀 [1-5]",
        ],
        "examples": ["{tr}bb 3", "{tr}🏀 4"],
    },
    groups_only=True,
)
async def _(event):
    "To get specific basket ball emoji animation"
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


@catub.cat_cmd(
    pattern=f"({FOOT_E_MOJI}|fb)( ([1-5])|$)",
    command=("fb", plugin_category),
    info={
        "header": "To get specific football animation.",
        "description": "will send and delete the football emoji animation until the selected outcome comes.",
        "usage": [
            "{tr}fb [1-5]",
            "{tr}⚽️ [1-5]",
        ],
        "examples": ["{tr}fb 3", "{tr}⚽️ 4"],
    },
    groups_only=True,
)
async def _(event):
    "To get specific football emoji animation"
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


@catub.cat_cmd(
    pattern=f"({SLOT_E_MOJI}|jp)( ([1-64])|$)",
    command=("jp", plugin_category),
    info={
        "header": "To get specific jackpot animation.",
        "description": "will send and delete the jackpot emoji animation until the selected outcome comes.",
        "usage": [
            "{tr}jp [1-64]",
            "{tr}🎰 [1-64]",
        ],
        "examples": ["{tr}jp 3", "{tr}🎰 4"],
    },
    groups_only=True,
)
async def _(event):
    "To get specific jackpot emoji animation"
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


@catub.cat_cmd(
    pattern=f"({BOWL_E_MOJI}|bowl)( ([1-6])|$)",
    command=("bowl", plugin_category),
    info={
        "header": "To get specific bowling animation.",
        "description": "will send and delete the bowling emoji animation until the selected outcome comes.",
        "usage": [
            "{tr}bowl [1-6]",
            "{tr}🎳 [1-6]",
        ],
        "examples": ["{tr}bowl 3", "{tr}🎳 4"],
    },
    groups_only=True,
)
async def _(event):
    "To get specific bowl emoji animation"
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "bowl":
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
