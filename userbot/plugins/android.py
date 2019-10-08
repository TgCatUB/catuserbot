# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
# Credit : PaperplaneExtended;___;
""" Userbot module containing commands related to android"""

import re
from requests import get
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.utils import register


GITHUB = 'https://github.com'
MAGISK_REPO = f'{GITHUB}/topjohnwu/Magisk/releases'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@register(outgoing=True, pattern="^.magisk$")
async def magisk(request):
    """ magisk latest releases """
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        page = BeautifulSoup(get(MAGISK_REPO).content, 'lxml')
        links = '\n'.join([i['href'] for i in page.findAll('a')])
        releases = ''
        try:
            latest_apk = re.findall(r'/.*MagiskManager-v.*apk', links)[0]
            releases += f'[{latest_apk.split("/")[-1]}]({GITHUB}/{latest_apk})\n'
        except IndexError:
            releases += "`can't find latest apk`"
        try:
            latest_zip = re.findall(r'/.*Magisk-v.*zip', links)[0]
            releases += f'[{latest_zip.split("/")[-1]}]({GITHUB}/{latest_zip})\n'
        except IndexError:
            releases += "`can't find latest zip`"
        try:
            latest_uninstaller = re.findall(r'/.*Magisk-uninstaller-.*zip', links)[0]
            releases += f'[{latest_uninstaller.split("/")[-1]}]({GITHUB}/{latest_uninstaller})\n'
        except IndexError:
            releases += "`can't find latest uninstaller`"
        await request.edit(releases)


@register(outgoing=True, pattern=r"^.device(?: |$)(\S*)")
async def device_info(request):
    """ get android device basic info from its codename """
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        device = request.pattern_match.group(1)
        if device:
            pass
        elif textx:
            device = textx.text
        else:
            await request.edit("`Usage: .device <codename> / <model>`")
            return
        found = [i for i in get(DEVICES_DATA).json()
                 if i["device"] == device or i["model"] == device]
        if found:
            reply = ''
            for item in found:
                brand = item['brand']
                name = item['name']
                codename = item['device']
                model = item['model']
                reply += f'{brand} {name}\n' \
                    f'**Codename**: `{codename}`\n' \
                    f'**Model**: {model}\n\n'
        else:
            reply = f"`Couldn't find info about {device}!`\n"
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    """ search for android codename """
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        brand = request.pattern_match.group(1).lower()
        device = request.pattern_match.group(2).lower()
        if brand and device:
            pass
        elif textx:
            brand = textx.text.split(' ')[0]
            device = ' '.join(textx.text.split(' ')[1:])
        else:
            await request.edit("`Usage: .codename <brand> <device>`")
            return
        found = [i for i in get(DEVICES_DATA).json()
                 if i["brand"].lower() == brand and device in i["name"].lower()]
        if found:
            reply = ''
            for item in found:
                brand = item['brand']
                name = item['name']
                codename = item['device']
                model = item['model']
                reply += f'{brand} {name}\n' \
                    f'**Codename**: `{codename}`\n' \
                    f'**Model**: {model}\n\n'
        else:
            reply = f"`Couldn't find {device} codename!`\n"
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    """ Mobile devices specifications """
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        brand = request.pattern_match.group(1).lower()
        device = request.pattern_match.group(2).lower()
        if brand and device:
            pass
        elif textx:
            brand = textx.text.split(' ')[0]
            device = ' '.join(textx.text.split(' ')[1:])
        else:
            await request.edit("`Usage: .specs <brand> <device>`")
            return
        all_brands = BeautifulSoup(
            get('https://www.devicespecifications.com/en/brand-more').content, 'lxml') \
            .find('div', {'class': 'brand-listing-container-news'}).findAll('a')
        brand_page_url = None
        try:
            brand_page_url = [i['href'] for i in all_brands if brand == i.text.strip().lower()][0]
        except IndexError:
            await request.edit(f'`{brand} is unknown brand!`')
        devices = BeautifulSoup(get(brand_page_url).content, 'lxml') \
            .findAll('div', {'class': 'model-listing-container-80'})
        device_page_url = None
        try:
            device_page_url = [i.a['href'] for i in BeautifulSoup(str(devices), 'lxml')
                               .findAll('h3') if device in i.text.strip().lower()][0]
        except IndexError:
            await request.edit(f"`can't find {device}!`")
        reply = ''
        info = BeautifulSoup(get(device_page_url).content, 'lxml') \
            .find('div', {'id': 'model-brief-specifications'})
        specifications = re.findall(r'<b>.*?<br/>', str(info))
        for item in specifications:
            title = re.findall(r'<b>(.*?)</b>', item)[0].strip()
            data = re.findall(r'</b>: (.*?)<br/>', item)[0]\
                .replace('<b>', '').replace('</b>', '').strip()
            reply += f'**{title}**: {data}\n'
        await request.edit(reply)


CMD_HELP.update({
    "magisk": "Get latest Magisk releases"
})
CMD_HELP.update({
    "device": ".device <codename>\nUsage: Get info about android device codename or model."
})
CMD_HELP.update({
    "codename": ".codename <brand> <device>\nUsage: Search for android device codename."
})
CMD_HELP.update({
    "specs": ".specs <brand> <device>\nUsage: Get device specifications info."
})
