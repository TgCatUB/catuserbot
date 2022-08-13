# \\ Created by-@Jisan7509 -- Github.com/Jisan09 //
#  \\   https://github.com/TgCatUB/catuserbot   //
#   \\       Plugin for @catuserbot            //
#    ```````````````````````````````````````````

import os
import urllib.request

import bs4
import requests
from PIL import Image, ImageDraw, ImageFont

from ..helpers import ellipse_create, file_check
from ..helpers.utils import reply_id
from . import catub, edit_delete, edit_or_reply

plugin_category = "utils"


bg_url_1 = "https://raw.githubusercontent.com/TgCatUB/CatUserbot-Resources/master/Resources/App/app-full.jpg"
bg_url_2 = "https://raw.githubusercontent.com/TgCatUB/CatUserbot-Resources/master/Resources/App/app-suggest.jpg"


def text_draw(font_name, font_size, img, text, width, hight, fill="white"):
    font = ImageFont.truetype(font_name, font_size)
    draw = ImageDraw.Draw(img)
    draw.text(
        (int(width), int(hight)),
        text=text,
        fill=fill,
        font=font,
    )


@catub.cat_cmd(
    pattern="app ([\s\S]*)",
    command=("app", plugin_category),
    info={
        "header": "To search any app in playstore",
        "description": "Searches the app in the playstore and provides the link to the app in playstore and fetchs app details",
        "usage": "{tr}app <name>",
    },
)
async def app_search(event):
    "To search any app in playstore."
    query = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not query:
        return await edit_delete(
            event, "`Enter an app name to get result from PlayStore..`"
        )
    await edit_or_reply(event, "`Searching!...`")
    try:
        final_name = query.replace(" ", "+")
        page = requests.get(
            f"https://play.google.com/store/search?q={final_name}&c=apps"
        )
        soup = bs4.BeautifulSoup(page.content, "lxml")
        fullapp_name = app_name = (
            soup.find("div", "vWM94c") or soup.find("span", "DdYX5")
        ).text
        dev_name = (soup.find("div", "LbQbAe") or soup.find("span", "wMUdtb")).text
        rating = (
            soup.find("div", "TT9eCd") or soup.find("span", "w2kbF")
        ).text.replace("star", "")
        app_icon = (
            soup.find("img", "T75of bzqKMd") or soup.find("img", "T75of stzEZd")
        )["src"].split("=s")[0]
        app_link = (
            "https://play.google.com"
            + (soup.find("a", "Qfxief") or soup.find("a", "Si6A0c Gy4nib"))["href"]
        )
        dev_link = (
            "https://play.google.com/store/apps/developer?id="
            + dev_name.replace(" ", "+")
        )
        review = soup.find("div", "g1rdde")
        downloads = soup.findAll("div", "ClM7O")
        info = soup.find("div", "omXQ6c")
    except AttributeError:
        return await edit_delete(
            event, "No result found in search. Please enter **Valid app name**"
        )
    downloads = f"{downloads[1].text}  downloads" if downloads else None
    info = info.text if info else None
    review = review.text if review else None
    bgurl = bg_url_1 if downloads and review else bg_url_2
    file_check(re=False, me=False, mo=False, it=False, fa=False, sp=False, go=True)
    if len(app_name) > 14:
        app_name = f"{app_name[:14]}..."
    pic_name = "playstore.png"
    logo = "app_logo.png"
    font = "temp/GoogleSans-Medium.ttf"
    urllib.request.urlretrieve(app_icon, logo)
    urllib.request.urlretrieve(bgurl, pic_name)
    background = Image.open(pic_name).resize((1024, 512))

    thumbmask = Image.new("RGBA", (1024, 512), 0)
    thumbmask.paste(background, (0, 0))

    thumb, x = ellipse_create(logo, 4, 0)
    thumbmask.paste(thumb, (680, 53), thumb)

    text_draw(font, 65, thumbmask, app_name, 50, 30)
    text_draw(font, 30, thumbmask, dev_name, 60, 120, "red")
    text_draw(font, 70, thumbmask, f"{rating} / 5", 190, 260)
    if bgurl == bg_url_1:
        text_draw(font, 35, thumbmask, review, 80, 420)
        text_draw(font, 30, thumbmask, downloads, 415, 420)
    thumbmask.save(pic_name)
    os.remove(logo)
    app_details = f" <b>{fullapp_name}</b>"
    app_details += f"\n\n<b>Developer :</b> <a href= {dev_link}>{dev_name}</a>"
    app_details += f"\n<b>Rating :</b> <code>{rating} ⭐ </code>"
    app_details += f"\n\n<b>Features :</b> <a href= {app_link}>View in Play Store</a>"
    await event.delete()
    await event.client.send_file(
        event.chat_id,
        pic_name,
        caption=app_details,
        parse_mode="HTML",
        reply_to=reply_to_id,
    )
    os.remove(pic_name)
