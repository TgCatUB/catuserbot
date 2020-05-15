# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various scrapers. """

import os
import time
import asyncio
import shutil
from bs4 import BeautifulSoup
import re
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from urllib.parse import quote_plus
from urllib.error import HTTPError
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
import asyncurban
from requests import get
from search_engine_parser import GoogleSearch
from google_images_download import google_images_download
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.utils import register
from telethon.tl.types import DocumentAttributeAudio
from userbot.utils import progress, humanbytes, time_formatter
from userbot.uniborgConfig import Config

CARBONLANG = "auto"
TTS_LANG = "en"
TRT_LANG = "en"

BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
BOTLOG = True

LANG = "en"


@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
 if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
 
   """ A Wrapper for carbon.now.sh """
   await e.edit("`Processing..`")
   CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
   global CARBONLANG
   textx = await e.get_reply_message()
   pcode = e.text
   if pcode[8:]:
         pcodee = str(pcode[8:])
         if "|" in pcodee:
               pcode, skeme = pcodee.split("|")
         else:
               pcode = pcodee
               skeme = None
   elif textx:
         pcode = str(textx.message)
         skeme = None # Importing message to module
   code = quote_plus(pcode) # Converting to urlencoded
   await e.edit("`Meking Carbon...\n25%`")
   url = CARBON.format(code=code, lang=CARBONLANG)
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.binary_location = GOOGLE_CHROME_BIN
   chrome_options.add_argument("--window-size=1920x1080")
   chrome_options.add_argument("--disable-dev-shm-usage")
   chrome_options.add_argument("--no-sandbox")
   chrome_options.add_argument("--disable-gpu")
   prefs = {'download.default_directory' : './'}
   chrome_options.add_experimental_option('prefs', prefs)
   driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
   driver.get(url)
   await e.edit("`Be Patient...\n50%`")
   download_path = './'
   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
   command_result = driver.execute("send_command", params)
   driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div/span[2]').click()
   if skeme != None:
         k_skeme = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div/span[2]/input')
         k_skeme.send_keys(skeme)
         k_skeme.send_keys(Keys.DOWN)
         k_skeme.send_keys(Keys.ENTER)
   else:
       color_scheme = str(random.randint(1,29))
       driver.find_element_by_id(("downshift-0-item-" + color_scheme)).click()
   driver.find_element_by_id("export-menu").click()
   driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
   driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
   await e.edit("`Processing..\n75%`")
   # Waiting for downloading
   sleep(2.5)
   color_name = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div/span[2]/input').get_attribute('value')
   await e.edit("`Done Dana Done...\n100%`")
   file = './carbon.png'
   await e.edit("`Uploading..`")
   await e.client.send_file(
         e.chat_id,
         file,
         caption="`Here's your carbon!` \n**Colour Scheme: **`{}`".format(color_name),
         force_document=True,
         reply_to=e.message.reply_to_msg_id,
         )
   os.remove('./carbon.png')
   driver.quit()
   # Removing carbon.png after uploading
   await e.delete() # Deleting msg
    


@register(outgoing=True, pattern=r"^\.wiki (.*)")
async def wiki(wiki_q):
    """ For .wiki command, fetch content from Wikipedia. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Page not found.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("output.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption="`Output too large, sending as file`",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query `{match}` was executed successfully")



@register(outgoing=True, pattern=r"^\.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Give a text or reply to a message to translate!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await trans.edit("Invalid destination language.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"From **{source_lan.title()}**\nTo **{transl_lan.title()}:**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.",
        )


@register(pattern="^\.lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """ For .lang command, change the default langauge of userbot scrapers. """
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await value.edit(
                f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Text to Speech"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`Invalid Language code !!`\n`Available language codes for TTS`:\n\n`{tts_langs()}`"
            )
            return
    await value.edit(f"`Language for {scraper} changed to {LANG.title()}.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`Language for {scraper} changed to {LANG.title()}.`")

def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return get_emoji_regexp().sub(u'', inputString)
