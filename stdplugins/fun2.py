"""COMMAND : .runs , .metoo , .pro """

from telethon import events
import random, re
from uniborg.util import admin_cmd

METOOSTR = [
    "`Me too thanks`",
    "`Haha yes, me too`",
    "`Same lol`",
    "`Me `",
    "`Same here`",
    "`Haha yes`",
    "`Same pinch `",
]
RUNSREACTS = [
    "`Runs to Thanos`",
    "`Runs to Modiji For Achey Din`",
    "`Runs far, far away from earth`",
    "`Running faster than usian bolt coz I'mma Bot`",
    "`Runs to no one`",
    "`This Group is too cancerous to deal with.`",
    "`Cya boss`",
    "`I am a mad person. Plox Ban me.`",
    "`I go away`",
    "`I am just walking off, coz me is too healthy.`",
    "`I switch off!`",
]
PRO_STRINGS = [
     "`You is pro user.`",
     "`Pros here -_- Time to Leave`",
     "`Pros everywhere`",
]
INSULT_STRINGS = [ 
    "`Owww ... Such a stupid idiot.`",
    "`Don't drink and type.`",
    "`Command not found. Just like your brain.`",
    "`Bot rule 544 section 9 prevents me from replying to stupid humans like you.`",
    "`Sorry, we do not sell brains.`",
    "`Believe me you are not normal.`",
    "`I bet your brain feels as good as new, seeing that you never use it.`",
    "`If I wanted to kill myself I'd climb your ego and jump to your IQ.`",
    "`You didn't evolve from apes, they evolved from you.`",
    "`What language are you speaking? Cause it sounds like bullshit.`",
    "`You are proof that evolution CAN go in reverse.`",
    "`I would ask you how old you are but I know you can't count that high.`",
    "`As an outsider, what do you think of the human race?`",
    "`Ordinarily people live and learn. You just live.`",
    "`Keep talking, someday you'll say something intelligent!.......(I doubt it though)`",
    "`Everyone has the right to be stupid but you are abusing the privilege.`",
    "`I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.`",
    "`You should try tasting cyanide.`",
    "`You should try sleeping forever.`",
    "`Pick up a gun and shoot yourself.`",
    "`Try bathing with Hydrochloric Acid instead of water.`",
    "`Go Green! Stop inhaling Oxygen.`",
    "`God was searching for you. You should leave to meet him.`",
    "`You should Volunteer for target in an firing range.`",
    "`Try playing catch and throw with RDX its fun.`",
]
# ===========================================
                          

@borg.on(admin_cmd(pattern="runs ?(.*)",allow_sudo=True))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(RUNSREACTS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = RUNSREACTS[bro]
    await event.edit(reply_text)


@borg.on(admin_cmd(pattern="metoo ?(.*)",allow_sudo=True))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(METOOSTR) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = METOOSTR[bro]
    await event.edit(reply_text)

		  
			  
@borg.on(admin_cmd(pattern="pro ?(.*)",allow_sudo=True))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(PRO_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = PRO_STRINGS[bro]
    await event.edit(reply_text)


@borg.on(admin_cmd(pattern="insult ?(.*)",allow_sudo=True))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(INSULT_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = INSULT_STRINGS[bro]
    await event.edit(reply_text)
			  
