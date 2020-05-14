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
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    """ For .sdm command, make seflf-destructable messages. """
    if "|" in input_str:
        counter, text = input_str.split("|")
    else:
        await event.edit("Invalid Syntax. Module stopping.SYNTAX:`.sdm number | text`")
        return
    text = text.strip()
    counter = counter.strip()
    text = (
            text
       )
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    time.sleep(counter)
        await smsg.delete()

        
@borg.on(admin_cmd(pattern"selfd", outgoing=True  ))
async def selfdestruct(destroy):
    """ For .selfd command, make seflf-destructable messages. """
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        counter, text = input_str.split("|")
    else:
        await event.edit("Invalid Syntax. Module stopping.SYNTAX:`.selfd number | text`")
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
