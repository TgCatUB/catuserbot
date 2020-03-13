# Copyleft 🄯 2017 UniBorg
#
# The below code might feel like copied, but
# https://t.me/MemeVideoBot?start=1333
#
# Licensed under the General Public License, Version 3 (the "License");
# you may use this file in compliance with the License.
#

"""RapidLeech plugin: Inspired by @SjProjects"""

import aiohttp
import asyncio
import json
import re
from bs4 import BeautifulSoup
from telethon.utils import get_inner_text
from uniborg.util import admin_cmd


logger.info(Config.OPEN_LOAD_LOGIN)
# https://t.me/RoseSupport/33801


@borg.on(admin_cmd(pattern="rl"))
async def _(event):
    if event.fwd_from:
        return
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    reply_message = await event.get_reply_message()
    if len(cmt) > 1:
        list_of_urls = cmt[1:]
    else:
        list_of_urls = get_inner_text(
            reply_message.message, reply_message.entities)
    converted_links = ""
    if len(list_of_urls) > 0:
        converted_links += "Trying to generate IP specific link\n\nഞെക്കി പിടി \n"
        for a_url in list_of_urls:
            converted_link_infos = await get_direct_ip_specific_link(a_url)
            if "url" in converted_link_infos:
                converted_link = converted_link_infos["url"]
                converted_links += f"[{a_url}]({converted_link}) \n\n"
            elif "err" in converted_link_infos:
                err = converted_link_infos["err"]
                converted_links += f"`{a_url}` returned `{err}`\n\n"
    await event.reply(converted_links)


async def get_direct_ip_specific_link(link: str):
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/openload.py#L246-L255
    OPEN_LOAD_DOMAINS = r"(?:openload\.(?:co|io|link|pw)|oload\.(?:tv|biz|stream|site|xyz|win|download|cloud|cc|icu|fun|club|info|press|pw|life|live|space|services|website)|oladblock\.(?:services|xyz|me)|openloed\.co)"
    OPEN_LOAD_VALID_URL = r"(?x)https?://(?P<host>(?:www\.)?%s)/(?:f|embed)/(?P<id>[a-zA-Z0-9-_]+)" % OPEN_LOAD_DOMAINS
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/openload.py#L246-L255
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/googledrive.py#L16-L27
    GOOGLE_DRIVE_VALID_URLS = r"(?x)https?://(?:(?:docs|drive)\.google\.com/(?:(?:uc|open)\?.*?id=|file/d/)|video\.google\.com/get_player\?.*?docid=)(?P<id>[a-zA-Z0-9_-]{28,})"
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/googledrive.py#L16-L27
    dl_url = None
    if "zippyshare.com" in link:
        async with aiohttp.ClientSession() as session:
            http_response = await session.get(link)
            http_response_text = await http_response.text()
            response_b_soup = BeautifulSoup(http_response_text, "html.parser")
            scripts = response_b_soup.find_all(
                "script", {"type": "text/javascript"})
            # calculations
            # check https://github.com/LameLemon/ziggy/blob/master/ziggy.py
            for script in scripts:
                if "getElementById('dlbutton')" in script.text:
                    regex_search_exp = re.search(
                        '= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);', script.text)
                    url_raw = regex_search_exp.group("url")
                    math = regex_search_exp.group("math")
                    dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
                    break
            #
            base_url = re.search("http.+.com", link).group()
            dl_url = {
                "url": base_url + eval(dl_url)
            }
    elif re.search(OPEN_LOAD_VALID_URL, link):
        # https://stackoverflow.com/a/47726003/4723940
        async with aiohttp.ClientSession() as session:
            openload_id = re.search(OPEN_LOAD_VALID_URL, link).group("id")
            step_one_url = "https://api.openload.co/1/file/dlticket?file={}&login={}&key={}".format(
                openload_id, Config.OPEN_LOAD_LOGIN, Config.OPEN_LOAD_KEY)
            http_response = await session.get(step_one_url)
            http_response_text = await http_response.text()
            http_response_json = json.loads(http_response_text)
            logger.info(http_response_json)
            if http_response_json["msg"] == "OK":
                # wait till wait time
                await asyncio.sleep(int(http_response_json["result"]["wait_time"]))
                # TODO: check if captcha is required
                step_two_url = "https://api.openload.co/1/file/dl?file={}&ticket={}".format(
                    openload_id, http_response_json["result"]["ticket"])
                http_response = await session.get(step_two_url)
                http_response_text = await http_response.text()
                http_response_json = json.loads(http_response_text)
                logger.info(http_response_json)
                if http_response_json["msg"] == "OK":
                    dl_file_url = http_response_json["result"]["url"]
                    dl_file_name = http_response_json["result"]["name"]
                    dl_file_size = http_response_json["result"]["size"]
                    dl_url = {
                        "url": dl_file_url,
                        "name": dl_file_name,
                        "size": dl_file_size
                    }
                else:
                    dl_url = {
                        "err": http_response_text
                    }
            else:
                dl_url = {
                    "err": http_response_text
                }
        # https://stackoverflow.com/a/47726003/4723940
    elif re.search(GOOGLE_DRIVE_VALID_URLS, link):
        file_id = re.search(GOOGLE_DRIVE_VALID_URLS, link).group("id")
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            step_zero_url = "https://drive.google.com/uc?export=download&id={}".format(file_id)
            http_response = await session.get(step_zero_url, allow_redirects=False)
            if "location" in http_response.headers:
                # in case of small file size, Google downloads directly
                file_url = http_response.headers["location"]
                if "accounts.google.com" in file_url:
                    dl_url = {
                        "err": "Private Google Drive URL"
                    }
                else:
                    dl_url = {
                        "url": file_url
                    }
            else:
                # in case of download warning page
                http_response_text = await http_response.text()
                response_b_soup = BeautifulSoup(http_response_text, "html.parser")
                warning_page_url = "https://drive.google.com" + response_b_soup.find("a", {"id": "uc-download-link"}).get("href")
                file_name_and_size = response_b_soup.find("span", {"class": "uc-name-size"}).text
                http_response_two = await session.get(warning_page_url, allow_redirects=False)
                if "location" in http_response_two.headers:
                    file_url = http_response_two.headers["location"]
                    if "accounts.google.com" in file_url:
                        dl_url = {
                            "err": "Private Google Drive URL"
                        }
                    else:
                        dl_url = {
                            "url": file_url,
                            "name": file_name_and_size
                        }
                else:
                    dl_url = {
                        "err": "Unsupported Google Drive URL"
                    }
    else:
        dl_url = {
            "err": "Unsupported URL"
        }
    return dl_url
