# CatUserbot module for getting the event of a event.

import io
import json
from datetime import datetime

import aiohttp
import requests
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, gvarstatus
from . import catub, edit_or_reply, logging, reply_id

plugin_category = "utils"

LOGS = logging.getLogger(__name__)
# Get time zone of the given country. Credits: @aragon12 and @zakaryan2004.
async def get_tz(con):
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


def fahrenheit(f):
    temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
    return temp[0]


def celsius(c):
    temp = str((c - 273.15)).split(".")
    return temp[0]


def sun(unix, ctimezone):
    return datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")


@catub.cat_cmd(
    pattern="climate(?:\s|$)([\s\S]*)",
    command=("climate", plugin_category),
    info={
        "header": "To get the weather report of a city.",
        "description": "Shows you the weather report of a city. By default it is Delhi, you can change it by {tr}setcity command.",
        "note": "For functioning of this plugin you need to set OPEN_WEATHER_MAP_APPID var you can  get value from https://openweathermap.org/",
        "usage": [
            "{tr}climate",
            "{tr}climate <city name>",
        ],
    },
)
async def get_weather(event):  # sourcery no-metrics
    "To get the weather report of a city."
    if not Config.OPEN_WEATHER_MAP_APPID:
        return await edit_or_reply(
            event, "`Get an API key from` https://openweathermap.org/ `first.`"
        )
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    CITY = gvarstatus("DEFCITY") or "Delhi" if not input_str else input_str
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                return await edit_or_reply(event, "`Invalid Country.`")
            CITY = newcity[0].strip() + "," + countrycode.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={Config.OPEN_WEATHER_MAP_APPID}"
    async with aiohttp.ClientSession() as _session:
        async with _session.get(url) as request:
            requeststatus = request.status
            requesttext = await request.text()
    result = json.loads(requesttext)
    if requeststatus != 200:
        return await edit_or_reply(event, "`Invalid Country.`")
    cityname = result["name"]
    curtemp = result["main"]["temp"]
    humidity = result["main"]["humidity"]
    min_temp = result["main"]["temp_min"]
    max_temp = result["main"]["temp_max"]
    pressure = result["main"]["pressure"]
    feel = result["main"]["feels_like"]
    desc = result["weather"][0]
    desc = desc["main"]
    country = result["sys"]["country"]
    sunrise = result["sys"]["sunrise"]
    sunset = result["sys"]["sunset"]
    wind = result["wind"]["speed"]
    winddir = result["wind"]["deg"]
    cloud = result["clouds"]["all"]
    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    div = 360 / len(dirs)
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")
    await edit_or_reply(
        event,
        f"🌡**Temperature:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        + f"🥰**Human Feeling** `{celsius(feel)}°C | {fahrenheit(feel)}°F`\n"
        + f"🥶**Min. Temp.:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        + f"🥵**Max. Temp.:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"☁️**Humidity:** `{humidity}%`\n"
        + f"🧧**Pressure** `{pressure} hPa`\n"
        + f"🌬**Wind:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n"
        + f"⛈**Cloud:** `{cloud} %`\n"
        + f"🌄**Sunrise:** `{sun(sunrise,ctimezone)}`\n"
        + f"🌅**Sunset:** `{sun(sunset,ctimezone)}`\n\n\n"
        + f"**{desc}**\n"
        + f"`{cityname}, {fullc_n}`\n"
        + f"`{time}`\n",
    )


@catub.cat_cmd(
    pattern="setcity(?:\s|$)([\s\S]*)",
    command=("setcity", plugin_category),
    info={
        "header": "To set default city for climate cmd",
        "description": "Sets your default city so you can just use .weather or .climate when ever you neededwithout typing city name each time",
        "note": "For functioning of this plugin you need to set OPEN_WEATHER_MAP_APPID var you can  get value from https://openweathermap.org/",
        "usage": [
            "{tr}climate",
            "{tr}climate <city name>",
        ],
    },
)
async def set_default_city(event):
    "To set default city for climate/weather cmd"
    if not Config.OPEN_WEATHER_MAP_APPID:
        return await edit_or_reply(
            event, "`Get an API key from` https://openweathermap.org/ `first.`"
        )
    input_str = event.pattern_match.group(1)
    CITY = gvarstatus("DEFCITY") or "Delhi" if not input_str else input_str
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                return await edit_or_reply(event, "`Invalid country.`")
            CITY = newcity[0].strip() + "," + countrycode.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={Config.OPEN_WEATHER_MAP_APPID}"
    request = requests.get(url)
    result = json.loads(request.text)
    if request.status_code != 200:
        return await edit_or_reply(event, "`Invalid country.`")
    addgvar("DEFCITY", CITY)
    cityname = result["name"]
    country = result["sys"]["country"]
    fullc_n = c_n[f"{country}"]
    await edit_or_reply(event, f"`Set default event as {cityname}, {fullc_n}.`")


@catub.cat_cmd(
    pattern="weather(?:\s|$)([\s\S]*)",
    command=("weather", plugin_category),
    info={
        "header": "To get the weather report of a city.",
        "description": "Shows you the weather report of a city . By default it is Delhi, you can change it by {tr}setcity command.",
        "usage": [
            "{tr}weather",
            "{tr}weather <city name>",
        ],
    },
)
async def _(event):
    "weather report today from 'wttr.in'"
    input_str = event.pattern_match.group(1)
    if not input_str:
        input_str = gvarstatus("DEFCITY") or "Delhi"
    output = requests.get(f"https://wttr.in/{input_str}?mnTC0&lang=en").text
    await edit_or_reply(event, output, parse_mode=_format.parse_pre)


@catub.cat_cmd(
    pattern="wttr(?:\s|$)([\s\S]*)",
    command=("wttr", plugin_category),
    info={
        "header": "To get the weather report of a city.",
        "description": "Shows you the weather report of a city for next 3 days . By default it is Delhi, you can change it by {tr}setcity command.",
        "usage": [
            "{tr}wttr",
            "{tr}wttr <city name>",
        ],
    },
)
async def _(event):
    "weather report for next 3 days from 'wttr.in'"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    if not input_str:
        input_str = gvarstatus("DEFCITY") or "Delhi"
    async with aiohttp.ClientSession() as session:
        sample_url = "https://wttr.in/{}.png"
        response_api_zero = await session.get(sample_url.format(input_str))
        response_api = await response_api_zero.read()
        with io.BytesIO(response_api) as out_file:
            await event.reply(
                f"**City : **`{input_str}`", file=out_file, reply_to=reply_to_id
            )
    try:
        await event.delete()
    except Exception as e:
        LOGS.info(str(e))
