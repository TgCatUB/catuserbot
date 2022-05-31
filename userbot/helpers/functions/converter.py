import os

from PIL import Image

from userbot.core.logger import logging
from userbot.core.managers import edit_or_reply
from userbot.helpers.functions.vidtools import take_screen_shot
from userbot.helpers.tools import fileinfo, media_type, meme_type
from userbot.helpers.utils.utils import runcmd

LOGS = logging.getLogger(__name__)


class CatConverter:
    async def _media_check(self, reply, dirct, file, memetype):
        if not os.path.isdir(dirct):
            os.mkdir(dirct)
        catfile = os.path.join(dirct, file)
        if os.path.exists(catfile):
            os.remove(catfile)
        try:
            catmedia = reply if os.path.exists(reply) else None
        except TypeError:
            if memetype in ["Video", "Gif"]:
                dirct = "./temp/catfile.mp4"
            elif memetype == "Audio":
                dirct = "./temp/catfile.mp3"
            catmedia = await reply.download_media(dirct)
        return catfile, catmedia

    async def to_image(self, event, reply, noedits=False, rgb=False):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype == "Document":
            return event, None
        catevent = (
            event
            if noedits
            else await edit_or_reply(
                event, "`Transfiguration Time! Converting to ....`"
            )
        )
        catfile, catmedia = await self._media_check(
            reply, "./temp", "meme.png", memetype
        )
        if memetype == "Photo":
            im = Image.open(catmedia)
            im.save(catfile)
        elif memetype in ["Audio", "Voice"]:
            await runcmd(f"ffmpeg -i '{catmedia}' -an -c:v copy '{catfile}' -y")
        elif memetype in ["Round Video", "Video", "Gif"]:
            await take_screen_shot(catmedia, "00.00", catfile)
        if mediatype == "Sticker":
            if memetype == "Animated Sticker":
                catcmd = f"lottie_convert.py --frame 0 -if lottie -of png '{catmedia}' '{catfile}'"
                stdout, stderr = (await runcmd(catcmd))[:2]
                if stderr:
                    LOGS.info(stdout + stderr)
            elif memetype == "Video Sticker":
                await take_screen_shot(catmedia, "00.00", catfile)
            elif memetype == "Static Sticker":
                im = Image.open(catmedia)
                im.save(catfile)
        if catmedia and os.path.exists(catmedia):
            os.remove(catmedia)
        if os.path.exists(catfile):
            if rgb:
                img = Image.open(catfile)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(catfile)
            return catevent, catfile, mediatype
        return catevent, None

    async def to_sticker(self, event, reply, noedits=False, rgb=False):
        filename = os.path.join("./temp/", "meme.webp")
        response = await self.to_image(event, reply, noedits, rgb)
        if response[1]:
            image = Image.open(response[1])
            image.save(filename, "webp")
            os.remove(response[1])
            return response[0], filename, response[2]
        return response[0], None

    async def to_webm(self, event, reply, noedits=False):
        # //Hope u dunt kang :/ @Jisan7509
        memetype = await meme_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Gif",
            "Video",
        ]:
            return event, None
        catevent = (
            event
            if noedits
            else await edit_or_reply(event, "__🎞Converting into Animated sticker..__")
        )
        catfile, catmedia = await self._media_check(
            reply, "./temp", "animate.webm", memetype
        )
        file = await fileinfo(catmedia)
        h = file["height"]
        w = file["width"]
        w, h = (-1, 512) if h > w else (512, -1)
        await runcmd(
            f"ffmpeg -to 00:00:02.900 -i '{catmedia}' -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an '{catfile}'"
        )  # pain
        if os.path.exists(catmedia):
            os.remove(catmedia)
        if os.path.exists(catfile):
            return catevent, catfile
        return catevent, None

    async def to_gif(self, event, reply, noedits=False):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Animated Sticker",
            "Video",
            "Gif",
        ]:
            return event, None
        catevent = (
            event
            if noedits
            else await edit_or_reply(
                event, "`Transfiguration Time! Converting to ....`"
            )
        )
        catfile, catmedia = await self._media_check(
            reply, "./temp", "meme.mp4", memetype
        )
        if mediatype == "Sticker":
            if memetype == "Video Sticker":
                await runcmd(f"ffmpeg -i '{catmedia}' -c copy '{catfile}'")
            elif memetype == "Animated Sticker":
                await runcmd(f"lottie_convert.py '{catmedia}' '{catfile}'")
        elif mediatype == "Gif":
            await runcmd(f"mv '{catmedia}' '{catfile}'")
        else:
            await runcmd(f"ffmpeg -i '{catmedia}' -c:v libx264 -fs 5M -an '{catfile}'")
        if catmedia and os.path.exists(catmedia):
            os.remove(catmedia)
        if os.path.exists(catfile):
            return event, catfile
        return event, None


Convert = CatConverter()
