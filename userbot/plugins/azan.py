# ported from uniborg
# https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvakti.py
import json

import requests

from ..sql_helper.globals import gvarstatus
from . import catub, edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="azan(?:\s|$)([\s\S]*)",
    command=("azan", plugin_category),
    info={
        "header": "Shows you the Islamic prayer times of the given city name.",
        "note": "you can set default city by using {tr}setcity command.",
        "usage": "{tr}azan <city name>",
        "examples": "{tr}azan hyderabad",
    },
)
async def get_adzan(adzan):
    "Shows you the Islamic prayer times of the given city name"
    input_str = adzan.pattern_match.group(1)
    LOKASI = gvarstatus("DEFCITY") or "Delhi" if not input_str else input_str
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        return await edit_delete(
            adzan, f"`Couldn't fetch any data about the city {LOKASI}`", 5
        )
    result = json.loads(request.text)
    catresult = f"<b>Islamic prayer times </b>\
            \n\n<b>City     : </b><i>{result['query']}</i>\
            \n<b>Country  : </b><i>{result['country']}</i>\
            \n<b>Date     : </b><i>{result['items'][0]['date_for']}</i>\
            \n<b>Fajr     : </b><i>{result['items'][0]['fajr']}</i>\
            \n<b>Shurooq    : </b><i>{result['items'][0]['shurooq']}</i>\
            \n<b>Dhuhr    : </b><i>{result['items'][0]['dhuhr']}</i>\
            \n<b>Asr    : </b><i>{result['items'][0]['asr']}</i>\
            \n<b>Maghrib    : </b><i>{result['items'][0]['maghrib']}</i>\
            \n<b>Isha     : </b><i>{result['items'][0]['isha']}</i>\
    "
    await edit_or_reply(adzan, catresult, "html")
