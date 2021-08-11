import calendar
import json
import os
import re
from datetime import datetime
from urllib.parse import quote

import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import AioHttp
from ..helpers.utils import _catutils, _format, reply_id

plugin_category = "tools"


LOGS = logging.getLogger(__name__)


@catub.cat_cmd(
    pattern="cur(?:\s|$)([\s\S]*)",
    command=("cur", plugin_category),
    info={
        "header": "To convert one currency value to other.",
        "description": "To find exchange rates of currencies.",
        "usage": "{tr}cur <value> <from currencyid> <to currencyid>",
        "examples": "{tr}cur 10 USD INR",
        "note": "List of currency ids are [Country & Currency](https://da.gd/j588M) or [Only Currency data](https://da.gd/obZIdk)",
    },
)
async def currency(event):
    """To convert one currency value to other."""
    if Config.CURRENCY_API is None:
        return await edit_delete(
            event,
            "__You haven't set the api value. Set Api var __`CURRENCY_API` __in heroku get value from https://free.currencyconverterapi.com__.",
            link_preview=False,
            time=10,
        )
    input_str = event.pattern_match.group(1)
    values = input_str.split(" ")
    if len(values) == 3:
        value, fromcurrency, tocurrency = values
    else:
        return await edit_delete(event, "__Use proper syntax. check__ `.help -c cur`")
    fromcurrency = fromcurrency.upper()
    tocurrency = tocurrency.upper()
    try:
        value = float(value)
        aresponse = await AioHttp().get_json(
            f"https://free.currconv.com/api/v7/convert?q={fromcurrency}_{tocurrency}&compact=ultra&apiKey={Config.CURRENCY_API}"
        )
        symbols = await AioHttp().get_raw(
            "https://raw.githubusercontent.com/sandy1709/CatUserbot-Resources/master/Resources/Data/currency.py"
        )

        symbols = json.loads(re.sub(", *\n *}", "}", symbols.decode("utf-8")))
        try:
            result = aresponse[f"{fromcurrency}_{tocurrency}"]
        except KeyError:
            return await edit_delete(
                event,
                "__You have used wrong currency codes or Api can't fetch details or try by restarting bot it will work if everything is fine.__",
                time=10,
            )
        output = float(value) * float(result)
        output = round(output, 4)
        await edit_or_reply(
            event,
            f"The Currency value of **{symbols[fromcurrency]}{value} {fromcurrency}** in **{tocurrency}** is **{symbols[tocurrency]}{output}**",
        )
    except Exception:
        await edit_or_reply(
            event,
            "__It seems you are using different currency value. which doesn't exist on earth.__",
        )


@catub.cat_cmd(
    pattern="scan( -i)?$",
    command=("scan", plugin_category),
    info={
        "header": "To scan the replied file for virus.",
        "flag": {"i": "to get output as image."},
        "usage": ["{tr}scan", "{tr}scan -i"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if not event.reply_to_msg_id:
        return await edit_or_reply(event, "```Reply to any user message.```")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await edit_or_reply(event, "```reply to a media message```")
    chat = "@VS_Robot"
    catevent = await edit_or_reply(event, " `Sliding my tip, of fingers over it`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await event.client.forward_messages(chat, reply_message)
            response1 = await conv.get_response()
            if response1.text:
                await event.client.send_read_acknowledge(conv.chat_id)
                return await catevent.edit(response1.text, parse_mode=_format.parse_pre)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            response3 = await conv.get_response()
            response4 = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await catevent.edit(
                "`You blocked `@VS_Robot` Unblock it and give a try`"
            )
        if not input_str:
            return await edit_or_reply(catevent, response4.text)
        await catevent.delete()
        await event.client.send_file(
            event.chat_id, response3.media, reply_to=(await reply_id(event))
        )


@catub.cat_cmd(
    pattern="decode$",
    command=("decode", plugin_category),
    info={
        "header": "To decode qrcode or barcode",
        "description": "Reply to qrcode or barcode to decode it and get text.",
        "usage": "{tr}decode",
    },
)
async def parseqr(event):
    "To decode qrcode or barcode"
    catevent = await edit_or_reply(event, "`Decoding....`")
    reply = await event.get_reply_message()
    downloaded_file_name = await reply.download_media()
    # parse the Official ZXing webpage to decode the QRCode
    command_to_exec = f"curl -s -F f=@{downloaded_file_name} https://zxing.org/w/decode"
    t_response, e_response = (await _catutils.runcmd(command_to_exec))[:2]
    if os.path.exists(downloaded_file_name):
        os.remove(downloaded_file_name)
    soup = BeautifulSoup(t_response, "html.parser")
    try:
        qr_contents = soup.find_all("pre")[0].text
        await edit_or_reply(catevent, f"**The decoded message is :**\n`{qr_contents}`")
    except IndexError:
        result = soup.text
        await edit_or_reply(catevent, f"**Failed to Decode:**\n`{result}`")
    except Exception as e:
        await edit_or_reply(catevent, f"**Error:**\n`{e}`")


@catub.cat_cmd(
    pattern="barcode ?([\s\S]*)",
    command=("barcode", plugin_category),
    info={
        "header": "To get barcode of given text.",
        "usage": "{tr}barcode <text>",
        "example": "{tr}barcode www.google.com",
    },
)
async def _(event):
    "to make barcode of given content."
    catevent = await edit_or_reply(event, "...")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = await reply_id(event)
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") + "\r\n" for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await event.client.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        os.remove(filename)
    except Exception as e:
        return await catevent.edit(str(e))
    end = datetime.now()
    ms = (end - start).seconds
    await edit_delete(catevent, "Created BarCode in {} seconds".format(ms))


@catub.cat_cmd(
    pattern="makeqr(?: |$)([\s\S]*)",
    command=("makeqr", plugin_category),
    info={
        "header": "To get makeqr of given text.",
        "usage": "{tr}makeqr <text>",
        "example": "{tr}makeqr www.google.com",
    },
)
async def make_qr(makeqr):
    "make a QR Code containing the given content."
    input_str = makeqr.pattern_match.group(1)
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = await reply_id(makeqr)
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = "".join(media.decode("UTF-8") + "\r\n" for media in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(
        makeqr.chat_id, "img_file.webp", reply_to=reply_msg_id
    )
    os.remove("img_file.webp")
    await makeqr.delete()


@catub.cat_cmd(
    pattern="cal ([\s\S]*)",
    command=("cal", plugin_category),
    info={
        "header": "To get calendar of given month and year.",
        "usage": "{tr}cal year ; month",
        "examples": "{tr}cal 2021 ; 5",
    },
)
async def _(event):
    "To get calendar of given month and year."
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(";")
    if len(input_sgra) != 2:
        return await edit_delete(event, "**Syntax : **`.cal year ; month `", 5)

    yyyy = input_sgra[0]
    mm = input_sgra[1]
    try:
        output_result = calendar.month(int(yyyy.strip()), int(mm.strip()))
        await edit_or_reply(event, f"```{output_result}```")
    except Exception as e:
        await edit_delete(event, f"**Error:**\n`{e}`", 5)


@catub.cat_cmd(
    pattern="ip(?:\s|$)([\s\S]*)",
    command=("ip", plugin_category),
    info={
        "header": "Find details of an IP address",
        "description": "To check detailed info of provided ip address.",
        "usage": "{tr}ip <mine/ip address",
        "examples": [
            "{tr}ip mine",
            "{tr}ip 13.106.3.255",
        ],
    },
)
async def spy(event):
    "To see details of an ip."
    inpt = event.pattern_match.group(1)
    if not inpt:
        return await edit_delete(event, "**Give an ip address to lookup...**", 20)
    check = "" if inpt == "mine" else inpt
    API = Config.IPDATA_API
    if API is None:
        return await edit_delete(
            event,
            "**Get an API key from [Ipdata](https://dashboard.ipdata.co/sign-up.html) & set that in heroku var `IPDATA_API`**",
            80,
        )
    url = requests.get(f"https://api.ipdata.co/{check}?api-key={API}")
    r = url.json()
    try:
        return await edit_delete(event, f"**{r['message']}**", 60)
    except KeyError:
        await edit_or_reply(event, "🔍 **Searching...**")
    ip = r["ip"]
    city = r["city"]
    postal = r["postal"]
    region = r["region"]
    latitude = r["latitude"]
    carrier = r["asn"]["name"]
    longitude = r["longitude"]
    country = r["country_name"]
    carriel = r["asn"]["domain"]
    region_code = r["region_code"]
    continent = r["continent_name"]
    time_z = r["time_zone"]["abbr"]
    currcode = r["currency"]["code"]
    calling_code = r["calling_code"]
    country_code = r["country_code"]
    currency = r["currency"]["name"]
    curnative = r["currency"]["native"]
    lang1 = r["languages"][0]["name"]
    time_zone = r["time_zone"]["name"]
    emoji_flag = r["emoji_flag"]
    continent_code = r["continent_code"]
    native = r["languages"][0]["native"]
    current_time = r["time_zone"]["current_time"]

    symbol = "₹" if country == "India" else curnative
    language1 = (
        f"<code>{lang1}</code>"
        if lang1 == native
        else f"<code>{lang1}</code> [<code>{native}</code>]"
    )

    try:
        lang2 = f', <code>{r["languages"][1]["name"]}</code>'
    except IndexError:
        lang2 = ""

    string = f"✘ <b>Lookup For Ip : {ip}</b> {emoji_flag}\n\n\
    <b>• City Name :</b>  <code>{city}</code>\n\
    <b>• Region Name :</b>  <code>{region}</code> [<code>{region_code}</code>]\n\
    <b>• Country Name :</b>  <code>{country}</code> [<code>{country_code}</code>]\n\
    <b>• Continent Name :</b>  <code>{continent}</code> [<code>{continent_code}</code>]\n\
    <b>• View on Map :  <a href = https://www.google.com/maps/search/?api=1&query={latitude}%2C{longitude}>Google Map</a></b>\n\
    <b>• Postal Code :</b> <code>{postal}</code>\n\
    <b>• Caller Code :</b>  <code>+{calling_code}</code>\n\
    <b>• Carrier Detail :  <a href = https://www.{carriel}>{' '.join(carrier.split()[:2])}</a></b>\n\
    <b>• Language :</b>  {language1} {lang2}\n\
    <b>• Currency :</b>  <code>{currency}</code> [<code>{symbol}{currcode}</code>]\n\
    <b>• Time Zone :</b> <code>{time_zone}</code> [<code>{time_z}</code>]\n\
    <b>• Time :</b> <code>{current_time[11:16]}</code>\n\
    <b>• Date :</b> <code>{current_time[:10]}</code>\n\
    <b>• Time Offset :</b> <code>{current_time[-6:]}</code>"
    await edit_or_reply(event, string, parse_mode="html")


@catub.cat_cmd(
    pattern="ifsc ([\s\S]*)",
    command=("ifsc", plugin_category),
    info={
        "header": "to get details of the relevant bank or branch.",
        "usage": "{tr}ifsc <ifsc code>",
        "examples": "{tr}ifsc SBIN0016086",
    },
)
async def _(event):
    "to get details of the relevant bank or branch."
    input_str = event.pattern_match.group(1)
    url = "https://ifsc.razorpay.com/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 200:
        return await edit_or_reply(event, "`{}`: {}".format(input_str, r.text))

    b = r.json()
    a = json.dumps(b, sort_keys=True, indent=4)
    # https://stackoverflow.com/a/9105132/4723940
    await edit_or_reply(event, str(a))


@catub.cat_cmd(
    pattern="color ([\s\S]*)",
    command=("color", plugin_category),
    info={
        "header": "To get color pic of given hexa color code.",
        "usage": "{tr}color <colour code>",
        "examples": "{tr}color #ff0000",
    },
)
async def _(event):
    "To get color pic of given hexa color code."
    input_str = event.pattern_match.group(1)
    message_id = await reply_id(event)
    if not input_str.startswith("#"):
        return await edit_or_reply(
            event, "**Syntax : **`.color <color_code>` example : `.color #ff0000`"
        )
    try:
        usercolor = ImageColor.getrgb(input_str)
    except Exception as e:
        return await event.edit(str(e))
    else:
        im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
        im.save("cat.png", "PNG")
        input_str = input_str.replace("#", "#COLOR_")
        await event.client.send_file(
            event.chat_id,
            "cat.png",
            force_document=False,
            caption=input_str,
            reply_to=message_id,
        )
        os.remove("cat.png")
        await event.delete()


@catub.cat_cmd(
    pattern="xkcd(?:\s|$)([\s\S]*)",
    command=("xkcd", plugin_category),
    info={
        "header": "Searches for the query for the relevant XKCD comic.",
        "usage": "{tr}xkcd <query>",
    },
)
async def _(event):
    "Searches for the query for the relevant XKCD comic."
    catevent = await edit_or_reply(event, "`processiong...........`")
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url, params={"action": "xkcd", "query": quote(input_str)}
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if not r.ok:
        return await catevent.edit("xkcd n.{} not found!".format(xkcd_id))
    data = r.json()
    year = data.get("year")
    month = data["month"].zfill(2)
    day = data["day"].zfill(2)
    xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
    safe_title = data.get("safe_title")
    data.get("transcript")
    alt = data.get("alt")
    img = data.get("img")
    data.get("title")
    output_str = """[\u2060]({})**{}**
[XKCD ]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(
        img, input_str, xkcd_link, safe_title, alt, day, month, year
    )
    await catevent.edit(output_str, link_preview=True)
