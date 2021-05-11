import asyncio
import random

from userbot import catub

from ..core.managers import edit_or_reply
from . import catmemes

plugin_category = "extra"


@catub.cat_cmd(
    pattern="abuse$",
    command=("abuse", plugin_category),
    info={
        "header": "shows you some abuse sentences",
        "usage": "{tr}abuse",
    },
)
async def abusing(abused):
    "random abuse string"
    reply_text = random.choice(catmemes.ABUSE_STRINGS)
    await edit_or_reply(abused, reply_text)


@catub.cat_cmd(
    pattern="abusehard$",
    command=("abusehard", plugin_category),
    info={
        "header": "shows you some gali sentences",
        "usage": "{tr}abusehard",
    },
)
async def fuckedd(abusehard):
    "random gali string"
    reply_text = random.choice(catmemes.ABUSEHARD_STRING)
    await edit_or_reply(abusehard, reply_text)


@catub.cat_cmd(
    pattern="rendi$",
    command=("rendi", plugin_category),
    info={
        "header": "shows you some gali sentences",
        "usage": "{tr}rendi",
    },
)
async def metoo(e):
    "random gali string"
    txt = random.choice(catmemes.RENDISTR)
    await edit_or_reply(e, txt)


@catub.cat_cmd(
    pattern="rape$",
    command=("rape", plugin_category),
    info={
        "header": "shows you some gali sentences",
        "usage": "{tr}rape",
    },
)
async def raping(raped):
    "random gali string"
    reply_text = random.choice(catmemes.RAPE_STRINGS)
    await edit_or_reply(raped, reply_text)


@catub.cat_cmd(
    pattern="fuck$",
    command=("fuck", plugin_category),
    info={
        "header": "shows you some gali sentences",
        "usage": "{tr}fuck",
    },
)
async def chutiya(fuks):
    "random gali string"
    reply_text = random.choice(catmemes.CHU_STRINGS)
    await edit_or_reply(fuks, reply_text)


@catub.cat_cmd(
    pattern="thanos$",
    command=("thanos", plugin_category),
    info={
        "header": "shows you some gali sentences",
        "usage": "{tr}thanos",
    },
)
async def thanos(thanos):
    "random gali string"
    reply_text = random.choice(catmemes.THANOS_STRINGS)
    await edit_or_reply(thanos, reply_text)


@catub.cat_cmd(
    pattern="kiss$",
    command=("kiss", plugin_category),
    info={
        "header": "shows you fun kissing animation",
        "usage": "{tr}kiss",
    },
)
async def _(event):
    "fun animation"
    catevent = await edit_or_reply(event, "`kiss`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵💋👰"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await catevent.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="fuk$",
    command=("fuk", plugin_category),
    info={
        "header": "shows you fun fucking animation",
        "usage": "{tr}fuk",
    },
)
async def _(event):
    "fun animation"
    catevent = await edit_or_reply(event, "`fuking....`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["👉       ✊️", "👉     ✊️", "👉  ✊️", "👉✊️💦"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await catevent.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="sex$",
    command=("sex", plugin_category),
    info={
        "header": "shows you fun sex animation",
        "usage": "{tr}sex",
    },
)
async def _(event):
    "fun animation"
    catevent = await edit_or_reply(event, "`sex`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵👼👰"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await catevent.edit(animation_chars[i % 4])
