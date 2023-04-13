# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import re
import time
from datetime import datetime

import requests
from selenium import webdriver

from ..Config import Config
from ..core.managers import edit_or_reply


async def chromeDriver(inputstr, event=None):
    if Config.CHROME_BIN is None:
        return None, "Need to install Google Chrome. Module Stopping."
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-in-incognito")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.CHROME_BIN
        if event:
            await edit_or_reply(event, "`Starting Google Chrome BIN`")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(inputstr)
        if event:
            await edit_or_reply(event, "`Calculating Page Dimensions`")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        if event:
            await edit_or_reply(event, "`Stoppping Chrome Bin`")
        driver.close()
        # capture the total work time
        end = datetime.now()
        ms = (end - start).seconds
        return im_png, f"**url : **{inputstr} \n**Time :** `{ms} seconds`"
    except Exception as e:
        return None, str(e)


class GooglePic:
    def __init__(self, image, site):
        self.image = image
        self.site = site

    def __hash__(self):
        return hash(self.image + self.site)

    @staticmethod
    def __title_fetch__(html):
        title = ""
        pattern1 = re.compile(r"Image search ([^\"]+)")
        pattern2 = re.compile(r"\],\"(.*?)(?=\",null,\[\[\"ROSTI\")")
        if match := pattern1.search(html):
            title = match.group(1)
        elif match := pattern2.search(html):
            title = match.group(1)
        return "Visual matches" if (len(title) > 100 or not title) else title

    @staticmethod
    def reverse_data(image_filename, flag=False):
        data = {"title": None, "lens": None, "google": None, "error": None}
        with open(image_filename, mode="rb") as f:
            url = f"https://lens.google.com/upload?ep=ccm&s=&st={int(time.time())}"
            try:
                res1 = requests.post(url, files={"encoded_image": f})
                if res1.ok:
                    data["lens"] = re.search(r"https?://[^\"]+", res1.text).group()
                    res2 = requests.get(data["lens"])
                    if res2.ok:
                        html = res2.text
                        if flag:
                            data["image_set"] = set()
                            for link in re.findall(
                                r'https://www.google.com/imgres\?imgurl.+?"', html
                            ):
                                decoded_link = link.encode().decode("unicode-escape")
                                image = re.search(r"imgurl=(.+?)&", decoded_link).group(
                                    1
                                )
                                site = re.search(
                                    r"imgrefurl=(.+?)&", decoded_link
                                ).group(1)
                                if image.endswith(
                                    (".jpg", ".jpeg", ".png", ".gif")
                                ) or site.endswith((".jpg", ".jpeg", ".png", ".gif")):
                                    data["image_set"].add(GooglePic(image, site))
                        google_url = re.search(
                            r"https://www.google.com/search\?tbs.+?(?=\")", html
                        )
                        data["title"] = GooglePic.__title_fetch__(html)
                        data["google"] = (
                            google_url.group().encode().decode("unicode_escape")
                        )
            except Exception as error:
                data["error"] = str(error)
        return data
