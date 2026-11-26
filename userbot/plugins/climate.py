# Special credits: @aragon12 and @zakaryan2004.

import io
import json
import urllib.parse
from datetime import datetime

import httpx
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


async def _get_wttr_climate(city):
    encoded_city = urllib.parse.quote_plus(city)
    url = f"https://wttr.in/{encoded_city}?format=j1"
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                return None
            data = resp.json()
    except Exception as e:
        LOGS.warning(f"wttr.in json request failed: {e}")
        return None

    current = data.get("current_condition", [{}])[0]
    nearest = data.get("nearest_area", [{}])[0]
    weather = data.get("weather", [{}])[0]
    astronomy = weather.get("astronomy", [{}])[0]

    cityname = nearest.get("areaName", [{}])[0].get("value") or city
    country = nearest.get("country", [{}])[0].get("value") or ""
    region = nearest.get("region", [{}])[0].get("value") or ""

    temp_c = current.get("temp_C", "N/A")
    temp_f = current.get("temp_F", "N/A")
    feel_c = current.get("FeelsLikeC", "N/A")
    feel_f = current.get("FeelsLikeF", "N/A")

    min_temp_c = weather.get("mintempC", "N/A")
    max_temp_c = weather.get("maxtempC", "N/A")
    min_temp_f = weather.get("mintempF", "N/A")
    max_temp_f = weather.get("maxtempF", "N/A")

    humidity = current.get("humidity", "N/A")
    pressure = current.get("pressure", "N/A")
    kmph = current.get("windspeedKmph", "0")
    mph = current.get("windspeedMiles", "0")
    findir = current.get("winddir16Point", "")
    cloud = current.get("cloudcover", "0")
    sunrise = astronomy.get("sunrise", "N/A")
    sunset = astronomy.get("sunset", "N/A")

    desc = current.get("weatherDesc", [{}])[0].get("value", "Clear")
    local_time = datetime.now().strftime("%A, %I:%M %p")
    loc = f"{cityname}, {region}, {country}" if region and region != cityname else f"{cityname}, {country}"

    return (
        f"🌡**Temperature:** `{temp_c}°C | {temp_f}°F`\n"
        f"🥰**Human Feeling:** `{feel_c}°C | {feel_f}°F`\n"
        f"🥶**Min. Temp.:** `{min_temp_c}°C | {min_temp_f}°F`\n"
        f"🥵**Max. Temp.:** `{max_temp_c}°C | {max_temp_f}°F`\n"
        f"☁️**Humidity:** `{humidity}%`\n"
        f"🧧**Pressure:** `{pressure} hPa`\n"
        f"🌬**Wind:** `{kmph} kmh | {mph} mph, {findir}`\n"
        f"⛈**Cloud:** `{cloud}%`\n"
        f"🌄**Sunrise:** `{sunrise}`\n"
        f"🌅**Sunset:** `{sunset}`\n\n\n"
        f"**{desc}**\n"
        f"`{loc}`\n"
        f"`{local_time}`\n"
    )


@catub.cat_cmd(
    pattern=r"climate(?:\s|$)([\s\S]*)",
    command=("climate", plugin_category),
    info={
        "header": "To get the weather report of a city.",
        "description": "Shows you the weather report of a city. By default it is Delhi, you can change it by {tr}setcity command.",
        "note": "Works out of the box without any API key. If OPEN_WEATHER_MAP_APPID is set, uses OpenWeatherMap.",
        "usage": [
            "{tr}climate",
            "{tr}climate <city name>",
        ],
    },
)
async def get_weather(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "To get the weather report of a city."
    input_str = "".join(event.text.split(maxsplit=1)[1:]).strip()
    CITY = input_str or gvarstatus("DEFCITY") or "Delhi"

    # 1. OpenWeatherMap path if API key is provided
    if Config.OPEN_WEATHER_MAP_APPID:
        try:
            timezone_countries = {timezone: country for country, timezones in c_tz.items() for timezone in timezones}
            req_city = CITY
            if "," in req_city:
                newcity = req_city.split(",")
                if len(newcity[1]) == 2:
                    req_city = f"{newcity[0].strip()},{newcity[1].strip()}"
                else:
                    country = await get_tz((newcity[1].strip()).title())
                    if country and f"{country}" in timezone_countries:
                        countrycode = timezone_countries[f"{country}"]
                        req_city = f"{newcity[0].strip()},{countrycode.strip()}"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={req_city}&appid={Config.OPEN_WEATHER_MAP_APPID}"
            async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
                request = await client.get(url)
            if request.status_code == 200:
                result = json.loads(request.text)
                cityname = result["name"]
                curtemp = result["main"]["temp"]
                humidity = result["main"]["humidity"]
                min_temp = result["main"]["temp_min"]
                max_temp = result["main"]["temp_max"]
                pressure = result["main"]["pressure"]
                feel = result["main"]["feels_like"]
                desc = result["weather"][0]["main"]
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
                return await edit_or_reply(
                    event,
                    f"🌡**Temperature:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
                    + f"🥰**Human Feeling:** `{celsius(feel)}°C | {fahrenheit(feel)}°F`\n"
                    + f"🥶**Min. Temp.:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
                    + f"🥵**Max. Temp.:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
                    + f"☁️**Humidity:** `{humidity}%`\n"
                    + f"🧧**Pressure:** `{pressure} hPa`\n"
                    + f"🌬**Wind:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n"
                    + f"⛈**Cloud:** `{cloud}%`\n"
                    + f"🌄**Sunrise:** `{sun(sunrise, ctimezone)}`\n"
                    + f"🌅**Sunset:** `{sun(sunset, ctimezone)}`\n\n\n"
                    + f"**{desc}**\n"
                    + f"`{cityname}, {fullc_n}`\n"
                    + f"`{time}`\n",
                )
        except Exception as e:
            LOGS.warning(f"OpenWeatherMap request failed: {e}")

    # 2. Zero-key open fallback via wttr.in JSON
    wttr_report = await _get_wttr_climate(CITY)
    if wttr_report:
        return await edit_or_reply(event, wttr_report)

    await edit_or_reply(event, f"`Could not find climate report for {CITY}. Check city name.`")


@catub.cat_cmd(
    pattern=r"setcity(?:\s|$)([\s\S]*)",
    command=("setcity", plugin_category),
    info={
        "header": "To set default city for climate cmd",
        "description": "Sets your default city so you can just use .weather or .climate whenever needed without typing city name each time",
        "usage": [
            "{tr}setcity",
            "{tr}setcity <city name>",
        ],
    },
)
async def set_default_city(event):
    "To set default city for climate/weather cmd"
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        current = gvarstatus("DEFCITY") or "Delhi"
        return await edit_or_reply(event, f"`Current default city is set to: {current}.`")

    # If OpenWeatherMap is configured, test against it
    if Config.OPEN_WEATHER_MAP_APPID:
        try:
            timezone_countries = {timezone: country for country, timezones in c_tz.items() for timezone in timezones}
            req_city = input_str
            if "," in req_city:
                newcity = req_city.split(",")
                if len(newcity[1]) == 2:
                    req_city = f"{newcity[0].strip()},{newcity[1].strip()}"
                else:
                    country = await get_tz((newcity[1].strip()).title())
                    if country and f"{country}" in timezone_countries:
                        countrycode = timezone_countries[f"{country}"]
                        req_city = f"{newcity[0].strip()},{countrycode.strip()}"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={req_city}&appid={Config.OPEN_WEATHER_MAP_APPID}"
            async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
                request = await client.get(url)
            if request.status_code == 200:
                result = json.loads(request.text)
                cityname = result["name"]
                country = result["sys"]["country"]
                fullc_n = c_n.get(f"{country}", country)
                addgvar("DEFCITY", cityname)
                return await edit_or_reply(event, f"`Set default city as {cityname}, {fullc_n}.`")
        except Exception as e:
            LOGS.warning(f"OpenWeatherMap validation failed: {e}")

    # Zero-key fallback: validate via wttr.in
    try:
        url = f"https://wttr.in/{urllib.parse.quote_plus(input_str)}?format=j1"
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                nearest = data.get("nearest_area", [{}])[0]
                cityname = nearest.get("areaName", [{}])[0].get("value") or input_str
                country = nearest.get("country", [{}])[0].get("value") or ""
                addgvar("DEFCITY", cityname)
                loc = f"{cityname}, {country}" if country else cityname
                return await edit_or_reply(event, f"`Set default city as {loc}.`")
    except Exception as e:
        LOGS.warning(f"wttr.in city validation failed: {e}")

    await edit_or_reply(event, f"`Invalid city: {input_str}. Could not set default city.`")


@catub.cat_cmd(
    pattern=r"weather(?:\s|$)([\s\S]*)",
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
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        input_str = gvarstatus("DEFCITY") or "Delhi"
    city = urllib.parse.quote_plus(input_str)
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(f"https://wttr.in/{city}?mnT0&lang=en")
        if resp.status_code != 200 or not resp.text.strip():
            return await edit_or_reply(event, f"__Could not retrieve weather report for `{input_str}`.__")
        output = resp.text
    await edit_or_reply(event, output, parse_mode=_format.parse_pre)


@catub.cat_cmd(
    pattern=r"wttr(?:\s|$)([\s\S]*)",
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
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        input_str = gvarstatus("DEFCITY") or "Delhi"
    city = urllib.parse.quote_plus(input_str)
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        sample_url = f"https://wttr.in/{city}.png"
        resp = await client.get(sample_url)
        if resp.status_code != 200:
            return await edit_or_reply(event, f"__Could not retrieve weather image for `{input_str}`.__")
        response_api = resp.content
        with io.BytesIO(response_api) as out_file:
            await event.reply(f"**City : **`{input_str}`", file=out_file, reply_to=reply_to_id)
    try:
        await event.delete()
    except Exception as e:
        LOGS.info(str(e))
