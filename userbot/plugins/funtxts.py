import nekos

from ..utils import admin_cmd


@borg.on(admin_cmd(pattern="tcat$"))
async def hmm(cat):
    if cat.fwd_from:
        return
    reactcat = nekos.textcat()
    await cat.edit(reactcat)


@borg.on(admin_cmd(pattern="why$"))
async def hmm(cat):
    if cat.fwd_from:
        return
    whycat = nekos.why()
    await cat.edit(whycat)


@borg.on(admin_cmd(pattern="fact$"))
async def hmm(cat):
    if cat.fwd_from:
        return
    factcat = nekos.fact()
    await cat.edit(factcat)
