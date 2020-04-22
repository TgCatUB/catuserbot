#autobio for @PhycoNinja13b, Edit bio strings Amigo if u use this plugin, Or else u are cursed :)
import asyncio
import time
from telethon import events
import random, re
from telethon.tl import functions
from telethon.errors import FloodWaitError
from userbot.utils import admin_cmd

from userbot import DEFAULT_BIO


DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else "set DEFAULT_BIO in heroku config vars "

DEL_TIME_OUT = 70


@borg.on(admin_cmd("autobio"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Changed Profile Picture"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
     
     
BIO_STRINGS = [
     "👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",
     "👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",

]


DEL_TIME_OUT = 30


@borg.on(admin_cmd(pattern="monkeybio"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    while True:
        bro = random.randint(0, len(BIO_STRINGS) - 1)    
        #input_str = event.pattern_match.group(1)
        Bio = BIO_STRINGS[bro]
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        #bio = f"📅 {DMY} | ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ | ⌚️ {HM}"
        logger.info(Bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=Bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Bio"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
