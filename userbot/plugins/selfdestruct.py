# For @UniBorg
# courtesy Yasir siddiqui
"""Self Destruct Plugin
.sd <time in seconds> <text>
"""


import time
from userbot import CMD_HELP
from telethon.errors import rpcbaseerrors
from userbot.utils import admin_cmd
import importlib.util



@borg.on(admin_cmd(pattern="sdm", outgoing=True  ))
async def selfdestruct(destroy):
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[5:7])
        text = str(destroy.text[7:])
        text = (
            text
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()  

        
@borg.on(admin_cmd(pattern="selfd", outgoing=True  ))
async def selfdestruct(destroy):
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[7:9])
        text = str(destroy.text[9:])
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

        
CMD_HELP.update({
    "selfdestruct":
    ".sdm number | [text]\
\nUsage: self destruct this message in number seconds \
\n\n.self number | [text]\
\nUsage:self destruct this message in number seconds with showing that it will destruct. \
"
})         
