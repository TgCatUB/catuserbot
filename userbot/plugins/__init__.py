import os
import re
import time
import heroku3
import requests
from ..helpers import *
from .. import StartTime
from ..uniborgConfig import Config
from .alive import check_data_base_heal_th


Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY

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



statstext = catalive

def catalive():
    _, check_sgnirts = check_data_base_heal_th()
    if Config.SUDO_USERS:
        sudo = "Enabled"
    else:
        sudo = "Disabled"
    uptime = await get_readable_time((time.time() - StartTime))
    dyno = await edit_or_reply(dyno, "`Processing...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    user_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {Var.HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Error: something bad happened`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    dyno = f"{AppHours}h {AppMinutes}m/{hours}h {minutes}"
    conclusion = f"Database : {_}\
                  \nSudo function : {sudo}\
                  \nUptime : {uptime}\
                  \nDyno's : {dyno}\
                  "
    return conclusion
    
