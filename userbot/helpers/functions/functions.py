import os
import zipfile
from random import choice

import requests

from ..resources.states import states

from uuid import uuid4

def rand_key():
    return str(uuid4())[:8]

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


# covid india data


async def covidindia(state):
    url = "https://www.mohfw.gov.in/data/datanew.json"
    req = requests.get(url).json()
    for i in states:
        if i == state:
            return req[states.index(i)]
    return None


# for stickertxt
async def waifutxt(text, chat_id, reply_to_id, bot):
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
