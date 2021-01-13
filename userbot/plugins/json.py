# yaml_format is ported from uniborg
@bot.on(admin_cmd(pattern="json$"))
@bot.on(sudo_cmd(pattern="json$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = catevent.stringify()
    await edit_or_reply(event, the_real_message, parse_mode=parse_pre)


@bot.on(admin_cmd(pattern="yaml$"))
@bot.on(sudo_cmd(pattern="yaml$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = _format.yaml_format(catevent)
    await edit_or_reply(event, the_real_message, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "json": """**Plugin : **`json`

  •  **Syntax : **`.json reply`
  •  **Function : **__reply to a message to get details of that message in json format__  

  •  **Syntax : **`.yaml reply`
  •  **Function : **__reply to a message to get details of that message in yaml format__ """
    }
)
