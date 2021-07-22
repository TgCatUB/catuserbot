# BY @Infinity20998 , @not_ayan
import random
import re
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.events import CallbackQuery

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import StartTime, catub, catversion, mention

ANIME_QUOTE = [
    "自業自得 - One’s act, one’s profit 💙",
    "十人十色 - Ten men, ten colors 💙",
    "起死回生 - Wake from death and return to life 💙",
    "我田引水 - Pulling water to my own rice paddy 💙",
    "悪因悪果 - Evil cause, evil effect 💙",
    "見ぬが花 - Not seeing is a flower 💙",
    "弱肉強食 - The weak are meat; the strong eat 💙",
    "酔生夢死 - Drunken life, dreamy death 💙",
    "一期一会 - One life, one encounter 💙",
    "異体同心 - Different body, same mind 💙",
    "羊頭狗肉 - Sheep head, dog meat 💙",
    "会者定離 - Meeting person always separated 💙",
    "美人薄命 - Beautiful person, thin life 💙",
    "自業自得 - Work of self, obtainment of self 💙",
    "虎穴に入らずんば虎子を得ず。- If you do not enter the tiger’s cave, you will not catch its cub 💙",
    "猿も木から落ちる。- Even monkeys fall from trees 💙",
    "蓼食う虫も好き好き – There are even bugs that eat knotweed 💙",
    "蛙の子は蛙。- Child of a frog is a frog 💙",
    "覆水盆に帰らず。- Spilt water will not return to the tray 💙",
    "猫に小判 - Gold coins to a cat 💙",
    "井の中の蛙大海を知らず。- A frog in a well does not know the great sea 💙",
    "二兎を追う者は一兎をも得ず。- One who chases after two hares won’t catch even one 💙",
    "門前の小僧習わぬ経を読む。- An apprentice near a temple will recite the scriptures untaught 💙",
    "七転び八起き - Fall down seven times, stand up eight 💙",
    "案ずるより産むが易し。- Giving birth to a baby is easier than worrying about it 💙",
    "馬鹿は死ななきゃ治らない。- Unless an idiot dies, he won’t be cured 💙",
    "秋茄子は嫁に食わすな。- Don’t let your daughter-in-law eat your autumn eggplants 💙",
    "花より団子 - Dumplings rather than flowers 💙",
]
plugin_category = "utils"

start = datetime.now()


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status, Plugin by [∞](https://t.me/Infinity20998),[Λｙａｎ](https://t.me/not_ayan)",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    ANIME = f"{random.choice(ANIME_QUOTE)}"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or ANIME
    CAT_IMG = gvarstatus("ALIVE_PIC")
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        cat_caption += f"┏━━━━━━━━━━━━━━━━┓\n"
        cat_caption += f"┃**{EMOJI} ᴀɴɪᴍᴇ ᴠᴇʀꜱɪᴏɴ :** `{catversion}`\n"
        cat_caption += f"┃**{EMOJI} ᴀᴡᴀᴋᴇ ꜱɪɴᴄᴇ :** `{uptime}\n`"
        cat_caption += f"┃**{EMOJI} ꜱᴇɴꜱᴇɪ :** {mention}\n"
        cat_caption += f"┃**{EMOJI} ʜᴇᴀʀᴛ :** `{check_sgnirts}`\n"
        cat_caption += f"┗━━━━━━━━━━━━━━━━┛\n"
        cat_caption += (
            f"┏━━━━━━━━━━━━━━┓\n┃ ⁭⁫**{EMOJI} ᴘɪɴɢ :** `{ms} ms` \n┗━━━━━━━━━━━━━━┛\n"
        )
        await event.client.send_file(
            event.chat_id,
            PIC,
            caption=cat_caption,
            reply_to=reply_to_id,
            allow_cache=True,
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} Database :** `{check_sgnirts}`\n"
            f"**{EMOJI} Telethon Version :** `{version.__version__}\n`"
            f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
            f"**{EMOJI} Python Version :** `{python_version()}\n`"
            f"**{EMOJI} Uptime :** `{uptime}\n`"
            f"**{EMOJI} Master:** {mention}\n",
        )


@catub.cat_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    cat_caption = f"**Catuserbot is Up and Running**\n"
    cat_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
