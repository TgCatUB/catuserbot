from telethon.tl.functions.messages import SaveDraftRequest

from . import catub

plugin_category = "tools"


@catub.cat_cmd(
    pattern="chain$",
    command=("chain", plugin_category),
    info={
        "header": "Reply this command to any converstion(or message) and it will find the chain length of that message",
        "usage": "{tr}chain <reply>",
    },
)
async def _(event):
    "To find the chain length of a message."
    await event.edit("`Counting...`")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await event.edit(f"Chain length: `{count}`")
