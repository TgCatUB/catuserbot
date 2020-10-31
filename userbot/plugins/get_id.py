from telethon.utils import pack_bot_file_id

from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@bot.on(admin_cmd(pattern="(get_id|id)( (.*)|$)"))
@bot.on(sudo_cmd(pattern="(get_id|id)( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(2)
    if input_str:
        p = await event.client.get_entity(input_str)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"The id of the user `{input_str}` is `{p.id}`"
                )
        except:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"The id of the chat/channel `{p.title}` is `{p.id}`"
                    )
            except:
                pass
        await edit_or_reply(event, "`Either give input as username or reply to user`")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                "Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id), bot_api_file_id
                ),
            )
        else:
            await edit_or_reply(
                event,
                "Current Chat ID: `{}`\nFrom User ID: `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                ),
            )
    else:
        await edit_or_reply(event, "Current Chat ID: `{}`".format(str(event.chat_id)))
