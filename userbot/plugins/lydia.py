import coffeehouse

@command(pattern="^.repcf", outgoing=True)
async def cf(event):
    if event.fwd_from:
        return
    await event.edit("Proccessing...")
    try:
        api_key = Var.LYDIA_API_KEY
        api_client = coffeehouse.API(api_key)
        session = api_client.create_session()
        session_id = session.id
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought(session_id, msg)
        await event.edit("**Lydia says**: {}".format(text_rep))
    except Exception as e:
        await event.edit(str(e))
