# ported from uniborg
# https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvakti.py
import json

import requests


@bot.on(admin_cmd(pattern="ezanvakti (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="ezanvakti (.*)", allow_sudo=True))
async def get_adzan(adzan):
    LOKASI = adzan.pattern_match.group(1)
    url = f"https://api.pray.zone/v2/times/today.json?city={LOKASI}"
    request = requests.get(url)
    if request.status_code != 200:
        await edit_delete(
            adzan, f"`Couldn't fetch any data about the city {LOKASI}`", 5
        )
        return
    result = json.loads(request.text)
    catresult = f"<b>Islamic prayer times </b>\
            \n\n<b>City     : </b><i>{result['results']['location']['city']}</i>\
            \n<b>Country  : </b><i>{result['results']['location']['country']}</i>\
            \n<b>Date     : </b><i>{result['results']['datetime'][0]['date']['gregorian']}</i>\
            \n<b>Hijri    : </b><i>{result['results']['datetime'][0]['date']['hijri']}</i>\
            \n\n<b>Imsak    : </b><i>{result['results']['datetime'][0]['times']['Imsak']}</i>\
            \n<b>Sunrise  : </b><i>{result['results']['datetime'][0]['times']['Sunrise']}</i>\
            \n<b>Fajr     : </b><i>{result['results']['datetime'][0]['times']['Fajr']}</i>\
            \n<b>Dhuhr    : </b><i>{result['results']['datetime'][0]['times']['Dhuhr']}</i>\
            \n<b>Asr      : </b><i>{result['results']['datetime'][0]['times']['Asr']}</i>\
            \n<b>Sunset   : </b><i>{result['results']['datetime'][0]['times']['Sunset']}</i>\
            \n<b>Maghrib  : </b><i>{result['results']['datetime'][0]['times']['Maghrib']}</i>\
            \n<b>Isha     : </b><i>{result['results']['datetime'][0]['times']['Isha']}</i>\
            \n<b>Midnight : </b><i>{result['results']['datetime'][0]['times']['Midnight']}</i>\
    "
    await edit_or_reply(adzan, catresult, "html")


CMD_HELP.update(
    {
        "ezanvakti": "**Plugin : **`ezanvakti`\
    \n\n**Syntax : **`.ezanvakti <city name>`\
    \n**Function : **__Shows you the Islamic prayer times of the given city name__"
    }
)
