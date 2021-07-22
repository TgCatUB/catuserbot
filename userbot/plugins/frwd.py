from userbot.utils import admin_cmd


@bot.on(admin_cmd(incoming=True))
async def _(event):
    from_chnl = -1001562866430
    if not event.is_private and event.chat_id == from_chnl:
        target_chnl = -1001489788469
        await event.client.send_message(target_chnl, event.message)
