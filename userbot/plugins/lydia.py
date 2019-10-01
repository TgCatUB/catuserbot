import coffeehouse
import asyncio
from telethon import events

# Non-SQL Mode
ACC_LYDIA = {}
SESSION_ID = {}

if Var.LYDIA_API_KEY:
    api_key = Var.LYDIA_API_KEY
    api_client = coffeehouse.API(api_key)

@command(pattern="^.repcf", outgoing=True)
async def repcf(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    try:
        session = api_client.create_session()
        session_id = session.id
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought((session_id, msg))
        await event.edit("**Lydia says**: {0}".format(text_rep))
    except Exception as e:
        await event.edit(str(e))

@command(pattern="^.addcf", outgoing=True)
async def addcf(event):
    if event.fwd_from:
        return
    await event.edit("Running on Non-SQL mode for now...")
    await asyncio.sleep(4)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = api_client.create_session()
        session_id = session.id
        ACC_LYDIA.update({str(event.chat_id) + " " + str(reply_msg.from_id): session})
        SESSION_ID.update({str(event.chat_id) + " " + str(reply_msg.from_id): session_id})
        await event.edit("Lydia successfully enabled for user: {} in chat: {}".format(str(reply_msg.from_id), str(event.chat_id)))
    else:
        await event.edit("Reply to a user to activate Lydia AI on them")

@command(pattern="^.remcf", outgoing=True)
async def remcf(event):
    if event.fwd_from:
        return
    await event.edit("Running on Non-SQL mode for now...")
    await asyncio.sleep(4)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[str(event.chat_id) + " " + str(reply_msg.from_id)]
        del SESSION_ID[str(event.chat_id) + " " + str(reply_msg.from_id)]
        await event.edit("Lydia successfully disabled for user: {} in chat: {}".format(str(reply_msg.from_id), str(event.chat_id)))
    except KeyError:
        await event.edit("This person does not have Lydia activated on him/her.")

@bot.on(events.NewMessage(incoming=True))
async def user(event):
    user_chat = str(event.chat_id)
    user_id = str(event.from_id)
    user_text = event.text
    for i in ACC_LYDIA:
        data = i.split(" ")
        if user_chat == data[0]:
            if user_id == data[1]:
                session = ACC_LYDIA[i]
                session_id = SESSION_ID[i]
                text_rep = session.think_thought((session_id, user_text))
                await event.edit(text_rep)

