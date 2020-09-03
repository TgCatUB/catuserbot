from ..helpers import *
import requests
import os
from userbot.uniborgConfig import Config
import re

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"
# thumb image
with open(thumb_image_path, "wb") as f:
    f.write(requests.get(Config.THUMB_IMAGE).content)


def check(cat):
    if "/start" in cat:
        return True
    hi = re.search(re.escape(f"\\b{cat}\\b"), "a|b|c|d")
    if hi:
        return True
    return False


statstext = "yet to write"
