import math
import os
import re
import time

import heroku3
import lottie
import requests
import spamwatch as spam_watch
from validators.url import url

from .. import *
from ..Config import Config
from ..helpers import *
from ..helpers import _cattools, _catutils, _format

# =================== CONSTANT ===================

USERID = Config.OWNER_ID or bot.uid
ALIVE_NAME = Config.ALIVE_NAME
AUTONAME = Config.AUTONAME
DEFAULT_BIO = Config.DEFAULT_BIO
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
BOT_USERNAME = Config.TG_BOT_USER_NAME_BF_HER
# mention user
mention = f"[{DEFAULTUSER}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{DEFAULTUSER}</a>"


Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

PM_START = []
PMMESSAGE_CACHE = {}
PMMENU = "pmpermit_menu" not in Config.NO_LOAD

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
    BOTLOG_CHATID = "me"
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

# Gdrive
G_DRIVE_CLIENT_ID = Config.G_DRIVE_CLIENT_ID
G_DRIVE_CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
G_DRIVE_DATA = Config.G_DRIVE_DATA
G_DRIVE_FOLDER_ID = Config.G_DRIVE_FOLDER_ID
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

# spamwatch support
if Config.SPAMWATCH_API:
    token = Config.SPAMWATCH_API
    spamwatch = spam_watch.Client(token)
else:
    spamwatch = None

cat_users = [bot.uid]
if Config.SUDO_USERS:
    for user in Config.SUDO_USERS:
        cat_users.append(user)


# ================================================

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


# thumb image
if Config.THUMB_IMAGE is not None:
    check = url(Config.THUMB_IMAGE)
    if check:
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(requests.get(Config.THUMB_IMAGE).content)
        except Exception as e:
            LOGS.info(str(e))


def check(cat):
    if "/start" in cat:
        return True
    try:
        hi = re.search(cat.lower(), "(a|b|c|d)", flags=re.IGNORECASE)
    except Exception:
        hi = False
    return bool(hi)


def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif isinstance(dictionary[key], list):
        if value in dictionary[key]:
            return
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
# ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
# uniborg


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "No Database is set"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "Functioning"
        is_database_working = True
    return is_database_working, output


async def catalive():
    _, check_sgnirts = check_data_base_heal_th()
    sudo = "Enabled" if Config.SUDO_USERS else "Disabled"
    uptime = await get_readable_time((time.time() - StartTime))
    try:
        useragent = (
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.149 Mobile Safari/537.36"
        )
        user_id = Heroku.account().id
        headers = {
            "User-Agent": useragent,
            "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
            "Accept": "application/vnd.heroku+json; version=3.account-quotas",
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        result = r.json()
        quota = result["account_quota"]
        quota_used = result["quota_used"]

        # Used
        remaining_quota = quota - quota_used
        math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)
        # Current
        App = result["apps"]
        try:
            App[0]["quota_used"]
        except IndexError:
            AppQuotaUsed = 0
        else:
            AppQuotaUsed = App[0]["quota_used"] / 60
            math.floor(App[0]["quota_used"] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)
        dyno = f"{AppHours}h {AppMinutes}m/{hours}h {minutes}m"
    except Exception as e:
        dyno = e
    return f"Catuserbot Stats\
                 \n\nDatabase : {check_sgnirts}\
                  \nSudo : {sudo}\
                  \nUptime : {uptime}\
                  \nDyno : {dyno}\
                  "


async def make_gif(event, reply, quality=None, fps=None):
    fps = fps or 1
    quality = quality or 256
    result_p = os.path.join("temp", "animation.gif")
    animation = lottie.parsers.tgs.parse_tgs(reply)
    with open(result_p, "wb") as result:
        await _catutils.run_sync(
            lottie.exporters.gif.export_gif, animation, result, quality, fps
        )
    return result_p
