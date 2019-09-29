@command(pattern="^.alive", outgoing=True)
async def hello_world(event):
    if event.fwd_from:
        return
    await event.edit("**HELLO WORLD**\n\nThe following is controlling me too!\n" + str(event.from_id) + " " + Var.SUDO_USERS)
