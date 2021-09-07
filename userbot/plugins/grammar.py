import requests
from bs4 import BeautifulSoup

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

tr = Config.COMMAND_HAND_LER

plugin_category = "extra"


@catub.cat_cmd(
    pattern="gcheck$",
    command=("gcheck", plugin_category),
    info={
        "header": "To Correct The grammar Of A Paragraph If It Has Any Error.",
        "description": "Reply to any English paragraph to correct its grammar",
        "usage": "{tr}gcheck reply",
    },
)
async def grammer(event):
    "To Correct The Grammar Of A Paragraph If It Has Any Error."
    re_message = await event.get_reply_message()
    if not re_message or not re_message.raw_text:
        return await edit_delete(
            event, "__Reply to a message to correct grammar in that message.__", 7
        )
    await edit_or_reply(event, "Checking for grammer.......")
    url = "https://orthographe.reverso.net/api/v1/Spelling"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    }
    data = {
        "autoReplace": "true",
        "generateRecommendations": "false",
        "generateSynonyms": "false",
        "getCorrectionDetails": "true",
        "interfaceLanguage": "en",
        "language": "eng",
        "locale": "Indifferent",
        "origin": "interactive",
        "text": re_message.raw_text,
    }
    response = requests.get(url, headers=headers, params=data)
    wrongs = response.json()["corrections"]
    result = re_message.raw_text
    if wrongs:
        try:
            for wrong in wrongs[::-1]:
                start = wrong["startIndex"]
                end = wrong["endIndex"] + 1
                correction = wrong["correctionText"]
                result = result[:start] + "**" + correction + "**" + result[end:]
        except KeyError:
            response = requests.get(url, headers=headers, params=data)
            wrongs = response.json()["corrections"]
            result = re_message.raw_text
            if wrongs:
                for wrong in wrongs[::-1]:
                    start = wrong["startIndex"]
                    end = wrong["endIndex"] + 1
                    correction = wrong["correctionText"]
                    result = result[:start] + "**" + correction + "**" + result[end:]
        except:
            await edit_or_reply(event, "An Error Occurred")
    if result != re_message.raw_text:
        return await edit_or_reply(event, result)
    await edit_delete(event, "__There is no grammer mistake in the replied text__", 7)


@catub.cat_cmd(
    pattern="pcheck$",
    command=("pcheck", plugin_category),
    info={
        "header": "Plagiarism Checker to check wheather the conetent is copied or not",
        "description": "Reply to any English paragraph to check its plagiarism",
        "usage": "{tr}pcheck reply",
    },
)
async def plagiarism(event):
    "Plagiarism Checker to check wheather the content is copied or not"
    re_message = await event.get_reply_message()
    if not re_message or not re_message.raw_text:
        return await edit_delete(
            event, "__Reply to a message to correct grammar in that message.__", 7
        )
    await edit_or_reply(event, "Checking for plagiarism.......")
    url = "https://capi.grammarly.com/api/check"
    headers = {
        "accept": "application/json",
        "content-type": "text/plain",
        "cookie": "grauth=AABJgifHi85_MMnflU4tyTCZPyWTNz-SnB_9gDdcpLb89TPKsrBMqzXQhLBOkJ6fuzBR5XTkymzwl2bV; csrf-token=AABJgrkKH913Z7iHqtGL+a5KAZ4Gy8Y2yIuC8A; gnar_containerId=cerd6ag5f7ga0mg2; _gcl_au=1.1.1716143064.1625920462; ga_clientId=2030085777.1625920462; funnel_firstTouchUtmSource=google; _gid=GA1.2.1168501191.1626888033; _gac_UA-6331378-16=1.1626888033.CjwKCAjwi9-HBhACEiwAPzUhHDlswcJfJBrPBRVRROm4Xgd8vsfYba7j3rI2Jf57FzrpTwjdCrqLRBoCv4gQAvD_BwE; _gcl_aw=GCL.1626888034.CjwKCAjwi9-HBhACEiwAPzUhHDlswcJfJBrPBRVRROm4Xgd8vsfYba7j3rI2Jf57FzrpTwjdCrqLRBoCv4gQAvD_BwE; _gcl_dc=GCL.1626888034.CjwKCAjwi9-HBhACEiwAPzUhHDlswcJfJBrPBRVRROm4Xgd8vsfYba7j3rI2Jf57FzrpTwjdCrqLRBoCv4gQAvD_BwE; funnelType=plagiarism; browser_info=CHROME:91:COMPUTER:SUPPORTED:FREEMIUM:WINDOWS_10:WINDOWS; redirect_location=eyJ0eXBlIjoiIiwibG9jYXRpb24iOiJodHRwczovL3d3dy5ncmFtbWFybHkuY29tL3BsYWdpYXJpc20tY2hlY2tlciJ9; _ga=GA1.2.2030085777.1625920462; _uetsid=f4e50e10ea4711eba0d1117bcf25b474; _uetvid=27d9d970e17b11eb8ca1cd20df76f927; _gat=1; _ga_CBK9K2ZWWE=GS1.1.1626971297.3.1.1626971743.0",
    }
    response = requests.post(
        url, headers=headers, data=re_message.raw_text.encode("utf8")
    )
    json = response.json()
    plagiarism = 0
    for x in json:
        if x["category"] == "Plagiarism":
            plagiarism = x["count"]
    if plagiarism != 0:
        result = f"The Content is **{plagiarism}% plagiarised**.\nYou can use `{tr}rephrase` to rephrase the content to remove plagiarism"
    else:
        result = "Your Content is **100% unique**"
    return await edit_or_reply(event, result)


@catub.cat_cmd(
    pattern="rephrase$",
    command=("rephrase", plugin_category),
    info={
        "header": "Rephraser to remove plagiarised content from text",
        "description": "Reply to any English paragraph to rephrase the content",
        "usage": "{tr}rephrase reply",
    },
)
async def plagiarism(event):
    "Rephraser to remove plagiarised content from text"
    re_message = await event.get_reply_message()
    if not re_message or not re_message.raw_text:
        return await edit_delete(
            event, "__Reply to a message to correct grammar in that message.__", 7
        )
    await edit_or_reply(event, "Rephrasing.......")
    url = "https://www.paraphrase-online.com/"
    data = {"field1": re_message.raw_text}
    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.content, "lxml")
    result = soup.find("div", {"id": "field2"}).text
    await edit_or_reply(event, f"`{result}`")
