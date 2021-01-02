from telethon import functions, types


def media_type(message):
    if message and message.photo:
        return "Photo"
    elif message and message.audio:
        return "Audio"
    elif message and message.voice:
        return "Voice"
    elif message and message.video_note:
        return "Round Video"
    elif message and message.gif:
        return "Gif"
    elif message and message.sticker:
        return "Sticker"
    elif message and message.video:
        return "Video"
    elif message and message.document:
        return "Document"
    else:
        return None


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
