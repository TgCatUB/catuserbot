# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.

""" Userbot module containing various scrapers. """
import os
import shutil
from time import sleep
from . import deEmojify
from requests import get
from html import unescape
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.error import HTTPError
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from .. import CMD_HELP, CHROME_DRIVER, GOOGLE_CHROME_BIN 

CARBONLANG = "auto"
LANG = "en"

@borg.on(admin_cmd(outgoing=True, pattern="carbon(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="carbon(?: |$)(.*)",allow_sudo = True))
async def carbon_api(e):
   """ A Wrapper for carbon.now.sh """
   await e.edit("`Processing..`")
   CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
   global CARBONLANG
   textx = await e.get_reply_message()
   pcode = e.text
   if pcode[8:]:
         pcode = str(pcode[8:])
   elif textx:
         pcode = str(textx.message) # Importing message to module
   pcode = deEmojify(pcode)
   code = quote_plus(pcode) # Converting to urlencoded
   cat = await edit_or_reply(e ,"`Meking Carbon...\n25%`")
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
   await cat.edit("`Be Patient...\n50%`")
   download_path = './'
   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
   command_result = driver.execute("send_command", params)
   driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
  # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
  # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
   await cat.edit("`Processing..\n75%`")
   # Waiting for downloading
   sleep(2.5)
   await cat.edit("`Done Dana Done...\n100%`")
   file = './carbon.png'
   await cat.edit("`Uploading..`")
   await e.client.send_file(
         e.chat_id,
         file,
         caption="Here's your carbon, \n Carbonised by cat",
         force_document=True,
         reply_to=e.message.reply_to_msg_id
         )
   os.remove('./carbon.png')
   driver.quit()
   # Removing carbon.png after uploading
   await cat.delete() # Deleting msg
   
CMD_HELP.update({
    "carbon":
    "**Syntax :** `.carbon` <reply to code>\
    \n**Usage : **Shows your code in different style\
    "
})   