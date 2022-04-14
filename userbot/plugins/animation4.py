import asyncio

from . import ALIVE_NAME, catub, edit_or_reply

plugin_category = "fun"


@catub.cat_cmd(
    pattern="kilr(?:\s|$)([\s\S]*)",
    command=("kilr", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}kilr",
    },
)
async def _(event):
    "animation command"
    name = event.pattern_match.group(1)
    if not name:
        name = "die"
    animation_interval = 0.7
    animation_ttl = range(8)
    event = await edit_or_reply(event, f"**Ready Commando **__{ALIVE_NAME}....")
    animation_chars = [
        "Ｆｉｉｉｉｉｒｅ",
        f"__**Commando **__{ALIVE_NAME}          \n\n_/﹋\_\n (҂`_´)\n <,︻╦╤─ ҉ - \n _/﹋\_\n",
        f"__**Commando **__{ALIVE_NAME}          \n\n_/﹋\_\n (҂`_´)\n  <,︻╦╤─ ҉ - -\n _/﹋\_\n",
        f"__**Commando **__{ALIVE_NAME}          \n\n_/﹋\_\n (҂`_´)\n <,︻╦╤─ ҉ - - -\n _/﹋\_\n",
        f"__**Commando **__{ALIVE_NAME}          \n\n_/﹋\_\n (҂`_´)\n<,︻╦╤─ ҉ - -\n _/﹋\_\n",
        f"__**Commando **__{ALIVE_NAME}          \n\n_/﹋\_\n (҂`_´)\n <,︻╦╤─ ҉ - \n _/﹋\_\n",
        f"__**Commando **__{ALIVE_NAME}         \n\n_/﹋\_\n (҂`_´)\n  <,︻╦╤─ ҉ - -\n _/﹋\_\n",
        f"__**Commando **__{ALIVE_NAME}          \n\n_/﹋\_\n (҂`_´)\n <,︻╦╤─ ҉ - - - {name}\n _/﹋\_\n",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 8])


@catub.cat_cmd(
    pattern="eye$",
    command=("eye", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}eye",
    },
)
async def _(event):
    "animation command"
    animation_interval = 3
    animation_ttl = range(10)
    event = await edit_or_reply(event, "👁👁")
    animation_chars = [
        "👁👁\n  👄  =====> Hey, How are you?",
        "👁👁\n  👅  =====> Everything okay?",
        "👁👁\n  💋  =====> Why are you staring at this?",
        "👁👁\n  👄  =====> You idiot",
        "👁👁\n  👅  =====> Go away",
        "👁👁\n  💋  =====> Stop laughing",
        "👁👁\n  👄  =====> It's not funny",
        "👁👁\n  👅  =====> I guess ur still looking",
        "👁👁\n  💋  =====> Ok man 😑",
        "👁👁\n  👄  =====> I go away then",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])
    await asyncio.sleep(animation_interval)
    await event.delete()


@catub.cat_cmd(
    pattern="thinking$",
    command=("thinking", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}thinking",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.05
    animation_ttl = range(288)
    event = await edit_or_reply(event, "thinking..")
    animation_chars = [
        "THINKING",
        "THI&K#N₹",
        "T+IN@I?G",
        "¿H$NK∆NG",
        "¶H×NK&N*",
        "NGITHKIN",
        "T+I#K@₹G",
        "THINKING",
        "THI&K#N₹",
        "T+IN@I?G",
        "¿H$NK∆NG",
        "¶H×NK&N*",
        "NGITHKIN",
        "T+I#K@₹G",
        "THINKING",
        "THI&K#N₹",
        "T+IN@I?G",
        "¿H$NK∆NG",
        "¶H×NK&N*",
        "NGITHKIN",
        "T+I#K@₹G",
        "THINKING",
        "THI&K#N₹",
        "T+IN@I?G",
        "¿H$NK∆NG",
        "¶H×NK&N*",
        "NGITHKIN",
        "T+I#K@₹G",
        "THINKING",
        "THI&K#N₹",
        "T+IN@I?G",
        "¿H$NK∆NG",
        "¶H×NK&N*",
        "NGITHKIN",
        "T+I#K@₹G",
        "THINKING... 🤔",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 36])


@catub.cat_cmd(
    pattern="snake$",
    command=("snake", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}snake",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(27)
    event = await edit_or_reply(event, "snake..")
    animation_chars = [
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◻️◻️️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "‎◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◻️◻️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◼️◻️◻️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◼️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️",
        "◻️◻️◻️◻️◻️\n◻️◼️◻️◼️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 27])


@catub.cat_cmd(
    pattern="human$",
    command=("human", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}human",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(16)
    event = await edit_or_reply(event, "human...")
    animation_chars = [
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛🚗\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛🚗⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛🚗⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛🚗⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛🚗⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛🚗⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n🚗⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬜⬜⬜😊⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛😊⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬜⬛⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛😊⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬜⬛⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬛⬜⬛⬛⬜⬛\n⬛⬛⬜⬛⬛⬛⬛\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛😊⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬜⬛⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬛⬛⬛⬛⬛⬛\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬛😊⬛⬜⬛\n⬛⬛⬜⬜⬜⬛⬛\n⬛⬛⬛⬜⬛⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬛⬛⬛⬛⬛⬛\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛😊⬛⬛⬛\n⬛⬛⬜⬜⬜⬛⬛\n⬛⬜⬛⬜⬛⬜⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n⬛⬛⬜⬛⬜⬛⬛\n🔲🔲🔲🔲🔲🔲🔲",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬜⬜⬜😊⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n🔲🔲🔲🔲🔲🔲🔲",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 16])


@catub.cat_cmd(
    pattern="mc$",
    command=("mc", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}mc",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(28)
    event = await edit_or_reply(event, "mc..")
    animation_chars = [
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◻️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◻️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◻️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◻️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◻️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◻️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◻️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◻️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◻️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◻️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◻️◼️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 28])


@catub.cat_cmd(
    pattern="virus$",
    command=("virus", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}virus",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(30)
    event = await edit_or_reply(event, "Injecting virus....")
    animation_chars = [
        "🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️◼️️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️◼️◼️🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "‎◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️\n◼️🔴🔵🌕♓♎⛎◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️🔴🔵🌕♓♎⛎🔴🔵🌕♓♎⛎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🔴🔵🌕♓♎⛎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
        "◼️◼️◼️◼️\n◼️◼️◼️◼️\n◼️◼️◼️◼️\n◼️◼️◼️◼️",
        "◼️◼️◼️\n◼️◼️◼️\n◼️◼️◼️",
        "◼️◼️\n◼️◼️",
        "◼️",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 30])


@catub.cat_cmd(
    pattern="repe$",
    command=("repe", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}repe",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.2
    animation_ttl = range(30)
    event = await edit_or_reply(event, "repe")
    animation_chars = [
        "**r**",
        "**ra**",
        "**rap**",
        "**rape**",
        "**rape_**",
        "**rape_t**",
        "**rape_tr**",
        "**rape_tra**",
        "**rape_trai**",
        "**rape_train**",
        "**ape_train🚅**",
        "**pe_train🚅🚃🚃**",
        "**e_train🚅🚃🚃🚃**",
        "**_train🚅🚃🚃🚃🚃**",
        "**train🚅🚃🚃🚃🚃🚃**",
        "**rain🚅🚃🚃🚃🚃🚃🚃**",
        "**ain🚅🚃🚃🚃🚃🚃🚃🚃**",
        "**in🚅🚃🚃🚃🚃🚃🚃🚃🚃**",
        "**n🚅🚃🚃🚃🚃🚃🚃🚃🚃🚃**",
        "🚅🚃🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃🚃",
        "🚃🚃🚃🚃",
        "🚃🚃🚃",
        "🚃🚃",
        "🚃",
        "**rApEd**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 30])


@catub.cat_cmd(
    pattern="nikal$",
    command=("nikal", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}nikal",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(6)
    event = await edit_or_reply(event, "nakal")
    animation_chars = [
        "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀   ⢳⡀⠀⡏⠀⠀⠀   ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀  ⠀   ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Nikal   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀⠀__⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
        "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀  ⠀⢳⡀⠀⡏⠀⠀⠀   ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀      ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Lavde   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀|__|⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
        "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀     ⠀⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Pehli   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀         ⡇\n  ⠙⢿⣯⠄⠀⠀(P)⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
        "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀     ⠀⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀   ⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Fursat  ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀   ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀⠀__ ⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
        "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀   ⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀ ⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Meeee   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀|__| ⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
        "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀  ⠀⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀  ⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Nikal   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀   ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀lodu⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 6])


@catub.cat_cmd(
    pattern="music$",
    command=("music", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}music",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1.5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "starting player...")
    animation_chars = [
        "⬤⬤⬤ 81% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:00** ▱▱▱▱▱▱▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `▶️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤⬤ 81% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:01** ▰▱▱▱▱▱▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤⬤ 81% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay  Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:02** ▰▰▱▱▱▱▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤⬤ 81% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:03** ▰▰▰▱▱▱▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:04** ▰▰▰▰▱▱▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:05** ▰▰▰▰▱▱▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:06** ▰▰▰▰▰▰▱▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:07** ▰▰▰▰▰▰▰▱▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:08** ▰▰▰▰▰▰▰▰▱▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:09** ▰▰▰▰▰▰▰▰▰▱ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏸️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
        "⬤⬤◯ 80% ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀`✖️`\n\n⠀⠀⠀⠀⠀[cee jay Music Player](tg://user?id=916234223)\n\n⠀⠀⠀⠀**Now Playing:shape of u**\n\n**00:10** ▰▰▰▰▰▰▰▰▰▰ **00:10**\n\n⠀⠀⠀⠀⠀`🔂` `⏮️` `⏪️` `⏺️` `⏩️` `⏭️`\n\n**⠀Next Song:** __Alan Walker - Alone.__\n\n⠀⠀⠀⠀**⠀Device: Nokia 1100**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="squ$",
    command=("squ", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}squ",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(
        event, "╔═══════════════════╗ \n  \n╚═══════════════════╝"
    )
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n \t░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ \t░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ ░ ░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ ░ ░ ░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ ░ ░ ░ ░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit("╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝")
    await asyncio.sleep(1)
    await event.edit(
        "╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝"
    )
    await asyncio.sleep(1)
    await event.edit(
        "╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝"
    )
    await asyncio.sleep(1)
    await event.edit(
        "╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝"
    )
    await asyncio.sleep(1)
    await event.edit(
        "╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝"
    )
    await asyncio.sleep(1)
    await event.edit(
        "╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝"
    )
    await asyncio.sleep(1)
    await event.edit(
        "╔═══════════════════╗ \n ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ \n╚═══════════════════╝"
    )
