"""
Thenks goes to Emily ( The creater of Poto cmd) from ftg userbot
"""

from PIL import Image, ImageFilter, UnidentifiedImageError

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "extra"

name = "Profile Photos"


@catub.cat_cmd(
    pattern="poto(?:\s|$)([\s\S]*)",
    command=("poto", plugin_category),
    info={
        "header": "To get user or group profile pic.",
        "description": "Reply to a user to get his profile pic or use command along\
        with profile pic number to get desired pic else use .poto all to get\
        all pics. If you don't reply to any one\
        then the bot will get the chat profile pic.",
        "usage": [
            "{tr}poto <number>",
            "{tr}poto all",
            "{tr}poto",
        ],
    },
)
async def potocmd(event):
    "To get user or group profile pic"
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user and user.sender:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "`No photo found of this NIBBA / NIBBI. Now u Die!`"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "all":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "`This user has no photos to show you`")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await edit_or_reply(
                    event, "```number Invalid!``` **Are you Comedy Me ?**"
                )
                return
        except BaseException:
            await edit_or_reply(event, "`Are you comedy me ?`")
            return
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "`No photo found of this NIBBA / NIBBI. Now u Die!`"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()


@catub.cat_cmd(
    pattern="blur(?:\s|$)([\s\S]*)",
    command=("blur", plugin_category),
    info={
        "header": "To blur picture.",
        "description": "Reply to a user to blur his profile picture , or reply to a photo to blur that.",
        "usage": [
            "{tr}blur <number> <reply to a picture / user text>",
            "{tr}blur <reply to a picture / user text>",
        ],
    },
)
async def potocmd(event):
    "To blur pic"
    reply_to_id = await reply_id(event)
    rinp = event.pattern_match.group(1)
    rimg = await event.get_reply_message()
    red = int(rinp) if rinp else 10
    pic_name = "blur.png"
    try:
        if rimg and rimg.media:
            await event.client.download_media(rimg, pic_name)
        else:
            user = rimg.sender_id
            await event.client.download_profile_photo(user, pic_name)
    except AttributeError:
        return await edit_delete(event, "`Replay to a user message... `")
    try:
        im1 = Image.open(pic_name)
        im2 = im1.filter(ImageFilter.GaussianBlur(radius=red))
        im2.save(pic_name)
    except UnidentifiedImageError:
        return await edit_delete(event, "`Replay to a picture or user message... `")
    await event.delete()
    await event.client.send_file(event.chat_id, pic_name, reply_to=reply_to_id)
