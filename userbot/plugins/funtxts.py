import nekos
from ..utils import admin_cmd

@borg.on(admin_cmd(pattern = "reactcat$"))
async def hmm(cat):
    if cat.fwd_from:
        return
    reactcat = nekos.textcat()
    await cat.edit(reactcat)
    
@borg.on(admin_cmd(pattern = "why$"))
async def hmm(cat):    
    if cat.fwd_from:
        return
    reactcat = nekos.why()
    await cat.edit(why)
    
@borg.on(admin_cmd(pattern = "fact$"))
async def hmm(cat):    
    if cat.fwd_from:
        return
    reactcat = nekos.fact()
    await cat.edit(why)    
