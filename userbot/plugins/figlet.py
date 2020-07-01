import pyfiglet
from userbot.utils import admin_cmd
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="figlet ?(.*)", outgoing=True))
async def figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {"slant": "slant", "3D": "3-d", "5line": "5lineoblique", "alpha": "alphabet", "banner": "banner3-D", "doh": "doh", "iso": "isometric1", "letter": "letters", "allig": "alligator", "dotm": "dotmatrix", "bubble": "bubble", "bulb": "bulbhead", "digi": "digital"}
    input_str = event.pattern_match.group(1)
    if ":" in input_str:
        text, cmd = input_str.split(":", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await event.edit("Please add some text to figlet")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await event.edit("Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await event.respond("‌‌‎`{}`".format(result))
    await event.delete()

CMD_HELP.update({
    "figlet":
    ".figlet text or **.figlet text : type\
    \n USAGE:the types are slant, 3D , 5line , alpha , banner ,  doh ,  iso ,  letter , allig , dotm , bubble , bulb , digi\
    \n NOTE: Nospace must be given after : and type\
    \nEXAMPLE : `.figlet hello :digi`"
})    
