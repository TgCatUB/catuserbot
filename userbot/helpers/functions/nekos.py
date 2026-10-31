import aiofiles
import httpx
from PIL import Image, ImageDraw, ImageFont
from validators.url import url

IMAGEGEN_API = "https://nekobot.xyz/api/imagegen"


async def fakegs(search, result):
    imgurl = "https://i.imgur.com/wNFr5X2.jpg"
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(imgurl)
    async with aiofiles.open("./temp/temp.jpg", "wb") as f:
        await f.write(resp.content)
    img = Image.open("./temp/temp.jpg")
    drawing = ImageDraw.Draw(img)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font1 = ImageFont.truetype("userbot/helpers/styles/ProductSans-BoldItalic.ttf", 20)
    font2 = ImageFont.truetype("userbot/helpers/styles/ProductSans-Light.ttf", 23)
    drawing.text((450, 258), result, fill=blue, font=font1)
    drawing.text((270, 37), search, fill=black, font=font2)
    img.save("./temp/temp.jpg")
    return "./temp/temp.jpg"


async def _imagegen(params, fmt):
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        r = (await client.get(IMAGEGEN_API, params=params)).json()
        sandy = r.get("message")
        if not url(sandy):
            return "check syntax once more"
        resp = await client.get(sandy)
    async with aiofiles.open("temp.png", "wb") as f:
        await f.write(resp.content)
    img = Image.open("temp.png").convert("RGB")
    out = "temp.webp" if fmt == "webp" else "temp.jpg"
    img.save(out, fmt)
    return out


async def trumptweet(text):
    return await _imagegen({"type": "trumptweet", "text": text}, "webp")


async def changemymind(text):
    return await _imagegen({"type": "changemymind", "text": text}, "webp")


async def kannagen(text):
    return await _imagegen({"type": "kannagen", "text": text}, "webp")


async def moditweet(text):
    return await _imagegen({"type": "tweet", "text": text, "username": "narendramodi"}, "webp")


async def tweets(text1, text2):
    return await _imagegen({"type": "tweet", "text": text1, "username": text2}, "webp")


async def iphonex(text):
    return await _imagegen({"type": "iphonex", "url": text}, "jpeg")


async def baguette(text):
    return await _imagegen({"type": "baguette", "url": text}, "jpeg")


async def threats(text):
    return await _imagegen({"type": "threats", "url": text}, "jpeg")


async def lolice(text):
    return await _imagegen({"type": "lolice", "url": text}, "jpeg")


async def trash(text):
    return await _imagegen({"type": "trash", "url": text}, "jpeg")


async def awooify(text):
    return await _imagegen({"type": "awooify", "url": text}, "jpeg")


async def trap(text1, text2, text3):
    return await _imagegen({"type": "trap", "name": text1, "author": text2, "image": text3}, "jpeg")


async def phcomment(text1, text2, text3):
    return await _imagegen({"type": "phcomment", "image": text1, "text": text2, "username": text3}, "jpeg")
