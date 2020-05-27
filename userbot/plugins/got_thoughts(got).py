# BY @Deonnn
"""
Game of Thrones Thoughts plugin
by @Deonnn
command .gott

"""

from telethon import events
from userbot import CMD_HELP 
import asyncio

import os

import sys

import random


from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"gott", allow_sudo=True))

async def _(event):

    if event.fwd_from:

        return

    await event.edit("Typing...")

    await asyncio.sleep(2)

    x=(random.randrange(1,40))

    if x==1:

        await event.edit("`\"The man who passes the sentence should swing the sword.\"`")

    if x==2:

        await event.edit("`\"When the snows fall and the white winds blow, the lone wolf dies but the pack survives!\"`")

    if x==3:

        await event.edit("`\"The things I do for love!\"`")

    if x==4:

        await event.edit("`\"I have a tender spot in my heart for cripples, bastards and broken things.\"`")

    if x==5:

        await event.edit("`\"Death is so terribly final, while life is full of possibilities.\"`")

    if x==6:

        await event.edit("`\"Once you’ve accepted your flaws, no one can use them against you.\"`")

    if x==7:

        await event.edit("`\"If I look back I am lost.\"`")    

    if x==8:

        await event.edit("`\"When you play the game of thrones, you win or you die.\"`")

    if x==9:

        await event.edit("`\"I grew up with soldiers. I learned how to die a long time ago.\"`")

    if x==10:

        await event.edit("`\"What do we say to the Lord of Death?\nNot Today!\"`")
        
    if x==11:

        await event.edit("`\"Every flight begins with a fall.\"`")
        
    if x==12:

        await event.edit("`\"Different roads sometimes lead to the same castle.\"`")
        
    if x==13:

        await event.edit("`\"Never forget what you are. The rest of the world will not. Wear it like armour, and it can never be used to hurt you.\"`")
        
    if x==14:

        await event.edit("`\"The day will come when you think you are safe and happy, and your joy will turn to ashes in your mouth.\"`")
        
    if x==15:

        await event.edit("`\"The night is dark and full of terrors.\"`")
        
    if x==16:

        await event.edit("`\"You know nothing, Jon Snow.\"`")
        
    if x==17:

        await event.edit("`\"Night gathers, and now my watch begins!\"`")
        
    if x==18:

        await event.edit("`\"A Lannister always pays his debts.\"`")
        
    if x==19:

        await event.edit("`\"Burn them all!\"`")
        
    if x==20:

        await event.edit("`\"What do we say to the God of death?\"`")
        
    if x==21:

        await event.edit("`\"There's no cure for being a c*nt.\"`")
        
    if x==22:

        await event.edit("`\"Winter is coming!\"`")
        
    if x==23:

        await event.edit("`\"That's what I do: I drink and I know things.\"`")
        
    if x==24:

        await event.edit("`\"I am the dragon's daughter, and I swear to you that those who would harm you will die screaming.\"`")
        
    if x==25:

        await event.edit("`\"A lion does not concern himself with the opinion of sheep.\"`")
        
    if x==26:

        await event.edit("`\"Chaos isn't a pit. Chaos is a ladder.\"`")
    
    if x==27:

        await event.edit("`\"I understand that if any more words come pouring out your c*nt mouth, I'm gonna have to eat every f*cking chicken in this room.\"`")
        
    if x==28:

        await event.edit("`\"If you think this has a happy ending, you haven't been paying attention.\"`")
        
    if x==29:

        await event.edit("`\"If you ever call me sister again, I'll have you strangled in your sleep.\"`")
        
    if x==30:

        await event.edit("`\"A girl is Arya Stark of Winterfell. And I'm going home.\"`")
        
    if x==31:

        await event.edit("`\"Any man who must say 'I am the King' is no true King.\"`")
        
    if x==32:

        await event.edit("`\"If I fall, don't bring me back.\"`")
        
    if x==33:

        await event.edit("`\"Lannister, Targaryen, Baratheon, Stark, Tyrell... they're all just spokes on a wheel. This one's on top, then that one's on top, and on and on it spins, crushing those on the ground.\"`")
        
    if x==34:

        await event.edit("`\"Hold the door!`")
        
    if x==35:

        await event.edit("`\"When people ask you what happened here, tell them the North remembers. Tell them winter came for House Frey.\"`")
        
    if x==36:

        await event.edit("`\"Nothing f*cks you harder than time.\"`")
        
    if x==37:

        await event.edit("`\"There is only one war that matters. The Great War. And it is here.\"`")
        
    if x==38:

        await event.edit("`\"Power is power!\"`")
        
    if x==39:

        await event.edit("`\"I demand a trial by combat!\"`")
        
    if x==40:

        await event.edit("`\"I wish I was the monster you think I am!\"`")
    if x==41:
        await event.edit("Never forget what you are. The rest of the world will not.Wear it like armor,\n and it can never be used to hurt you.")
    if x==42:
        await event.edit("There is only one thing we say to death: **Not today.**")
    if x==43:
        await event.edit("If you think this has a happy ending, you haven’t been **paying attention**.")
    if x==44:
        await event.edit("Chaos isn’t a pit. Chaos is a ladder.")
    if x==45:
        await event.edit("You know nothing, **Jon Snow**")
    if x==46:
        await event.edit("**Winter** is coming.")
    if x==47:
        await event.edit("When you play the **game of thrones**, you win or you die.")    
    if x==48:
        await event.edit("I'm not going to **stop** the wheel, I'm going to **break** the wheel.")
    if x==49:
        await event.edit("When people ask you what happened here, tell them the **North remembers**. Tell them winter came for **House Frey**.")
    if x==50:
        await event.edit("When the snows fall and the white winds blow,\n the lone wolf dies, but the pack **survives**.")
    
