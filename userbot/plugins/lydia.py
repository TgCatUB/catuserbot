import coffeehouse

@command(pattern="^.repcf", outgoing=True)
async def cf(event):
    if event.fwd_from:
        return
    try:
        api_key = Var.LYDIA_API_KEY
        api_client = coffeehouse.API(api_key)
        cf_session = api_client.create_session()
        reply = event.get_reply_message()
        text_rep = session.think_thought(session.id, reply.text)
        await event.edit("**Lydia says**: {0}".format(text_rep))
    except:
        return
