# For @UniBorg
# (c) Shrimadhav U K

from telethon import events, functions, types
import asyncio


@borg.on(events.NewMessage(pattern=r"\-listmyusernames", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.channels.GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    await event.edit(output_str)
