import asyncio


@bot.on(admin_cmd(pattern="undlt"))
@bot.on(sudo_cmd(pattern="undlt", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await borg.get_admin_log(
            event.chat_id, limit=7, search="", edit=False, delete=True
        )
        for i in a:
            await event.reply(i.original.action.message)
    else:
        await edit_or_reply(event, "You need administrative permissions in order to do this command"
        )
        await asyncio.sleep(3)
        await event.delete()

CMD_HELP.update(
       {
           "undlt":   """**plugin : **`undlt`

     •**Syntax: **`!undlt`
     •**Function: **Sends 7 recently deleted messages in a group. Admin privileges required
     """
        }
        )
