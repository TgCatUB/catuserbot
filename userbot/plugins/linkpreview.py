import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from urlextract import URLExtract

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv

extractor = URLExtract()

plugin_category = "utils"


@catub.cat_cmd(
    pattern="ctg(?: |$)([\s\S]*)",
    command=("ctg", plugin_category),
    info={
        "header": "Reply to link To get link preview using telegrah.s.",
        "usage": "{tr}ctg <reply/text>",
    },
)
async def ctg(event):
    "To get link preview"
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me link to search..**", 20)
    urls = extractor.find_urls(input_str)
    if not urls:
        return await edit_delete(event, "**There no link to search in the text..**", 20)
    chat = "@chotamreaderbot"
    await edit_or_reply(event, "```Processing...```")
    async with event.client.conversation(chat) as conv:
        try:
            msg_flag = await conv.send_message(urls[0])
        except YouBlockedUserError:
            await edit_or_reply(
                event, "**Error:** Trying to unblock & retry, wait a sec..."
            )
            await catub(unblock("chotamreaderbot"))
            msg_flag = await conv.send_message(urls[0])
        await asyncio.sleep(2)
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        if response.text.startswith(""):
            await edit_or_reply(event, "Am I Dumb Or Am I Dumb?")
        else:
            await edit_or_reply(event, response.message, link_preview=True)
        await delete_conv(event, chat, msg_flag)
