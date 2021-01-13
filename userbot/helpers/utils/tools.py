from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from telethon import functions, types

from ..tools import media_type


async def media_to_pic(event, reply):
    mediatype = media_type(reply)
    if mediatype not in ["Photo", "Round Video", "Gif", "Sticker", "Video"]:
        await edit_delete(
            event,
            "`In the replied message. I cant extract any image to procced further reply to proper media`",
        )
        return None
    catmedia = await reply.download_media(file="./temp")
    catevent = await edit_or_reply(
        event, f"`Transfiguration Time! Converting {mediatype} to image`"
    )
    catfile = os.path.join("./temp/", "meme.png")
    if mediatype == "Sticker":
        if catmedia.endswith(".tgs"):
            await runcmd(
                f"lottie_convert.py --frame 0 -if lottie -of png '{catmedia}' '{catfile}'"
            )
        elif catmedia.endswith(".webp"):
            im = Image.open(catmedia)
            im.save(catfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        extractMetadata(createParser(catmedia))
        await runcmd(f"rm -rf '{catfile}'")
        err = (
            await runcmd(f"ffmpeg -i '{catmedia}' -vframes 1 -an -ss 1 '{catfile}'")
        )[1]
        if not os.path.exists(catfile):
            await edit_delete(
                catevent, f"`Sorry. I can't extract a image from this {mediatype}`"
            )
            print(err)
            return None
    else:
        im = Image.open(catmedia)
        im.save(catfile)
    await runcmd(f"rm -rf '{catmedia}'")
    return [catevent, catfile, mediatype]


async def unsavegif(event, sandy):
    try:
        await event.client(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=sandy.media.document.id,
                    access_hash=sandy.media.document.access_hash,
                    file_reference=sandy.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except:
        pass
