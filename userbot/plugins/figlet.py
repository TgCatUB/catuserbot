import pyfiglet
from . import deEmojify

@bot.on(admin_cmd(pattern="figlet (\w+) (.+)", outgoing=True))
@bot.on(sudo_cmd(pattern="figlet (\w+) (.+)", allow_sudo=True))
async def figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "basic": "basic",
        "binary": "binary",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    style = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    try:
        font = style_list[style]
    except KeyError:
        return await edit_delete(event , "**Invalid styleselected**, __Check__ `.info figlet`.")
    result = pyfiglet.figlet_format(deEmojify(text), font=font)
    await event.respond(f"‌‌‎`{result}`")
    await event.delete()


CMD_HELP.update(
    {
        "figlet": "**Plugin :**`figlet`\
        \n\n• **Syntax : **`.figlet text or .figlet text ; type`\
    \n• **Usage : **the types are `slant`, `3D`, `5line`, `alpha`, `banner`, `doh`, `iso`, `letter`, `allig`, `dotm`, `bubble`, `bulb`, `digi`, `binary`, `basic`\
    \n• **Example : **`.figlet hello ; digi`"
    }
)
