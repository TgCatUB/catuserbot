import pyfiglet

from . import deEmojify

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


@bot.on(admin_cmd(pattern="figlet(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="figlet(?: |$)(.*)", allow_sudo=True))
async def figlet(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if ";" in input_str:
        cmd, text = input_str.split(";", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await edit_or_reply(event, "`Give some text to change it`")
        return
    style = cmd
    text = text.strip()
    if style is not None:
        try:
            font = CMD_FIG[style.strip()]
        except KeyError:
            return await edit_delete(
                event, "**Invalid style selected**, __Check__ `.info figlet`."
            )
        result = pyfiglet.figlet_format(deEmojify(text), font=font)
    else:
        result = pyfiglet.figlet_format(deEmojify(text))
    await edit_or_reply(event, result, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "figlet": "**Plugin :**`figlet`\
        \n\n• **Syntax : **`.figlet type ; text`\
    \n• **Usage : **the types are `slant`, `3D`, `5line`, `alpha`, `banner`, `doh`, `iso`, `letter`, `allig`, `dotm`, `bubble`, `bulb`, `digi`, `binary`, `basic`\
    \n• **Example : **`.figlet digi ; hello`"
    }
)
