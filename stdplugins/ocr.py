"""Optical Character Recognition by OCR.Space
Syntax: .ocr <LangCode>
Available Languages: .ocrlanguages"""
import json
import os
from PIL import Image
import requests
from uniborg.util import admin_cmd


def ocr_space_file(filename, overlay=False, api_key=Config.OCR_SPACE_API_KEY, language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.json()


def ocr_space_url(url, overlay=False, api_key=Config.OCR_SPACE_API_KEY, language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.json()


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(
        current, total, (current / total) * 100))


@borg.on(admin_cmd(pattern="ocrlanguages"))
async def get_ocr_languages(event):
    if event.fwd_from:
        return
    languages = {}
    languages["English"] = "eng"
    languages["Arabic"] = "ara"
    languages["Bulgarian"] = "bul"
    languages["Chinese (Simplified)"] = "chs"
    languages["Chinese (Traditional)"] = "cht"
    languages["Croatian"] = "hrv"
    languages["Czech"] = "cze"
    languages["Danish"] = "dan"
    languages["Dutch"] = "dut"
    languages["Finnish"] = "fin"
    languages["French"] = "fre"
    languages["German"] = "ger"
    languages["Greek"] = "gre"
    languages["Hungarian"] = "hun"
    languages["Korean"] = "kor"
    languages["Italian"] = "ita"
    languages["Japanese"] = "jpn"
    languages["Polish"] = "pol"
    languages["Portuguese"] = "por"
    languages["Russian"] = "rus"
    languages["Slovenian"] = "slv"
    languages["Spanish"] = "spa"
    languages["Swedish"] = "swe"
    languages["Turkish"] = "tur"
    a = json.dumps(languages, sort_keys=True, indent=4)
    await event.edit(str(a))


@borg.on(admin_cmd(pattern="ocr (.*)"))
async def parse_ocr_space_api(event):
    if event.fwd_from:
        return
    await event.edit("Processing 🙄🙇‍♂️🙇‍♂️🙇‍♀️")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await borg.download_media(
        await event.get_reply_message(),
        Config.TMP_DOWNLOAD_DIRECTORY,
        progress_callback=progress
    )
    if downloaded_file_name.endswith((".webp")):
        downloaded_file_name = conv_image(downloaded_file_name)
    test_file = ocr_space_file(filename=downloaded_file_name, language=lang_code)
    ParsedText = "hmm"
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
        ProcessingTimeInMilliseconds = str(int(test_file["ProcessingTimeInMilliseconds"]) // 1000)
    except Exception as e:
        await event.edit("Errors.\n `{}`\nReport This to @UniBorg\n\n`{}`".format(str(e), json.dumps(test_file, sort_keys=True, indent=4)))
    else:
        await event.edit("Read Document in {} seconds. \n{}".format(ProcessingTimeInMilliseconds, ParsedText))
    os.remove(downloaded_file_name)
    await event.edit(ParsedText)


def conv_image(image):
    im = Image.open(image)
    im.save(image, "PNG")
    new_file_name = image + ".png"
    os.rename(image, new_file_name)
    return new_file_name


