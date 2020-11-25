import nekos

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP


@bot.on(admin_cmd(pattern="tcat$"))
@bot.on(sudo_cmd(pattern="tcat$", allow_sudo=True))
async def hmm(cat):
    if cat.fwd_from:
        return
    reactcat = nekos.textcat()
    await edit_or_reply(cat, reactcat)


@bot.on(admin_cmd(pattern="why$"))
@bot.on(sudo_cmd(pattern="why$", allow_sudo=True))
async def hmm(cat):
    if cat.fwd_from:
        return
    whycat = nekos.why()
    await edit_or_reply(cat, whycat)


@bot.on(admin_cmd(pattern="fact$"))
@bot.on(sudo_cmd(pattern="fact$", allow_sudo=True))
async def hmm(cat):
    if cat.fwd_from:
        return
    factcat = nekos.fact()
    await edit_or_reply(cat, factcat)


CMD_HELP.update(
    {
        "funtxts": """__**PLUGIN NAME :** Funtxts__
\n\n📌** CMD ➥** `.tcat`
\n**USAGE   ➥  **__Sens you some random cat facial text art__
\n\n📌** CMD ➥** `.why`
\n**USAGE   ➥  **__Asks some random Funny questions__
\n\n📌** CMD ➥** `.fact`
\n**USAGE   ➥  **__Sends you some random facts__"""
    }
)
