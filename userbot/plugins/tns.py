from userbot.utils import admin_cmd


@bot.on(admin_cmd(incoming=True))
async def _(event):
    from_chnl = -1001592228587
    if not event.is_private and event.chat_id == from_chnl:
        target_chnl = -1001445526942
        pluto = await event.client.send_message(target_chnl, event.message)
        await event.client.pin_message(target_chnl, pluto)
