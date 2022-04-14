import json
import re

from bs4 import BeautifulSoup
from requests import get

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="magisk$",
    command=("magisk", plugin_category),
    info={
        "header": "To Get latest Magisk releases",
        "usage": "{tr}magisk",
    },
)
async def kakashi(event):
    "Get latest Magisk releases"
    magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk-files/"
    magisk_dict = {
        "⦁ **Stable**": magisk_repo + "master/stable.json",
        "⦁ **Beta**": magisk_repo + "master/beta.json",
        "⦁ **Canary**": magisk_repo + "master/canary.json",
    }
    releases = "**Latest Magisk Releases**\n\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [APK v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[Changelog]({data["magisk"]["note"]})\n'
        )
    await edit_or_reply(event, releases)


@catub.cat_cmd(
    pattern="device(?: |$)(\S*)",
    command=("device", plugin_category),
    info={
        "header": "To get android device name/model from its codename",
        "usage": "{tr}device <codename>",
        "examples": "{tr}device whyred",
    },
)
async def device_info(event):
    "get android device name from its codename"
    textx = await event.get_reply_message()
    codename = event.pattern_match.group(1)
    if not codename:
        if textx:
            codename = textx.text
        else:
            return await edit_delete(event, "`Usage: .device <codename> / <model>`")
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Brand**: {item['brand']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="codename(?: |)([\S]*)(?: |)([\s\S]*)",
    command=("codename", plugin_category),
    info={
        "header": "To Search for android device codename",
        "usage": "{tr}codename <brand> <device>",
        "examples": "{tr}codename Xiaomi Redmi Note 5 Pro",
    },
)
async def codename_info(event):
    textx = await event.get_reply_message()
    brand = event.pattern_match.group(1).lower()
    device = event.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await edit_delete(event, "`Usage: .codename <brand> <device>`")

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    if not devices:
        return await edit_or_reply(event, f"__I couldn't find {brand}.__")
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Search results for {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Device**: {item['device']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="specs(?: |)([\S]*)(?: |)([\s\S]*)",
    command=("specs", plugin_category),
    info={
        "header": "To Get info about android device .",
        "usage": "{tr}specs",
        "examples": "{tr}specs Xiaomi Redmi Note 5 Pro",
    },
)
async def devices_specifications(event):
    "Mobile devices specifications"
    textx = await event.get_reply_message()
    brand = event.pattern_match.group(1).lower()
    device = event.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await edit_delete(event, "`Usage: .specs <brand> <device>`")
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml"
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        return await edit_delete(event, f"`{brand} is unknown brand!`")
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        return await edit_delete(event, f"`can't find {device}!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="twrp(?: |$)(\S*)",
    command=("twrp", plugin_category),
    info={
        "header": "To Get latest twrp download links for android device.",
        "usage": "{tr}twrp <codename>",
        "examples": "{tr}twrp whyred",
    },
)
async def twrp(event):
    "get android device twrp"
    textx = await event.get_reply_message()
    device = event.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        return await edit_delete(event, "`Usage: .twrp <codename>`")
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        return await edit_delete(event, reply)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await edit_or_reply(event, reply)
