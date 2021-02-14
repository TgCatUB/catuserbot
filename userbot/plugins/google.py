# reverse search and google search  plugin for cat
import io
import os
import re
import urllib
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from PIL import Image
from search_engine_parser import GoogleSearch

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@bot.on(admin_cmd(outgoing=True, pattern=r"gs (.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"gs (.*)"))
async def gsearch(q_event):
    catevent = await edit_or_reply(q_event, "`searching........`")
    match = q_event.pattern_match.group(1)
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await catevent.edit(
        "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg, link_preview=False
    )
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + match + "` was executed successfully",
        )


@bot.on(admin_cmd(pattern="grs$"))
@bot.on(sudo_cmd(pattern="grs$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    OUTPUT_STR = "Reply to an image to do Google Reverse Search"
    if event.reply_to_msg_id:
        catevent = await edit_or_reply(event, "Pre Processing Media")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        BASE_URL = "http://www.google.com"
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (
                    downloaded_file_name,
                    open(downloaded_file_name, "rb"),
                ),
                "image_content": "",
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(
                SEARCH_URL, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await catevent.edit("Found Google Result. Pouring some soup on it!")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # document.getElementsByClassName("r5a77d"): PRS
        try:
            prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
            prs_anchor_element = prs_div.find("a")
            prs_url = BASE_URL + prs_anchor_element.get("href")
            prs_text = prs_anchor_element.text
            # document.getElementById("jHnbRc")
            img_size_div = soup.find(id="jHnbRc")
            img_size = img_size_div.find_all("div")
        except Exception:
            return await edit_delete(
                catevent, "`Sorry. I am unable to find similar images`"
            )
        end = datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """{img_size}
<b>Possible Related Search : </b> <a href="{prs_url}">{prs_text}</a> 
<b>More Info : </b> Open this <a href="{the_location}">Link</a> 
<i>fetched in {ms} seconds</i>""".format(
            **locals()
        )
    await catevent.edit(OUTPUT_STR, parse_mode="HTML", link_preview=False)


@bot.on(admin_cmd(pattern=r"reverse(?: |$)(\d*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"reverse(?: |$)(\d*)", allow_sudo=True))
@errors_handler
async def _(img):
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await bot.download_media(message, photo)
    else:
        await edit_or_reply(img, "`Reply to photo or sticker nigger.`")
        return
    if photo:
        catevent = await edit_or_reply(img, "`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            await catevent.edit("`Unsupported , most likely.`")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]
        if response != 400:
            await img.edit(
                "`Image successfully uploaded to Google. Maybe.`"
                "\n`Parsing source now. Maybe.`"
            )
        else:
            await catevent.edit("`Google told me to fuck off.`")
            return
        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]
        if guess and imgspage:
            await catevent.edit(f"[{guess}]({fetchUrl})\n\n`Looking for this Image...`")
        else:
            await catevent.edit("`Can't find this piece of shit.`")
            return

        lim = img.pattern_match.group(1) or 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(
                entity=await img.client.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await catevent.edit(
            f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})"
        )


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results


async def scam(results, lim):
    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")
    imglinks = []
    counter = 0
    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)
    for imglink in oboi:
        counter += 2
        if counter <= int(lim):
            imglinks.append(imglink)
        else:
            break
    return imglinks


CMD_HELP.update(
    {
        "google": "**Plugin :**`google`\
        \n\n•  **Syntax :** `.gs <limit> <query>` or `.gs <limit> (replied message)`\
        \n•  **Function : **will google  search and sends you top 10 results links.\
        \n\n•  **Syntax :** `.grs` reply to image\
        \n•  **Function : **will google reverse search the image and shows you the result.\
        \n\n•  **Syntax : **`.reverse limit`\
        \n•  **Function : **Reply to a pic/sticker to revers-search it on Google Images !!"
    }
)
