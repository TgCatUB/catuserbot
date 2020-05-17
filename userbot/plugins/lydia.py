from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
import asyncio
from telethon import events
from userbot import CMD_HELP

# Non-SQL Mode
ACC_LYDIA = {}

if Var.LYDIA_API_KEY:
    api_key = Var.LYDIA_API_KEY
    api_client = API(api_key)
    lydia = LydiaAI(api_client)


@command(pattern="^.addcf", outgoing=True)
async def addcf(event):
    if event.fwd_from:
        return
    await event.edit("Running on Non-SQL mode for now...")
    await asyncio.sleep(2)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = lydia.create_session()
        session_id = session.id
        if reply_msg.from_id is None:
            return await event.edit("Invalid user type.")
        ACC_LYDIA.update({(event.chat_id & reply_msg.from_id): session})
        await event.edit("auto reply succesfully enabled")
    else:
        await event.edit("Reply to a user to activate Lydia AI on them")

@command(pattern="^.remcf", outgoing=True)
async def remcf(event):
    if event.fwd_from:
        return
    await event.edit("Running on Non-SQL mode for now...")
    await asyncio.sleep(2)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[event.chat_id & reply_msg.from_id]
        await event.edit("auto reply disabled")
    except Exception:
        await event.edit("This person does not have Lydia activated on him/her.")


@bot.on(events.NewMessage(incoming=True))
async def user(event):
    user_text = event.text
    try:
        session = ACC_LYDIA[event.chat_id & event.from_id]
        msg = event.text
        async with event.client.action(event.chat_id, "typing"):
            text_rep = session.think_thought(msg)
            wait_time = 0
            for i in range(len(text_rep)):
                wait_time = wait_time + 0.1
            await asyncio.sleep(wait_time)
            await event.reply(text_rep)
    except (KeyError, TypeError):
        return
    
    
    
CMD_HELP.update({
    "lydia":
    ".addcf reply to a user\
    \nUSAGE: your bot will auto reply to the tagged user until you stops it by `.remcf`\
    \n\n.remcf reply to the user to who you want to disable the lydia\
    \n\n for functioning this plugin you need to set the heroku var\
    \n the key is `LYDIA_API_KEY` and get var from `https://coffeehouse.intellivoid.net/`\
"
})    
    
