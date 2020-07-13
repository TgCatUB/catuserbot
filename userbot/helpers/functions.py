import requests , os, re
from bs4 import BeautifulSoup
from asyncio import sleep
from random import choice
from telethon import events
from emoji import get_emoji_regexp
from PIL import Image
from validators.url import url

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

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


#for getmusic

async def catmusic(cat,DEFAULT_AUDIO_QUALITY):
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
  command = ('youtube-dl --extract-audio --audio-format mp3 --audio-quality ' +DEFAULT_AUDIO_QUALITY + ' ' + video_link)	
  os.system(command)

#for getmusicvideo

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
    command = ('youtube-dl -f "[filesize<20M]" ' +video_link)  
    os.system(command)

# for stickertxt

async def waifutxt(text, chat_id ,reply_to_id , bot, borg):
    animus = [0, 1, 2, 3, 4, 7, 9, 15, 20, 22, 27, 29, 32, 33, 34, 37, 38, 
              41, 42, 44, 45, 47, 48, 51, 52, 53, 55, 56, 57, 58, 61, 62, 63]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{choice(animus)}{(deEmojify(text))}")
    cat = await sticcers[0].click( "me" ,
                            hide_via=True)
    if cat:
        await borg.send_file(int(chat_id) , cat , reply_to = reply_to_id ) 
        await cat.delete()

async def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return get_emoji_regexp().sub(u'', inputString)
    
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
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"

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
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"    
    
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
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"     
    
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
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"      
