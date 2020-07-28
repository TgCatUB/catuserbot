from userbot import catdef
from pySmartDL import SmartDL
from PIL import Image, ImageDraw, ImageFont
import shutil
from userbot.uniborgConfig import Config

#thumb image
downloaded_file_name = "./DOWNLOADS/thumb_image.jpg"
downloader = SmartDL(Config.THUMB_IMAGE, downloaded_file_name, progress_bar=False)
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
