from telethon.tl.functions.messages import SaveDraftRequest

from ..core.managers import edit_delete, edit_or_reply
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
async def chain(event):
    "To find the chain length of a message."
    msg = await event.get_reply_message()
    if not msg:
        return await edit_delete(event, "```reply to a message```", 10)
    chat = (await catub.get_entity(event.chat_id)).id
    msg_id = msg.id
    await edit_or_reply(event, "`Counting...`")
    count = -1
    if msg.reply_to:
        msg_id = msg.reply_to.reply_to_msg_id
        if msg.reply_to.reply_to_top_id:
            msg_id = msg.reply_to.reply_to_top_id
    thread = f"https://t.me/c/{chat}/{msg_id}?thread={msg_id}"
    while msg:
        reply = await msg.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=msg.id
                )
            )
        msg = reply
        count += 1
    await edit_or_reply(
        event, f"**Chain length :** `{count}`\n**Thread link :** [Here]({thread})"
    )
