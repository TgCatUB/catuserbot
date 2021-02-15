try:
    from pyjokes import get_joke
except:
    install_pip("pyjokes") 
    from pyjokes import get_joke

from ..utils import admin_cmd , sudo_cmd
from . import CMD_HELP

@bot.on(admin_cmd("joke$",outgoing = True))
@bot.on(sudo_cmd(pattern="joke$", allow_sudo=True))
async def _(event):
    await edit_or_reply(event , get_joke())

CMD_HELP.update({
    "jokes":"**Plugin : **`jokes`\
    \n\n  •  **Syntax : **`.joke`\
    \n  •  **Function : **__Sends some random joke__"
})