"""No Logic Pligon for @PepeBot
\nCoding by Legend @NeoMatrix90
\nType .logic to see many logical fact
"""
from telethon import events
import asyncio
import random

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"logic", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.logic", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("`processing man wait 2sec can't you wait......`")
    await asyncio.sleep(2)
    x=(random.randrange(1,7))
    if x==1:
        await event.edit("`Do You Know, Some Mosquitos Became Ghosts, When you *Killed* Them...`")
    if x==2:
        await event.edit("`Do You Know, Mosquitoes has Teleportation Power...`")
    if x==3:
        await event.edit("`Do You Know, When you see a bearded Goat, that means you juat saw a *Smarter Goat* than YOU....`")
    if x==4:
        await event.edit("`Do You Know, when You give some ruppess to a Bus Conductor, He will give You a Piece of Paper, *Called Ticket*...`")
    if x==5:
        await event.edit("`Do You Know, Bus are called Bus, Because they are Bus....`")
    if x==6:
        await event.edit("`Do You Know, There's a Huge Difference between *Cartoon amd Anime*...`")
    if x==7:
        await event.edit("`Do You Know, We can't see Ghosts But Ghosts Can see Us...`")
