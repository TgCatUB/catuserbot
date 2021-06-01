import logging
import random

from moviepy.editor import VideoFileClip
from PIL import Image, ImageOps

from ...core.logger import logging

LOGS = logging.getLogger(__name__)


async def vid_to_gif(inputfile, outputfile, speed=None, starttime=None, endtime=None):
    try:
        clip = VideoFileClip(inputfile)
        if starttime is not None and endtime is not None:
            clip = clip.subclip(int(starttime), int(endtime))
        if speed is not None:
            clip = clip.speedx(float(speed))
        clip.write_gif(outputfile, logger=None)
        return outputfile
    except Exception as e:
        LOGS.error(e)
        return None


async def r_frames(image, w, h, outframes):
    for i in range(1, w, w // 30):
        img1 = img2 = image.copy()
        temp = Image.new("RGB", (w, h))
        img1 = img1.resize((i, h))
        img2 = img2.resize((w - i, h))
        temp.paste(img1, (0, 0))
        temp.paste(img2, (i, 0))
        outframes.append(temp)
    return outframes


async def l_frames(image, w, h, outframes):
    for i in range(1, w, w // 30):
        img1 = img2 = image.copy()
        temp = Image.new("RGB", (w, h))
        img1 = ImageOps.mirror(img1.resize((i, h)))
        img2 = ImageOps.mirror(img2.resize((w - i, h)))
        temp.paste(img1, (0, 0))
        temp.paste(img2, (i, 0))
        temp = ImageOps.mirror(temp)
        outframes.append(temp)
    return outframes


async def ud_frames(image, w, h, outframes, flip=False):
    for i in range(1, h, h // 30):
        img1 = img2 = image.copy()
        temp = Image.new("RGB", (w, h))
        img1 = img1.resize((w, i))
        img2 = img2.resize((w, h - i))
        temp.paste(img1, (0, 0))
        temp.paste(img2, (0, i))
        if flip:
            temp = ImageOps.flip(temp)
        outframes.append(temp)
    return outframes


async def spin_frames(image, w, h, outframes):
    image.thumbnail((512, 512), Image.ANTIALIAS)
    img = Image.new("RGB", (512, 512), "black")
    img.paste(image, ((512 - w) // 2, (512 - h) // 2))
    image = img
    way = random.choice([1, -1])
    for i in range(1, 60):
        img = image.rotate(i * 6 * way)
        outframes.append(img)
    return outframes


async def invert_frames(image, w, h, outframes):
    image.convert("RGB")
    invert = ImageOps.invert(image)
    outframes.append(image)
    outframes.append(invert)
    return outframes
