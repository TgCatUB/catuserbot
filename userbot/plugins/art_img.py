"""
Created by @Jisan7509
plugin for Cat_Userbot
☝☝☝
You remove this, you gay.
"""
import os

from telethon.errors.rpcerrorlist import YouBlockedUserError

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import clippy
from . import _cattools, catub, convert_toimage, mention, reply_id

plugin_category = "extra"


@catub.cat_cmd(
    pattern="iascii ?([\s\S]*)",
    command=("iascii", plugin_category),
    info={
        "header": "Convert media to ascii art.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into ascii.",
        "usage": [
            "{tr}iascii <reply to a media>",
        ],
    },
)
async def bad(event):
    "Make a media to ascii art"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edit_delete(event, "```Reply to a media file...```")
    c_id = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output_file = os.path.join("./temp", "jisan.jpg")
    output = await _cattools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/jisan.jpg")
    kakashi = await edit_or_reply(event, "```Wait making ASCII...```")
    async with event.client.conversation("@asciiart_bot") as conv:
        try:
            msg = await conv.send_file(output_file)
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await kakashi.edit(
                "```Please unblock @asciiart_bot and try again```"
            )
        if response.text.startswith("Forward"):
            await kakashi.edit(
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await kakashi.delete()
            await event.client.send_file(
                event.chat_id,
                response,
                reply_to=c_id,
                caption=f"**➥ Image Type :** ASCII Art\n**➥ Uploaded By :** {mention}",
            )
            await event.client.send_read_acknowledge(conv.chat_id)
    await event.client.delete_messages(conv.chat_id, [msg.id, response.id])
    if os.path.exists(output_file):
        os.remove(output_file)


@catub.cat_cmd(
    pattern="line ?([\s\S]*)",
    command=("line", plugin_category),
    info={
        "header": "Convert media to line image.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into line image.",
        "usage": [
            "{tr}line <reply to a media>",
        ],
    },
)
async def pussy(event):
    "Make a media to line image"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edit_delete(event, "```Reply to a media file...```")
    c_id = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output_file = os.path.join("./temp", "jisan.jpg")
    output = await _cattools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/jisan.jpg")
    kakashi = await edit_or_reply(event, "```Processing....```")
    async with event.client.conversation("@Lines50Bot") as conv:
        try:
            msg = await conv.send_file(output_file)
            pic = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await kakashi.edit("```Please unblock @Lines50Bot and try again```")
        await kakashi.delete()
        await event.client.send_file(
            event.chat_id,
            pic,
            reply_to=c_id,
            caption=f"**➥ Image Type :** LINE Art \n**➥ Uploaded By :** {mention}",
        )
    await event.client.delete_messages(conv.chat_id, [msg.id, pic.id])
    if os.path.exists(output_file):
        os.remove(output_file)


@catub.cat_cmd(
    pattern="clip ?([\s\S]*)",
    command=("clip", plugin_category),
    info={
        "header": "Convert media to sticker by clippy",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into sticker by clippy.",
        "usage": [
            "{tr}clip <reply to a media>",
        ],
    },
)
async def cat(event):
    "Make a media to clippy sticker"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edit_delete(event, "```Reply to a media file...```")
    cat = await edit_or_reply(event, "```Processing...```")
    c_id = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output_file = os.path.join("./temp", "jisan.jpg")
    output = await _cattools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/jisan.jpg")
    await cat.delete()
    await clippy(event.client, output_file, event.chat_id, c_id)
    if os.path.exists(output_file):
        os.remove(output_file)
