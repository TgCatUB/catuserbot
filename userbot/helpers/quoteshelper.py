from PIL import Image, ImageDraw, ImageFont, ImageOps
from telethon.tl import types, functions
from fontTools.ttLib import TTFont 
from fontTools.unicode import Unicode 
import emoji
import textwrap
import urllib
import logging
import random
import json
import os
import re

COLORS = [
    "#F07975", "#F49F69", "#F9C84A", "#8CC56E", "#6CC7DC", "#80C1FA", "#BCB3F9", "#E181AC"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

async def process(msg, user, client, reply, replied=None):
    if not os.path.isdir(".tmp"):
        os.mkdir(".tmp", 0o755)
        urllib.request.urlretrieve(
           'https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Regular.ttf',
           '.tmp/Roboto-Regular.ttf')
        urllib.request.urlretrieve(
           'https://github.com/erenmetesar/modules-repo/raw/master/Quivira.otf',
           '.tmp/Quivira.otf')
        urllib.request.urlretrieve(
           'https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Medium.ttf',
           '.tmp/Roboto-Medium.ttf')
        urllib.request.urlretrieve(
           'https://github.com/erenmetesar/modules-repo/raw/master/DroidSansMono.ttf',
           '.tmp/DroidSansMono.ttf')
        urllib.request.urlretrieve(
           'https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Italic.ttf',
           '.tmp/Roboto-Italic.ttf')
        
async def drawer(width, height):
    # Top part
    top = Image.new('RGBA', (width, 20), (0,0,0,0))
    draw = ImageDraw.Draw(top)
    draw.line((10, 0, top.width - 20, 0),  fill=(29, 29, 29, 255), width=50)
    draw.pieslice((0, 0, 30, 50), 180, 270, fill=(29, 29, 29, 255))
    draw.pieslice((top.width - 75, 0, top.width, 50), 270, 360, fill=(29, 29, 29, 255))
    # Middle part
    middle = Image.new("RGBA", (top.width, height + 75), (29, 29, 29, 255)) 
    # Bottom part
    bottom = ImageOps.flip(top)
    return top, middle, bottom

async def fontTest(letter):
    test = TTFont(".tmp/Roboto-Medium.ttf")
    for table in test['cmap'].tables:
        if ord(letter) in table.cmap.keys():
            return True
          
async def get_entity(msg):
    bold = {0: 0}
    italic = {0: 0}
    mono = {0: 0}
    link = {0: 0}
    if not msg.entities:
        return bold, mono, italic, link
    for entity in msg.entities:
        if isinstance(entity, types.MessageEntityBold):
            bold[entity.offset] = entity.offset + entity.length
        elif isinstance(entity, types.MessageEntityItalic):
            italic[entity.offset] = entity.offset + entity.length
        elif isinstance(entity, types.MessageEntityCode):
            mono[entity.offset] = entity.offset + entity.length
        elif isinstance(entity, types.MessageEntityUrl):
            link[entity.offset] = entity.offset + entity.length
        elif isinstance(entity, types.MessageEntityTextUrl):
            link[entity.offset] = entity.offset + entity.length
        elif isinstance(entity, types.MessageEntityMention):
            link[entity.offset] = entity.offset + entity.length
    return bold, mono, italic, link

async def doctype(name, size, type, canvas):
    font = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 38)
    doc = Image.new("RGBA", (130, 130), (29, 29, 29, 255))
    draw = ImageDraw.Draw(doc)
    draw.ellipse((0, 0, 130, 130), fill="#434343")
    draw.line((66, 28, 66, 53), width=14, fill="white")
    draw.polygon([(67, 77), (90, 53), (42, 53)], fill="white")
    draw.line((40, 87, 90, 87), width=8, fill="white")
    canvas.paste(doc, (160,23))
    draw2 = ImageDraw.Draw(canvas)
    draw2.text((320, 40), name, font=font, fill="white")
    draw2.text(
        (320, 97), size
        + type , font=font, fill="#AAAAAA")
    return canvas

async def no_photo(reply, tot):
    pfp = Image.new("RGBA", (105, 105), (0, 0, 0, 0))
    pen = ImageDraw.Draw(pfp)
    color = random.choice(COLORS)
    pen.ellipse((0, 0, 105, 105), fill=color)
    letter = "" if not tot else tot[0]
    font = ImageFont.truetype(".tmp/Roboto-Regular.ttf", 60)
    pen.text((32, 17), letter, font=font, fill="white")
    return pfp, color

async def emoji_fetch(emoji):
    emojis = json.loads(
        urllib.request.urlopen("https://github.com/erenmetesar/modules-repo/raw/master/emojis.txt").read().decode())
    if emoji in emojis:
        img = emojis[emoji]
        return await Quote.transparent(urllib.request.urlretrieve(img, ".tmp/emoji.png")[0])
    else:
        img = emojis["⛔"]
        return await Quote.transparent(urllib.request.urlretrieve(img, ".tmp/emoji.png")[0])
        
async def transparent(emoji):
    emoji = Image.open(emoji).convert("RGBA")
    emoji.thumbnail((40, 40))     
        # Mask
        mask = Image.new("L", (40, 40), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 40, 40), fill=255)
        return emoji, mask

async def replied_user(draw, tot, text, maxlength, title):
    namefont = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 38)
    namefallback= ImageFont.truetype(".tmp/Quivira.otf", 38)
    textfont = ImageFont.truetype(".tmp/Roboto-Regular.ttf", 32)
    textfallback = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 38)
    maxlength = maxlength + 7 if maxlength < 10 else maxlength
    text = text[:maxlength - 2] + ".." if len(text) > maxlength else text
    draw.line((165, 90, 165, 170), width=5, fill="white")
    space = 0
    for letter in tot:
        if not await Quote.fontTest(letter):
            draw.text((180 + space, 86), letter, font=namefallback, fill="#888888")
            space += namefallback.getsize(letter)[0]
        else:
            draw.text((180 + space, 86), letter, font=namefont, fill="#888888")
            space += namefont.getsize(letter)[0]
    space = 0
    for letter in text:
        if not await Quote.fontTest(letter):
            draw.text((180 + space, 132), letter, font=textfallback, fill="#888888")
            space += textfallback.getsize(letter)[0]
        else:
            draw.text((180 + space, 132), letter, font=textfont, fill="white")
            space += textfont.getsize(letter)[0]

async def quotexxx(message):
    """Converts the replied message into an independent sticker"""
    await message.delete()
    reply = await message.get_reply_message()
    msg = reply.message
    repliedreply = await reply.get_reply_message()
    user = (
        await message.client.get_entity(reply.forward.sender) if reply.fwd_from
        else reply.sender)
    res, canvas = await Quote.process(msg, user, message.client, reply, repliedreply)
    if not res:
        return
    canvas.save('.tmp/sticker.webp')
    await message.respond(file=".tmp/sticker.webp")
    os.remove('.tmp/sticker.webp')       
