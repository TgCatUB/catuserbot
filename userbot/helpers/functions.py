import requests
from bs4 import BeautifulSoup
import os

def get_readable_time(seconds: int) -> str:
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

def catmusic(cat,DEFAULT_AUDIO_QUALITY):
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
