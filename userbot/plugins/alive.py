"""Check if userbot alive or not . """
import os
import time
import asyncio
from telethon import events
from userbot import StartTime , catdef, catversion
from userbot import ALIVE_NAME, CMD_HELP
from userbot.utils import admin_cmd
from telethon import version
from platform import python_version, uname

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"

ALIVE_PIC = os.environ.get("ALIVE_PIC", None)
CAT_IMG = ALIVE_PIC

@borg.on(admin_cmd(outgoing=True, pattern="alive$"))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = alive.message
    uptime = catdef.get_readable_time((time.time() - StartTime))
    if alive.reply_to_msg_id:
        reply_to_id = await alive.get_reply_message()

    if CAT_IMG:
         cat_caption = "🚴‍♂️**MY BOT IS RUNNING SUCCESFULLY**\n\n"
         cat_caption += "⏳`Database Status :` Databases Functioning Normally!\n"   
         cat_caption += f"⏳`Telethon Version:` **{version.__version__}**\n"
         cat_caption += f"⏳`Python Version:` **{python_version()}**\n"
         cat_caption += f"⏳`CatUserbot Version`: **{catversion}**\n"
         cat_caption += f"⏳`Cat Uptime`: **{uptime}**\n"         
         cat_caption += "💠**Cat is Always With You, My Masters!**\n"
         cat_caption += "⏳`Modified by :` [✰Sᴀͥʀᴀͣᴛͫʜ™️✰](http://t.me/Sur_vivor)\n"
         cat_caption += "⏳`Created by :` Snapdragon, Anubis, Sandeep\n"
         cat_caption += f"⏳`Owner Name :` {DEFAULTUSER}\n\n"
         cat_caption += "**[⚜️DEPLOY CATUSERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)**"
         await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption)
         await alive.delete()
    else:
        await alive.edit("🚴‍♂️**MY BOT IS RUNNING SUCCESFULLY**\n\n"
                         "⏳`Database Status :` Databases Functioning Normally!\n"
                         f"⏳`Telethon Version:` **{version.__version__}**\n"
                         f"⏳`Python Version:` **{python_version()}**\n"
                         f"⏳`Catuserbot Version`: **{catversion}**\n"
                         f"⏳`Cat Uptime`: **{uptime}**\n"                        
                         "💠**Cat is Always With You, My Masters!**\n"
                         "⏳`Modified by :` [✰Sᴀͥʀᴀͣᴛͫʜ™️✰](http://t.me/Sur_vivor)\n"
                         "⏳`Created by :` Snapdragon, Anubis, Sandeep\n"
                         f"⏳`Owner Name :` {DEFAULTUSER}\n\n"
                         "**[⚜️DEPLOY CATUSERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)**"
                        )

CMD_HELP.update({"alive": "`.alive` :\
      \nUSAGE: Type .alive to see wether your bot is working or not. "
})
