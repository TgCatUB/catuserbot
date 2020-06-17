"""Send Chat Actions
Syntax: .fake <option>
        fake options: Options for fake

typing
contact
game
location
voice
round
video
photo
document
cancel"""

import asyncio
from userbot.utils import admin_cmd
from userbot import CMD_HELP
from random import  randint
 
@borg.on(admin_cmd(pattern="scam ?(.*)"))
async def scam(event):
    """ Just a small command to fake chat actions for fun !! """
    options = [
        'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
        'photo', 'document', 'cancel'
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:  # Let bot decide action and time
        scam_action = choice(options)
        scam_time = randint(30, 60)
    elif len(args) == 1:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:  # User decides both action and time
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("`Invalid Syntax !!`")
        return
    try:
        if (scam_time > 0):
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return
        
        
CMD_HELP.update({
    "scam":
    ".scam <action> <time>\
    \nUsage: Type .scam (action name) this shows the fake action in the group  the actions are typing ,contact ,game, location, voice, round, video,photo,document, cancel.\
    "
})            
