"""Auto Profile Updation Commands
.autoname"""
from telethon import events
import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
from userbot.utils import admin_cmd
from userbot import AUTONAME


DEL_TIME_OUT = 60
DEFAULTUSER = str(AUTONAME) 


@borg.on(admin_cmd(pattern="autoname"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"Auto Name has been started by my Master") 

    while True:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"{HM} {DEFAULTUSER} {DM}"
        logger.info(name)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                first_name=name
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
    
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Name"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
    
