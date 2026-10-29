import math  # noqa F401
import os  # noqa F401
import re  # noqa F401
import time  # noqa F401

import heroku3
import requests
import spamwatch as spam_watch
from validators.url import url

from .. import *
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply  # noqa F401
from ..core.session import catub
from ..helpers import *
from ..helpers.utils import (
    _catutils,  # noqa F401
    _format,  # noqa F401
    install_pip,  # noqa F401
    reply_id,  # noqa F401
)
from ..sql_helper.globals import gvarstatus  # noqa F401

# =================== CONSTANT ===================
bot = catub
LOGS = logging.getLogger(__name__)
USERID = catub.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
ALIVE_NAME = Config.ALIVE_NAME

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

# mention user
mention = f"[{Config.ALIVE_NAME}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{Config.ALIVE_NAME}</a>"

PM_START = []
PMMESSAGE_CACHE = {}
PMMENU = "pmpermit_menu" not in Config.NO_LOAD

# Gdrive
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

# spamwatch support
if Config.SPAMWATCH_API:
    token = Config.SPAMWATCH_API
    try:
        spamwatch = spam_watch.Client(token)
    except Exception as e:
        LOGS.info(f"SpamWatch initialization failed: {e}")
        spamwatch = None
else:
    spamwatch = None


# ================================================

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


# thumb image
if Config.THUMB_IMAGE is not None:
    if check := url(Config.THUMB_IMAGE):
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(requests.get(Config.THUMB_IMAGE).content)
        except Exception as e:
            LOGS.info(str(e))


def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif isinstance(dictionary[key], list):
        if value in dictionary[key]:
            return
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]
