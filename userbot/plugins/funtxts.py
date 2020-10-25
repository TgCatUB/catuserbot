import nekos

from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="tcat$"))
@borg.on(sudo_cmd(pattern="tcat$", allow_sudo=True))
async def hmm(cat):
    if cat.fwd_from:
        return
    reactcat = nekos.textcat()
    await edit_or_reply(cat, reactcat)


@borg.on(admin_cmd(pattern="why$"))
@borg.on(sudo_cmd(pattern="why$", allow_sudo=True))
async def hmm(cat):
    if cat.fwd_from:
        return
    whycat = nekos.why()
    await edit_or_reply(cat, whycat)


@borg.on(admin_cmd(pattern="fact$"))
@borg.on(sudo_cmd(pattern="fact$", allow_sudo=True))
async def hmm(cat):
    if cat.fwd_from:
        return
    factcat = nekos.fact()
    await edit_or_reply(cat, factcat)
