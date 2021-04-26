import random

from . import ALIVE_NAME, catmemes

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


@bot.on(admin_cmd(pattern="congo$"))
@bot.on(sudo_cmd(pattern="congo$", allow_sudo=True))
async def _(e):
    txt = random.choice(catmemes.CONGOREACTS)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="shg$"))
@bot.on(sudo_cmd(pattern="shg$", allow_sudo=True))
async def shrugger(e):
    txt = random.choice(catmemes.SHGS)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="runs$"))
@bot.on(sudo_cmd(pattern="runs$", allow_sudo=True))
async def runner_lol(e):
    txt = random.choice(catmemes.RUNSREACTS)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="noob$"))
@bot.on(sudo_cmd(pattern="noob$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(catmemes.NOOBSTR)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="insult$"))
@bot.on(sudo_cmd(pattern="insult$", allow_sudo=True))
async def insult(e):
    txt = random.choice(catmemes.INSULT_STRINGS)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="hey$"))
@bot.on(sudo_cmd(pattern="hey$", allow_sudo=True))
async def hoi(e):
    txt = random.choice(catmemes.HELLOSTR)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="pro$"))
@bot.on(sudo_cmd(pattern="pro$", allow_sudo=True))
async def proo(e):
    txt = random.choice(catmemes.PRO_STRINGS)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(pattern=f"react ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="react ?(.*)", allow_sudo=True))
async def _(e):
    input_str = e.pattern_match.group(1)
    if input_str in "happy":
        emoticons = catmemes.FACEREACTS[0]
    elif input_str in "think":
        emoticons = catmemes.FACEREACTS[1]
    elif input_str in "wave":
        emoticons = catmemes.FACEREACTS[2]
    elif input_str in "wtf":
        emoticons = catmemes.FACEREACTS[3]
    elif input_str in "love":
        emoticons = catmemes.FACEREACTS[4]
    elif input_str in "confused":
        emoticons = catmemes.FACEREACTS[5]
    elif input_str in "dead":
        emoticons = catmemes.FACEREACTS[6]
    elif input_str in "sad":
        emoticons = catmemes.FACEREACTS[7]
    elif input_str in "dog":
        emoticons = catmemes.FACEREACTS[8]
    else:
        emoticons = catmemes.FACEREACTS[9]
    txt = random.choice(emoticons)
    await edit_or_reply(e, txt)


@bot.on(admin_cmd(outgoing=True, pattern="10iq$"))
@bot.on(sudo_cmd(pattern="10iq$", allow_sudo=True))
async def iqless(e):
    await edit_or_reply(e, "♿")


@bot.on(admin_cmd(pattern="fp$"))
@bot.on(sudo_cmd(pattern=f"fp$", allow_sudo=True))
async def facepalm(e):
    await e.edit("🤦‍♂")


@bot.on(admin_cmd(outgoing=True, pattern="bt$"))
@bot.on(sudo_cmd(pattern="bt$", allow_sudo=True))
async def bluetext(e):
    """Believe me, you will find this useful."""
    if e.is_group:
        await edit_or_reply(
            e,
            "/BLUETEXT /MUST /CLICK.\n"
            "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS?",
        )


@bot.on(admin_cmd(pattern="session$"))
@bot.on(sudo_cmd(pattern="session$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**telethon.errors.rpcerrorlist.AuthKeyDuplicatedError: The authorization key (session file) was used under two different IP addresses simultaneously, and can no longer be used. Use the same session exclusively, or use different sessions (caused by GetMessagesRequest)**"
    await event.edit(mentions)


CMD_HELP.update(
    {
        "memestext": "**Plugin : **`memestext`\
        \n\n  •  **Syntax :** `.congo`\
        \n  •  **Function : **Congratulate the people.\
        \n\n  •  **Syntax :** `.shg`\
        \n  •  **Function : **Shrug at it !!\
        \n\n  •  **Syntax :** `.runs`\
        \n  •  **Function : **Run, run, RUNNN!\
        \n\n  •  **Syntax :** `.noob`\
        \n  •  **Function : **Whadya want to know? Are you a NOOB?\
        \n\n  •  **Syntax :** `.insult`\
        \n  •  **Function : **insult someone\
        \n\n  •  **Syntax :** `.hey`\
        \n  •  **Function : **start a conversation with people\
        \n\n  •  **Syntax :** `.pro`\
        \n  •  **Function : **If you think you're pro, try this.\
        \n\n  •  **Syntax :** `.react` <type>\
        \n  •  **Function : **Make your userbot react. types are <happy ,think ,wave ,wtf ,love ,confused,dead, sad,dog>\
        \n\n  •  **Syntax :** `.10iq`\
        \n  •  **Function : **You retard !!\
        \n\n  •  **Syntax :** `.fp`\
        \n  •  **Function : **send you face pam emoji!\
        \n\n  •  **Syntax :** `.bt`\
        \n  •  **Function : **Believe me, you will find this useful.\
        \n\n  •  **Syntax :** `.session`\
        \n  •  **Function : **telethon session error code(fun)\
        "
    }
)
