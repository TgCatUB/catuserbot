from telethon import events
import asyncio
import json
import requests
from urllib.parse import quote
from userbot.utils import admin_cmd
from PIL import Image, ImageColor
import os
from datetime import datetime
import qrcode
import barcode
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from userbot import CMD_HELP
from telethon.errors.rpcerrorlist import YouBlockedUserError
import logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)


@borg.on(admin_cmd(pattern="scan ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("```reply to a media message```")
        return
    chat = "@DrWebBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Reply to actual users message.```")
        return
    await event.edit(" `Sliding my tip, of fingers over it`")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=161163358))
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @sangmatainfo_bot and try again```")
            return
        if response.text.startswith("Forward"):
            await event.edit("```can you kindly disable your forward privacy settings for good?```")
        else:
            if response.text.startswith("Select"):
                await event.edit("`Please go to` @DrWebBot `and select your language.`")
            else:
                await event.edit(f"**Antivirus scan was completed. I got dem final results.**\n {response.message.message}")


@borg.on(admin_cmd(pattern=r"decode$", outgoing=True))
async def parseqr(qr_e):
    """ For .decode command, get QR Code/BarCode content from the replied photo. """
    downloaded_file_name = await qr_e.client.download_media(
        await qr_e.get_reply_message())
    # parse the Official ZXing webpage to decode the QRCode
    command_to_exec = [
        "curl", "-X", "POST", "-F", "f=@" + downloaded_file_name + "",
        "https://zxing.org/w/decode"
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    os.remove(downloaded_file_name)
    if not t_response:
        logger.info(e_response)
        logger.info(t_response)
        await qr_e.edit("Failed to decode.")
        return
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await qr_e.edit(qr_contents)


@borg.on(admin_cmd(pattern="barcode ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("...")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(
            bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await borg.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        os.remove(filename)
    except Exception as e:
        await event.edit(str(e))
        return
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Created BarCode in {} seconds".format(ms))
    await asyncio.sleep(5)
    await event.delete()


@borg.on(admin_cmd(pattern=r"makeqr(?: |$)([\s\S]*)", outgoing=True))
async def make_qr(makeqr):
    """ For .makeqr command, make a QR Code containing the given content. """
    input_str = makeqr.pattern_match.group(1)
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(
                previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = ""
            for media in m_list:
                message += media.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(makeqr.chat_id,
                                  "img_file.webp",
                                  reply_to=reply_msg_id)
    os.remove("img_file.webp")
    await makeqr.delete()


@borg.on(admin_cmd(pattern="calendar (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split("-")
    if len(input_sgra) == 3:
        yyyy = input_sgra[0]
        mm = input_sgra[1]
        dd = input_sgra[2]
        required_url = "https://calendar.kollavarsham.org/api/years/{}/months/{}/days/{}?lang={}".format(
            yyyy, mm, dd, "en")
        headers = {"Accept": "application/json"}
        response_content = requests.get(required_url, headers=headers).json()
        a = ""
        if "error" not in response_content:
            current_date_detail_arraays = response_content["months"][0]["days"][0]
            a = json.dumps(
                current_date_detail_arraays,
                sort_keys=True,
                indent=4)
        else:
            a = response_content["error"]
        await event.edit(str(a))
    else:
        await event.edit("SYNTAX: .calendar YYYY-MM-DD")
    end = datetime.now()
    (end - start).seconds


@borg.on(admin_cmd(pattern="currency (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from)
            current_response = requests.get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit("{} {} = {} {}".format(number, currency_from, rebmun, currency_to))
            else:
                await event.edit("Welp, Hate to tell yout this but this Currency isn't supported **yet**.\n__Try__ `.currencies` __for a list of supported currencies.__")
        except e:
            await event.edit(str(e))
    else:
        await event.edit("**Syntax:**\n.currency amount from to\n**Example:**\n`.currency 10 usd inr`")
    end = datetime.now()
    (end - start).seconds


@borg.on(admin_cmd(pattern="currencies$"))
async def currencylist(ups):
    if ups.fwd_from:
        return
    request_url = "https://api.exchangeratesapi.io/latest?base=USD"
    current_response = requests.get(request_url).json()
    dil_wale_puch_de_na_chaaa = current_response["rates"]
    hmm = ""
    for key, value in dil_wale_puch_de_na_chaaa.items():
        hmm += f"`{key}`" + "\t\t\t"
    await ups.edit(f"**List of some currencies:**\n{hmm}\n")


@borg.on(admin_cmd(pattern="ifsc (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://ifsc.razorpay.com/{}".format(input_str)
    r = requests.get(url)
    if r.status_code == 200:
        b = r.json()
        a = json.dumps(b, sort_keys=True, indent=4)
        # https://stackoverflow.com/a/9105132/4723940
        await event.edit(str(a))
    else:
        await event.edit("`{}`: {}".format(input_str, r.text))


@borg.on(admin_cmd(pattern="color (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
            im.save("cat.png", "PNG")
            input_str = input_str.replace("#", "#COLOR_")
            await borg.send_file(
                event.chat_id,
                "cat.png",
                force_document=False,
                caption=input_str,
                reply_to=message_id
            )
            os.remove("cat.png")
            await event.delete()
    else:
        await event.edit("Syntax: `.color <color_code>` example : `.color #ff0000`")


@borg.on(admin_cmd(pattern="xkcd ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url,
                params={
                    "action": "xkcd",
                    "query": quote(input_str)
                }
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if r.ok:
        data = r.json()
        year = data.get("year")
        month = data["month"].zfill(2)
        day = data["day"].zfill(2)
        xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
        safe_title = data.get("safe_title")
        data.get("transcript")
        alt = data.get("alt")
        img = data.get("img")
        data.get("title")
        output_str = """[\u2060]({})**{}**
[XKCD ]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(img, input_str, xkcd_link, safe_title, alt, day, month, year)
        await event.edit(output_str, link_preview=True)
    else:
        await event.edit("xkcd n.{} not found!".format(xkcd_id))

CMD_HELP.update({
    'tools':
    "`.scan` reply to media or file\
\n**USEAGE : **it scans the media or file and checks either any virus is in the file or media\
\n\n`.makeqr` <content>\
\n**USEAGE : **Make a QR Code from the given content.\
\nExample: .makeqr www.google.com\
\n\n`.barcode `<content>\
\n**USEAGE : **Make a BarCode from the given content.\
\nExample: `.barcode` www.google.com\
\n\n`.decode` <reply to barcode/qrcode> \
\n**USAGE : **to get decoded content of those codes.\
\n\n`.currency` amount (from currency) (to currency)\
\n**USAGE : **Currency converter for userbot **Example :** `.currency 10 usd inr`\
\n\n`.currencies`\
\n**USAGE : **Shows you the some list of currencies\
\n\n`.ifsc` <IFSC code>\
\n**USAGE : ** to get details of the relevant bank or branch **Example :** `.ifsc SBIN0016086`\
\n\n`.color` <color_code> \
\n**USEAGE : **sends you a plain image of the color example :`.color #ff0000`\
\n\n`.xkcd` <query>\
\n**USEAGE : **Searches for the query for the relevant XKCD comic "
})
