# For @UniBorg
# courtesy Yasir siddiqui
"""Self Destruct Plugin
.sd <time in seconds> <text>
"""


import time

from telethon.errors import rpcbaseerrors
from userbot.utils import admin_cmd
import importlib.util



@borg.on(admin_cmd("sd", outgoing=True  ))
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[4:6])
        text = str(destroy.text[6:])
        text = (
            text
            + "\n\n`This message shall be self-destructed in "
            + str(counter)
            + " seconds`"
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()
