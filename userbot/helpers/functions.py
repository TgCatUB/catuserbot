import requests 
import os
import re
import subprocess
from bs4 import BeautifulSoup
from asyncio import sleep
from random import choice
from telethon import events
from emoji import get_emoji_regexp
from PIL import Image
from validators.url import url
from telethon.tl.types import Channel

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
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

#gban
async def admin_groups(cat):
    catgroups = []
    async for dialog in cat.client.iter_dialogs():
        entity = dialog.entity  
        if isinstance(entity, Channel):
            if entity.megagroup:
                if entity.creator or entity.admin_rights:
                   catgroups.append(entity.id)
    return catgroups

#for getmusic
async def catmusic(cat , QUALITY):
  search = cat
  headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
  html = requests.get('https://www.youtube.com/results?search_query='+search, headers=headers).text
  soup = BeautifulSoup(html, 'html.parser')
  for link in soup.find_all('a'):
    if '/watch?v=' in link.get('href'):
        # May change when Youtube Website may get updated in the future.
        video_link = link.get('href') 
        break
  video_link =  'http://www.youtube.com/'+video_link
  if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
  command = ('youtube-dl -o "./temp/%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality ' + QUALITY + ' ' + video_link)
  os.system(command)
  thumb = ('youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download ' + video_link)
  os .system(thumb)


async def catmusicvideo(cat):
    search = cat
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    html = requests.get('https://www.youtube.com/results?search_query='+search, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if '/watch?v=' in link.get('href'):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get('href') 
            break    
    video_link =  'http://www.youtube.com/'+video_link
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    command = ('youtube-dl -o "./temp/%(title)s.%(ext)s" -f "[filesize<20M]" ' +video_link)  
    os.system(command)
    thumb = ('youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download ' + video_link)
    os .system(thumb)

# for stickertxt
async def waifutxt(text, chat_id ,reply_to_id , bot, borg):
    animus = [0, 1, 2, 3, 4, 9, 15, 20, 22, 27, 29, 32, 33, 34, 37, 38, 
              41, 42, 44, 45, 47, 48, 51, 52, 53, 55, 56, 57, 58, 61, 62, 63]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{choice(animus)}{text}")
    cat = await sticcers[0].click( "me" ,
                            hide_via=True)
    if cat:
        await borg.send_file(int(chat_id) , cat , reply_to = reply_to_id ) 
        await cat.delete()

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats 
    "]+")

def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)
  
def convert_toimage(image):
    img = Image.open(image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")
    os.remove(image)
    return "temp.jpg"

# for nekobot
async def trumptweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.webp", "webp")    
        return "temp.webp"

async def changemymind(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"
    
async def kannagen(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.webp", "webp")    
        return "temp.webp"    
    
async def moditweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.webp", "webp")    
        return "temp.webp"     
    
async def tweets(text1,text2):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.webp", "webp")    
        return "temp.webp"      

async def iphonex(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=iphonex&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"       

async def baguette(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=baguette&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"     

async def threats(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"     

async def lolice(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=lolice&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"     

async def trash(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"     

async def awooify(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=awooify&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"     

async def trap(text1,text2,text3):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"

async def phcomment(text1,text2,text3):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")    
    return "temp.jpg"
