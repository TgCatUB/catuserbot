from telethon import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest



@bot.on(admin_cmd(pattern="add ?(.*)"))
@bot.on(sudo_cmd(pattern="add ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await edit_delete(
            event, "`.invite` users to a chat, not to a Private Message", 5
        )
    else:
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await edit_delete(event, f"`{str(e)}`", 5)
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await edit_delete(event, f"`{str(e)}`", 5)

        await edit_or_reply(event, f"`{to_add_users} is/are Invited Successfully`")
     
async def get_users(event):
    sender = await event.get_sender()
        me = await event.client.get_me()
            if not sender.id == me.id:
                    
await edit_delete(event, "`processing...`")
                        else:
                                await edit_or_delete(event, "`processing...`")
                                    await get_chatinfo(event)
                                        chat = await event.get_chat()
                                            if event.is_private:

event, "`.invite` users to a chat, not to a Private Message", 5
        )
                                                        s = 0
                                                            f = 0
                                                                error = "None"
    await edit_delete("**TerminalStatus**\n\n`Collecting Users.......`")
        async for user in event.client.iter_participants(kraken.full_chat.id):
                try:
                            if error.startswith("Too"):
                                            return await edit_delete(
                                                                f"**Terminal Finished With Error**\n(`May Got Limit Error from telethon Please try agin Later`)\n**Error** : \n`{error}`\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people"
                                                                                )
                                                                                            await event.client(
                                                                                                            functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
                                                                                                                        )
                                                                                                                                    s = s + 1
                                                                                                                                                await edit_delete(
                                                                                                                                                                f"**Terminal Running...**\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people\n\n**× LastError:** `{error}`"
                                                                                                                                                                            )
                                                                                                                                                                                    except Exception as e:
                                                                                                                                                                                                error = str(e)
                                                                                                                                                                                                            f = f + 1
                                                                                                                                                                                                                return await edit_delete(
                                                                                                                                                                                                                        f"**Terminal Finished** \n\n• Successfully Invited `{s}` people \n• failed to invite `{f}` people"
     )

CMD_HELP.update(
    {
        "add": """**Plugin : **`add`

  •  **Syntax : **`.add username(s)/userid(s)`
  •  **Function : **__Add the given user/users to the group where u used the command__
"""
    }
)
