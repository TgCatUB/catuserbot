from userbot import catdef
import requests
import os

#thumb image
with open("./DOWNLOADS/thumb_image.jpg", "wb") as f:
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
