# Created By @StarkXD 
# Fixed By @MrConfused 
# UserBot Plugin To Send Fresh Proxies From Proxyscrape.com
# Banned For Sensible Userbot And Users.
# Usage : For Http Proxy : .proxyhttp , For Socks4 : .proxysocks4 , For socks5 : .proxysocks5 

from telethon import events
from userbot.utils import admin_cmd 
from pySmartDL import SmartDL
import os

STARK_HTTP = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all" 
HTTP_TXT = ("**Proxy Info** \nType: __HTTPS__ \nTimeOut: __10000__ \nCountry: __All__ \nSsl: All \nAnonymity: __All__ \n[Click Here To View Or Download File Manually](https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all) \nUploaded By [Friday](https://github.com/starkgang/FridayUserBot) \n**Here Is Your Proxy** 👇")
STARK_SOCKS4 = "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all"
SOCKS4_TXT = ("**Proxy Info** \nType: __SOCKS4__ \nTimeOut: __10000__ \nCountry: __All__ \nSsl: __Only For Http Proxy__ \nAnonymity: __Only For Http__ \n[Click Here To View Or Download File Manually](https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all) \nUploaded By [Friday](https://github.com/starkgang/FridayUserBot) \n**Here Is Your Proxy** 👇")
STARK_SOCKS5 = "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all"
SOCKS5_TXT = ("**Proxy Info** \nType: __SOCKS4__ \nTimeOut: __10000__ \nCountry: __All__ \nSsl: __Only For Http Proxy__ \nAnonymity: __Only For Http__ \n[Click Here To View Or Download File Manually](https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all) \nUploaded By [Friday](https://github.com/starkgang/FridayUserBot) \n**Here Is Your Proxy** 👇")

@borg.on(admin_cmd(pattern="proxyhttp")) 
async def starkxD(event): 
    chat = await event.get_chat() 
    file_name = "proxy_http.txt"
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY , file_name)
    downloader = SmartDL( f"{STARK_HTTP}" , downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False) 
    await borg.send_message(event.chat_id , HTTP_TXT)
    await event.client.send_file(event.chat_id , downloaded_file_name) 
    
@borg.on(admin_cmd(pattern="proxysocks4")) 
async def starkgang(event): 
    chat = await event.get_chat() 
    file_name = "proxy_socks4.txt"
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY , file_name)
    downloader = SmartDL( f"{STARK_SOCKS4}" , downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False) 
    await borg.send_message(event.chat_id , SOCKS4_TXT)
    await event.client.send_file(event.chat_id , downloaded_file_name) 
 
@borg.on(admin_cmd(pattern="proxysocks5")) 
async def friday(event): 
    chat = await event.get_chat() 
    file_name = "proxy_socks5.txt"
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY , file_name)
    downloader = SmartDL( f"{STARK_SOCKS5}" , downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False) 
    await borg.send_message(event.chat_id , SOCKS5_TXT)
    await event.client.send_file(event.chat_id , downloaded_file_name) 
    