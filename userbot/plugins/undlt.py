import asyncio


@bot.on(admin_cmd(pattern="undlt ?(.*)"))
@bot.on(sudo_cmd(pattern="undlt ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        try:
            cat = int(event.pattern_match.group(1))
            input_str = cat
        except Exception:
            input_str = 5
    else:
        input_str = 5
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=input_str, search="", edit=False, delete=True
        )
        for i in a:
            await event.reply(i.original.action.message)
    else:
        event = await edit_or_reply(
            event, "`You need administrative permissions in order to do this command`"
        )
        await asyncio.sleep(3)
        await event.delete()


CMD_HELP.update(
    {
        "undlt": "**Plugin :** `undlt`\
        \n**Syntax : **`.undlt <count>`\
        \n**Usage: **Fetches last <count> number of deleted messages and sends you(you must be admin in that group)  \
"
    }
)
