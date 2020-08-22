from userbot import catdef
import requests
import os
from userbot.uniborgConfig import Config
import re 

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
     os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"
#thumb image
with open(thumb_image_path, "wb") as f:
    f.write(requests.get(Config.THUMB_IMAGE).content)
    
deEmojify = catdef.deEmojify
trumptweet = catdef.trumptweet 
changemymind = catdef.changemymind
kannagen = catdef.kannagen
moditweet = catdef.moditweet
tweets = catdef.tweets
waifutxt = catdef.waifutxt
catmusic = catdef.catmusic 
catmusicvideo = catdef.catmusicvideo
admin_groups = catdef.admin_groups
iphonex = catdef.iphonex
baguette = catdef.baguette
threats = catdef.threats
lolice = catdef.lolice
trash = catdef.trash
awooify = catdef.awooify
convert_toimage = catdef.convert_toimage
trap = catdef.trap
phcomment = catdef.phcomment
extract_time = catdef.extract_time
take_screen_shot = catdef.take_screen_shot
runcmd = catdef.runcmd

def check(cat):
    if "/start" in cat:
        return True 
    hi = re.search(f"\\b{cat}\\b" ,"a|b|c|d")
    if hi:
        return True
    return False

statstext = "yet to write"
