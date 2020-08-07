import nekos
from ..utils import admin_cmd

@borg.on(admin_cmd(pattern = "reactcat$")
async def hmm(cat):
    if cat.fwd_from:
        return
    reactcat = nekos.textcat()
    await cat.edit(reactcat)
