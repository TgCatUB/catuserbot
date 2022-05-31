import logging
import os
import random
from typing import Optional

from PIL import Image, ImageOps

from ...core.logger import logging
from ..utils.utils import runcmd

LOGS = logging.getLogger(__name__)


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


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -hide_banner -loglevel quiet -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}' -y"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
