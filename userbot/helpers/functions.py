import os
import re
import time
import urllib.request
import zipfile
from datetime import datetime
from random import choice

import PIL.ImageOps
import requests
from emoji import get_emoji_regexp
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import Channel, PollAnswer
from validators.url import url
from youtubesearchpython import VideosSearch

from .resources.states import states


def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


# gban


async def admin_groups(cat):
    catgroups = []
    async for dialog in cat.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            catgroups.append(entity.id)
    return catgroups


# for getmusic


async def yt_search(cat):
    try:
        cat = urllib.parse.quote(cat)
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + cat
        )
        user_data = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_link = []
        k = 0
        for i in user_data:
            if user_data:
                video_link.append("https://www.youtube.com/watch?v=" + user_data[k])
            k += 1
            if k > 3:
                break
        if video_link:
            return video_link[0]
        return "Couldnt fetch results"
    except Exception:
        return "Couldnt fetch results"


async def sanga_seperator(sanga_list):
    for i in sanga_list:
        if i.startswith("🔗"):
            sanga_list.remove(i)
    s = 0
    for i in sanga_list:
        if i.startswith("Username History"):
            break
        s += 1
    usernames = sanga_list[s:]
    names = sanga_list[:s]
    return names, usernames


# unziping file
async def unzip(downloaded_file_name):
    with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
        zip_ref.extractall("./temp")
    downloaded_file_name = os.path.splitext(downloaded_file_name)[0]
    return f"{downloaded_file_name}.gif"


async def ytsearch(query, limit):
    result = ""
    videolinks = VideosSearch(query.lower(), limit=limit)
    for v in videolinks.result()["result"]:
        textresult = f"[{v['title']}](https://www.youtube.com/watch?v={v['id']})\n"
        try:
            textresult += f"**Description : **`{v['descriptionSnippet'][-1]['text']}`\n"
        except Exception:
            textresult += "**Description : **`None`\n"
        textresult += f"**Duration : **__{v['duration']}__  **Views : **__{v['viewCount']['short']}__\n"
        result += f"☞ {textresult}\n"
    return result


# https://github.com/pokurt/LyndaRobot/blob/7556ca0efafd357008131fa88401a8bb8057006f/lynda/modules/helper_funcs/string_handling.py#L238


async def extract_time(cat, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d", "w")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            cat.edit("Invalid time amount specified.")
            return ""
        if unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        elif unit == "w":
            bantime = int(time.time() + int(time_num) * 7 * 24 * 60 * 60)
        else:
            # how even...?
            return ""
        return bantime
    await cat.edit(
        f"Invalid time type specified. Expected m , h , d or w but got: {time_val[-1]}"
    )
    return ""


song_dl = "youtube-dl --force-ipv4 --write-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"
thumb_dl = "youtube-dl --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "youtube-dl --force-ipv4 --write-thumbnail  -o './temp/%(title)s.%(ext)s' -f '[filesize<20M]' {video_link}"
name_dl = (
    "youtube-dl --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)


# For polls


def Build_Poll(options):
    return [PollAnswer(option, bytes(i)) for i, option in enumerate(options, start=1)]


def convert_toimage(image, filename=None):
    filename = filename or os.path.join("./temp/", "temp.jpg")
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(filename, "jpeg")
    os.remove(image)
    return filename


def convert_tosticker(response, filename=None):
    filename = filename or os.path.join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    os.remove(response)
    return filename


# covid india data


async def covidindia(state):
    url = "https://www.mohfw.gov.in/data/datanew.json"
    req = requests.get(url).json()
    for i in states:
        if i == state:
            return req[states.index(i)]
    return None


# for nekobot


async def fakegs(search, result):
    imgurl = "https://i.imgur.com/wNFr5X2.jpg"
    with open("./temp/temp.jpg", "wb") as f:
        f.write(requests.get(imgurl).content)
    img = Image.open("./temp/temp.jpg")
    drawing = ImageDraw.Draw(img)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font1 = ImageFont.truetype("userbot/helpers/styles/ProductSans-BoldItalic.ttf", 20)
    font2 = ImageFont.truetype("userbot/helpers/styles/ProductSans-Light.ttf", 23)
    drawing.text((450, 258), result, fill=blue, font=font1)
    drawing.text((270, 37), search, fill=black, font=font2)
    img.save("./temp/temp.jpg")
    return "./temp/temp.jpg"


async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def moditweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def tweets(text1, text2):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def iphonex(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def baguette(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=baguette&url={text}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def threats(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def lolice(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=lolice&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def awooify(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=awooify&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phcomment(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


# http://effbot.org/imagingbook/imageops.html
# https://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging/38378828


async def invert_colors(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(endname)


async def flip_image(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.flip(image)
    inverted_image.save(endname)


async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.grayscale(image)
    inverted_image.save(endname)


async def mirror_file(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.mirror(image)
    inverted_image.save(endname)


async def solarize(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.solarize(image, threshold=128)
    inverted_image.save(endname)


async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


# for stickertxt
async def waifutxt(text, chat_id, reply_to_id, bot, borg):
    animus = [
        0,
        1,
        2,
        3,
        4,
        9,
        15,
        20,
        22,
        27,
        29,
        32,
        33,
        34,
        37,
        38,
        41,
        42,
        44,
        45,
        47,
        48,
        51,
        52,
        53,
        55,
        56,
        57,
        58,
        61,
        62,
        63,
    ]
    sticcers = await bot.inline_query("stickerizerbot", f"#{choice(animus)}{text}")
    cat = await sticcers[0].click("me", hide_via=True)
    if cat:
        await bot.send_file(int(chat_id), cat, reply_to=reply_to_id)
        await cat.delete()
