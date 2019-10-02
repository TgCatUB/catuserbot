"""
Carbon Scraper Plugin for Userbot. //text in creative way.
usage: .carbon //as a reply to any text message

Thanks to @AvinashReddy3108 for a Base Plugin.
Go and Do a star on his repo: https://github.com/AvinashReddy3108/PaperplaneExtended/

"""
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from telethon import events
from urllib.parse import quote_plus
from urllib.error import HTTPError
from time import sleep
import asyncio
import os

@borg.on(events.NewMessage(pattern=r"\.carbon", outgoing=True))
async def carbon_api(e):
 if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
   """ A Wrapper for carbon.now.sh """
   await e.edit("Processing...")
   CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
   CARBONLANG = "en"
   textx = await e.get_reply_message()
   pcode = e.text
   if pcode[8:]:
         pcode = str(pcode[8:])
   elif textx:
         pcode = str(textx.message) # Importing message to module
   code = quote_plus(pcode) # Converting to urlencoded
   url = CARBON.format(code=code, lang=CARBONLANG)
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.binary_location = Config.GOOGLE_CHROME_BIN
   chrome_options.add_argument("--window-size=1920x1080")
   chrome_options.add_argument("--disable-dev-shm-usage")
   chrome_options.add_argument("--no-sandbox")
   chrome_options.add_argument('--disable-gpu')
   prefs = {'download.default_directory' : './'}
   chrome_options.add_experimental_option('prefs', prefs)
   await e.edit("Processing 30%")

   driver = webdriver.Chrome(executable_path=Config.CHROME_DRIVER, options=chrome_options)
   driver.get(url)
   download_path = './'
   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
   command_result = driver.execute("send_command", params)

   driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
   sleep(5) # this might take a bit.
   driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
   sleep(5)
   await e.edit("Processing 50%")
   driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
   sleep(5) #Waiting for downloading

   await e.edit("Processing 90%")
   file = './carbon.png'
   await e.edit("Done!!")
   await e.client.send_file(
         e.chat_id,
         file,
         caption="《《CARBON BY PRINCE》》",
         force_document=False,
         reply_to=e.message.reply_to_msg_id,
         )

   os.remove('./carbon.png')
   # Removing carbon.png after uploading
   await e.delete() # Deleting msg
