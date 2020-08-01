import asyncio
from telethon import events
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd
from userbot import CMD_HELP

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"

@borg.on(admin_cmd(pattern="scam ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    input_str = event.pattern_match.group(1)
    action = "typing"
    if input_str:
        action = input_str
    async with borg.action(event.chat_id, action):
        await asyncio.sleep(86400)  # type for 10 seconds        
     
@borg.on(admin_cmd(pattern="prankpromote ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    to_promote_id = None
    rights = ChatAdminRights(
        post_messages=True
    )
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_promote_id = r_mesg.sender_id
    elif input_str:
        to_promote_id = input_str
    try:
        await borg(EditAdminRequest(event.chat_id, to_promote_id, rights, ""))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit("Successfully Promoted")
        
@borg.on(admin_cmd(pattern=f"padmin$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 20)
    await event.edit("promoting.......")
    animation_chars = [
            "**Promoting User As Admin...**",
            "**Enabling All Permissions To User...**",
            "**(1) Send Messages: ☑️**",
            "**(1) Send Messages: ✅**",
            "**(2) Send Media: ☑️**",
            "**(2) Send Media: ✅**",
            "**(3) Send Stickers & GIFs: ☑️**",
            "**(3) Send Stickers & GIFs: ✅**",    
            "**(4) Send Polls: ☑️**",
            "**(4) Send Polls: ✅**",
            "**(5) Embed Links: ☑️**",
            "**(5) Embed Links: ✅**",
            "**(6) Add Users: ☑️**",
            "**(6) Add Users: ✅**",
            "**(7) Pin Messages: ☑️**",
            "**(7) Pin Messages: ✅**",
            "**(8) Change Chat Info: ☑️**",
            "**(8) Change Chat Info: ✅**",
            "**Permission Granted Successfully**",
            f"**pRoMooTeD SuCcEsSfUlLy bY: {DEFAULTUSER}**"
 ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 20])
                
CMD_HELP.update({
    "fake":
    ".scam <action> \
    \n**USAGE : **Type .scam (action name) this shows the fake action in the group  the actions are typing ,contact ,game, location, voice, round, video,photo,document, cancel.\
    \n\n`.prankpromote` reply to user to who you want to prank promote\
    \n**USAGE : **it promotes him to admin but he will not have any permission to take action that is he can see rection actions but cant take any admin action\
    \n\n`.padmin`\
    \n**USAGE : ** An animation that shows enableing all permissions to him that he is admin(fake promotion)\
    "
})            
