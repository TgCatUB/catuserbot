# Random RGB Sticklet by @PhycoNinja13b

#Exclusive for My personal Repo
#Requirement of this plugin is very high (Kumbhkaran ki aulad) 
#Currently Loaded 6 Language support!! (will add more with time) 
#Dare To edit this part! U will be tored apart! 

'''Arabic = .ara
Urdu = .ur
Hindi = .hi
Malayalam = .mal
Gujrati = .guj
Bengali = .ben  '''


import io
import textwrap
import random
from telethon import events

from PIL import Image, ImageDraw, ImageFont

from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="ara (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)
    
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = "MaterLang_Fonts/NotoNaskhArabic-Regular.ttf"

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()


@borg.on(admin_cmd(pattern="ur (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)
    
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = "MaterLang_Fonts/NotoNastaliqUrdu-Regular.ttf"
 
    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()


@borg.on(admin_cmd(pattern="hi (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = "MaterLang_Fonts/NotoSerifDevanagari-Bold.ttf"
    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()

@borg.on(admin_cmd(pattern="mal (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = "MaterLang_Fonts/NotoSansMalayalam-Regular.ttf"

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()

@borg.on(admin_cmd(pattern="guj (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)

    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = "MaterLang_Fonts/NotoSansGujarati-Regular.ttf"

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()

@borg.on(admin_cmd(pattern="ben (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)

    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = "MaterLang_Fonts/NotoSansBengali-SemiBold.ttf"

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()
