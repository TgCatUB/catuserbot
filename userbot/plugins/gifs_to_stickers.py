from io import BytesIO

from userbot import utils
from PIL import Image
from telethon import types, utils, events
from telethon.tl.functions.messages import SaveGifRequest, UploadMediaRequest

sticker_to_gif = storage.sticker_to_gif or {}
access_hashes = storage.access_hashes or {}
gif_to_sticker = {str(gif): int(sticker) for sticker, gif in sticker_to_gif.items()}


async def convert_sticker_to_gif(sticker):
    gif_id = sticker_to_gif.get(str(sticker.id), None)
    if gif_id:
        access_hash = access_hashes[str(gif_id)]
        return types.InputDocument(gif_id, access_hash, b'')
    file = BytesIO()
    await borg.download_media(sticker, file=file)
    file.seek(0)

    # remove alpha
    im = Image.open(file)
    alpha = im.convert('RGBA').getchannel('A')
    size = max(im.width, im.height)
    new_im = Image.new('RGBA', (size, size), (40, 40, 40, 255))
    xy = (round((size - im.width) / 2), round((size - im.height) / 2))
    new_im.paste(im, box=xy, mask=alpha)
    file = BytesIO()
    new_im.save(file, format='gif')
    file.seek(0)

    # upload file
    file = await borg.upload_file(file, part_size_kb=512)
    file = types.InputMediaUploadedDocument(file, 'video/mp4', [])
    media = await borg(UploadMediaRequest('me', file))
    media = utils.get_input_document(media)

    # save (that's right, this is relational json)
    sticker_to_gif[str(sticker.id)] = media.id
    gif_to_sticker[str(media.id)] = sticker.id
    access_hashes[str(sticker.id)] = sticker.access_hash
    access_hashes[str(media.id)] = media.access_hash
    storage.sticker_to_gif = sticker_to_gif
    storage.access_hashes = access_hashes

    return media


@borg.on(util.admin_cmd(r'^\.ss$'))
async def on_save(event):
    await event.delete()
    target = await event.get_reply_message()
    media = target.gif or target.sticker
    if not media:
        return
    if target.sticker:
        media = await convert_sticker_to_gif(media)
    await borg(
        SaveGifRequest(id=media, unsave=False)
    )


@borg.on(events.NewMessage(outgoing=True))
async def on_sticker(event):
    if not event.sticker:
        return
    media = await convert_sticker_to_gif(event.sticker)
    await borg(
        SaveGifRequest(id=media, unsave=False)
    )


@borg.on(events.NewMessage(outgoing=True))
async def on_gif(event):
    if not event.gif:
        return
    sticker_id = gif_to_sticker.get(str(event.gif.id), None)
    if not sticker_id:
        return
    access_hash = access_hashes[str(sticker_id)]
    sticker = types.InputDocument(sticker_id, access_hash, b'')

    await event.delete()
    await borg.send_message(
        await event.get_input_chat(),
        file=sticker,
        reply_to=event.message.reply_to_msg_id
    )
